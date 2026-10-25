# 全域 AI Agent 規則

> **一律用繁體中文（台灣用語）回答使用者**，不論使用哪個模型、哪個 Effort 等級，細節見第 3 節。
> **提問先行（重要）**：需求、規格或做法有不明確、而且會影響結果的地方時，**先停下來問使用者，確認後再動手**，不要自己假設。理由：使用者不是專業工程師，方向猜錯時不一定看得出來，重做的成本很高。不影響結果的小事（例如變數命名）照常識處理即可，不必詢問。

> 安裝位置：Claude Code → `~/.claude/CLAUDE.md`；Antigravity → `~/.gemini/GEMINI.md`；Codex → `~/.codex/AGENTS.md`；OpenCode → `~/.config/opencode/AGENTS.md`
> 規則本體在 ai.agent_rules 倉庫的 `global_rules.md`，要修改請改倉庫再重新執行安裝腳本，不要直接改安裝後的檔案。
> 優先順序：專案根目錄 `AGENTS.md` > 工作區 `AGENTS.md`（例：`D:\AI_Workspace\AGENTS.md`）> 本全域規則。

## 0. 關於使用者

- 非專業程式設計師，以 Vibe Coding 方式開發；個人專案以金融交易工具與遊戲輔助工具為主，另有公司工作用的專案。
- 說明請淺白、少用術語；交付可直接執行的完整檔案與操作步驟，不要只給片段。

## 1. 電腦環境

| 代號 | 電腦 | AI 工具 | 安裝軟體 | 網路 | 用途 |
|---|---|---|---|---|---|
| 住家開發機（home） | 住家個人電腦（Windows 或 Ubuntu，可能不只一台） | Claude Code、Antigravity、Codex、OpenCode | 不限 | 外網、GitHub；不能連公司內網 | 個人專案；公司專案開發（經 GitHub 與公司開發機同步） |
| 公司開發機（dev） | 公司個人電腦，Win11 | Claude Code、Antigravity、Codex、OpenCode | 不限 | 外網、GitHub；不能連公司內網 | 公司專案開發；GitHub 與管制機之間的中繼 |
| 管制機（controlled） | 公司電腦，Win10 22H2 | Antigravity、Codex、OpenCode | **受限**：無管理員權限、有防毒軟體攔截 | **唯一能連公司內網的電腦**（內網伺服器、NAS）；外網有限制：不能連 GitHub，PyPI、python.org、CDN、Google 雲端硬碟網頁、Google API（`www.googleapis.com`、`oauth2.googleapis.com`，2026-10-13）實測可連，其他網站未確認 | 公司專案接力開發、內網功能驗證、發布 |
| 同事電腦 | 公司同事使用 | 無 | 受限，通常沒有 Python | 公司內網 | 只執行發布出去的成品 |

- 住家開發機與公司開發機合稱「開發機」，兩台都連不到公司內網。
- 安裝後的規則檔最後一行 `THIS MACHINE:` 標示這台電腦的身分（home / dev / controlled），以此判斷目前在哪一台；沒有標示時先詢問使用者。
- 只適用於某一台的規則放在 `machine_rules/<電腦代號>.md`，安裝時只附加到那一台（例如管制機的防毒與網路限制只出現在管制機）。開發機上的 AI 不受管制機專屬規則限制，但寫給管制機或同事電腦執行的程式仍要相容（見公司專案規則與第 7 節）。
- 管制機要用到表上沒列的外部網站或服務時，先請使用者在管制機實測能不能連，不要假設可以。
- 每個專案的 `AGENTS.md` 要註明「目標執行環境」；沒有註明時先詢問使用者。

- 開發用 CLI：使用者要求檢查時，依 README「開發用 CLI 清單」逐一確認（`Get-Command`／Ubuntu `command -v`），列出缺少的工具，**經使用者同意再安裝**；使用者新裝了其他開發用 CLI 時，提醒補進清單。

## 2. 公司專案

