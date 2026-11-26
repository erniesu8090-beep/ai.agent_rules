# 雲端沙盒專屬規則（只安裝在雲端沙盒／遠端代理環境）

> 本段由安裝腳本附加在全域規則之後，專用於遠端 Linux 容器與沙盒 VM。實體機（home／dev／controlled）不受本段限制。
> 規則本體在 ai.agent_rules 倉庫的 `machine_rules/sandbox.md`。

## A. 權限與套件安裝（User Space）
- **非 Root 帳號**：執行身分為非特權帳號，嚴禁嘗試探測或執行 `sudo`、`su`、`apt` 或修改系統底層 `/etc`。
- **套件安裝**：一律安裝於使用者空間（User Space）。Python 限用專案獨立虛擬環境（`uv` 或 `python3 -m venv .venv`），Node.js 限用專案 `node_modules`，禁止全域污染。

## B. 網路、代理與外掛認證
- **Proxy 代理**：對外連線受本機代理（`HTTP_PROXY` / `HTTPS_PROXY`）控管，禁止 unset、繞過或探測代理端點。
- **認證機制**：Git / GitHub 操作一律依賴環境已預先認證的外掛或 CLI（如 `gh`、GitHub plugin），不得擅自覆寫全域帳密與 token。

## C. 網頁預覽與伺服器（No Localhost）
- **無 Localhost 直連**：雲端虛擬機與使用者電腦網路隔離，使用者瀏覽器無法開啟 `localhost`，嚴禁指示使用者連線 `localhost`。
- **預覽優先走 Artifact**：靜態網頁、儀表板與互動 UI 優先生成獨立 HTML Artifact（依循內建 `generative_ui` 技能或獨立 HTML 規範）供介面內直接檢視；Web 伺服器必須以守護程序/背景模式（`IsDaemon: true`）啟動。

## D. 生命週期、子代理與防死鎖
- **即時落盤**：虛擬機具臨時性（Ephemeral），每階段完成必須即時更新 `PROGRESS.md` 並 commit，避免對話重置遺失進度。
- **子代理限制**：子代理僅限 `inherit` 工作區模式（不支援 branch/share）；大範圍閱讀與搜尋派唯讀子代理。
- **無輪詢喚醒**：沙盒具備事件喚醒機制，終端嚴禁使用 `while sleep` 進行死迴圈輪詢；非互動指令避免卡在 stdin。
