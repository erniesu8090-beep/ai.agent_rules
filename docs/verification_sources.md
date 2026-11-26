# 查證狀態與來源總表

> 用途：集中管理「哪些說法有官方依據、哪些只是推測、哪些查不到」，方便每月重新查證，也避免同一件事在不同文件寫成不同版本。
> 說明：本表**沿用原文件在 2026-10-19～2026-10-28 的查證結果**，2026-10-29 整併，2026-10-31～11-26 陸續增補與官網直開複查。狀態改變時，同步更新來源文件與本表。
> 圖例：**官方**＝官方文件或官方部落格；**二手**＝第三方轉述；**實測**＝本機實際測試；**推測**＝合理判斷但無來源；**查不到**＝找不到資料，不得補成事實。

| 標示 | 意思 | 能不能直接相信 |
|---|---|---|
| 官方 | 官方文件或官方部落格 | 可以，但注意版本與日期 |
| 二手 | 第三方轉述，未對上官方原文 | 當線索，重要決策前再查 |
| 實測 | 本機實際測試 | 只代表該版本、該環境 |
| 推測 | 合理判斷，沒有來源 | 不要當結論；需要實測 |
| 查不到 | 找不到資料 | 誠實留白，不要補成事實 |

---

## 一、Claude Code

| 主題 | 結論 | 狀態 | 來源 | 查證日 |
|---|---|---|---|---|
| 讀 `AGENTS.md` | v2.1.277 起原生讀取；路徑上有 `CLAUDE.md` 時全部跳過且不提示 | 官方 | https://code.claude.com/docs/en/memory | 2026-10-28 |
| 兩者都讀設定 | `instructionFiles: "claude-md-and-agents-md"`；v2.1.285 前外掛 ID 為 `agents-md@builtin`，之後亦支援 `cc-plugin-agents-md@builtin` | 官方 | 同上 | 2026-10-28 |
| `/memory` 列出 `AGENTS.md` | 需 v2.1.280+ | 官方 | 同上 | 2026-10-28 |
| `/doctor prompt-audit` | v2.1.283+（別名 `/checkup prompt-audit`，透過內建 `/claude-api` 技能運作）；掃描專案與全域 `CLAUDE.md`、`AGENTS.md`、`rules`、`skills`、`commands`、`subagents`、`output-styles`，找舊模型過時高壓寫法（如 `CRITICAL`）、失效路徑與矛盾規則，先出報告與 Diff 經確認才套用 | 官方 | https://code.claude.com/docs/en/memory 、https://code.claude.com/docs/en/commands | 2026-11-14 |
| 隨需載入規則字元上限 | v2.1.309 起，200K 視窗為 40,000 字元、1M 視窗為 150K～200K 字元，超過只取開頭 | 官方 | 同上（2026-11-22 複查） | 2026-11-22 |
| 自動記憶範圍 | 只存使用者資訊、被糾正的回饋、專案背景、外部參照；除錯修法通常不存；只存本機 | 官方 | 同上 | 2026-10-28 |
| `permissions.deny` 路徑 | 相對路徑以啟動資料夾為起點；文件記載支援 `Read(C:/...)`、`Read(//c/...)` 與 `permissions.blockReadsOutsideWorkingDirectories`（v2.1.327 強化），跨資料夾仍待實測且存繞過風險；只涵蓋內建檔案工具 | 官方 | https://code.claude.com/docs/en/large-codebases 、https://code.claude.com/docs/en/permissions 、https://horadecodar.com.br/impedir-claude-code-editar-arquivos/（二手） | 2026-11-22 |
| 被 deny 的檔案會從 Claude 的檔案列表中隱藏 | deny 的檔案在列表中不顯示 | 二手 | https://www.petefreitag.com/blog/claude-code-permissions/ | 2026-10-25 |
| `deny` 對 Bash 的效力 | `cat` 可能被擋，Python 一行指令仍可能讀到 | 二手 | https://www.developersdigest.tech/blog/keep-secrets-away-from-ai-coding-agents-2026 | 2026-10-25 |
| `.claudeignore` | 2026-10-22 實測無法阻止讀取或觸發審查 | 實測 | 本倉庫 `PROGRESS.md` 第五節 | 2026-10-22 |
| `/sandbox` 平台 | 只支援 macOS（Seatbelt）與 Linux／WSL2（bubblewrap + socat）；原生 Windows 不支援 | 官方 | https://code.claude.com/docs/en/security | 2026-10-25 |
| `AskUserQuestion` 工具與版本 | 官方確認為澄清問題工具（1-4題、2-4選項）；v2.0.21 起 | 官方（工具）／二手（v2.0.21 版本號） | https://code.claude.com/docs/en/agent-sdk/approvals ；claudelog.com、atcyrus.com（二手） | 2026-10-31 |
| Plugins 插件體系 | 完整套件體系，打包 tools、skills、agents、hooks、MCP；支援 marketplace.json（本機/URL/GitHub）與 claude plugin／/plugin 指令 | 官方 | https://code.claude.com/docs/en/plugins | 2026-11-02 |
| 子代理模型支援 | `.claude/agents/*.md` 支援 `haiku`、`sonnet`、`opus`、`inherit`；鎖定自家 Claude 系列，不支援原生跨廠牌模型 | 官方 | https://code.claude.com/docs/en/sub-agents | 2026-11-03 |
| v2.1.314～v2.1.325 權限、沙盒與排程變更 | 新增 `permissions.blockWritesOutsideWorkingDirectories`、`permissions.denyInsteadOfPrompting`、`CLAUDE_CODE_SUBAGENT_EFFORT`；沙盒 Bash 預設改走權限詢問（須設 `sandbox.autoAllowBashIfSandboxed: true`）、排程／`/loop` 跑含 `allowed-tools`／`hooks` Skill 預設先詢問、開啟沙盒時子目錄 `.claude/skills` 須 `/cd` 才載入；新增實驗性 Code Mode 與未識別模型預設 1M 視窗 | 官方 | https://code.claude.com/docs/en/changelog | 2026-11-15 |
| v2.1.326～v2.1.330 Code Mode、Hooks 與排程變更 | `v2.1.326`：Agent Teams 可併用 Code Mode、檢查 `--allowedTools`／`--disallowedTools`／`--tools` 不完整規則並警告；`v2.1.327`：強化 `permissions.blockReadsOutsideWorkingDirectories` 對 Bash 指令之詢問／拒絕；`v2.1.328～329`：Code Mode 下非致命 `PreToolUse` hook 錯誤預設不阻擋（須於 command/HTTP/`mcp_tool` hook 明定 `"onFailure": "block"`）、拒絕讀取逾 256 MiB 行範圍、信任對話框標示 hooks 聲明路徑、`/tasks` 顯示排程／`/loop`／goal／對話 forks、`/mcp` 顯示遠端拒絕 `Server message`、`CLAUDE_CODE_MAX_OUTPUT_TOKENS` 提示；`v2.1.330`：Enterprise Admin Console `claude auth login`、macOS/Linux `easel` 圖表模式、`CLAUDE_CODE_FULL_SIGN_IN_LINK=1`、排程與 `/loop` 最長延至 30 天、恢復 `max_tokens` 超限自動重試 | 官方（2026-11-22 瀏覽器直開核實） | https://code.claude.com/docs/en/changelog | 2026-11-22 |

