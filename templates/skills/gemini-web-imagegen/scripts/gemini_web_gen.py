#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemini Web Image Generator CLI (全域跨專案無頭生圖與自動取 Cookie 工具)
功能：
1. 免 API Key，直接沿用個人 gemini.google.com 網頁版登入額度生成圖片（支援文生圖與參考圖改圖）。
2. 自動從本機已登入的 Chromium/Edge/Chrome 設定檔透過 CDP 無頭提取 __Secure-1PSID 與 __Secure-1PSIDTS。
3. 自動進行 Lanczos 2K 超解析補償與微銳化，確保輸出長邊達 2048px / 2560px。
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import shutil
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from typing import List, Optional, Tuple

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from curl_cffi.requests import WebSocket
from gemini_webapi import GeminiClient, GeneratedImage
from PIL import Image, ImageFilter, ImageOps

GEMINI_APP_URL = "https://gemini.google.com/app"

TARGET_2K_SIZES = {
    "16:9": (2560, 1440),
    "9:16": (1440, 2560),
    "3:4": (1920, 2560),
    "4:3": (2560, 1920),
    "1:1": (2048, 2048),
}


def get_global_cookie_path() -> Path:
    """取得安全的本機 Cookie 儲存路徑（優先使用專案 cookies.json，否則存於使用者家目錄設定區）"""
    env_path = os.getenv("GEMINI_COOKIE_FILE", "").strip()
    if env_path:
        return Path(env_path).resolve()

    cwd_cookie = Path.cwd() / "cookies.json"
    if cwd_cookie.is_file():
        return cwd_cookie

    home_dir = Path(os.environ.get("USERPROFILE") or os.path.expanduser("~"))
    global_dir = home_dir / ".gemini" / "webapi_auth"
    global_dir.mkdir(parents=True, exist_ok=True)
    return global_dir / "cookies.json"


def load_cookies() -> Tuple[Optional[str], Optional[str]]:
    """讀取目前已保存的 __Secure-1PSID 與 __Secure-1PSIDTS"""
    psid = os.getenv("GEMINI_1PSID", "").strip()
    psidts = os.getenv("GEMINI_1PSIDTS", "").strip()
    if psid and psidts:
        return psid, psidts

    # 依序檢查：當前目錄 -> 全域設定目錄 -> 作圖風格專案目錄
    home_dir = Path(os.environ.get("USERPROFILE") or os.path.expanduser("~"))
    candidates = [
        get_global_cookie_path(),
        home_dir / "Documents" / "AI AGENT 工作區" / "專案完成區" / "文書" / "作圖風格" / "cookies.json",
        Path("D:/AI_Workspace/專案完成區/文書/作圖風格/cookies.json"),
    ]
    for path in candidates:
        if path.is_file():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    p1 = data.get("__Secure-1PSID", "").strip()
                    p2 = data.get("__Secure-1PSIDTS", "").strip()
                elif isinstance(data, list):
                    cmap = {c.get("name"): c.get("value", "") for c in data if isinstance(c, dict)}
                    p1 = cmap.get("__Secure-1PSID", "").strip()
                    p2 = cmap.get("__Secure-1PSIDTS", "").strip()
                else:
                    p1, p2 = "", ""
                if p1 and p2 and "請貼上" not in p1:
                    return p1, p2
            except Exception:
                pass
    return None, None


def save_cookies(psid: str, psidts: str) -> Path:
    """儲存最新 Cookie 至安全路徑"""
    target = get_global_cookie_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "__Secure-1PSID": psid,
        "__Secure-1PSIDTS": psidts,
    }
    target.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return target


