---
name: google-flow-bridge
description: 在任何專案中調用本地 Google Flow 自動化工具（flow.google.com）生成 AI 圖片（Nano Banana 2K）或影片（Veo MP4）素材，消耗使用者 Google 帳號內的 Flow 專屬點數與每日免費配額。當使用者提到「用 Flow 生圖」、「用 Flow 生片」、「調用 Google Flow」、「Google Flow 生成」時載入。
---

# Google Flow 跨專案影像與影片生成橋接 (Google Flow Bridge)

本技能允許 AI Agent（Antigravity、Claude Code、Codex、OpenCode 等）在任何專案的工作環境中，直接調用本機已持久化登入的 Google Flow 自動化工具，免 API 金鑰、直接消耗 Google One / Flow 帳號點數與每日免費額度生成高品質圖片與影片。

## 前置條件與自動路徑偵測

Google Flow 工具通常位於以下路徑（腳本已內建自動回退與偵測）：
- `$HOME\Documents\AI AGENT 工作區\GOOGLE FLOW`
- `<工作區磁碟>:\AI_Workspace\GOOGLE FLOW` 或 `<工作區磁碟>:\AI AGENT實驗區\GOOGLE FLOW`

PowerShell 通用路徑解析起手式：
```powershell
$flowRoot = @(
    "$HOME\Documents\AI AGENT 工作區\GOOGLE FLOW"
) + ((Get-PSDrive -PSProvider FileSystem).Root | ForEach-Object {
    Join-Path $_ "AI_Workspace\GOOGLE FLOW"
    Join-Path $_ "AI AGENT實驗區\GOOGLE FLOW"
}) | Where-Object { Test-Path $_ } | Select-Object -First 1

if (-not $flowRoot) { throw "找不到 Google Flow 專案目錄，請確認已放置於工作區。" }
$flowPy = Join-Path $flowRoot ".venv\Scripts\python.exe"
$flowMain = Join-Path $flowRoot "src\main.py"
```

## 1. 查詢 Flow 剩餘點數與方案

```powershell
$flowRoot = @(
    "$HOME\Documents\AI AGENT 工作區\GOOGLE FLOW"
) + ((Get-PSDrive -PSProvider FileSystem).Root | ForEach-Object {
    Join-Path $_ "AI_Workspace\GOOGLE FLOW"
    Join-Path $_ "AI AGENT實驗區\GOOGLE FLOW"
}) | Where-Object { Test-Path $_ } | Select-Object -First 1
$flowPy = Join-Path $flowRoot ".venv\Scripts\python.exe"
$flowMain = Join-Path $flowRoot "src\main.py"

& $flowPy $flowMain --credits
```

## 2. 在當前專案中生成圖片 (Nano Banana 2.1 - 2K PNG)

```powershell
$flowRoot = @(
    "$HOME\Documents\AI AGENT 工作區\GOOGLE FLOW"
) + ((Get-PSDrive -PSProvider FileSystem).Root | ForEach-Object {
    Join-Path $_ "AI_Workspace\GOOGLE FLOW"
    Join-Path $_ "AI AGENT實驗區\GOOGLE FLOW"
}) | Where-Object { Test-Path $_ } | Select-Object -First 1
$flowPy = Join-Path $flowRoot ".venv\Scripts\python.exe"
$flowMain = Join-Path $flowRoot "src\main.py"

$projectRoot = (Get-Location).Path
$targetDir = Join-Path $projectRoot "assets\generated"
if (-not (Test-Path $targetDir)) { New-Item -ItemType Directory -Force -Path $targetDir | Out-Null }

$outputFile = Join-Path $targetDir ("flow_img_" + (Get-Date -Format "yyyyMMdd_HHmmss") + ".png")
$prompt = "A cinematic shot of a futuristic cyberpunk city with neon lights, 8k resolution"

# 執行自動化生圖 (約 25~45 秒)
& $flowPy $flowMain --mode image --prompt $prompt --output $outputFile

if ($LASTEXITCODE -eq 0 -and (Test-Path $outputFile)) {
    Write-Host "Google Flow 生圖成功：$outputFile"
}
```

## 3. 在當前專案中生成影片 (Veo - MP4)