---

## 二、Antigravity

| 主題 | 結論 | 狀態 | 來源 | 查證日 |
|---|---|---|---|---|
| 規則檔位置 | 全域 `~/.gemini/AGENTS.md`、`GEMINI.md`、`~/.gemini/config/*`、`~/.gemini/config/rules/*.md`；CLI 另讀 `~/.gemini/antigravity-cli/rules/*.md` | 官方 | https://antigravity.google/docs/rules/ | 2026-10-28 |
| 往上找規則範圍 | 只到工作區根目錄（workspace root），不會超過 | 官方 | 同上 | 2026-10-28 |
| 開啟 Git 倉庫的範圍 | 只到該倉庫根目錄 | 實測 | 2026-10-10 本機 | 2026-10-10 |
| 容量限制 | 單檔展開 `@[label](path)` 後上限 24,000 bytes（超過依行邊界截斷）；全域與 `always_on` 規則共享 20,000 tokens 預算（`defaultRulesBudget`），超標時最大檔案降級為路徑指標 | 官方 | 同上與本機內建 `agy-customizations/docs/rules.md` | 2026-11-14 |
| 模組化規則與無聲丟棄 | 獨立 `AGENTS.md`／`GEMINI.md` 不支援 frontmatter；`rules/*.md` 必填 `trigger`（`always_on`／`model_decision`／`glob`／`manual`），誤寫駝峰（`alwaysOn`）、漏填條件欄位、`glob` 萬用字元開頭未加引號或子資料夾未註冊於 `rules.json` 皆會被無聲丟棄／忽略 | 官方 | 同上與本機內建 `agy-customizations/docs/json_configs.md` | 2026-11-14 |
| `/plan`、`/grill-me`、`/learn` | 規劃、一次一題訪談、`/learn` 具備 `Schema check` 與 `Prefers updates over new files` 並先產出 `learning_proposal.md` 經核准後寫入 | 官方 | https://antigravity.google/docs/slash-commands/ 、https://antigravity.google/docs/commands/learn/ | 2026-11-14 |
| 提示詞健檢（Prompt Audit）對應機制 | 無內建 `/doctor` 指令（GitHub 上 `doctor` 屬第三方 `rmyndharis/antigravity-skills` 外部腳本）；官方以 `/agy-customizations`（載入自訂指南除錯修復）＋ `/learn` ＋ CLI `/context` 與 `/skills reload` 組合對應；自建全域技能為 `/prompt-audit` | 官方 | https://antigravity.google/docs/commands/agy-customizations/ 、https://antigravity.google/docs/cli/reference/ | 2026-11-22 |
| 舊 Workflows 與新版 Dynamic Workflows | 舊 Workflows 2026-10-19 起停止運作，用 `/migrate-workflows` 轉 Skills；**v2.32.0 正式推出 Dynamic Workflows**（以內建 Python runtime 編排平行子代理） | 官方 | https://antigravity.google/docs/migration/workflows-to-skills/ 、https://antigravity.google/docs/changelog/ | 2026-11-15 |
| `Stop` Hook 防漏圖卡機制 | 全域 `~/.gemini/config/hooks.json` 支援 `Stop` 事件（`NO_TOOL_CALL` 觸發，含 `continuationActive` 防迴圈、`transcriptPath`），回傳 `{"decision": "continue", "reason": "..."}` 可拉回模型補發 `ask_question` | 官方／實測 | 本機內建 `agy-customizations/docs/hooks.md` 與 `tests/test_ag_stop_card_guard.py` | 2026-11-25 |
| `ask_question` 支援複選與自由填寫 | 是；`is_multi_select` | 官方 | https://dev.to/googleai/elevating-antigravity-agent-skills-part-1-interactive-ui-workflows-6l2 | 2026-10-25 |
| `ask_question` 選項格式 | `options` 為單一字串陣列，沒有獨立 `description` | 實測 | 本機 session JSON Schema | 2026-10-25 |
| 是否有背景自動記憶 | 無；只有手動 `/learn` | 官方 | Antigravity customizations 文件 | 2026-10-25 |
| Gemini 3.8 Flash 上線日 | 2026-09-01 | 官方 | https://antigravity.google/blog/gemini-3-8-flash-in-google-antigravity/ | 2026-10-25 |
| 模型正式名稱 gemini-3.8-flash／gemini-4-argon | 官方模型標籤與正式名稱 | 官方 | https://ai.google.dev/gemini-api/docs/antigravity-agent | 2026-10-25 |
| 規劃時不會主動跳提問卡片（需規則或 /plan /grill-me 觸發） | 規劃時預設不跳卡片，需靠指令或規則明確點名觸發 | 實測（使用者觀察） | 本機 | 2026-10-30 |
| Gemini 4 Argon 可用方案 | 需 Google AI Pro 以上 | 官方 | https://antigravity.google/docs/models/ | 2026-10-25 |
| Gemini CLI 停止服務 | 2026-06-18 起對 AI Pro、AI Ultra、免費個人帳號停止；企業與付費 API Key 例外 | 官方 | https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/ | 2026-10-25 |
| `agy -p` 呼叫 `image-generator` 子代理跨工具生圖 | 單純呼叫 `image-generator` 不執行 shell，圖片自動存入 `~/.gemini/antigravity-cli/brain/<對話ID>/`，免終端機權限確認 | 實測 | 2026-10-25 本機實測 `agy` v1.4.7 | 2026-10-25 |
| Plugins 插件體系 (v2.28.2) | v2.28.2 (2026-10-29) 正式推出 Marketplace 與 Partner 插件（Figma、Linear、Google Drive 等）；plugin.json 打包 skills/agents/rules/MCP/hooks；圖形化 Accounts Tab 管理 OAuth 憑證；指令 /plugin | 官方 | https://antigravity.google/docs/plugins/ 與 https://antigravity.google/changelog | 2026-11-02 |
| 子代理模型支援 | `invoke_subagent` 與自訂 agent 採模型等級抽象（`inherit`、`flash_lite`、`flash`、`pro`）；無原生跨廠牌自選型號 | 官方／實測 | Antigravity subagent schema 與本機實測 | 2026-11-03 |
| Remote VM 對話生命週期 | 每個對話獨立配發 VM（`provisioned for this conversation`），非多對話共享 | 官方／實測 | 官方環境規格與本機實測 | 2026-11-06 |
| 專案對話 vs Outside of Project 權限隔離 | 專案對話自動 clone 並注入 Scoped Token；專案外對話（Outside of Project）為空白 VM，無私人 Repo 權限，手動 clone 報 403（GraphQL: Resource not accessible by integration / 403） | 實測 | 2026-11-06 實測截圖與報錯 | 2026-11-06 |
| 持久層與符號連結 | `~/.gemini` 軟連結至 `/shared/user/.gemini`，跨對話持久保存；其餘路徑為臨時性沙盒（Ephemeral） | 官方／實測 | 官方環境規格與 `ls -la ~` 實測 | 2026-11-06 |
| 專案路徑結構 | 自動 clone 於 `/home/antigravity/<GitHub擁有者>/<專案名稱>` | 實測 | 2026-11-06 VM 環境實測 | 2026-11-06 |
| Localhost 隔離與預覽 | 使用者本機瀏覽器無法連線 VM 的 localhost，需產出單一 HTML Artifact 供 UI 預覽 | 官方／實測 | 官方環境規格與實測 | 2026-11-06 |
| v2.29～v2.34.0 模型、`/swarm`、Orchestrator 與 MCP Apps 更新 | 新增 `Gemini 4 Carbon`／`Hydrogen`／`Neon`（2026-11-18 起 Pro/Ultra/Enterprise 預設模型）與 `Orchestrator (Neon)`（`Gemini 4 Neon` 規劃＋`Gemini 4 Hydrogen` 實作）；v2.29 推 Voice Mode、Remote Agents、修復 worktree 未保留 uncommitted 變更與可摺疊提問卡片；v2.30 支援一鍵匯入外掛且單對話權限獨立；v2.31 推出 `/swarm`；v2.33 支援 SSH 遠端 Linux、GitHub PR 狀態卡與內建瀏覽器 `Cmd/Ctrl+F`；**v2.34.0（2026-11-20）**正式支援 `MCP Apps`、`Gemini 4 Neon` 與 `Orchestrator (Neon)`，並於 v2.33.0～v2.34.0 修正單選題卡上移清除自訂回答及方向鍵選取停用選項（官網未見「可自訂 Orchestrator 模式」或「write-in previews」條目） | 官方（2026-11-22 瀏覽器直開核實） | https://antigravity.google/docs/changelog/ 、https://antigravity.google/blog/gemini-4-carbon-in-google-antigravity/ | 2026-11-22 |
| `Orchestrator (Neon)` 雙模型自動接力機制 | 維持單一對話脈絡與共用記憶，背後切換 `Orchestrator Model`（如 `Gemini 4 Neon High`，負責看碼、規劃、檢視進度與卡住時接手修正）與 `Executor Model`（如 `Gemini 4 Hydrogen Medium`，負責搜尋、改碼、建置、跑測試）；不開平行分身、無隔離記憶 | 官方 | https://antigravity.google/docs/models/ 、https://antigravity.google/docs/changelog/ | 2026-11-26 |
| EGM 外掛（Elephant-Goldfish Model v0.1.1） | 開源多角色設計與審查外掛；含 7 個技能（`egm-brainstorm`／`draft`／`review`／`resolve`／`review-loop`／`bootstrap`／`drift-report`）與 10 個專屬子代理角色；Elephant 主對話保有上下文，Goldfish 以無歷史對話之隔離子代理審查文件與原始碼，底層依賴可建立隔離子代理之執行環境 | 官方／實測 | https://egm.dev 、https://github.com/google/elephant-goldfish-model 與外掛目錄（`~/.gemini/config/plugins/egm/`） | 2026-11-26 |