def find_browser_executable() -> Optional[Path]:
    """自動尋找系統中的 Edge 或 Chrome 執行檔"""
    prog_x86 = Path(os.environ.get("PROGRAMFILES(X86)", ""))
    prog = Path(os.environ.get("PROGRAMFILES", ""))
    local_app = Path(os.environ.get("LOCALAPPDATA", ""))

    candidates = [
        prog_x86 / "Microsoft" / "Edge" / "Application" / "msedge.exe",
        prog / "Microsoft" / "Edge" / "Application" / "msedge.exe",
        local_app / "Microsoft" / "Edge" / "Application" / "msedge.exe",
        prog / "Google" / "Chrome" / "Application" / "chrome.exe",
        prog_x86 / "Google" / "Chrome" / "Application" / "chrome.exe",
        local_app / "Google" / "Chrome" / "Application" / "chrome.exe",
    ]
    for p in candidates:
        if p.is_file():
            return p

    for cmd in ("msedge", "chrome", "google-chrome", "chromium"):
        found = shutil.which(cmd)
        if found:
            return Path(found)
    return None


def get_profile_dir() -> Path:
    """尋找已登入 Google 的持久化瀏覽器 Profile"""
    home_dir = Path(os.environ.get("USERPROFILE") or os.path.expanduser("~"))
    candidates = [
        home_dir / "Documents" / "AI AGENT 工作區" / "GOOGLE FLOW" / "data" / "browser_profile",
        home_dir / "Documents" / "AI AGENT 工作區" / "專案完成區" / "文書" / "作圖風格" / "data" / "browser_profile",
        Path("D:/AI_Workspace/GOOGLE FLOW/data/browser_profile"),
    ]
    for p in candidates:
        if p.exists():
            return p

    fallback = home_dir / ".gemini" / "webapi_auth" / "browser_profile"
    fallback.mkdir(parents=True, exist_ok=True)
    return fallback


def find_free_debug_port(start_port: int = 9240) -> int:
    port = start_port
    while port < start_port + 50:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("localhost", port)) != 0:
                return port
        port += 1
    return start_port


def fetch_cookies_via_cdp(port: int) -> Tuple[Optional[str], Optional[str]]:
    try:
        with urllib.request.urlopen(f"http://localhost:{port}/json", timeout=3) as resp:
            targets = json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None, None

    ws_url = None
    if isinstance(targets, list):
        for t in targets:
            if isinstance(t, dict) and t.get("type") == "page" and t.get("webSocketDebuggerUrl"):
                ws_url = t["webSocketDebuggerUrl"]
                if "gemini.google.com" in t.get("url", ""):
                    break

    if not ws_url:
        try:
            with urllib.request.urlopen(f"http://localhost:{port}/json/version", timeout=3) as resp:
                ver_info = json.loads(resp.read().decode("utf-8"))
                ws_url = ver_info.get("webSocketDebuggerUrl")
        except Exception:
            return None, None

    if not ws_url:
        return None, None

    ws = WebSocket()
    try:
        ws.connect(ws_url)
        ws.send_json({"id": 1, "method": "Network.getAllCookies"})
        data = ws.recv_json()
        cookies = data.get("result", {}).get("cookies", []) if isinstance(data, dict) else []
        psid, psidts = None, None
        for c in cookies:
            if "google.com" in c.get("domain", ""):
                if c.get("name") == "__Secure-1PSID" and c.get("value"):
                    psid = c["value"]
                elif c.get("name") == "__Secure-1PSIDTS" and c.get("value"):
                    psidts = c["value"]
        return psid, psidts
    except Exception:
        return None, None
    finally:
        try:
            ws.close()
        except Exception:
            pass