- 定義：`AGENTS.md` 的目標執行環境含管制機或同事電腦的專案；上一層資料夾就是「公司工作區」。
- 公司專案的詳細規則（內網與發布、成品的防毒相容、除錯與回報、跨專案規範審查）寫在該專案 `AGENTS.md` 的「公司專案規則」區塊，由 ai.agent_rules 倉庫的 `templates/AGENTS_company.md` 建立。
- 區塊開頭有「公司規則版本：日期」。專案沒有這個區塊、或範本的版本比較新時，先讀範本照做，並提醒使用者合併（整段替換開始與結束標記之間的內容）；`AGENTS.md` 註明「本專案不套用」的除外。
- 資料保密：錯誤訊息或截圖可能含有內網主機名稱、IP、帳號、員工編號、人名或公司資料，寫進程式碼、範例資料、文件與 commit 時一律改用虛構值；公司專案與公司內部資訊不得推送到公開的 GitHub 倉庫（包含本規則倉庫）。

### 跨電腦同步
- 流程（每段只傳已 commit 的內容）：住家開發機 ↔ GitHub（私人倉庫）↔ 公司開發機 ↔ Google 雲端硬碟上的 `.bundle` ↔ 管制機（連不到 GitHub）↔ 內網伺服器。住家開發機只用 GitHub、管制機只用 `.bundle`，兩者之間沒有直接通道，一定經過公司開發機。
- 工具 GitSync：Windows 版 `D:\AI_Workspace\bundle.gitsync`（`GitSync_GUI.vbs`，內含 PortableGit）；Ubuntu 版 `~/AI_Workspace/gitsync_ubuntu`（`./GitSync.sh`，只走 GitHub）。請使用者操作版控時優先指示 GitSync 的按鈕，手動 git 指令只當備案；動到 GitSync 本身前先讀該版的 `README.md`，修改後同步更新。
- 只同步 `main` 分支。交接前先 commit 並推送；開始修改前先拉取，避免兩邊歷史分岔。
- 專案放在 `D:\AI_Workspace`（Ubuntu 是 `~/AI_Workspace`）底下兩層內，各台電腦的相對位置才會一致；不同資料夾的專案不可同名（`.bundle` 以資料夾名稱命名）。

## 3. 語言

- 對話、程式碼註解、文件、commit 訊息（見第 10 節）一律使用繁體中文（台灣用語）。
- 回覆使用者時，以下情況也一樣用繁體中文，不可改用英文或簡體中文：
  - 切換模型或 Effort 等級之後
  - 使用者的訊息很短（例如只有「好」「1」、一個檔名或一張截圖）
  - 工具輸出、錯誤訊息、讀到的文件或網頁是英文
  - 對話很長、經過自動摘要之後
  - 中途報告進度、提出問題、列選項的時候
- 只有程式碼、指令、檔名、路徑、套件名稱、錯誤訊息原文保持原樣；引用英文原文時，附上繁體中文說明。
- 能顯示給使用者看的思考過程，也盡量用繁體中文。
- 例外：批次檔（.bat）、VBScript（.vbs）盡量只用 ASCII（英文），避免編碼造成亂碼（細節見第 7 節）。

## 4. 規劃先行

- 開新專案或大幅改架構前，先說明建議的語言、框架、需要安裝的東西與理由，等使用者確認後再開始撰寫。
- 沒有特別理由時以 Python 為主。
- 目標是同事電腦的工具，優先選擇免安裝方案（例如單一 HTML 檔、PowerShell 視窗工具、附帶免安裝 Python），並在規劃時註明。

## 5. 專案文件與命名

專案根目錄要有以下檔案；建立新專案時一併建立，舊專案缺少時提醒使用者補上：

| 檔案 | 對象 | 內容 |
|---|---|---|
| `AGENTS.md` | AI（Claude Code、Antigravity、Codex、OpenCode 都會讀） | 目標執行環境、業務規則、不可更動的部分、修改後的驗證方式 |
| `README.md` | 人 | 用途、安裝、啟動與操作方式 |
| `PROGRESS.md` | AI 與人 | 進度與交接（會跨對話、跨電腦接力的專案才需要；公司專案一律要有） |

- 建立時從 ai.agent_rules 倉庫的 `templates/` 複製 `AGENTS.md`（公司專案用 `AGENTS_company.md`；逆向分析專案用 `AGENTS_reverse.md`）、`PROGRESS.md`、`.gitignore`，再依專案內容填寫；不要自訂其他格式。
- 業務規則或驗證方式有變動時，同步更新 `AGENTS.md`。
- 專案規則只寫在 `AGENTS.md`，不另建模組化規則資料夾（`.agents/rules/`、`.claude/rules/`）；只有規則多到需要「依檔案類型分開套用」時才拆。發現只有一個、且永遠套用（`always_on`）的規則檔時，建議併入 `AGENTS.md` 後刪除。
- 工作區規則檔只在「好幾個專案共用、但不適合放全域」（例如公司內部資訊）時才建立，檔名用 `AGENTS.md`（例：`D:\AI_Workspace\AGENTS.md`）；全域規則已涵蓋的內容不要重複寫。
- 注意：Antigravity、Codex、OpenCode 往上找規則檔只到 Git 倉庫根目錄為止，讀不到專案外的工作區 `AGENTS.md`（2026-10-10 實測）。工作區規則只對 Claude Code 有效；所有工具都要遵守的規則放全域或專案。