---

## 三、Codex 與 OpenCode V2

| 主題 | 結論 | 狀態 | 來源 | 查證日 |
|---|---|---|---|---|
| Codex 規則檔與容量限制 | 全域 `~/.codex/AGENTS.md`；專案從 Git／專案根目錄往下合併 `AGENTS.md`（預設不讀 `CLAUDE.md`）；預設合計上限 32 KiB | 官方 | https://developers.openai.com/codex/guides/agents-md/ | 2026-10-24 |
| Codex 提問工具 `request_user_input` | 預設於 Plan mode 啟用；一般模式需在 `config.toml` 設 `[features] default_mode_request_user_input = true` | 實測／官方 | 本機 `codex features list` 與 GitHub `openai/codex` | 2026-10-25 |
| Codex `$imagegen` 跨工具呼叫 | 透過 `codex exec` 可走本機 ChatGPT 登入額度呼叫內建 `image_gen` 產圖 | 實測 | 本機 `codex-imagegen-bridge` 技能實測 | 2026-10-24 |
| Codex 免費方案不提供內建生圖（`image_gen`） | 免費 ChatGPT 帳號在 Codex CLI（0.167.0／0.171.0、`gpt-6-luna`／`gpt-5.6-terra`）工作階段皆不掛載 `image_gen` 工具，僅 Plus／Pro 付費方案支援 | 實測／官方方案說明 | 2026-11-24 本機 `codex exec` 實測與 OpenAI 方案說明 | 2026-11-24 |
| Codex 子代理模型支援 | `.codex/agents/*.toml` 支援自家 GPT/Codex 型號或 `inherit`；不支援原生跨廠牌模型 | 官方 | https://developers.openai.com/codex/config-reference/ | 2026-11-03 |
| OpenCode V2 規則檔格式 | 只讀 `AGENTS.md`，不讀 `CLAUDE.md`；無 fallback | 官方 | https://opencode.ai/v2/docs/instructions/ | 2026-10-28 |
| OpenCode V2 往上找規則範圍 | 找到家目錄；工作區在家目錄以外時只到專案根目錄 | 官方 | 同上 | 2026-10-28 |
| OpenCode V2 工作區規則 | 要用 `opencode.jsonc` 的 `instructions` 指定 | 官方 | https://opencode.ai/v2/docs/config/ | 2026-10-28 |
| OpenCode V2 權限 | `permissions` 的 `*` 會跨 `/`；可管 `external_directory` | 官方 | https://opencode.ai/v2/docs/permissions/ | 2026-10-28 |
| OpenCode V2 Hooks | 無宣告式 hooks，用 Plugin | 官方 | https://opencode.ai/v2/docs/plugins/ | 2026-10-28 |
| OpenCode V2 提問工具 | `question`，選項有 `label`／`description` | 官方 | https://opencode.ai/v2/docs/agents/ | 2026-10-28 |
| OpenCode V2 Plugins 擴充體系 | @opencode/plugin SDK（TypeScript/npm）；可擴充 server（tools/hooks/agents）、TUI 與桌面 GUI 面板；opencode.jsonc 的 plugins 陣列宣告；支援本機與 npm（Bun 自動快取） | 官方 | https://opencode.ai/v2/docs/plugins/ | 2026-11-02 |
| OpenCode V2 子代理模型支援 | `.opencode/agents/*.md` 或 `opencode.jsonc` 的 `mode: subagent` 支援任意 `provider/model`（如 `openrouter/...`、`anthropic/...`）；原生支援異質多模型混搭 | 官方 | https://opencode.ai/v2/docs/agents/ | 2026-11-03 |
| OpenCode V2 Free 共享池限速機制 | 官方未公開固定 RPM，採動態共享池；尖峰或連續 heavy prompt 會跳 `Rate limit exceeded` / `Free usage limit reached`，受 IP/CGNAT 影響 | 官方／二手（Reddit） | https://teamorouter.com 與 Reddit r/opencode 回報 | 2026-11-04 |
| OpenCode V2 併發控制（ConcurrencyManager） | 槽位式 FIFO 佇列，單一 provider/model 預設並發上限通常為 5 個任務 | 官方（架構） | DeepWiki 與 GitHub OpenCode 架構文件 | 2026-11-04 |
| OpenCode V2 子代理對 Free 額度消耗 | Reddit 社群回報多子代理/背景任務（如 DeepSeek Flash）是造成急速耗盡配額與 429 鎖定的主因 | 二手（Reddit） | Reddit r/opencode 討論串 | 2026-11-04 |
| OpenCode V2 `--agent plan` 唯讀鎖定與桌面 App 規則載入 | `opencode run --agent plan` 可從底層沒收寫入工具鎖定唯讀；桌面 App 自動載入 `~/.config/opencode/AGENTS.md` 並辨識 `THIS MACHINE` | 實測 | 2026-11-04 本機與管制機實測 | 2026-11-04 |
| OpenCode V2 11 月巡檢與 v2.2.0～v2.3.2 更新 | 確認 `AGENTS.md`（可用 `OPENCODE_DISABLE_CLAUDE_CODE=1` 停用 `~/.claude/CLAUDE.md` 回退）、`opencode.jsonc` 與 `permissions` 陣列無破壞性異動；v2.2.0 推實驗性 Desktop Plugins 與動態 Session Instructions API（`ctx.session.instructions.entry.put/list/remove`，不破系統快取），v2.3.2 優化 leading developer message 快取與自訂 cache TTL | 官方（規則與權限）／二手（v2.2.0～v2.3.2 搜尋轉錄） | https://opencode.ai/v2/docs/ 、https://opencode.ai/v2/docs/instructions/ 、https://opencode.ai/v2/docs/permissions/ | 2026-11-22 |

