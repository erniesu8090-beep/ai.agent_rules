# 管制機專屬規則（只安裝在管制機）

> 由 `install.bat controlled` 附加，僅管制機 AI 讀（`home`／`dev` 不受限）。限制「AI 在本機的操作」；「成品本身」防毒相容在公司專案 `AGENTS.md`「公司專案規則」區塊，三台適用。本體在 `ai.agent_rules/machine_rules/controlled.md`。

## A. 防毒行為監控（Apex One）
防毒會直接終止「AI 背景程序 → 產生或啟動腳本、繞過執行原則」並發告警。在本機：
- **不在終端機用指令產生可執行腳本**（`.bat`、`.cmd`、`.ps1`、`.vbs`），如 `Set-Content`、`Out-File`、`echo >`、`[IO.File]::WriteAllText`；專案原始檔（`Launcher.bat`、`scripts\popup.ps1`）用編輯工具建改不受限。
- **終端機禁用 Bypass 與呼外部程式的 VBS**：指令禁帶 `-ExecutionPolicy Bypass`、`-ep bypass`；不從終端機跑含 Bypass 的啟動器（`Launcher.bat`、`GitSync_GUI.bat`，請使用者雙擊回報）；**禁寫或跑呼 `Shell.Application`（`ShellExecute`）的 `.vbs`**，會被防毒攔截發告警（2026-10-20 實測）。
- **臨時腳本與可直跑指令**：一次性腳本用程式碼區塊交使用者存檔雙擊（檔案總管雙擊不攔）。可直跑：`git`（`D:\AI_Workspace\bundle.gitsync\PortableGit\cmd\git.exe`）、`py -3.11`、`.venv\Scripts\python.exe` 及唯讀診斷（`Get-Process`、`Test-NetConnection`、`curl.exe -I`、`Resolve-DnsName`、`Get-ChildItem`）。被攔立刻停並告知，勿換寫法重試。

## B. 安裝軟體與 Python
- 僅裝「目前使用者、免管理員」軟體（見 UAC 盾牌就停）；AI 工具僅 Antigravity 與 OpenCode（無 Claude Code、Codex）。
- Python 3.11.9 未加 PATH（本機目前僅有 3.11 與 3.12，無 3.13）：建 venv 用 `py -3.11 -m venv .venv`，執行一律用 `.venv\Scripts\python.exe`（勿直呼 `python` 指到 Win 假捷徑）。

## C. 終端機與語法
- 為 Windows PowerShell 5.1，禁 PS7 語法（見 `guidelines/script_encoding.md`）：`?.`、`??`、`&&`／`||`、三元 `a ? b : c`、`ConvertFrom-Json -AsHashtable`、`ForEach-Object -Parallel`。字碼頁 950（Big5）：含中文 `.ps1` 必存 UTF-8 with BOM；cmd `type` 看 UTF-8 會亂碼，改用記事本。

## D. 網路（2026-11-17～18 最新實測）
- **內網**：唯一可連公司內網（伺服器、NAS）。
- **全時段可連**：PyPI、python.org、npm（`registry.npmjs.org`）、一般 CDN；Google 雲端硬碟網頁版、`dl.google.com`、`script.google.com`、`www.googleapis.com`、`*.run.app`、`generativelanguage.googleapis.com`、`cloudaicompanion.googleapis.com`、`api.opencode.ai`（OpenCode 免費端點）。
- **日間開放（`07:30~17:30`）**：`oauth2.googleapis.com`（OAuth 授權）、`github.com`、`api.github.com`、`gist.github.com`（支援 `git` 與核心 `gh`；非此時段仍阻斷）。
- **全時段阻斷／逾時**（未確認先請使用者實測）：`raw.githubusercontent.com`、`objects.githubusercontent.com`、`codeload.github.com`（影響 Raw、Releases、LFS；非上班時段同步改用 `.bundle`）、`*.gvt1.com`（`edgedl.me.gvt1.com` 致 Antigravity 自動更新卡住，下載改 `dl.google.com`）、`openrouter.ai`（OpenCode 限官方免費模型）與 Codex／OpenAI 生圖（管制機生圖走 Antigravity `image-generator` 或由開發機帶入）。
