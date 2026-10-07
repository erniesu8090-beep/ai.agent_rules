
# 管制機專屬規則（只安裝在管制機）

> 本段由 `install.bat controlled` 附加在全域規則之後，只有管制機上的 AI 工具看得到。開發機（home／dev）不受本段限制。
> 本段限制的是「AI 在這台電腦上的操作」；「成品本身」的防毒相容規則在全域規則第 2 節，三台都適用。
> 規則本體在 ai.agent_rules 倉庫的 `machine_rules/controlled.md`。

## A. 防毒行為監控（Apex One）

管制機的端點防毒會直接終止「AI 工具的背景程序 → 產生或啟動腳本、繞過執行原則」這類行為，並發出資安告警。在這台電腦上：

- **不在終端機用指令產生可執行腳本**（.bat、.cmd、.ps1、.vbs），例如 `Set-Content`、`Out-File`、`echo >`、`[IO.File]::WriteAllText`。專案的原始檔（例如 `Launcher.bat`、`scripts\popup.ps1`）用編輯工具建立或修改，不受此限。
- **終端機指令不可出現 `-ExecutionPolicy Bypass`、`-ep bypass`** 等繞過執行原則的參數。
- **不從終端機執行內含 Bypass 的啟動器或工具**（例如專案的 `Launcher.bat`、GitSync 的 `GitSync_GUI.bat`）；需要測試時，請使用者自己雙擊執行，再回報結果或截圖。
- 臨時、一次性要執行的腳本：用程式碼區塊交給使用者，由使用者用記事本存檔後自己執行（使用者在檔案總管雙擊不會被攔截）。
- 可以直接執行：`git`（`D:\AI_Workspace\bundle.gitsync\PortableGit\cmd\git.exe`）、`py -3.11`、`.venv\Scripts\python.exe`，以及只讀取資訊的診斷指令（例如 `Get-Process`、`Test-NetConnection`、`curl.exe -I`、`Resolve-DnsName`、`Get-ChildItem`）。
- 指令被防毒攔截時：停下來，把防毒的訊息告訴使用者，不要換一種寫法重試。

## B. 終端機與語法

- 終端機是 Windows PowerShell 5.1，不可使用 PowerShell 7 才有的語法：`?.`、`??`、`&&`／`||`、三元運算 `a ? b : c`、`ConvertFrom-Json -AsHashtable`、`ForEach-Object -Parallel` 等。
- 主控台字碼頁是 950（Big5）：含中文的 `.ps1` 必須是 UTF-8 with BOM，否則中文會變亂碼並破壞語法。

## C. 網路

- 企業防火牆會阻擋 `*.gvt1.com`（例如 `edgedl.me.gvt1.com`，約 20 秒後連線逾時），Google 系列工具（Antigravity 等）的自動更新會卡住；`dl.google.com` 可以連。需要下載 Google 工具的安裝檔時，把網址中的 `edgedl.me.gvt1.com` 換成 `dl.google.com`。
- 其他未列在全域規則第 1 節的外部網站，先請使用者實測能不能連，不要假設可以。