---

## 四、安全機制與環境

| 主題 | 結論 | 狀態 | 來源 | 查證日 |
|---|---|---|---|---|
| Claude 資安防護會誤判 | 官方說明防護刻意設得廣，可能誤判正當資安工作 | 官方 | https://arte.itlibra.com/en/articles/claude-code-safeguards-flagged-this-message | 2026-10-25 |
| 讀資安檔會被凍結 | 多位使用者回報；不需攻擊性指令 | 二手 | https://claudeissues.com/issue/68791-bug-cyber-safeguard-false-positive-blocks-security-review-skill-in-a-fresh-sessi | 2026-10-25 |
| 一次誤判可能擋整個對話 | 有回報指機制會看整段對話累積內容 | 二手 | https://claudeissues.com/issue/63751-bug-aup-cyber-safeguard-false-positives-on-legitimate-own-software-hardening-one | 2026-10-25 |
| Cyber Verification Program | 可申請，但有人回報通過後仍被擋；官方處置（/rewind、/feedback、CVP）見 troubleshooting 文件 | 官方（處置）／二手（被擋回報） | https://code.claude.com/docs/en/troubleshooting （官方）；https://claudeissues.com/issue/86352-bug-claude-code-cybersecurity-safeguards-blocking-approved-cyber-verification-pr （二手） | 2026-10-31 |
| 多次觸發是否停權 | 官方區分「單次 session refusal」與「反覆違規導致之帳號停權（可至 `claude.ai/restricted` 申訴）」，但觸發幾次會停權之次數門檻條款仍未見；只有使用者回報推論 | 官方（申訴區分）／**查不到**（次數門檻） | https://claude.com/ 與官方支援說明（2026-11-22 複查） | 2026-11-22 |
| `deny` 能否一定防凍結 | 無官方說明 | **查不到** | 無 | 2026-10-25 |
| Python 3.11 安全更新 | 到 2027-10 結束（管制機目前維持 3.11，2026-11-26 實測無 3.13） | 官方 | https://peps.python.org/pep-0664/ | 2026-10-25 |
| Python 3.13 安全更新（NAS 容器鏡像用） | 到 2029-10 結束 | 官方 | https://peps.python.org/pep-0719/ | 2026-11-16 |
| `google-colab-cli` 平台 | 只支援 Linux、macOS；Windows 不支援 | 官方 | https://pypi.org/project/google-colab-cli/ | 2026-10-27 |
| Colab G4 顯卡 | NVIDIA RTX PRO 6000 Blackwell Server Edition，96GB GDDR7 | 官方 | Colab 官方資源頁 | 2026-10-27 |
| Gemini 生圖高頻呼叫限流（HTTP 429） | 連續快速呼叫易觸發 RPM 上限與 429 `RESOURCE_EXHAUSTED` 暫時冷卻（5～15 分鐘）；批次腳本需加 15～20 秒間隔與 60 秒退避 | 實測 | 2026-10-26 批量生圖實測 | 2026-10-26 |
| 管制機 VBS `Shell.Application` 防毒攔截 | VBScript 呼叫 `Shell.Application`（`ShellExecute`）啟動外部程式會被端點防毒（Apex One）行為監控直接攔截並告警；GUI 啟動優先改用 `.cmd`／`.bat` 搭配 `start` | 實測 | 2026-10-20 管制機實測 | 2026-10-20 |
| 管制機 Codex 生圖無法連線 | 管制機無法連線至 OpenAI / Codex 生圖服務，在管制機生圖直接走 Antigravity `image-generator` 子代理 | 實測 | 2026-10-27 管制機實測 | 2026-10-27 |
| 管制機防火牆日間放行時段 | 上班時間 `07:30~17:30` 開放 `github.com`、`api.github.com`、`gist.github.com`、`oauth2.googleapis.com`；全時段可連 `*.run.app`、`api.opencode.ai`；`raw`/`objects`/`codeload`、`*.gvt1.com`、`openrouter.ai` 全時段阻斷 | 實測 | 2026-11-17～18 管制機實測 | 2026-11-18 |
| Gemini Web 網頁版生圖備援（`gemini-web-imagegen`） | 透過 `gemini-webapi >= 2.1.1` 與 Chromium CDP（`ws.send_json` Text Frame）自動無頭提取 `__Secure-1PSID`／`__Secure-1PSIDTS`，支援跨專案 2K 文生圖與 `files=[...]` 改圖 | 實測 | 2026-11-08 本機實測 `gemini_web_gen.py` | 2026-11-08 |

