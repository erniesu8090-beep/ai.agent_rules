# ai.agent_rules

我的 AI 寫程式工具（Claude Code、Antigravity）共用的**全域規則檔**，放在 GitHub 上方便每台電腦下載安裝。

## 檔案說明

| 檔案 | 用途 |
|---|---|
| `global_rules.md` | 全域規則本體（要改規則就改這個檔） |
| `AGENTS.md`、`CLAUDE.md` | 維護本倉庫時給 AI 看的專案規則 |
| `install.bat` | Windows 安裝：雙擊執行 |
| `install.sh` | Linux / macOS 安裝 |
| `templates/` | 新專案範本：`AGENTS.md`、`CLAUDE.md`、`PROGRESS.md`、`.gitignore` |

## 安裝

三台有 AI 工具的電腦都要安裝：住家開發機、公司開發機、管制機。

1. 取得這個倉庫，放在 `D:\AI_Workspace\ai.agent_rules`（Ubuntu 放在 `~/AI_Workspace/ai.agent_rules`）：
   - 住家開發機、公司開發機：從 GitHub `git clone`。
   - 管制機（連不到 GitHub）：用 GitSync 同步。先在公司開發機用 GitSync「管理專案 / .venv」→「可加入的資料夾」把本倉庫加入清單並推送到 `.bundle`；再到管制機下載 `.bundle`，用「從 .bundle 建立」取得本倉庫。
2. Windows：雙擊 `install.bat`，依提示按 `1`、`2` 或 `3` 選擇這台是哪一台電腦。
   Linux / macOS：執行 `sh install.sh`。
3. 重新啟動 Claude Code / Antigravity。

| 按鍵 | 電腦 |
|---|---|
| `1` | 住家開發機（home）：住家個人電腦 |
| `2` | 公司開發機（dev）：公司個人電腦，可連外網與 GitHub、不能連內網 |
| `3` | 管制機（controlled）：公司電腦，唯一能連內網、外網與安裝受限 |

安裝腳本會把 `global_rules.md`，加上這台電腦的專屬規則 `machine_rules\<電腦代號>.md`（有這個檔案才加），最後加一行 `THIS MACHINE: <電腦代號>`，複製到：

| 工具 | 位置 |
|---|---|
| Claude Code | `使用者資料夾\.claude\CLAUDE.md` |
| Antigravity | `使用者資料夾\.gemini\GEMINI.md` |

原本已有的檔案會先備份成 `CLAUDE.md.日期_時間.bak`，內容相同則略過。

### 各台電腦的專屬規則（machine_rules）

| 檔案 | 安裝到 | 內容 |
|---|---|---|
| `machine_rules\controlled.md` | 只有管制機 | 防毒行為監控的禁止事項（終端機不產生腳本、不用 `-ExecutionPolicy Bypass`、啟動器請使用者雙擊）、PowerShell 5.1 語法、被擋的網域 |

- 住家開發機與公司開發機不會安裝這些限制，所以那兩台的 Claude Code / Antigravity 可以照常在終端機測試。
- 專案裡的 `AGENTS.md` 三台共用，不寫各台電腦的限制。
- 要給某一台加專屬規則時，新增 `machine_rules\home.md` 或 `machine_rules\dev.md` 即可，安裝腳本會自動附加。

### 管制機上的 Antigravity 設定建議

| 設定 | 建議值 | 原因 |
|---|---|---|
| Terminal Command Auto Execution | Always Proceed | 防毒限制已寫進管制機專屬規則，AI 從源頭就不會產生會被攔截的指令，終端機可以自動執行，不必每個指令都確認 |
| Non-Workspace File Access（工作區外的檔案存取） | Always Ask 或 OFF | 避免 AI 讀寫工作區以外的資料夾 |

## 修改規則

1. 編輯倉庫裡的 `global_rules.md`，或只給某一台的 `machine_rules\<電腦代號>.md`（不要直接改安裝後的檔案，下次安裝會被覆蓋）。
2. 重新執行安裝腳本。
3. 提交並推送到 GitHub；公司開發機拉取後再推送到 `.bundle` 給管制機。各台拉取後再執行一次安裝腳本。

## 規則的三個層級

| 層級 | 位置 | 寫什麼 |
|---|---|---|
| 全域 | 本倉庫 `global_rules.md` | 所有電腦、所有專案通用：電腦環境、雙機接力開發、語言、.venv、編碼、機密 |
| 工作區 | 例如 `D:\AI_Workspace` 底下的規則檔 | 公司內部才有的資訊：內網磁碟對應、同步工具位置、專案清單 |
| 專案 | 各專案根目錄 `AGENTS.md` | 該專案特有：目標執行環境、業務規則、不可更動的部分、驗證方式 |