def extract_cookies_from_browser(headless: bool = True, wait_seconds: int = 15) -> Tuple[Optional[str], Optional[str]]:
    """透過 Chromium CDP 無頭或視窗模式自動提取解密後的 Cookie"""
    browser_exe = find_browser_executable()
    if not browser_exe:
        return None, None

    profile_dir = get_profile_dir()
    for lock_name in ("SingletonLock", "SingletonCookie", "SingletonSocket"):
        lock_file = profile_dir / lock_name
        try:
            if lock_file.exists():
                lock_file.unlink(missing_ok=True)
        except Exception:
            pass

    port = find_free_debug_port()
    cmd = [
        str(browser_exe),
        f"--user-data-dir={profile_dir}",
        f"--remote-debugging-port={port}",
        f"--remote-allow-origins=http://localhost:{port}",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-blink-features=AutomationControlled",
    ]
    if headless:
        cmd.append("--headless=new")
    cmd.append(GEMINI_APP_URL)

    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    psid, psidts = None, None
    try:
        deadline = time.time() + wait_seconds
        while time.time() < deadline:
            time.sleep(2.0)
            psid, psidts = fetch_cookies_via_cdp(port)
            if psid and psidts:
                time.sleep(2.0)
                n_psid, n_psidts = fetch_cookies_via_cdp(port)
                if n_psid and n_psidts:
                    psid, psidts = n_psid, n_psidts
                break
    finally:
        try:
            proc.terminate()
            proc.wait(timeout=5)
        except Exception:
            try:
                proc.kill()
            except Exception:
                pass
    return psid, psidts


def ensure_2k_resolution(img_path: Path, aspect_ratio: str = "16:9") -> Tuple[int, int]:
    """將生成圖片進行 Lanczos 2K 放大與邊緣微銳化"""
    if not img_path.exists():
        return (0, 0)
    with Image.open(img_path) as im:
        im = im.convert("RGB")
        w, h = im.size
        target_w, target_h = TARGET_2K_SIZES.get(aspect_ratio, (2560, 1440))
        if max(w, h) < 2048 or (w, h) != (target_w, target_h):
            src_ratio = w / max(h, 1)
            dst_ratio = target_w / max(target_h, 1)
            if abs(src_ratio - dst_ratio) / dst_ratio <= 0.15:
                upscaled = ImageOps.fit(im, (target_w, target_h), method=Image.Resampling.LANCZOS)
            else:
                scale = 2560.0 / max(w, h)
                new_w = max(int(round(w * scale)), 2048 if w >= h else int(round(w * scale)))
                new_h = max(int(round(h * scale)), 2048 if h >= w else int(round(h * scale)))
                upscaled = im.resize((new_w, new_h), resample=Image.Resampling.LANCZOS)
            upscaled = upscaled.filter(ImageFilter.UnsharpMask(radius=1.1, percent=115, threshold=2))
            upscaled.save(img_path, format="PNG", optimize=True)
            return upscaled.size
        return (w, h)


