# 個人跨機環境與工作流規則（home / dev / controlled）

> 本段由安裝腳本在 `home`、`dev`、`controlled` 模式自動附加（`general` 通用模式不載入），定義個人多機分工與同步流程。
> 規則本體在 ai.agent_rules 倉庫的 `machine_rules/personal.md`。

## 1. 個人電腦環境與分工

| 代號 | 電腦 | AI 工具 | 安裝軟體 | 網路 | 用途 |
|---|---|---|---|---|---|
| 住家開發機（home） | 住家個人電腦（Windows 或 Ubuntu） | Claude Code、Antigravity、Codex、OpenCode | 不限 | 外網、GitHub；不能連公司內網 | 個人專案；公司專案開發（經 GitHub 與公司開發機同步） |
| 公司開發機（dev） | 公司個人電腦，Win11 | Claude Code、Antigravity、Codex、OpenCode | 不限 | 外網、GitHub；不能連公司內網 | 公司專案開發；GitHub 與管制機之間的中繼 |
| 管制機（controlled） | 公司電腦，Win10 22H2 | Antigravity、OpenCode | **受限**：無管理員權限、有防毒攔截 | **唯一能連公司內網**（伺服器、NAS）；外網受限（見 `machine_rules/controlled.md`） | 公司專案接力開發、內網功能驗證、發布 |
| 同事電腦 | 公司同事使用 | 無 | 受限，通常無 Python | 公司內網 | 只執行發布出去的成品 |

- 住家與公司開發機合稱「開發機」（皆連不到公司內網）；開發機上的 AI 不受管制機專屬規則限制，但寫給管制機或同事電腦執行的程式仍要相容。
- 管制機的可連／不可連清單在 `machine_rules/controlled.md`（該檔只裝在管制機，開發機上找不到是正常的，不要去找）；管制機要用到未確認的外部網站或服務時，先請使用者在管制機實測能不能連。

## 2. 跨電腦同步與個人環境補充

- **跨機同步流程**（每段只傳已 commit 的 `main` 分支）：住家開發機 ↔ GitHub（私人倉庫）↔ 公司開發機 ↔ Google 雲端硬碟上的 `.bundle` ↔ 管制機（連不到 GitHub）↔ 內網伺服器。交接前先 commit 並推送；開始修改前先拉取，避免兩邊歷史分岔。
- **工具 GitSync**：Windows 版 `D:\AI_Workspace\bundle.gitsync`（`GitSync_GUI.vbs`，內含 PortableGit）；Ubuntu 版 `~/AI_Workspace/gitsync_ubuntu`（`./GitSync.sh`，只走 GitHub）。請使用者操作版控時優先指示 GitSync 的按鈕（停損時提醒用 GitSync 提交先不要勾選改壞的檔案），手動 git 指令只當備案；動到 GitSync 本身前先讀該版的 `README.md`，修改後同步更新。
- **工作區結構**：專案放在 `D:\AI_Workspace`（Ubuntu 是 `~/AI_Workspace`）底下兩層內，各台電腦相對位置才會一致；不同資料夾的專案不可同名（`.bundle` 以資料夾名稱命名）。公司專案的上一層資料夾就是「公司工作區」。
- **Python 3.11 補充**：個人專案以金融交易與遊戲輔助工具為主（用現有 Python 3）；公司專案在每台電腦固定用 Python 3.11 系列，`requirements.txt` 全部鎖定版本，Ubuntu 開發機用 `uv venv --python 3.11 --seed .venv` 建立（不動系統 Python）。Python 3.11 安全更新到 2027-10 結束（PEP 664），升級前不改用其他版本、不用無 GIL 版（`3.13t`／`3.14t`）；若已過 2027-01 且還沒升級，提醒使用者（見 README「Python 升級評估」）。
- **個人敏感專案阻擋**：`google.cloud_oauth.relay` 已由安裝腳本寫入 `~/.claude/settings.json` 的 `permissions.deny` 與 `~/.config/opencode/opencode.jsonc`，嚴禁 Claude Code 讀取或繞過。