---

## 五、原理與研究（本目錄文件用）

| 主題 | 來源 | 狀態 |
|---|---|---|
| Agent 迴圈、上下文管理、規則檔、多代理、可靠性、成本 | Harvard CS2680 Modern AI Systems（Fall 2026），https://cs2680.com/ | 原整理，2026-10-19 查證課程頁 |
| 驗收方法、先規劃、上下文管理 | Claude Code 官方 Best practices，https://code.claude.com/docs/en/best-practices | 官方 |
| 進度檔、功能清單、git 交接 | Anthropic Engineering：Effective harnesses for long-running agents | 官方 |
| 獨立評審（規劃／生成／評審） | Anthropic Engineering：Harness design for long-running application development | 官方 |
| 入口檔約 100 行、規則寫成自訂檢查 | OpenAI：Harness engineering: leveraging Codex in an agent-first world | 官方；成果數字為單一內部專案 |
| 每檔低於 200 行 | 第三方轉述 Anthropic 記憶文件 | 二手 |
| 每檔 200 行是硬性門檻 | 官方沒有這個說法；只是參考值 | **查不到** |
| Prompt→Context→Harness→Loop 演進 | 原整理引用 Addy Osmani《Loop Engineering》系列與 CLI `/loop`、`/goal` | 未重新查證 |
| Ambient Agents、Agent Inbox | 原整理引用 Harrison Chase（LangChain）與 Sequoia Capital | 未重新查證 |
| Meta-Harness、OO-Harness | 原整理引用 OmniAgent、arXiv:2610.28380 | 未重新查證（研究階段） |
| 「用 JSON 比 Markdown 不易被改壞」 | 原整理引用二手來源 | 二手 |
| 在規則最前面明確點名工具名稱（Gemini 3 提示建議） | https://developers.googleblog.com/new-gemini-api-updates-for-gemini-3 | 官方 |
| 用程式碼呼叫 MCP、延後載入工具以省上下文 | Anthropic Engineering：Code execution with MCP（原整理無網址） | 官方；「省 98%」未核實 |
| 工具延後載入、輸出上限、只在尾端追加以利快取 | OpenAI：How GPT-5.6 fuses frontier intelligence with frontier efficiency（原整理無網址） | 官方 |
| AGENTS.md 在犯錯時更新、讓內部工具可被 AI 使用 | Greg Brockman 2026-02 貼文（第三方轉載） | 二手 |
| /goal 運作與風險 | 多篇第三方文章 | 二手 |
| 子代理派工判斷、防同時改同檔、兩段式刪除、迴圈四問與人肉迴圈固化 | 韋哥科技教室 YouTube 系列（EP03 `5xckjKM-s20`、EP04 `JnDTgPuCpcs`、EP07 `raEr02U_mj8`、EP09 `WzgS8mFzCgg`、EP10 `e6M2Zqda8j4`） | 二手（實務經驗整理，2026-10-31 核對逐字稿） |
| 權限詢問約 93% 使用者直接按同意（核准疲勞）、間接提示詞注入風險 | 韋哥科技教室 EP06（`N5v4AUfWasM`）引述研究數據與 Google 官方安全風險說明 | 二手（影片轉述，93% 原始論文出處未細查） |