async def generate_image_async(
    prompt: str,
    output_path: Path,
    ref_image: Optional[Path] = None,
    aspect_ratio: str = "16:9",
) -> Tuple[bool, str]:
    psid, psidts = load_cookies()
    if not psid or not psidts:
        print("[Gemini Web] 未找到現成 Cookie，正在從瀏覽器設定檔自動提取...")
        psid, psidts = extract_cookies_from_browser(headless=True, wait_seconds=15)
        if psid and psidts:
            save_cookies(psid, psidts)

    if not psid or not psidts:
        return False, "無法取得 __Secure-1PSID 與 __Secure-1PSIDTS，請先執行 --refresh-cookies 登入。"

    proxy = os.getenv("HTTPS_PROXY") or os.getenv("HTTP_PROXY") or None
    client = GeminiClient(secure_1psid=psid, secure_1psidts=psidts, proxy=proxy)
    try:
        try:
            await client.init(timeout=90, auto_close=False, close_delay=300, auto_refresh=True)
        except Exception:
            await client.close()
            print("[Gemini Web] Cookie 已過期，正在從瀏覽器自動刷新...")
            psid, psidts = extract_cookies_from_browser(headless=True, wait_seconds=15)
            if not psid or not psidts:
                return False, "Cookie 過期且自動刷新失敗，請執行 --login 重新登入。"
            save_cookies(psid, psidts)
            client = GeminiClient(secure_1psid=psid, secure_1psidts=psidts, proxy=proxy)
            await client.init(timeout=90, auto_close=False, close_delay=300, auto_refresh=True)

        if hasattr(client, "secure_1psidts") and client.secure_1psidts:
            save_cookies(psid, client.secure_1psidts)

        cleaned = prompt.strip()
        keywords = ("generate", "create", "draw", "redraw", "transform", "生成", "繪製", "產生", "改圖")
        has_action = any(k in cleaned.lower() for k in keywords)
        final_prompt = cleaned if has_action else f"Generate an image: {cleaned}"
        if "aspect ratio" not in final_prompt.lower() and "長寬比" not in final_prompt:
            final_prompt = f"{final_prompt}\n\nAspect ratio: {aspect_ratio}."

        files: List[str] = []
        if ref_image and ref_image.is_file():
            files.append(str(ref_image.resolve()))

        if files:
            response = await client.generate_content(final_prompt, files=files)
        else:
            response = await client.generate_content(final_prompt)

        generated_imgs = [img for img in response.images if isinstance(img, GeneratedImage)]
        if not generated_imgs and response.images:
            generated_imgs = list(response.images)

        if not generated_imgs:
            snippet = response.text[:200] if response.text else "無文字回應"
            return False, f"Gemini 網頁端未回傳圖片。回應摘要：{snippet}"

        output_path.parent.mkdir(parents=True, exist_ok=True)
        temp_name = f"temp_web_{ int(time.time()) }_{output_path.stem}.png"
        saved_str = await generated_imgs[0].save(path=str(output_path.parent), filename=temp_name)
        actual_saved = Path(saved_str) if saved_str else (output_path.parent / temp_name)

        if actual_saved.exists():
            actual_saved.replace(output_path)
            w, h = ensure_2k_resolution(output_path, aspect_ratio)
            return True, f"成功生成 2K 圖片：{output_path} ({w}x{h})"

        return False, "圖片下載失敗，找不到暫存檔。"
    finally:
        try:
            await client.close()
        except Exception:
            pass


def main() -> int:
    parser = argparse.ArgumentParser(description="Gemini Web 免費額度跨專案 AI 生圖工具")
    parser.add_argument("--prompt", "-p", type=str, help="生圖或改圖提示詞")
    parser.add_argument("--output", "-o", type=str, help="輸出 PNG 圖片路徑")
    parser.add_argument("--ref", "-r", type=str, default=None, help="參考圖片路徑 (選填，供 Image-to-Image 改圖)")
    parser.add_argument("--aspect", "-a", type=str, default="16:9", help="長寬比：16:9, 9:16, 3:4, 4:3, 1:1 (預設 16:9)")
    parser.add_argument("--refresh-cookies", action="store_true", help="無頭從瀏覽器提取最新 Cookie 並測試連線")
    parser.add_argument("--login", action="store_true", help="彈出瀏覽器視窗供手動登入 Google 並提取 Cookie")
    args = parser.parse_args()

    if args.refresh_cookies or args.login:
        headless = not args.login
        wait_sec = 120 if args.login else 15
        print(f"[Gemini Web] 正在啟動瀏覽器提取 Cookie (headless={headless})...")
        psid, psidts = extract_cookies_from_browser(headless=headless, wait_seconds=wait_sec)
        if not psid or not psidts:
            print("[失敗] 未能提取到 __Secure-1PSID 與 __Secure-1PSIDTS。")
            return 1
        saved_path = save_cookies(psid, psidts)
        print(f"[成功] 已儲存 Cookie 至：{saved_path}")
        return 0

    if not args.prompt or not args.output:
        parser.error("生圖模式請提供 --prompt 與 --output 參數。")

    out_path = Path(args.output).resolve()
    ref_path = Path(args.ref).resolve() if args.ref else None
    ok, msg = asyncio.run(
        generate_image_async(
            prompt=args.prompt,
            output_path=out_path,
            ref_image=ref_path,
            aspect_ratio=args.aspect,
        )
    )
    print(msg)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
