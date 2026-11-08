---
name: gemini-web-imagegen
description: 使用個人 gemini.google.com 網頁版 Cookie 額度（免 API Key、零 API 費用）在任何專案中生成 2K AI 圖片或進行參考圖風格改圖（Image-to-Image）。當使用者提到「用 Gemini 網頁版生圖」、「用 Gemini Web 生圖」、「用 Cookie 額度生圖」，或當 Codex ($imagegen) 與 Antigravity 內建生圖觸發 429 配額上限時作為第三優先備援載入。
---

# Gemini Web 網頁版免費額度生圖橋接 (Gemini Web Imagegen Bridge)

本技能允許四大 AI Agent（Claude Code、Antigravity、Codex、OpenCode）在任何專案中，直接調用 `gemini-webapi` 結合 Chromium CDP 自動 Cookie 提取技術，免 API 金鑰、零費用消耗個人 `gemini.google.com` 網頁版額度生成 2K 高畫質點陣圖（支援純文字生圖與附帶參考圖的 Image-to-Image 改圖）。

## 定位與觸發時機

1. **指名調用**：使用者明確要求「用 Gemini 網頁版生圖」、「用 Gemini Web 生圖」、「用第三引擎生圖」。
2. **第三優先備援（Priority 3）**：當第一優先（Codex `$imagegen`）與第二優先（Antigravity `image-generator` 子代理）因短時間密集生圖觸發 `429 RESOURCE_EXHAUSTED`（5 小時配額上限）時，無縫切換至本技能接續出圖。

## 前置環境與自動探索

本技能隨附獨立執行腳本 `scripts/gemini_web_gen.py`。執行時優先使用已安裝 `gemini-webapi>=2.1.1` 與 `pillow>=10.0.0` 的虛擬環境（如當前專案 `.venv` 或「作圖風格」專案的 `.venv`），若均無則自動於 `~/.gemini/webapi_venv` 建立共用輕量虛擬環境。

PowerShell 通用執行起手式：
```powershell
# 1. 定位技能腳本路徑（相容四大 Agent 全域技能目錄）
$skillScript = @(
    "$HOME\.gemini\config\skills\gemini-web-imagegen\scripts\gemini_web_gen.py",
    "$HOME\.claude\skills\gemini-web-imagegen\scripts\gemini_web_gen.py",
    "$HOME\.codex\skills\gemini-web-imagegen\scripts\gemini_web_gen.py",
    "$HOME\.config\opencode\skills\gemini-web-imagegen\scripts\gemini_web_gen.py"
) | Where-Object { Test-Path $_ } | Select-Object -First 1

# 2. 尋找已裝妥 gemini-webapi 的 Python 環境，若無則初始化 ~/.gemini/webapi_venv
$pyExe = @(
    "$PWD\.venv\Scripts\python.exe",
    "$HOME\Documents\AI AGENT 工作區\專案完成區\文書\作圖風格\.venv\Scripts\python.exe",
    "D:\AI_Workspace\專案完成區\文書\作圖風格\.venv\Scripts\python.exe",
    "$HOME\.gemini\webapi_venv\Scripts\python.exe"
) | Where-Object { Test-Path $_ } | Select-Object -First 1

if (-not $pyExe) {
    $venvDir = "$HOME\.gemini\webapi_venv"
    python -m venv $venvDir
    $pyExe = "$venvDir\Scripts\python.exe"
    & $pyExe -m pip install -q "pillow>=10.0.0" "gemini-webapi>=2.1.1" "curl_cffi>=0.6.0"
}
```

## 1. 文字直接生成 2K 圖片 (Text-to-Image)

```powershell
$project = (Get-Location).Path
$target = Join-Path $project "assets\generated\gemini_web_output.png"
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $target) | Out-Null

& $pyExe $skillScript `
    --prompt "Generate an ultra-detailed architectural illustration of Taipei 101 in vintage woodcut poster style" `
    --aspect "16:9" `
    --output $target
```

## 2. 附帶參考圖進行風格改圖 (Image-to-Image)

```powershell
$project = (Get-Location).Path
$refImg = Join-Path $project "assets\reference.jpg"
$target = Join-Path $project "assets\generated\gemini_web_styled.png"

& $pyExe $skillScript `
    --prompt "Transform the uploaded photo into a classic Prussian blue cyanotype botanical specimen print" `
    --ref $refImg `
    --aspect "3:4" `
    --output $target
```

## 3. 自動刷新或重新登入 Cookie（免按 F12）

腳本內建「**自動無頭 CDP 提取與自癒機制**」：生圖時若找不到或發現 Cookie 過期，會自動在背景啟動無頭 Edge/Chrome 從持久化設定檔提取解密後的 `__Secure-1PSID` 與 `__Secure-1PSIDTS` 存入 `~/.gemini/webapi_auth/cookies.json`。

若需要手動強制刷新或彈出視窗重新登入 Google：
```powershell
# 無頭自動提取刷新
& $pyExe $skillScript --refresh-cookies

# 若未登入，彈出專用瀏覽器視窗供登入 Google（登入完成自動存檔關閉）
& $pyExe $skillScript --login
```

## 已知技術眉角（必守規範）

1. **`gemini-webapi` 2.x API 規範**：
   - 傳遞參考圖片時，參數名稱必須為 `files=[...]`（舊版 `images=[...]` 已棄用，傳入會導致 `AsyncSession.request() got an unexpected keyword argument 'images'`）。
   - 儲存圖片 `GeneratedImage.save(path, filename)` 已移除舊版 `skip_invalid_filename` 參數（預設 `full_size=True` 抓取高畫質原圖並回傳實際存檔路徑字串）。
2. **CDP WebSocket 通訊**：透過 `curl_cffi.requests.WebSocket` 連接 Chromium CDP 時，必須使用 `ws.send_json(...)` 發送 Text Frame，不可使用 `ws.send(bytes)`（Binary Frame 會遭 Chromium 直接斷線報 `curl: (52)`）。
3. **機密安全**：提取出的 `cookies.json` 預設集中存放於使用者家目錄 `~/.gemini/webapi_auth/cookies.json`（若存放於專案目錄，必須確認已列入 `.gitignore`），嚴禁讀取或印出完整 Cookie 明文至對話紀錄，亦嚴禁提交至 Git。