### `CLAUDE.md` 與 `AGENTS.md`
- 開發機的 Claude Code 由安裝腳本設定成 `CLAUDE.md` 與 `AGENTS.md` 都讀（`~/.claude/settings.json` 的 `instructionFiles: "claude-md-and-agents-md"`）。沒有這個設定時，路徑上只要有 `CLAUDE.md`、`.claude/CLAUDE.md` 或 `CLAUDE.local.md`，所有 `AGENTS.md` 都會被跳過、不提示。
- 自己的專案與工作區只寫 `AGENTS.md`，不建立上述三種檔案、不用 `/init`：Antigravity 與 Codex 預設不讀 `CLAUDE.md`（OpenCode 雖有 `CLAUDE.md` 相容回退，但已有 `AGENTS.md` 時只讀 `AGENTS.md`）。
- fork 別人的專案已有 `CLAUDE.md`：不修改、不刪除（方便同步上游），自己的規則寫在 `AGENTS.md`；`CLAUDE.md` 的內容 Antigravity 與 Codex 預設讀不到，需要時先問使用者要不要在 `AGENTS.md` 摘要重點。
- 確認方法（Claude Code）：開新對話時自行比對，目前資料夾與上層資料夾有 `AGENTS.md`、但載入的規則裡沒有它的內容時，開頭就告訴使用者，並檢查 `~/.claude/settings.json`；使用者也可以執行 `/memory` 人工確認。
- 各家 coding agent 的規則載入方式見 ai.agent_rules 倉庫的 `doc/coding_agent_features.md`；處理規則檔、Skill、Hook 設定時，該檔「最後全面查證」超過 1 個月就提醒使用者重新查證。

### 進度交接檔 `PROGRESS.md`
- 有 `PROGRESS.md` 的專案，`AGENTS.md` 開頭要寫「接手工作前先讀 `PROGRESS.md`」；新對話開始時依序讀 `AGENTS.md` → `PROGRESS.md`，再動手。
- 分工：`AGENTS.md` 放長期不變的規則；`PROGRESS.md` 放會變動的進度、決定與待辦。某個決定變成長期規則時，搬進 `AGENTS.md`。
- 固定章節（範本：`ai.agent_rules/templates/PROGRESS.md`）：目前階段／使用者已確認的事（附日期）／待使用者決定（編號；決定後加刪除線並移到「已確認」）／已查證的發現（附出處）／試過但無效的做法（含最後一個正常運作的 commit）／下一步／接手須知（環境、工具用法、不在 Git 的資料與放置方式）／修訂紀錄。
- 每次工作告一段落、或使用者說要換電腦時更新：開頭「最後更新：日期（電腦）」，電腦依 `THIS MACHINE` 判斷；修訂紀錄加一列「日期｜電腦｜內容」。
- 更新後跟著同一次 commit 一起提交（停損時例外，只提交 `PROGRESS.md`，見第 9 節）；沒有 commit 的話，另一台電腦拿不到最新進度。
- 只寫結論與出處，不貼大段原文或對話紀錄；機密規則同第 8 節。
- 使用者對提醒回答「之後再說」時，當場寫進「待使用者決定」並附日期與原因；只在對話中提醒，換對話就會遺失。

### 命名
- 命名：專案根目錄用「點」或「底線」組合（例：`tw.stock_assistant`、`tickets_snatcher`）；專案內部的檔案與資料夾只用底線。

