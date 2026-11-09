# 管制機專屬規則（只安裝在管制機）

> 本段由 `install.bat controlled` 附加在全域規則之後，只有管制機上的 AI 工具看得到（開發機 home／dev 不受本段限制）。本段限制「AI 在這台電腦上的操作」；「成品本身」的防毒相容規則在各公司專案 `AGENTS.md` 的「公司專案規則」區塊，三台都適用。規則本體在 ai.agent_rules 倉庫的 `machine_rules/controlled.md`。

## A. 防毒行為監控（Apex One）
管制機的端點防毒會直接終止「AI 工具的背景程序 → 產生或啟動腳本、繞過執行原則」這類行為，並發出資安告警。在這台電腦上：
- **不在終端機用指令產生可執行腳本**（.bat、.cmd、.ps1、.vbs），例如 `Set-Content`、`Out-File`、`echo >`、`[IO.File]::WriteAllText`；專案的原始檔（例如 `Launcher.bat`、`scripts\popup.ps1`）用編輯工具建立或修改，不受此限。
- **終端機禁用 Bypass 與呼叫外部程式的 VBS**：終端機指令不可出現 `-ExecutionPolicy Bypass`、`-ep bypass` 等繞過參數；不從終端機執行內含 Bypass 的啟動器或工具（例如專案的 `Launcher.bat`、GitSync 的 `GitSync_GUI.bat`，需要測試時請使用者自己雙擊執行再回報結果或截圖）；**不撰寫或執行呼叫 `Shell.Application`（`ShellExecute`）的 .vbs 腳本**，呼叫外部程式會被端點防毒行為監控直接攔截並發出資安告警（2026-10-20 實測）。
- **臨時腳本與可直接執行的指令**：臨時、一次性要執行的腳本用程式碼區塊交給使用者，由使用者用記事本存檔後自己雙擊執行（檔案總管雙擊不會被攔截）。可以直接執行：`git`（`D:\AI_Workspace\bundle.gitsync\PortableGit\cmd\git.exe`）、`py -3.11`、`.venv\Scripts\python.exe`，以及只讀取資訊的診斷指令（例如 `Get-Process`、`Test-NetConnection`、`curl.exe -I`、`Resolve-DnsName`、`Get-ChildItem`）。指令被防毒攔截時：停下來，把防毒的訊息告訴使用者，不要換一種寫法重試。

## B. 安裝軟體與 Python
- 只能安裝「僅限目前使用者、不需管理員權限」的軟體（出現 UAC 盾牌就停下）；AI 工具僅使用 Antigravity 與 OpenCode（無法使用 Claude Code 與 Codex）。
- Python 3.11.9 以「僅限目前使用者」安裝、未加入 PATH：建 venv 用 `py -3.11 -m venv .venv`，執行一律用 `.venv\Scripts\python.exe`。不要直接呼叫 `python`，它會指到 Windows 內建的假捷徑。

## C. 終端機與語法
- 終端機是 Windows PowerShell 5.1，不可使用 PowerShell 7 才有的語法：`?.`、`??`、`&&`／`||`、三元運算 `a ? b : c`、`ConvertFrom-Json -AsHashtable`、`ForEach-Object -Parallel` 等。主控台字碼頁是 950（Big5）：含中文的 `.ps1` 必須是 UTF-8 with BOM，否則中文會變亂碼並破壞語法；在 cmd 用 `type` 看 UTF-8 檔案會亂碼，請改用記事本開。

## D. 網路
- **內網與外網可正常連線（實測可連）**：唯一能連公司內網（內網伺服器、NAS）的電腦。外網可連：PyPI、python.org、npm（`registry.npmjs.org`）、一般 CDN；Google 雲端硬碟網頁版、`dl.google.com`、`script.google.com`（GAS 中繼）、`www.googleapis.com`；AI 模型與助理端點 `generativelanguage.googleapis.com`（Gemini 核心模型）、`cloudaicompanion.googleapis.com`（AI 程式助理端點）、`api.opencode.ai`（OpenCode 免費模型端點）。
- **外網受限與無法連線**（其他未確認的外部網站或服務，先請使用者在管制機實測能不能連，不要假設可以）：
  - **不能連 GitHub、OpenRouter 與 Codex 生圖**：代碼同步由開發機透過 Google 雲端硬碟的 `.bundle` 帶過來；OpenRouter（`openrouter.ai`）與 Codex／OpenAI 生圖無法連線（2026-10-27、11-03 實測），在管制機上 OpenCode 限用官方免費模型，生圖直接走第二優先的 Antigravity 內建 `image-generator` 子代理，或在開發機生成後以 `.bundle` 帶過來。
  - **無法連線至 `oauth2.googleapis.com`（2026-10-22 實測）與 `*.gvt1.com`（逾時）**：Antigravity 無法刷新 OAuth Token 換取模型額度，GitSync「API 直連」模式無法換發 Google Drive Access Token（需切換為「手動」模式透過瀏覽器上傳/下載 `.bundle`）；`edgedl.me.gvt1.com` 等會讓 Google 系列工具（Antigravity 等）自動更新卡住，下載 Google 安裝檔時手動把網址中的 `edgedl.me.gvt1.com` 換成 `dl.google.com` 即可。