越下層越優先。新專案可直接複製 `templates/` 裡的檔案開始；需要跨對話、跨電腦接力的專案（公司專案一律需要）再加上 `PROGRESS.md`，記錄進度與交接。

### 什麼時候需要工作區層

工作區層**不是必要的**。全域規則已經涵蓋所有專案共用的內容時，「全域 + 專案」兩層就夠了。

| 適合建立工作區規則檔 | 不需要 |
|---|---|
| 好幾個專案共用、但**不能放進全域**的內容：全域規則倉庫會推上 GitHub，公司主機名稱、內網磁碟對應、公司專案清單這類資訊只能放這裡 | 內容全域規則已經有了（例如 GitSync 流程、管制機限制）→ 重複寫只會增加維護負擔，日後還可能兩邊不一致 |
| 只適用某個資料夾底下的專案（例如只在公司專案資料夾內才套用的規範） | 只有一個專案會用到 → 寫在該專案的 `AGENTS.md` |

原則：**能放全域就放全域，只有一個專案用就放專案**；工作區只裝「夾在中間」的內容。

## 各工具自動讀取的規則檔

| | Claude Code | Antigravity |
|---|---|---|
| 全域 | `~/.claude/CLAUDE.md` | `~/.gemini/GEMINI.md` |
| 專案 | `CLAUDE.md`（**不會**自動讀 `AGENTS.md`） | `AGENTS.md`（原生支援）、`GEMINI.md` |
| 子資料夾 | 子資料夾的 `CLAUDE.md`（處理該資料夾的檔案時才讀） | 往上層資料夾搜尋 `AGENTS.md`／`GEMINI.md` |
| 模組化規則 | `.claude/rules/*.md`（可在檔頭指定只套用到哪些檔案）；全域 `~/.claude/rules/` | `.agents/rules/*.md`（或 `.agent/rules/`） |
| 引用其他檔 | 在 `CLAUDE.md` 寫 `@檔案路徑` | — |

- **只維護一份**：專案規則全部寫在 `AGENTS.md`；`CLAUDE.md` 只放一行 `@AGENTS.md` 當轉接頭（Claude Code 認的檔名是 `CLAUDE.md`）。專案內不需要 `GEMINI.md`。
- **只給某個工具的內容**：Claude 專用的寫在 `CLAUDE.md` 的 `@AGENTS.md` 下一行；Antigravity 專用的放 `GEMINI.md`。一般情況不需要。
- **模組化資料夾兩家不通用**：Claude Code 不讀 `.agents/rules/`，Antigravity 不讀 `.claude/rules/`。規則要拆檔又要共用時，放在 `.agents/rules/`，再在 `CLAUDE.md` 逐一引用：
  ```
  @AGENTS.md
  @.agents/rules/gui.md
  ```
  規則不多時維持單一 `AGENTS.md` 即可。

### 什麼時候適合模組化規則

模組化規則是把規則拆成很多小檔，每個小檔在檔頭設定「什麼時候才套用」：

| 觸發方式（Antigravity 寫法） | 意思 |
|---|---|
| `always_on` | 永遠套用，效果和寫在 `AGENTS.md` 完全一樣 |
| 指定檔案範圍（例如 `*.bat`） | 只有處理符合的檔案時才載入 |
| 由 AI 判斷 | AI 依小檔的說明自行決定要不要讀 |
| 手動 | 使用者在對話中指名時才套用 |

好處是 AI 不用每次載入全部規則，比較省額度、也比較不會被無關規則干擾。

| 適合拆成模組化 | 維持單一 `AGENTS.md` |
|---|---|
| 規則很多（例如幾百行），而且明顯分成互不相干的幾類：前端、後端、部署腳本各有一大套規範 | 規則不多，一份檔案就讀得完（個人專案、一般公司小工具幾乎都屬於這種） |
| 某些規則只跟特定檔案有關，例如只在改 `.bat` 時才需要的編碼規範 | 只拆出一個檔、又設成 `always_on` → 沒有任何好處，反而要維護兩份 |

原則：**預設只用 `AGENTS.md`**，等到 `AGENTS.md` 長到難以維護、而且內容能依檔案類型切開時再拆。拆的時候照上一節的方式放在 `.agents/rules/`，並在 `CLAUDE.md` 逐一引用，讓兩個工具都讀得到。

> 以上依 2026-10 時兩邊工具的說明整理，細節（例如 `.claude/rules/` 指定檔案範圍的寫法）以官方文件為準。

> 本倉庫目前是 GitHub 私人倉庫，但仍不要寫入公司內部主機名稱、內網路徑、員工編號等資訊：全域規則會安裝到每台電腦，倉庫日後也可能公開。這類資訊請寫在工作區或專案的規則檔。
> claude.ai 網頁版的 Instructions 是另外設定的，不會讀這個檔案。