### 專案內資料夾（商業軟體式收納）
- **根目錄極簡化**：比照商業軟體，專案根目錄只放「啟動器（`.bat`、`.cmd`、`.vbs`、`.exe`、`.sh`）」、「使用說明（`README.md`、`使用說明.txt`）」、「AI 規則與交接檔（`AGENTS.md`、`PROGRESS.md`）」與必要的環境設定檔（`.gitignore`、`.env`、`requirements.txt`、`.venv/`）；**禁止**在根目錄散落 `.py` 程式碼、零散素材、測試檔或中繼檔，一律分類收進 `src/`、`assets/`、`config/`、`data/`、`logs/`、`tests/` 等子資料夾。
- 常用資料夾與用途見 README「專案內資料夾」；有需要才建立，不預先建立空資料夾。
- `web/` 整個資料夾就是發布白名單，不放開發用的檔案；`sample_data/` 一律用虛構值；`logs/`、`scratch/` 列入 `.gitignore`。
- 同一套業務同時有網站靜態版和 Python 版時，判定或計算的核心只維護一份，由兩邊共用。
- 既有專案的資料夾名稱已經寫進程式路徑時，可以維持原名，並在該專案的 `AGENTS.md` 註明例外。

## 6. Python 環境

- 全域 Python 只保留直譯器本體與基礎工具（pip、setuptools），嚴禁在全域安裝任何第三方套件（包含 `pip install --user`）。
- 每個專案使用獨立虛擬環境 `.venv`；執行、測試指令一律使用 `.venv` 內的 Python。
- Python 版本：公司專案（`AGENTS.md` 的目標執行環境含管制機或同事電腦）在每台電腦都用 3.11 系列，`requirements.txt` 全部鎖定版本；Ubuntu 開發機沒有 3.11，用 `uv venv --python 3.11 --seed .venv` 建立，不動系統 Python。其他個人專案用該台電腦現有的 Python 3。
- Python 3.11 的安全更新到 2027-10 結束；升級前不改用 3.11 以外的版本，不使用無 GIL 版（`3.13t`／`3.14t`）。對話中提到 Python 版本時，若已過 2027-01 且還沒升級，提醒使用者（評估步驟見 README「Python 升級評估」）。
- `requirements.txt` 完整列出所有第三方套件；有已知相容性問題的套件要鎖定版本並註明原因。
- 個人專案的啟動腳本要自動處理：沒有 `.venv` 就建立、`requirements.txt` 有變動就重新安裝，然後啟動程式。公司專案的啟動器依公司專案規則，不自動建立 `.venv`。

## 7. 路徑、編碼與腳本

