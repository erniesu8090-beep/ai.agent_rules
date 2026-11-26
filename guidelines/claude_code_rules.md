# Claude Code 進階規則與防凍結指引（`guidelines/claude_code_rules.md`）

> 本檔收納 Claude Code 專屬的 `CLAUDE.md` 並存細節、資安防凍結處置與新版設定評估備忘；核心跨工具原則保留於 `global_rules.md`，詳細技術機制與實測紀錄見 `docs/claude_code_permissions_deny.md`。

## 1. 互動提問與安裝位置

- 互動式選擇題工具：Claude Code 使用 `AskUserQuestion`。
- 全域規則安裝位置：`~/.claude/CLAUDE.md`（由 `install.bat`／`install.sh` 自動寫入）。
- Git 共同作者署名：`Co-authored-by: Claude <noreply@anthropic.com>`（見 `global_rules.md` 第 10 節）。

## 2. `CLAUDE.md` 與 `AGENTS.md` 並存規範

- 安裝腳本在非管制機（`home`、`dev`、`general`、`sandbox`）會將 `~/.claude/settings.json` 設定為 `CLAUDE.md` 與 `AGENTS.md` 同時載入（`instructionFiles: "claude-md-and-agents-md"`，同時寫入 `agents-md@builtin` 與 `cc-plugin-agents-md@builtin` 兩種外掛 ID）。
- 沒有此設定時，路徑上只要存在 `CLAUDE.md`、`.claude/CLAUDE.md` 或 `CLAUDE.local.md`，Claude Code 會跳過所有 `AGENTS.md`。
- 自有專案與工作區只維護 `AGENTS.md`，不建立上述三種檔案、不使用 `/init`；fork 別人的專案保留原 `CLAUDE.md`，自己的規則寫在 `AGENTS.md`（需摘要先問）。
- **確認方法**：開新對話時自行比對，若資料夾有 `AGENTS.md` 但未載入，開頭就告知使用者並檢查 `~/.claude/settings.json`（使用者也可執行 `/memory` 人工確認，需 v2.1.280+）。

## 3. 資安防凍結規則（`permissions.deny` 與 `safeguards` 處置）

- **開新專案詢問**：建立新專案 `SPEC.md` 時，以選擇題卡片詢問使用者「是否套用 Claude Code 資安防凍結規則（設 `permissions.deny` 改由他家處理）？」。
- **工具安全分流**：敏感專案（如 OAuth 憑證中繼、網路代理、隧道、逆向等）一律交由 Claude Code 以外的 coding agent（如 Antigravity）處理。
- **受限路徑保護**：不讀取、開啟、搜尋或列出 `settings.json` 的 `permissions.deny` 所列受限路徑（例如 `Read(./**/google.cloud_oauth.relay/**)`），不使用 Bash（`cat`、`type`、Python 等）繞過讀取，也不對含資安內容的資料夾執行 `/security-review`；需要受限資料夾的名稱或內容時，先詢問使用者。
- **觸發 `safeguards` 錯誤時的處置**：
  - 若對話出現 `safeguards flagged this message` 或 `cyber-related safeguards` 錯誤，立即停止重試。
  - 告知使用者按 `Esc` 兩次或輸入 `/rewind` 退回觸發前的檢查點，再換做法（亦可透過 `/feedback` 回報誤判，或申請 Cyber Verification Program）。
  - 不可讀取疑似引發問題的檔案來追查原因。

## 4. 新版設定評估備忘（2026-11-22 追蹤）

- **工作區外防讀／防寫與 Windows `permissions.deny`（v2.1.314+／v2.1.327）**：Windows `permissions.deny` 可優先實測 `Read(C:/...)`／`Read(//c/...)` 路徑寫法，並評估同時啟用 `permissions.blockReadsOutsideWorkingDirectories`（v2.1.327 擴充在 bypass/auto 模式下對 Bash 指令之詢問或拒絕）與 `permissions.blockWritesOutsideWorkingDirectories`；無人值守排程可評估 `permissions.denyInsteadOfPrompting`。
- **Code Mode `PreToolUse` Hook 阻擋語法（v2.1.328～v2.1.329）**：在 Code Mode 下非致命 `PreToolUse` hook 錯誤預設**不再阻擋**工具執行；未來若設定阻擋性 hook（涵蓋 command、HTTP 與 `mcp_tool`），須明確加入 `"onFailure": "block"`。
- **沙盒與排程權限收緊（v2.1.325+）**：沙盒內 Bash 指令預設改走權限詢問（若需維持免詢問須設 `sandbox.autoAllowBashIfSandboxed: true`）；排程與 `/loop` 執行含 `allowed-tools` 或 `hooks` 的 Skill 前預設詢問（須在 `permissions.allow` 加入 `Skill(名稱)`）。
- **沙盒內巢狀 Skill 載入邊界（v2.1.319+）**：開啟 Bash 沙盒時，子目錄 `.claude/skills` 須在該子目錄啟動或 `/cd` 進入後才會載入，且附加目錄內的 `.claude` 設定／Skills／Hooks 禁止寫入。