---

## 六、目前列為「推測」或「查不到」的項目

| 項目 | 目前處理 | 下次要做 |
|---|---|---|
| 各家 harness 是否會主動觸發提問卡片 | 免記指令，由全域規則開頭強制點名提問卡片工具（整合規劃、迴圈驗證、動態子代理與 EGM 技能）；見對照表第五節 | 用四個固定任務實測 |
| `deny` 降低凍結機率的成效 | 標「推測」，不誇大 | 跨資料夾實測 |
| `deny` 跨資料夾保護 | 標「尚待實測」；避免在敏感專案上層啟動 | 從兩個不同資料夾啟動實測 |
| Windows 的 `//` 絕對路徑寫法 | Permissions 文件已載有 `Read(C:/...)`、`Read(//c/...)` 與 `blockReadsOutsideWorkingDirectories`，但仍存繞過風險 | 跨資料夾實測 |
| 多次觸發 safeguards 是否停權 | 標「官方區分 session refusal 與帳號停權，次數門檻查不到」 | 每月查官方條款 |
| Antigravity 是否有背景自動記憶 | 2026-11-22 直開官網 Changelog 複查仍查無 | 每月追蹤 |
| Antigravity 新 workflows 系統 | 已於 v2.32.0 公布 Dynamic Workflows（以內建 Python runtime 編排平行子代理） | 已結案（後續追蹤實戰表現） |
| `ask_question` 是否有獨立 `description` 欄位 | 2026-11-22 複查仍無獨立 `description` 欄位 | 每月查官方規範 |
| Antigravity、OpenCode 的 Hook／權限對應細節 | 部分未查證 | 需要時查官方文件 |
| Meta-Harness／OO-Harness 的實際可用性 | 當研究方向 | 有官方實作再評估 |

---

## 七、每月重新查證流程

1. 打開 `docs/coding_agent_features_table.md`，照第六節官方網址逐頁對照。
2. 只改有變動的列，更新該列與開頭的「最後全面查證」。
3. 對照第三節「依賴本表的規則」，修改受影響的規則檔。
4. 更新本表對應列與查證日。
5. 執行提示詞與規則健檢：在 Claude Code 執行 `/doctor prompt-audit`（v2.1.283+），或在任一 Agent 呼叫全域技能 `/prompt-audit`（自動執行 `audit_scanner.py` 快篩語法、24KB／200 行上限與失效路徑）。
6. 照 `docs/rule_maintenance_sop.md` 第五節跑收尾驗證。

> 查證時**先查官方文件再寫，不憑記憶**；查不到就寫查不到，不要用推論補成事實。工具版本、設定欄位、日期都屬高風險資訊。