- 路徑：禁止硬編碼磁碟代號（`C:\`、`D:\`）與反斜線，使用 `pathlib.Path`，並以程式檔所在位置推算專案路徑；檔名大小寫保持一致（Linux 區分大小寫）。
- 文字檔（.py、.json、.md、.html、.csv）一律 UTF-8；Python 開檔時明確指定 `encoding="utf-8"`。
- `.bat`：CRLF 換行，開頭加 `cd /d "%~dp0"`，路徑變數一律加雙引號。預設只用 ASCII；確實需要中文時（例如既有的公司工具），存成 ANSI / Big5（CP950），不可存 UTF-8，並避開第二個位元組是 `\`、`|`、`^` 的字（例如「許、功、蓋」）。
- `.vbs`：只用 ASCII。
- `.ps1`：含中文時存成 UTF-8 with BOM（Windows PowerShell 5.1 才不會亂碼）。要在管制機或同事電腦執行的 `.ps1` 只能用 PowerShell 5.1 語法（不可用 `?.`、`??`、`&&`／`||`、三元運算等 PowerShell 7 語法）。交給使用者雙擊的 `.bat` 啟動 `.ps1` 時，在 `.bat` 檔案內寫 `powershell -NoProfile -ExecutionPolicy Bypass -File`。
- `.sh`：LF 換行，並具備執行權限。
- 需要在 Linux 執行的專案：Windows 專屬指令（taskkill、netstat、start、cmd.exe 等）必須以 `sys.platform` 判斷分流，並同時提供 Linux 對應作法。

## 8. 機密與安全

- API Key、密碼、憑證放在 `.env`（或專案指定的位置），由程式讀取，並提供 `.env.example` 範本；禁止寫死在程式碼中。
- `.gitignore` 至少排除：`.env`、`.env.*`（保留 `!.env.example`）、憑證檔（`*.pfx` 等）、`.venv/`、`__pycache__/`、`*.log`、本機快取資料。
- 未經使用者同意：不得 `git push`（包含推送到 `.bundle`）、不得刪除或覆寫資料檔與歷史資料、不得修改全域設定。
- 寫給使用者用的工具，刪除檔案時移到資源回收筒、覆寫前先備份，不直接永久刪除。

## 9. 開發與驗證

- 串接外部 API 前，先查專案內的 API 文件資料夾（例如 `docs/api`）；沒有時再查官方文件，並說明資料來源。
- 呼叫有額度或次數限制的 API（例如券商行情）時，節制測試次數。
- **AI 生圖限制（順序不可顛倒）**：需要生成點陣圖素材時，**第一優先**使用 Codex 內建 `$imagegen`（在 Codex 內直接呼叫，或在 Antigravity／Claude Code／OpenCode 透過 `codex-imagegen-bridge` 技能以 `codex exec` 連動 ChatGPT 登入額度）；**第二優先**使用 Antigravity 內建 `gemini-3.1-flash-image` 或更高版本（在 Antigravity 內直接呼叫 `image-generator` 子代理，或在其他工具透過 `agy-imagegen-bridge` 技能以 `agy -p` 連動 Antigravity 登入額度，詳見 README「AI 生圖規範」）。嚴禁使用 Pollinations 等第三方免費生圖網站、帶浮水印或降畫質服務，未經使用者明確同意亦不得呼叫需 `OPENAI_API_KEY` 的付費 API。
- 修改後依專案 `AGENTS.md` 的驗證方式自我檢查，至少確認語法正確、程式可以啟動；宣告完成前要實際執行驗證，並附上輸出。
- 不可刪除、跳過或修改既有測試、放寬判定條件來讓測試通過。
- 只改與任務相關的檔案；需要動到其他檔案時先說明理由。
- 大任務先拆成步驟（寫進 `PROGRESS.md` 的「下一步」），一次只做一步，每步驗證後再進下一步。
- 同一個問題修了兩次仍失敗：停止修改，把摘要（症狀、已排除的原因、已嘗試的修法與各自結果、目前最可能的原因、最後一個正常運作的 commit、下一步建議）寫進 `PROGRESS.md`，請使用者決定是否開新對話或換模型接手。最後一個正常運作的 commit 以使用者告知為準，沒說就先問。
- 停損時只 commit `PROGRESS.md`，改壞的程式碼不 commit（留給同一台電腦的接手者用 `git diff` 檢視）；回報時列出這些未提交的檔案，提醒使用者用 GitSync 提交時先不要勾選。
- 只有使用者能實測的部分（例如管制機上的內網功能、遊戲內效果、下單、盤中行情），要明確說明怎麼測、預期看到什麼結果。
- 區分「確認」與「推測」：除錯時看不到實際檔案或畫面、說明程式架構或流程（含畫流程圖）時，分清楚哪些是實際讀到程式碼或畫面確認的、哪些是推測，推測的部分明確標示，不要把推測當成結論；並附上可以驗證的指令或操作步驟（流程圖至少挑一條主要流程）與預期結果。
- 查證類回答（版本號、發布日期、支援的 Python／作業系統、價格、API 規格）：每一項標示「已查證（附來源網址或指令）」或「推測」，查不到就寫查不到，不可用推論補成事實；先列事實、再給建議，兩者分開寫；不用「令人驚喜」「萬無一失」「100% 穩定」這類誇張用語，結論前後要一致（例如 `abi3` 代表後續版本通用，就不可同時說新版不支援）。
- 程式涉及登入／帳密、權限、刪除或覆寫檔案、下單或金流時，修改後主動用白話說明風險（可能出什麼事、怎麼防範、怎麼測），不等使用者問。
- 測試要能真正證明結論：例如 pip 顯示 `Using cached` 不代表能連網、`Requirement already satisfied` 不代表能安裝。
- 回報時如實說明哪些已驗證、哪些未驗證；測試失敗要附上錯誤訊息。

## 10. 版本控制（Git）

- commit 訊息用繁體中文，精簡說明主要變更。
- 共同作者以「實際編寫程式碼的助理」為準，不是執行 `git commit` 的助理；署名放在訊息最末尾，前面空一行：
  - Claude Code 編寫：`Co-authored-by: Claude <noreply@anthropic.com>`
  - Antigravity 編寫：`Co-authored-by: Antigravity <noreply@google.com>`
  - Codex 編寫：`Co-authored-by: Codex <noreply@openai.com>`
  - OpenCode 編寫：`Co-authored-by: OpenCode <noreply@opencode.ai>`
  - 多個助理都有貢獻：多行並列。
- 這個對話中自己沒有參與編寫、使用者卻要求 commit 時，先問使用者主要編寫者，不可擅自署名自己。
