#!/usr/bin/env python3
"""Antigravity Stop Hook：偵測漏發 ask_question 互動圖卡並自動拉回補發。

僅於 terminationReason == "NO_TOOL_CALL" 且 continuationActive 非 True 時檢查，
若本輪最後一則模型回覆結尾包含引導使用者選擇／確認選項的文字，
或以純文字選項清單替代互動圖卡且未呼叫任何工具，則回傳 decision=continue。
任何異常皆 Fail-Open 輸出 {} 並以 0 結束。
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_RE_FENCED_CODE = re.compile(r"```[\s\S]*?```")
_RE_INLINE_CODE = re.compile(r"`[^`\n]*`")

# 條件 A1：冒號結尾 + 明確引導選擇／勾選／確認以下問題或選項
_RE_COLON_END = re.compile(r"[：:]\s*$")
_RE_GUIDE_PHRASE = re.compile(
    r"(?:請(?:先|幫我|再|直接)?(?:選擇|勾選|點選|選取|挑選|確認以下|確認下列|決定以下|從以下|見下方|透過下方)"
    r"|以下(?:幾個|三|兩|\d+)?(?:個)?(?:問題|選項|方案|項目)"
    r"|請回覆以下)"
)

# 條件 A2：明確提及下方卡片／圖卡／選項卻未呼叫工具
_RE_WIDGET_POINTER = re.compile(
    r"(?:透過下方(?:的)?(?:卡片|圖卡|選項)"
    r"|請見下方(?:的)?(?:卡片|圖卡|選項)"
    r"|下方(?:卡片|圖卡)(?:確認|選擇|勾選)"
    r"|點選下方)"
)

# 條件 B：純文字選項清單（至少 2 項） + 尾端索取選擇
_RE_TEXT_OPTION_LINE = re.compile(
    r"^\s*(?:[1-9]\.|[①②③④⑤]|\([1-9]\))\s+.*(?:方案|Recommended|推薦|—)",
    re.MULTILINE,
)
_RE_ASK_CHOICE_TAIL = re.compile(
    r"(?:請(?:回覆|輸入|選擇|告訴我).{0,12}(?:編號|數字|選項|方案|1|2)"
    r"|想選哪|要選哪|採用哪(?:一|種|個)|選哪(?:一|個|種))"
)

_CONTINUE_REASON = (
    "[Stop Hook 防漏圖卡] 你剛才的回覆結尾包含引導使用者選擇或確認選項的文字，"
    "但未實際呼叫 ask_question 工具。請不要重複前面的背景說明，"
    "立刻直接呼叫 ask_question 補發互動圖卡。"
)


def _strip_code(text: str) -> str:
    """移除 fenced 與 inline code，避免程式碼範例造成誤判；fenced block 保留佔位行防前導冒號外露。"""
    cleaned = _RE_FENCED_CODE.sub("\n[CODE_BLOCK]\n", text)
    cleaned = _RE_INLINE_CODE.sub("", cleaned)
    return cleaned


def detect_missing_card(content: str) -> str | None:
    """檢查回覆文字是否疑似漏發互動圖卡，命中回傳原因代號，否則回傳 None。"""
    if not content or not content.strip():
        return None

    cleaned = _strip_code(content).strip()
    if not cleaned:
        return None

    tail = cleaned[-450:]
    lines = [ln.strip() for ln in tail.splitlines() if ln.strip()]
    if not lines:
        return None

    last_line = lines[-1]
    last_two = "\n".join(lines[-2:])

    if _RE_COLON_END.search(last_line) and _RE_GUIDE_PHRASE.search(last_two):
        return "guide_colon_tail"

    if _RE_WIDGET_POINTER.search(last_two):
        return "widget_pointer_without_tool"

    option_matches = _RE_TEXT_OPTION_LINE.findall(tail)
    if len(option_matches) >= 2 and _RE_ASK_CHOICE_TAIL.search(tail[-220:]):
        return "plain_text_option_list"

    return None


def _get_last_turn_response(transcript_path: Path) -> tuple[str, bool] | None:
    """讀取 transcript.jsonl 本輪最後一筆模型回覆，回傳 (content, has_tool_calls)。"""
    if not transcript_path.is_file():
        return None

    lines = transcript_path.read_text(encoding="utf-8", errors="replace").splitlines()
    for raw in reversed(lines):
        raw = raw.strip()
        if not raw:
            continue
        try:
            rec = json.loads(raw)
        except Exception:
            continue
        if not isinstance(rec, dict):
            continue

        rec_type = rec.get("type")
        source = rec.get("source")
        if rec_type == "USER_INPUT" or source == "USER_EXPLICIT":
            break

        if rec_type == "PLANNER_RESPONSE" or (source == "MODEL" and "content" in rec):
            tool_calls = rec.get("tool_calls")
            has_tools = bool(tool_calls) if isinstance(tool_calls, list) else False
            content = rec.get("content") or ""
            if not isinstance(content, str):
                content = str(content)
            return content, has_tools

    return None


def evaluate_stop_payload(payload: dict) -> dict:
    """評估 Stop Hook payload 並回傳輸出 dict。"""
    if not isinstance(payload, dict):
        return {}
    if payload.get("terminationReason") != "NO_TOOL_CALL":
        return {}
    if payload.get("continuationActive") is True:
        return {}

    transcript_raw = payload.get("transcriptPath")
    if not transcript_raw or not isinstance(transcript_raw, str):
        return {}

    last_resp = _get_last_turn_response(Path(transcript_raw))
    if last_resp is None:
        return {}

    content, has_tools = last_resp
    if has_tools:
        return {}

    if detect_missing_card(content) is not None:
        return {"decision": "continue", "reason": _CONTINUE_REASON}

    return {}


def main() -> int:
    """程式進入點，維持 Fail-Open。"""
    if hasattr(sys.stdin, "reconfigure"):
        sys.stdin.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    result: dict = {}
    try:
        raw_input = sys.stdin.read()
        if raw_input and raw_input.strip():
            payload = json.loads(raw_input)
            result = evaluate_stop_payload(payload)
    except Exception:
        result = {}

    sys.stdout.write(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
