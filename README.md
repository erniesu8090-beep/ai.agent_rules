# ai.agent_rules

我的 AI 寫程式工具（Claude Code、Antigravity）共用的**全域規則檔**，放在 GitHub 上方便每台電腦下載安裝。

## 檔案說明

| 檔案 | 用途 |
|---|---|
| `global_rules.md` | 全域規則本體（要改規則就改這個檔） |
| `AGENTS.md`、`CLAUDE.md` | 維護本倉庫時給 AI 看的專案規則 |
| `install.bat` | Windows 安裝：雙擊執行 |
| `install.sh` | Linux / macOS 安裝 |
| `templates/` | 新專案範本：`AGENTS.md`、`CLAUDE.md`、`.gitignore` |

## 安裝

三台有 AI 工具的電腦都要安裝：家用機、開發機、管制機。

1. 取得這個倉庫，放在 `D:\AI_Workspace\ai.agent_rules`：
   - 家用機、開發機：`git clone`。
   - 管制機（連不到 GitHub）：用 GitSync 同步。先在家用機或開發機用 GitSync「管理專案 / .venv」→「可加入的資料夾」把本倉庫加入清單並推送到 `.bundle`；再到管制機下載 `.bundle`，用「從 .bundle 建立」取得本倉庫。
2. Windows：雙擊 `install.bat`，依提示按 `1`、`2` 或 `3` 選擇這台是哪一台電腦。
   Linux / macOS：執行 `sh install.sh`。
3. 重新啟動 Claude Code / Antigravity。

| 按鍵 | 電腦 |
|---|---|
| `1` | 家用機（home） |
| `2` | 開發機（dev）：公司個人電腦，可連外網、不能連內網 |
| `3` | 管制機（controlled）：公司電腦，連內網、安裝受限 |

安裝腳本會把 `global_rules.md` 加上一行 `THIS MACHINE: <電腦代號>`，複製到：

| 工具 | 位置 |
|---|---|
| Claude Code | `使用者資料夾\.claude\CLAUDE.md` |
| Antigravity | `使用者資料夾\.gemini\GEMINI.md` |

原本已有的檔案會先備份成 `CLAUDE.md.日期_時間.bak`，內容相同則略過。

## 修改規則

1. 編輯倉庫裡的 `global_rules.md`（不要直接改安裝後的檔案，下次安裝會被覆蓋）。
2. 重新執行安裝腳本。
3. 用 GitSync 提交，推送到 `.bundle` 與 GitHub；其他電腦拉取後再執行一次安裝腳本。

## 規則的三個層級

| 層級 | 位置 | 寫什麼 |
|---|---|---|
| 全域 | 本倉庫 `global_rules.md` | 所有電腦、所有專案通用：電腦環境、雙機接力開發、語言、.venv、編碼、機密 |
| 工作區 | 例如 `D:\AI_Workspace` 底下的規則檔 | 公司內部才有的資訊：內網磁碟對應、同步工具位置、專案清單 |
| 專案 | 各專案根目錄 `AGENTS.md` | 該專案特有：目標執行環境、業務規則、不可更動的部分、驗證方式 |

越下層越優先。新專案可直接複製 `templates/` 裡的三個檔案開始。

> 這是公開倉庫：公司內部主機名稱、內網路徑、員工編號等資訊請寫在工作區或專案的規則檔，不要寫進這裡。
> claude.ai 網頁版的 Instructions 是另外設定的，不會讀這個檔案。
