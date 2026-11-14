# 個人跨機環境與工作流規則（home / dev / controlled）

> 由安裝腳本於 `home`、`dev`、`controlled` 附加（`general` 不載入），定義多機分工與同步；本體在 `ai.agent_rules/machine_rules/personal.md`。

## 1. 個人電腦環境與分工
| 代號 | 電腦 | AI 工具 | 軟體 | 網路 | 用途 |
|---|---|---|---|---|---|
| 住家開發機（home） | 住家（Win／Ubuntu） | 四家皆有 | 不限 | 外網、GitHub；無內網 | 個人／公司專案開發（經 GitHub 與 dev 同步） |
| 公司開發機（dev） | 公司個人機 Win11 | 四家皆有 | 不限 | 外網、GitHub；無內網 | 公司專案開發；GitHub 與管制機中繼 |
| 管制機（controlled） | 公司機 Win10 22H2 | Antigravity、OpenCode | **受限**：無管理員、防毒攔截 | **唯一連內網**（伺服器、NAS）；外網受限（見 `controlled.md`） | 接力、內網驗證、發布 |
| 同事電腦 | 公司同事機 | 無 | 受限，常無 Python | 公司內網 | 只跑發布成品 |

- `home` 與 `dev` 合稱「開發機」（無內網），不受管制機限制，但寫給管制機或同事機的程式須相容。管制機連線表在 `machine_rules/controlled.md`（僅裝管制機，開發機無此檔勿找）；管制機用未確認外網服務先請使用者實測。

## 2. 跨電腦同步與個人環境補充
- **跨機同步 GitSync**：只傳已 commit 的 `main`；Win 版 `D:\AI_Workspace\bundle.gitsync`（`GitSync_GUI.vbs`）、Ubuntu 版 `~/AI_Workspace/gitsync_ubuntu`（`./GitSync.sh`，只走 GitHub）；版控優先指示 GitSync 按鈕（停損不勾改壞檔），手動 git 備用；見 GitSync `README.md`。
- **工作區結構**：專案放 `D:\AI_Workspace`（Ubuntu `~/AI_Workspace`）下兩層內，各機相對位置才一致；不同資料夾專案禁同名（`.bundle` 以資料夾命名）。公司專案上一層即「公司工作區」。
- **Python 3.11 補充**：個人專案以金融交易與遊戲輔助為主（現有 Python 3）；公司專案固定 3.11 系列，`requirements.txt` 全鎖版，Ubuntu 用 `uv venv --python 3.11 --seed .venv` 建（不動系統 Python）。3.11 安全更新至 2027-10（PEP 664），升級前不換版、不用無 GIL 版（`3.13t`／`3.14t`）；過 2027-01 未升提醒（見 README「Python 升級評估」）。
- **敏感專案阻擋**：`google.cloud_oauth.relay` 已入 `~/.claude/settings.json` 的 `permissions.deny` 與 `~/.config/opencode/opencode.jsonc`，嚴禁 Claude Code 讀取或繞過。