```powershell
$flowRoot = @(
    "$HOME\Documents\AI AGENT 工作區\GOOGLE FLOW"
) + ((Get-PSDrive -PSProvider FileSystem).Root | ForEach-Object {
    Join-Path $_ "AI_Workspace\GOOGLE FLOW"
    Join-Path $_ "AI AGENT實驗區\GOOGLE FLOW"
}) | Where-Object { Test-Path $_ } | Select-Object -First 1
$flowPy = Join-Path $flowRoot ".venv\Scripts\python.exe"
$flowMain = Join-Path $flowRoot "src\main.py"

$projectRoot = (Get-Location).Path
$targetDir = Join-Path $projectRoot "assets\generated"
if (-not (Test-Path $targetDir)) { New-Item -ItemType Directory -Force -Path $targetDir | Out-Null }

$outputFile = Join-Path $targetDir ("flow_vid_" + (Get-Date -Format "yyyyMMdd_HHmmss") + ".mp4")
$prompt = "A drone flying over majestic snowy mountains at sunrise, smooth cinematic camera motion"

# 執行自動化生片 (支援 --duration 3s~15s, --resolution 360p[30點]/720p[60點], 預設 --outputs 1 單部生成省點數)
& $flowPy $flowMain --mode video --aspect 16:9 --duration 15s --resolution 360p --outputs 1 --prompt $prompt --output $outputFile

if ($LASTEXITCODE -eq 0 -and (Test-Path $outputFile)) {
    Write-Host "Google Flow 生片成功：$outputFile"
}
```

## 4. 接續生成既有影片 (Veo Extend - 鏡頭接續)

```powershell
$flowRoot = @(
    "$HOME\Documents\AI AGENT 工作區\GOOGLE FLOW"
) + ((Get-PSDrive -PSProvider FileSystem).Root | ForEach-Object {
    Join-Path $_ "AI_Workspace\GOOGLE FLOW"
    Join-Path $_ "AI AGENT實驗區\GOOGLE FLOW"
}) | Where-Object { Test-Path $_ } | Select-Object -First 1
$flowPy = Join-Path $flowRoot ".venv\Scripts\python.exe"
$flowMain = Join-Path $flowRoot "src\main.py"

$projectRoot = (Get-Location).Path
$targetDir = Join-Path $projectRoot "assets\generated"
if (-not (Test-Path $targetDir)) { New-Item -ItemType Directory -Force -Path $targetDir | Out-Null }

$outputFile = Join-Path $targetDir ("flow_extend_" + (Get-Date -Format "yyyyMMdd_HHmmss") + ".mp4")
$prompt = "The camera pans down to reveal a hidden ancient temple hidden beneath the trees"

# 執行接續生片 (以畫布上上一段影片的最後一幀為基準繼續生下一段分鏡，每次延長最多 10 秒)
& $flowPy $flowMain --extend --duration 10s --prompt $prompt --output $outputFile
```

## 5. 分鏡劇本與角色一致性管線 (Storyboard Pipeline)

汲取 FlowKit 最佳實踐：
- **角色外貌與分鏡動作嚴格分離**：
  - 角色實體 (Entity)：只寫外表、面容、服裝特徵（直向 9:16 肖像），產生基準參考圖。
  - 分鏡場景 (Scene)：只寫動作與電影運鏡（橫向 16:9），絕不重述角色長相。
- **時序分段切分 (Sub-clip Temporal Staging)**：
  - 例如：`0-4s: [運鏡] + 起始動作. 4-10s: [運鏡] + 核心動作. 10-15s: [運鏡] + 收尾接續.`
- **調用方式**：
  ```powershell
  $flowRoot = @(
      "$HOME\Documents\AI AGENT 工作區\GOOGLE FLOW"
  ) + ((Get-PSDrive -PSProvider FileSystem).Root | ForEach-Object {
      Join-Path $_ "AI_Workspace\GOOGLE FLOW"
      Join-Path $_ "AI AGENT實驗區\GOOGLE FLOW"
  }) | Where-Object { Test-Path $_ } | Select-Object -First 1
  $flowPy = Join-Path $flowRoot ".venv\Scripts\python.exe"
  $flowMain = Join-Path $flowRoot "src\main.py"

  # 執行完整分鏡劇本 (自動生成角色基準圖 -> 循序生成各分鏡影片與 Extend 接續)
  & $flowPy $flowMain --storyboard "data/storyboards/gundam_wing_pilot_demo.json"

  # 僅生成角色基準參考圖
  & $flowPy $flowMain --storyboard "data/storyboards/gundam_wing_pilot_demo.json" --refs-only
  ```

## 注意事項與除錯

1. **語系自動鎖定**：本工具已融合 `?hl=en` 參數，強制將 Google Flow 介面保持為英文 DOM，避免不同語系按鈕失效。
2. **登入態過期**：若終端機報錯提示「需要登入驗證」，請切換到 Google Flow 專案目錄執行 `start.bat` 選項 `[1]` 重新在跳出的原生視窗中完成驗證。
3. **影片運算時間**：Veo 影片伺服器端排程與渲染需時約 1~3 分鐘，工具內建最長 300 秒智慧輪詢監控。
4. **點數扣除**：直接消耗使用者該 Google 帳號內的 Flow 專屬點數與每日 50 點免費配額，完全不產生 Google Cloud API 費用。
