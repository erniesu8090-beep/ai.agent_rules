# Coding agent 功能對照表

> 整併自：原 coding_agent_features.md、lightweight_llm_improvement.md、interactive_question_rules.md（2026-10-31 併入第五節）；原始版本已移至資源回收筒或可查 Git 歷史。
> 範圍：只收**寫程式用的 coding agent**（Claude Code、Antigravity、Codex、OpenCode）；聊天介面（claude.ai、Gemini Apps、ChatGPT 網頁版）不在本表。
> 用途：設計 `global_rules.md`、`templates/` 規則與安裝腳本的依據。**每一列都有查證日期**；最後一次全面查證超過 1 個月就要重新查。
> 最後全面查證：2026-11-22（2026-11-15 巡檢匯整 ＋ 2026-11-22 官網複查：Antigravity v2.29～v2.34.0／Dynamic Workflows／Gemini 4 Neon／Orchestrator (Neon)／MCP Apps、Claude Code v2.1.314～v2.1.330、OpenCode V2 v2.2.0～v2.3.2；2026-11-26 補齊四種子代理／EGM／Codex 免費生圖限制）
> 標記：「—」查無對應功能；「⚠」只有第三方來源、本機實測或尚未查證。

---

## 一、納入的 coding agent

| 代號 | 工具 | 全域規則安裝位置 | 官方文件 |
|---|---|---|---|
| `claude` | Claude Code（CLI、桌面 App、IDE） | `~/.claude/CLAUDE.md`；開發機另設 `~/.claude/settings.json`（兩者都讀＋`permissions.deny`） | https://code.claude.com/docs/en/ |
| `antigravity` | Antigravity（App、IDE、CLI `agy`） | `~/.gemini/GEMINI.md`；非管制機另設 `~/.gemini/config/hooks.json` | https://antigravity.google/docs/ |
| `codex` | OpenAI Codex（CLI `codex`、桌面 App、IDE） | `~/.codex/AGENTS.md`；非管制機另設 `~/.codex/config.toml`（啟用提問卡片） | https://developers.openai.com/codex/ |
| `opencode` | OpenCode V2（TUI、桌面 App、Web） | `~/.config/opencode/AGENTS.md`；另設 `~/.config/opencode/opencode.jsonc` | https://opencode.ai/v2/docs/ |

> Gemini CLI 自 2026-06-18 起對 AI Pro、AI Ultra 與免費個人帳號停止服務，後繼者為 Antigravity CLI（`agy`）；企業授權與付費 API Key 不受影響（已查證，2026-05-19 Google 官方部落格）。本表不收 Gemini CLI。

---

## 二、功能對照

### 2-1 規則檔（每次對話都載入）

| 功能 | Claude Code | Antigravity | Codex | OpenCode | 查證日 |
|---|---|---|---|---|---|
| 全域規則 | `~/.claude/CLAUDE.md`；組織 managed CLAUDE.md | `~/.gemini/AGENTS.md`、`~/.gemini/GEMINI.md`、`~/.gemini/config/AGENTS.md`、`~/.gemini/config/GEMINI.md`；模組化 `~/.gemini/config/rules/*.md`（需 frontmatter）；CLI 另讀 `~/.gemini/antigravity-cli/rules/*.md` | `~/.codex/AGENTS.override.md` 或 `~/.codex/AGENTS.md` | `~/.config/opencode/AGENTS.md`（系統層另讀 `/etc/opencode`、`%ProgramData%\opencode`） | 2026-10-28 |
| 專案／目錄規則 | `CLAUDE.md`、`.claude/CLAUDE.md`、`CLAUDE.local.md`，目前資料夾與所有上層全部串接；子資料夾的檔案讀到該資料夾檔案時才載入 | 任一目錄的 `AGENTS.md`、`GEMINI.md`，或 `<dir>/.agents/` 底下；累加，衝突時較具體的目錄優先 | 從 Git／專案根目錄往下到目前資料夾，依序合併 `AGENTS.override.md` 或 `AGENTS.md` | 任一目錄的 `AGENTS.md`，由遠而近合併；子資料夾的檔案讀到該資料夾時才載入 | 2026-10-28 |
| 讀 `AGENTS.md` | v2.1.277 起原生讀取，但路徑上有 `CLAUDE.md`／`.claude/CLAUDE.md`／`CLAUDE.local.md` 時**全部跳過、不提示**（`~/.claude/CLAUDE.md` 不算）。可在 `~/.claude/settings.json` 設 `instructionFiles: "claude-md-and-agents-md"` 改成兩者都讀（專案層無效；v2.1.285 前外掛 ID 為 `agents-md@builtin`，v2.1.285 起亦支援 `cc-plugin-agents-md@builtin`，或用 `/config`） | 原生常駐 | 原生常駐（預設不讀 `CLAUDE.md`，除非在 `config.toml` 設 `project_doc_fallback_filenames`） | **唯一格式**：只讀 `AGENTS.md`，不讀 `CLAUDE.md`（V2 官方明訂無 fallback，可用 `OPENCODE_DISABLE_CLAUDE_CODE=1` 停用 `~/.claude/CLAUDE.md` 回退） | 2026-11-22 |
| AI 看得出載入哪些規則 | 是：每個規則檔附完整路徑（「Contents of <路徑>」），可自行比對；人工確認用 `/memory`（需 v2.1.280+ 才會列出直接讀入的 `AGENTS.md`） | ⚠ 未查證 | `/status` 可檢視目前載入設定 | 開新對話自動載入；實體對話開頭直接反映規則與末尾 `THIS MACHINE`（2026-11-04 實測確認） | 2026-11-04 |
| 往上找規則的範圍 | 一直到磁碟根目錄 | 只到工作區根目錄（workspace root，不會超過）；2026-10-10 實測開啟 Git 倉庫時只到該倉庫根目錄 | 只到 Git／專案根目錄 | 從工作區往上找到**家目錄**；工作區在家目錄以外時只到專案根目錄（`D:\AI_Workspace` 屬此類，要另用 `instructions` 指定） | 2026-10-28 |
| 引用其他檔 | `@path`，展開嵌入，最多 4 層；程式碼區塊內不展開 | `@[label](path)` 展開嵌入；`@filename` 只轉成絕對路徑 | — | 不支援 `@` 展開；改用 `opencode.jsonc` 的 `instructions`（相對路徑、glob、`~/`、絕對路徑、HTTP(S)） | 2026-10-28 |
| 模組化規則 | `.claude/rules/*.md`，遞迴掃描；frontmatter `paths` 限定檔案 | 工作區 `.agents/rules/*.md`、全域 `~/.gemini/config/rules/*.md`（CLI 為 `~/.gemini/antigravity-cli/rules/*.md`），預設只掃第一層（子資料夾須註冊於 `.agents/rules.json` 的 `entries`，否則忽略）；獨立 `AGENTS.md`／`GEMINI.md` **不支援 frontmatter**；`rules/*.md` 必填 `trigger`（`always_on`／`model_decision`／`glob`／`manual`），誤寫駝峰（`alwaysOn`）、漏填條件欄位或 `glob` 以 `*` 開頭未加雙引號皆會**靜默丟棄** | 子目錄放 `AGENTS.md`（註：`~/.codex/rules/*.rules` 是指令執行的白名單規則，不是文字規則） | 巢狀 `AGENTS.md`（按需載入）＋ `instructions` 陣列 | 2026-11-14 |
| 容量限制 | 建議每檔 200 行內；隨需載入規則（子資料夾 `CLAUDE.md`、`paths` 限定規則）v2.1.309 起單檔有字元上限（200K 視窗為 40,000 字元、1M 視窗為 150K～200K 字元），超過只取開頭 | 每檔 24,000 bytes（展開 `@[label](path)` 後），超過依行邊界截斷；全域與 `always_on` 規則共享 20,000 tokens 預算（`defaultRulesBudget`），超標時最大檔案降級為路徑指標（內建外掛規則豁免） | 預設合計 32 KiB（`project_doc_max_bytes = 32768`），超過靜默截斷 | —（查無上限，只受模型上下文限制；⚠ v2.2.0+ 插件支援動態 Session Instructions API `ctx.session.instructions.entry.put/list/remove` 增量附加不破系統 Prompt Cache，v2.3.2 優化 leading developer message 與自訂 cache TTL） | 2026-11-22 |
| 規則自我檢查（Prompt Audit） | `/doctor prompt-audit`（別名 `/checkup prompt-audit`，v2.1.283+，由內建 `/claude-api` 技能運作）：掃描 `CLAUDE.md`、`AGENTS.md`、`.claude/` 與 `~/.claude/` 下的規則與技能，找舊模型高壓贅詞（如全大寫 `CRITICAL`）、失效路徑與矛盾規則，先出報告與 Diff 經確認才改；亦可調用全域技能 `/prompt-audit` | 無同名 `/doctor` 指令（GitHub 上 `doctor` 屬第三方腳本）；官方以 **`/agy-customizations`**（載入自訂系統規範除錯修復）＋ **`/learn`**（含 `Schema check` 與 `Prefers updates over new files` 並產出 `learning_proposal.md`）＋ CLI **`/context`**（桌面版搭配 `usage-monitor` 外掛）組合達成；實務已封裝全域技能 **`/prompt-audit`**（附 `audit_scanner.py` 靜態快篩） | 無內建指令；共用全域技能 **`/prompt-audit`**（搭配 `audit_scanner.py` 靜態快篩） | 無內建指令；共用全域技能 **`/prompt-audit`**（搭配 `audit_scanner.py` 靜態快篩） | 2026-11-22 |

### 2-2 按需載入與流程

| 功能 | Claude Code | Antigravity | Codex | OpenCode | 查證日 |
|---|---|---|---|---|---|
| 規劃與訪談 | Plan mode（見 permission-modes 文件） | `/plan`（訪談後產生可審閱的實作計畫）、`/grill-me`（一次一題、推薦答案排第一）；可組合 `/plan /grill-me 任務` | Plan mode（預設啟用 `request_user_input`） | 內建 `plan` agent（唯讀，不改專案檔；TUI 切換）＋自訂 `/plan` 指令 | 2026-10-28 |
| Skills | `~/.claude/skills/`、`.claude/skills/`；`/名稱` 或依描述自動（v2.1.319 開啟 Bash 沙盒時，子目錄 `.claude/skills` 須在該目錄啟動或 `/cd` 進入才載入；v2.1.325 排程與 `/loop` 跑含 `allowed-tools`／`hooks` 的 Skill 前預設詢問，須於 `permissions.allow` 加 `Skill(name)`） | 工作區 `.agents/skills/`（非標準路徑於 `.agents/skills.json` 註冊）；全域 App/IDE `~/.gemini/config/skills/`，CLI `~/.gemini/antigravity-cli/skills/`；`/名稱` 或自動（CLI 用 `/skills reload`，桌面版下輪生效）；v2.30 支援從 Claude Code／Codex／Cursor 一鍵匯入至外掛 | 工作區 `.agents/skills/`；全域 `~/.codex/skills/`、`~/.agents/skills/`；`$名稱` 或依描述自動 | `~/.config/opencode/skills/`、`.opencode/skills/<id>/SKILL.md`；**相容讀** `~/.claude/skills/`、`.claude/skills/`、`.agents/skills/`；依描述自動或 `@skill-id` | 2026-11-15 |
| 手動流程 | Skill 設 `disable-model-invocation: true`；舊 `.claude/commands/` 仍可用；v2.1.323 新增實驗性 Code Mode（JS 呼叫工具）與 `plugin.json` `engines` 版本檢查；v2.1.326 支援 Agent Teams 併用 Code Mode、檢查 `--allowedTools`／`--disallowedTools`／`--tools` 不完整規則並警告、支援 `CLAUDE_CODE_MAX_OUTPUT_TOKENS`；v2.1.329 拒絕 Code Mode 讀超 256 MiB 行範圍、`/tasks` 顯示排程／`/loop`／goal／對話 forks、`/mcp` 顯示遠端拒絕 `Server message`；v2.1.330 新增 Enterprise Admin Console `claude auth login`、macOS/Linux 內建圖表模式 `easel`、`CLAUDE_CODE_FULL_SIGN_IN_LINK=1`、排程與 `/loop` 最長延至 30 天、恢復 `max_tokens` 超限自動重試 | 舊 Workflows 2026-10-19 起停止運作（用 `/migrate-workflows` 轉 Skills）；**v2.32.0 正式推出 Dynamic Workflows**（以內建 Python runtime 編排平行子代理）；v2.34.0 新增 `Gemini 4 Neon`、`Orchestrator (Neon)` 與 `MCP Apps` 支援 | 以 `$skill-name` 點名觸發 Skill | `.opencode/commands/*.md` 或 `commands` 設定（可指定 `agent`／`model`；`subagent: true` 背景執行） | 2026-11-22 |
| 子代理 | `~/.claude/agents/`、`.claude/agents/`；v2.1.316 新增 `CLAUDE_CODE_SUBAGENT_EFFORT`、v2.1.318 背景逾 3 分鐘指令自動背景化保活快取、v2.1.319 `/tasks` 重開已完成子代理（細節見 2-2-1） | `.agents/agents/<name>.md`、全域 `~/.gemini/config/agents/`；v2.29 修復 Git worktree 未保留未提交變更、v2.31 新增 `/swarm`、v2.34.0 推出 `Orchestrator (Neon)`（`Gemini 4 Neon` 規劃＋`Gemini 4 Hydrogen` 實作）（細節見 2-2-1） | `.toml` 子代理設定與內建平行子代理（細節見 2-2-1） | `~/.config/opencode/agents/`、`.opencode/agents/<name>.md`；`mode: subagent`（細節見 2-2-1） | 2026-11-22 |
| 回應風格 | Output styles：`~/.claude/output-styles`、`.claude/output-styles`；`/output-style` | ⚠ 導覽列有「Personas」頁，未查證 | — | —（自訂 agent 的 `system` 可換系統提示） | 2026-10-28 |
| Plugins | 完整套件：打包 tools、skills、agents、hooks、MCP；`plugin.json`；支援團隊/公開市集（`marketplace.json`）；CLI `claude plugin`、Session `/plugin` | 名稱空間套件（v2.28+）：`plugin.json` 打包 skills、agents、rules、MCP、hooks；市集（Marketplace）分展架與精選；圖形化 Accounts 頁籤管理 OAuth 憑證（如 Google Drive 等 CLI）；指令 `/plugin`；v2.34.0 正式支援 **MCP Apps**（工具於對話渲染互動 UI） | —（透過 Skills 與 MCP servers 擴充） | 模組化套件（TypeScript/npm）：`@opencode/plugin`；可擴充 server（tools、hooks、agents）、TUI 與桌面 GUI 面板；`opencode.jsonc` 的 `plugins` 陣列宣告；本機與 npm 套件（Bun 自動快取）；⚠ v2.2.0 推出實驗性 Desktop Plugins 與動態 Session Instructions API（僅搜尋轉錄） | 2026-11-22 |

#### 2-2-1 四大工具子代理（Subagent）跨模型調度與設定格式對照

> 查證日期：2026-11-03～2026-11-26（官方文件與實測）  
> 重點結論：
> 1. **生態邊界**：大廠官方工具（Claude Code、Codex、Antigravity）受限於商業生態，原生子代理**僅限自家模型體系或抽象等級**；**OpenCode 是唯一原生支援跨廠牌自由混搭（異質 Multi-Agent）的開放架構**。
> 2. **原生 Custom Agent 定位**：官方設計主要用於「固定專職人設免重複輸入、工具限制防呆（如唯讀）、以及透過自家模型等級（Flash/Lite/Haiku）分流降成本」。
> 3. **外部 CLI 派工定位**：克服大廠同門模型「雙胞胎思維同質化盲區」，透過外部 CLI（如 OpenCode CLI）呼叫完全獨立的開源模型（如 DeepSeek）擔任客觀 Verifier 挑錯，且零消耗主力 Token。

##### ① 四大工具子代理支援度比較表

| 項目 | Claude Code | Antigravity (agy) | Codex (OpenAI) | OpenCode |
|---|---|---|---|---|
| **設定檔格式** | Markdown ＋ **YAML Frontmatter** | Markdown ＋ **YAML Frontmatter** | **TOML** 設定檔 | Markdown ＋ **YAML** 或 **JSONC** |
| **定義檔存放路徑** | 專案 `.claude/agents/*.md`<br>全域 `~/.claude/agents/*.md` | 專案 `.agents/agents/*.md`<br>全域 `~/.gemini/config/agents/*.md` | 專案 `.codex/agents/*.toml`<br>全域 `~/.codex/agents/*.toml` | 專案 `.opencode/agents/*.md`<br>全域 `~/.config/opencode/agents/*.md`（或 `opencode.jsonc`） |
| **模型指定機制** | 自家型號別名：`haiku`、`sonnet`、`opus`、`inherit` | **模型等級抽象（Tiers）**：`flash_lite`、`flash`、`pro`、`inherit` | 自家型號：`gpt-6.1-sol`、`gpt-6.1-terra`、`gpt-6-luna`、`gpt-6-astra`（`gpt-5.5` 已於 2026-10-14 退役；v0.167 `PreToolUse` 先於 Guardian 審查；v0.169 `codex exec` 未信任目錄須加 `--trust`） | **完整 Provider 路由**：`provider/model`（如 `anthropic/claude-...`、`openrouter/...`） |
| **能否跨廠牌混搭？** | **否**（完全鎖定 Anthropic 自家 Claude 模型） | **否**（依當前對話主模型家族做等級分流，無法脫鉤自選第三方品牌） | **否**（完全鎖定 OpenAI 自家 GPT/Codex 體系） | **是（唯一原生支援）**：主對話與子代理可來自完全不同的模型供應商 |
| **實務跨模型解法** | 外部 CLI 派工（如調用 OpenCode CLI） | **外部 CLI 派工**（透過終端執行 `opencode run -m ...`） | 外部 CLI 派工 | 原生支援在設定檔或指令中直接指定 |
| **多代理人叢集（Swarm）** | 實驗性 **Agent Teams**（`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`） | **原生支援 Native Swarm**（指令 `/swarm`、共享看板、Coordinator／Worker／Verifier／Narrator／Monitor） | 否（僅單層平行 subagents） | 支援自訂多 agent 鏈式與平行執行 |
| **工作區隔離（Workspace）** | 共用工作區或獨立終端窗格（`tmux`） | **原生三模式**：`inherit`（共用）、`share`（Git worktree 獨立工作副本，免衝突平行修改）、`branch`（獨立 clone） | 共用工作區 | 工作區繼承（或各指令自訂目錄） |
| **對話歷史分岔（Forking）** | 否（空白對話啟動） | **原生支援**（`fork: "coordinator"` 或指定成員，分岔延續既有上下文） | 否（空白對話） | 支援自訂 prompt 上下文注入 |

##### ② 各工具子代理設定檔範例

* **Claude Code (`.claude/agents/code-reviewer.md`)**：
  ```markdown
  ---
  name: code-reviewer
  description: 專門審查程式碼品質與安全性。當需要 review 或改完程式碼時主動使用。
  tools: Read, Grep, Glob
  model: haiku
  ---
  你是一位資深程式碼審查員。請針對剛才修改的程式碼進行邊界條件與潛在漏洞檢查。
  ```

* **Antigravity (`.agents/agents/code-reviewer.md`)**：
  ```markdown
  ---
  name: code-reviewer
  subagent: true
  model: pro
  description: 針對複雜變更進行深度架構與邏輯檢查。
  ---
  你是一位唯讀審查子代理。請專注於邏輯錯誤、空值與邊界條件。
  ```

* **Codex (`.codex/agents/code-reviewer.toml`)**：
  ```toml
  name = "code-reviewer"
  description = "Use for validating boundary conditions and potential security bugs."
  model = "gpt-6-luna"
  model_reasoning_effort = "medium"
  developer_instructions = """
  Perform read-only review on the modified files and list issues by severity.
  """
  ```

* **OpenCode (`.opencode/agents/reviewer.md`)**：
  ```markdown
  ---
  description: 跨模型獨立挑錯審查員
  mode: subagent
  model: openrouter/anthropic/claude-sonnet-5.5
  permissions:
    - action: edit
      resource: "*"
      effect: deny
  ---
  以第二雙眼睛的視角審查當前變更，指出邏輯盲區與潛在異常。
  ```

##### ③ 外部 CLI 派工實戰指南（OpenCode 子代理規範，2026-11-04 實測整理）

當 Antigravity、Claude Code 或 Codex 主對話需要調用 OpenCode 擔任外部獨立子代理時，必須遵循以下工程防呆與派工準則：

1. **Windows 背景調用防卡死與唯讀鎖定三要素**：
   ```cmd
   cmd /c "opencode run --agent plan -m <模型名稱> --auto \"<任務提示詞>\" < nul"
   ```
   - `cmd /c`：在 Windows 下確保命令解譯器正確處理引號與輸出導向。
   - `--agent plan`（核心唯讀鎖定，2026-11-04 實測確認）：強制指定 OpenCode 內建的 Plan 規劃模式，從底層沒收檔案寫入與修改工具，保證子代理絕不變更專案檔案。
   - `--auto`：自動確認所有非高危操作，避免 CLI 等待使用者互動確認而停滯。
   - `< nul`（核心防卡死）：Windows 下非互動進程常因等待 stdin 結束符號（EOF）而陷入無窮等待；導向空輸入確保進程順暢退出。
2. **子代理數量與動態工作池（Worker Pool：線上最多 3 個）**：
   - **0 個（不派）**：單檔小修改、修小錯、前後步驟高度依賴的任務（留在主對話做，避免掉細節與浪費 token）。
   - **1 個（預設）**：讀巨型檔案/Log、日常程式碼修改後的「客觀視角唯讀抓漏」。
   - **多子代理（動態工作池）**：涉及金流、登入權限或架構大改的高風險任務，可派多個獨立視角分工審查（總任務數量不設死上限）；執行時採「**階梯式錯峰啟動（間隔 5～10 秒）＋ 線上並行上限 3 個（Worker Pool）**」，任一子代理完成後立即動態遞補下一個，兼顧防範 429 併發限速與最小化總等待時間。
3. **OpenCode Free 限速與底層槽位限制**：
   - OpenCode 內部 `ConcurrencyManager` 預設槽位為 5；且 Free 通道採動態共享池，嚴格遵守上述線上最多 3 個並行與錯峰啟動規範。
4. **漸進式封裝（Progressive Disclosure）**：
   - 具體 CLI 命令封裝於獨立技能母本庫 `ai.agent_skills` 之 `opencode-runner/SKILL.md`（預設帶入 `opencode/deepseek-v4.1-flash-free#high`），由 `install.bat`／`install.sh` 自動觸發全域派發；全域規則只保留觸發原則，將常駐 Prompt 消耗壓在 200 行以內。
5. **受限環境（管制機）限制**：
   - 管制機禁止調用需要連線 OpenRouter 等外部商業 API 的模型，僅可使用本機或核准通道。

##### ④ 四種子代理協同型態與團隊架構（2026-11 查證更新）

> 查證日期：2026-11-26（Antigravity 內建 `invoke_subagent`、`native_swarm`、`Orchestrator`、EGM v0.1.1 外掛規格 ＋ Claude Code Agent Teams 實測比對）  
> 重點結論：實務上依任務範圍與協同深度分為**四種子代理模式**（加上留在主對話的「單模型」或「**Orchestrator 雙模型自動接力**」，共五種派工決策）。請注意 **Orchestrator 並非隔離子代理**，而是同一對話脈絡內的雙模型接力；詳細機制見第 5 點。

1. **四種子代理模式對照表**：

| 比較維度 | 模式一：原生單工子代理（`invoke_subagent` / Task） | 模式二：外部異質唯讀子代理（`opencode-runner`） | 模式三：EGM 外掛審查團隊（Elephant-Goldfish Model） | 模式四：多會話團隊協同（Swarm / Agent Teams） |
|---|---|---|---|---|
| **核心定位** | 主代理的「隨行小助手」 | 外部客觀視角的「獨立抓漏員」 | 規格發想、文件審查與補寫之「失憶評審團」 | 虛擬戰情室「跨模組平行開發團隊」 |
| **典型代表／觸發** | Antigravity `invoke_subagent`（`research`、`browser`、`self`）；Claude Code `Task` | OpenCode CLI（`cmd /c "opencode run ... < nul"`） | `google/elephant-goldfish-model` 外掛：7 個 `/egm-*` 技能＋10 個隔離評審角色（提問卡片第 ④ 題或 `/` 觸發） | **Antigravity Native Swarm**（使用者輸入 `/swarm`）<br>**Claude Code Agent Teams**（實驗性旗標） |
| **檔案權限** | 依定義（`research` 唯讀沙盒、`browser` 瀏覽器、`self` 繼承主代理） | **強制鎖定唯讀**（`--agent plan`，底層沒收寫入工具） | 主對話（Elephant）草擬／彙整；金魚評審（Goldfish）預設隔離唯讀審查文件與原始碼 | **具備完整檔案寫入權限**（各成員可指派獨立工作複本或終端實例）＋專職 `verifier` 唯讀驗收 |
| **通訊與結構** | 階層式（一對一主從），完成後摘要回報主對話 | 階層式（單向回報），結果輸出後收斂 | 外掛流程編排：多隻失憶金魚平行挑錯，由 `egm-synthesizer`（或編排者）彙總後交回主對話決策 | **網狀通訊**：Antigravity 為共享看板（`@name` 門鈴喚醒）；Claude Code 為 Mailbox 信箱 |
| **生命週期** | 單次任務，完成即結束 | 單次 CLI 程序，跑完即關閉 | 單次工作流階段（發想／草擬／審查／補文件），各金魚每次從零上下文啟動 | **長效常駐（Stateful）**，多輪對話推進直到整個功能完工 |
| **工作區隔離** | 共享工作區或唯讀沙盒（`self` 可選 `branch`/`share`） | 共享工作區（純讀取） | 各自獨立對話上下文（不繼承先前對話歷史，避免確認偏誤）；底層依賴 `invoke_subagent` | 支援工作區隔離（Antigravity `share`/`branch`；Claude Code `tmux` 獨立窗格） |
| **額度消耗** | 低至中等（可選 `flash` / `flash_lite` 省額度） | 極低（使用 Free 閘道或本機模型，零消耗主力 Token） | 中至偏高（平行喚起多隻金魚角色，故提問卡片預設「略過」省額度） | **極高（Quota Heavy）**，多代理人在線且高頻看板互動 |
| **跨工具支援** | Claude Code、Antigravity、Codex、OpenCode 皆有對應機制 | 跨平台通用 CLI | 支援 Antigravity、Claude Code、Codex 等（需執行環境可建立全新隔離子代理） | **Antigravity 原生支援**；**Claude Code 實驗性支援**；OpenCode 尚無原生看板團隊 |

2. **Antigravity Native Swarm 團隊架構核心規格**：
   - **五大角色編制**：
     - `Coordinator`（協調者）：主 Agent 擔任，與使用者溝通；**原則上不親自寫代碼**（"Do not do the work"），專注拆分任務、監控進度與仲裁。
     - `Worker`（工作代理）：以職能具體命名（如 `parser`、`ui`，嚴禁 `agent-1`），各認領互不衝突的模組獨立編寫與提交。
     - `Verifier`（驗證員）：每 2~4 個 Worker 配置 1 名，專責跑測試、檢視 diff 挑錯並在看板回報，不親自改碼以防同檔衝突。
     - `Narrator`（進度記錄員）：選配（依附 `swarm_narrator` 技能），持續維持 UI Overview（更新 `view.json`），絕不在看板發言。
     - `Monitor`（死結巡檢員）：選配（依附 `swarm_monitor` 技能），以背景 Cron（每 3 分鐘）巡查看板，發現全員死結時主動 `@` 責任人喚醒。
   - **喚醒與門鈴機制（Doorbell Mechanism）**：成員平時處於休眠（`waiting`，0 Token 成本）；只有被 `@name`、`@#channel` 或廣播 `@all` 標記時才會被喚醒執行一輪；引用歷史紀錄須使用序號（如 `#4`）。
   - **工作區隔離與分岔（`share` / `branch` / `fork`）**：寫碼 Worker 採 `share`（worktree 獨立複本）或 `branch` 隔離；派生成員時可設 `fork` 繼承指定歷史對話。
   - **模型分級調度（Model Tiering 效益）**：主對話使用高階推理模型（如 **Gemini 4 Neon**／**Carbon**／**Argon**）擔任 Coordinator，Workers 指派輕快省額度的 **Gemini 4 Hydrogen** 或 **Gemini 3.8 Flash**。

3. **Claude Code Agent Teams 團隊架構核心規格（實驗性）**：
   - **啟用方式**：在 `~/.claude/settings.json` 的 `env` 區塊加入 `"CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"`，或啟動時帶入 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 claude`。
   - **核心架構元件**：`Team Lead`、`Teammates`（獨立 Context Window）、`Shared Task List`（支援相依鎖定）、`Mailbox`（Teammates 間可直接非同步互傳訊息）；支援 `--teammate-mode tmux` 分割窗格顯示；可混搭自家 Haiku/Sonnet/Opus，不跨廠牌。

4. **EGM（Elephant-Goldfish Model，v0.1.1）外掛架構核心規格（2026-11-26 查證）**：
   - **三元角色分工**：`Elephant`（主對話，保有完整上下文）＋ `Goldfish`（隔離失憶子代理，只讀文件與引用原始碼進行盲區審查）＋ `You`（使用者拍板權衡）。
   - **7 個斜線技能（`egm/skills/`）**：規格設計流（`egm-brainstorm`、`egm-draft`、`egm-review`、`egm-resolve`、`egm-review-loop`）與既有專案維護（`egm-bootstrap`、`egm-drift-report`），附 10 個專屬子代理角色（如 `egm-synthesizer`、`egm-design`、`egm-zoom-out` 等）。
   - **與 Swarm 互補**：EGM 專攻「寫碼前設計定案與文件審查／補齊」，Swarm 專攻「跨模組平行寫碼開發與驗收」。

5. **Orchestrator（Antigravity 單一對話內的「大腦＋手腳」雙模型自動接力，2026-11-26 補充）**：
   - **定位釐清（非隔離子代理）**：在同一個對話裡維持**同一條對話脈絡與共用記憶**，背後自動切換 `Orchestrator Model`（如 `Gemini 4 Neon High` 規劃與卡住接手）與 `Executor Model`（如 `Gemini 4 Hydrogen Medium` 搜尋、改碼、建置與測試），**不會平行開分身，也沒有隔離記憶**，無法取代隔離子代理模式。

### 2-3 強制執行與記憶

| 功能 | Claude Code | Antigravity | Codex | OpenCode | 查證日 |
|---|---|---|---|---|---|
| Hooks | `settings.json`；`PreToolUse` 可阻擋；`PreCompact` 上限 10,000 字元（v2.1.314）；v2.1.323 `plugin validate` 支援 TS hooks 型別檢查；v2.1.328～329 Code Mode 下非致命 `PreToolUse` hook 錯誤預設不再阻擋（須於 command/HTTP/`mcp_tool` hook 明定 `"onFailure": "block"`）、信任對話框標示 hooks 聲明路徑 | 工作區 `.agents/hooks.json`、全域 `~/.gemini/config/hooks.json`；支援 `SessionStart`、`PreToolUse`（可 `deny`）、`PostToolUse`、`PreInvocation`、`PostInvocation`、`Stop`（含 `continuationActive` 防無限迴圈） | `config.toml`／`hooks.json`；另 `~/.codex/rules/*.rules` 可設指令 `prefix_rule` 放行或阻擋 | 無宣告式 hooks；用 Plugin（`~/.config/opencode/plugins/`、`.opencode/plugins/*.ts`） | 2026-11-25 |
| 拒絕讀取特定路徑 | `settings.json` 的 `permissions.deny`（例：`Read(./**/<資料夾>/**)`，相對路徑以啟動資料夾為起點；文件記載支援 `Read(C:/...)`、`Read(//c/...)` 與 `permissions.blockReadsOutsideWorkingDirectories`，v2.1.327 強化對 Bash 詢問與拒絕，⚠ 跨資料夾保護尚待實測），只擋內建讀檔工具；`.claudeignore` 實測無效；v2.1.314 新增 `permissions.blockWritesOutsideWorkingDirectories`、v2.1.319 新增 `permissions.denyInsteadOfPrompting`、v2.1.325 起沙盒內 Bash 預設改走詢問 | —（v2.30 權限模式單對話獨立套用且 Auto 轉正；v2.31/v2.32 瀏覽器下載須核准且跨站 iframe 預設登出隱藏） | —（沙盒管寫入範圍，無宣告式讀檔黑名單） | `opencode.jsonc` 的 `permissions`：`{action:"read", resource:"*<資料夾>*", effect:"deny"}`（`*` 會跨 `/`）；`external_directory` 可管工作區外的路徑 | 2026-11-22 |
| 自動記憶 | `~/.claude/projects/<專案>/memory/MEMORY.md`（前 200 行／25KB 自動載入；只存使用者資訊、被糾正的回饋、專案背景、外部參照，除錯修法通常不存；只存該機器，不隨 Git 同步） | —（無背景自動記憶；僅手動 `/learn`，先提案、核准後寫入） | `~/.codex/memories_*.sqlite` | —（無背景自動記憶） | 2026-11-15 |
| 附加系統提示 | `--append-system-prompt` | — | `-c developer_instructions=...` | agent 的 `system` 欄位（會取代該 agent 的基礎系統提示） | 2026-10-28 |
| 互動式選擇題卡片 | `AskUserQuestion`（⚠ v2.0.21+ 為第三方來源；原生單選、複選 `multiSelect`、自由填寫；選項分 `label` 與 `description`） | `ask_question`（官方確認支援單選、複選 `is_multi_select`、自動附自由填寫；v2.26 停駐輸入框上方、v2.29 支援摺疊並在直接回覆新訊息時自動取消；v2.33.0～v2.34.0 修正單選上移清除自訂回答與方向鍵誤選停用選項；本機實測 `options` 為單一字串陣列，無獨立 `description` 欄位） | `request_user_input`（預設於 Plan mode 啟用；一般模式需設 `[features] default_mode_request_user_input = true`，由安裝腳本設定） | `question`（原生單選／複選／自由填寫；選項有 `label` 與 `description`） | 2026-11-22 |

### 2-4 執行環境與雲端沙盒架構（本機 IDE/CLI vs 雲端 Remote VM）

> 查證日期：2026-11-06（官方環境規格與實測，詳見 `docs/verification_sources.md`）

#### ① 本機電腦 vs 雲端 Remote VM 差異對照表

| 項目 | 本機開發機（Windows / Ubuntu） | 雲端 Remote VM（Antigravity 遠端沙盒） |
|---|---|---|
| **運行環境** | 實體機或本機容器（Windows 10/11、Ubuntu） | 雲端獨立 Debian 12 Linux 沙盒虛擬機 |
| **VM 生命週期** | 持續常駐，手動重啟 | **對話級獨立配發（`provisioned for this conversation`）**：每個新對話為獨立全新 VM，不同對話互不干擾 |
| **專案放置路徑** | `D:\AI_Workspace\<專案名稱>` 或 `~/AI_Workspace/...` | `/home/antigravity/<GitHub擁有者>/<專案名稱>` |
| **專案綁定與權限機制** | 本機直接讀取磁碟；憑證依本機 git 設定 | **專案對話**：開機自動 clone 專案並注入專屬 Scoped Token；<br/>**非專案對話（Outside of Project）**：空白 VM，無私人 Repo 權限（手動 clone 會拋 403 錯誤） |
| **資料持久性** | **全磁碟持久保存** | **臨時性（Ephemeral）**：除 `/shared/user/.gemini/`（軟連結至 `~/.gemini`）與已 push 至 GitHub 的代碼外，其餘檔案在對話重置或結束時銷毀 |
| **系統權限** | 具備管理員或一般使用者權限 | **受限非 root（`antigravity` 帳號）**，嚴禁探測 `sudo`、`su` 或修改 `/etc`；套件安裝限於 User space（`uv`、`.venv`、`npm`） |
| **網路與 Proxy** | 直連外網或公司內網（管制機） | 流量全數經由 `agy-plugin-proxy`（`HTTP_PROXY` / `HTTPS_PROXY`）控管與憑證注入，受網域名稱白名單限制 |
| **網頁與 Localhost** | 開發者瀏覽器可直連 `http://localhost:<PORT>` | **使用者本機瀏覽器無法連線 VM 的 localhost**；前端/視覺化優先產出單一 HTML Artifact（Generative UI）供介面內直接檢視 |

#### ② 雲端沙盒實務陷阱與工程應對

1. **「Outside of Project」存取失效陷阱**：在 Antigravity 開啟新對話時，若未選擇專案（Outside of Project），VM 預設不掛載程式碼且不發放私人 Repo Token，手動 `git clone` 會出現 `403 Write access to repository not granted`。處理專案任務務必從專案介面開新對話。
2. **即時落盤保命準則**：因沙盒 VM 為臨時性環境，未提交的代碼與進度隨對話銷毀即滅失；任務告一段落必須即時將進度寫入 `PROGRESS.md` 並執行 `git commit + push`。
3. **無 Localhost 混淆預防**：AI 在雲端 VM 執行 Web 服務時，切忌向使用者回報「請於瀏覽器開啟 http://localhost:xxxx」，應主動採用 Artifact 封裝預覽。

---

## 三、依賴本表的規則

工具改版、某一列變了，就檢查對應的規則要不要改。新增依賴工具行為的規則時，補一列。

| 規則（所在位置） | 依據的列 |
|---|---|
| 安裝腳本同時設定新舊外掛 ID「兩者都讀」；自己的專案不建 `CLAUDE.md`；fork 保留 `CLAUDE.md`（`global_rules.md` 第 5 節、`guidelines/claude_code_rules.md`、`install.bat`、`install.sh`、README） | 讀 `AGENTS.md`；Antigravity、Codex 與 OpenCode V2 不讀 `CLAUDE.md` |
| Claude Code 開新對話自行比對有沒有讀到 `AGENTS.md`；`/memory` 需 v2.1.280+（`guidelines/claude_code_rules.md`、README） | AI 看得出載入了哪些規則檔 |
| 工作區規則要靠 `~/.config/opencode/opencode.jsonc` 的 `instructions` 指定才對 OpenCode 生效；四家都要遵守的規則放全域或專案（`global_rules.md` 第 5 節、`AGENTS.md`、README） | 往上層找規則的範圍、引用其他檔 |
| 安裝腳本建立 `opencode.jsonc`（`instructions` ＋ `permissions`），已存在只檢查（`install.bat`、`install.sh`、README） | 引用其他檔、拒絕讀取特定路徑 |
| 不建 `.agents/rules/`、`.claude/rules/`，只用 `AGENTS.md`（`global_rules.md` 第 5 節） | 模組化規則 |
| `global_rules.md` 200 行內且最長合成版 < 24,000 bytes（本倉庫 `AGENTS.md`） | 容量限制 |
| 安裝位置（`install.bat`、`install.sh`、`global_rules.md` 開頭） | 全域規則 |
| 資安防凍結阻擋讀取敏感專案與啟動資料夾限制（`global_rules.md` 第 8 節、`guidelines/claude_code_rules.md`、`install.bat`、`install.sh`、README、`docs/claude_code_permissions_deny.md`） | 拒絕讀取特定路徑 |
| 免記指令全自動提問卡片：規劃／3 檔以上／跨檔案／單檔大改／EGM 觸發詞前強制呼叫選擇題卡片，整合「規劃方案＋自我迴圈驗證＋動態子代理（含 `/swarm` 提示）／EGM」；禁寫冒號引導結尾句（`global_rules.md` 開頭與第 4、9 節、README、本表第五節） | 互動式選擇題卡片、子代理 |
| 開發機 Antigravity `Stop` Hook 防漏發 `ask_question`（`templates/hooks/ag_stop_card_guard.py`、`install.bat`、`install.sh`、README；管制機因防毒不裝） | Hooks |
| 安裝腳本自動連動 `ai.agent_skills` 派發至四家工具全域技能目錄（`install.bat`、`install.sh`、`AGENTS.md`、README） | Skills |
| AI 生圖優先順序（Antigravity → Gemini Web → Codex 付費；免費版 Codex 不提供 `image_gen`）、429 防鎖與跨專案技能整合（`global_rules.md` 第 9 節、README） | Skills、子代理 |
| 調用 OpenCode CLI 擔任外部子代理時依 `opencode-runner` Skill 強制加 `--agent plan` 唯讀鎖定、`--auto`、`< nul` 防卡死與動態工作池（`global_rules.md` 開頭與第 9 節、本表 2-2-1 節） | 規劃與訪談、子代理 |
| 除錯後篩選重要陷阱與漏掉的測試，先提案確認再於任務收尾時補進專案 `AGENTS.md`（已知的坑放檔案最末尾維持快取命中），維持 10 條／200 行（`global_rules.md` 第 9 節、`templates/AGENTS*.md`、本表第五節） | 自動記憶、容量限制 |
| 雲端沙盒專屬規則 `machine_rules/sandbox.md`（非 root 權限邊界、Proxy 限制、無 Localhost 直連與 Artifact UI 預覽、即時落盤、子代理 `inherit` 模式）（`machine_rules/sandbox.md`、`install.sh`、`install.bat`、README） | 執行環境與雲端沙盒架構 |

---

## 四、新增 coding agent 的步驟

1. 第一節加一列：代號、工具、全域規則位置、官方文件入口。
2. 第二節每張表加一欄；查不到的功能填「—」，只有間接來源就標「⚠」。
3. 第三節逐條檢查：新工具讀不讀得到 `AGENTS.md`、會不會被其他檔名蓋掉。
4. 改 `install.bat`、`install.sh`，多安裝一個目的地（安裝前備份的規定不變）。
5. 更新 README「各工具自動讀取的規則檔」、`global_rules.md` 開頭的安裝位置。
6. 同步更新 `docs/verification_sources.md` 的來源與查證日。

---

## 五、Harness 差異與補強：讓其他 agent 接近 Claude Code 體驗

### 5-0 一句話目的

使用者以 Claude Code 的 Vibe Coding 體驗為基準（只用白話講需求，不記 `/plan`、`/grill-me`、`/goal` 等指令）；其他 agent 缺的不是模型能力，而是 harness 沒有主動觸發的機制，所以一律用「**規則強制點名提問卡片工具＋卡片整合題目（規劃方案、自我迴圈驗證、動態子代理／EGM）**」取代手動打指令。

### 5-1 落差表

| 落差 | Claude Code（基準） | 其他 agent 常見表現 | 補強做法（免記指令，全靠提問卡片與規則） |
|---|---|---|---|
| 主動提問與規劃 | 動手前跳選擇題卡片，先給計畫等核准 | 直接改檔，或只在對話裡問一句 | 規則開頭改為獨立「動手前硬門檻（未跳圖卡禁寫／改／刪檔）」：收緊免問為明確白名單、禁止「自認小改／只有一種解法」跳過，並規定「禁寫冒號引導結尾句，背景講完同回合直接呼叫工具」（`ask_question`／`AskUserQuestion`／`question`／`request_user_input`）；Codex 一般模式由安裝腳本啟用 `default_mode_request_user_input`；Antigravity 開發機／通用機另裝 `Stop` Hook（`ag_stop_card_guard.py`）自動拉回補發 |
| 選項品質 | 標題＋說明＋優缺點 | 只有簡短名詞，缺決策資訊 | 固定選項格式：首項標 `(Recommended)`，每項寫「方案 — 白話做法、優缺點」 |
| 自我迴圈驗證 | 會主動跑測試並修到過 | 傾向「看起來完成」就交差 | 提問卡片必問「② 自我迴圈驗證方式」；任務開頭寫驗收標準，改完自動跑驗證修到過（最多兩次）並附輸出 |
| 子代理與流程調度 | 大任務適時分工或獨立審查 | 不主動派，或亂派小任務浪費額度 | AI 先判斷任務是否合適（大範圍查檔、改後唯讀審查、高風險變更），合適時在卡片動態加問「③ 是否派子代理」（並於大型平行任務提示可指定 `/swarm`）；觸及設計定案／審查時動態加問「④ 是否啟動 EGM（預設略過）」 |
| 記憶沉澱 | 被糾正時自動記下回饋 | 不會自動記；要人提醒 | 除錯後先提案，經同意於任務收尾時寫入專案 `AGENTS.md`（已知的坑置於最末尾維持快取） |
| 規則遵循 | 長規則也能抓到重點 | 規則一長就漏看（各家都會，見 `ai_agent_engineering.md` 第五節） | 規則 200 行內且 < 24,000 bytes、提問卡片規則放最開頭 |

### 5-2 五個補強做法

| 對策 | 做法 | 為什麼有效 | 成本 |
|---|---|---|---|
| 1. 提問卡片取代背指令 | 直接講白話需求（不打 `/plan`、`/grill-me`）；規則強制動手前呼叫 `ask_question`／`AskUserQuestion`／`question`／`request_user_input` | 維持 Vibe Coding 體驗，不用記各家指令，模型也有明確工具可呼叫 | 幾行規則 |
| 2. 卡片整合「規劃＋迴圈驗證＋動態子代理／EGM」 | 卡片必問「① 規劃與影響檔案」「② 自我迴圈驗證方式」；任務合適時動態加問「③ 是否派子代理分工／審查」「④ 是否啟動 EGM（預設略過）」 | 一張卡片同時對齊做什麼、怎麼驗收、要不要派子代理或啟用 EGM；不合適時不多問，避免核准疲勞 | 幾行規則 |
| 3. 固定選項格式 | 首項標 `(Recommended)`，每項寫「方案 — 白話做法、優缺點」 | 決策資訊不靠模型臨場發揮 | 幾行規則 |
| 4. 自我迴圈驗證到底 | 開頭寫「怎樣算做完」，改完自動跑驗證、沒過自己修（最多 2 次） | 把「感覺完成」變成自動閉環檢查 | 一次設定 |
| 5. 經驗沉澱先提案 | 只補讀程式碼推斷不出的坑，經同意於任務收尾時寫入 | 規則不會越長越失焦，且不破壞當下對話快取 | 每次一行 |

> 核心原則：**把指令藏進提問卡片裡**。使用者只負責講需求與點選卡片，規劃、子代理派工與自我迴圈驗證都由 AI 在卡片中主動提出（各家內建指令僅留本表 2-2 節備查）。

### 5-3 提問卡片：四家規格差異

| 項目 | Claude Code | Antigravity | Codex | OpenCode |
|---|---|---|---|---|
| 工具名稱 | `AskUserQuestion`（已查證官方） | `ask_question` | `request_user_input` | `question` |
| 單選／複選 | `multiSelect` | `is_multi_select` | 支援選項清單選擇 | 原生支援 |
| 自由填寫 | 原生 | 原生自動附 write-in 與 Submit／Skip | 支援自訂輸入 | 原生 |
| 選項結構 | `label`＋`description` 兩欄 | **本機實測為單一字串陣列**，沒有獨立 `description`；系統預設要求選項寫成使用者的直接回答，所以要靠規則要求附上白話優缺點 | 具標題、說明與選項清單 | `label`＋`description` |
| 推薦標示 | 第一項加 `(Recommended)` | 系統提示要求第一項加 `(Recommended)` | 第一項加 `(Recommended)` | 第一項加 `(Recommended)` |

#### 5-3-1 Claude Code／OpenCode 的選項寫法

```json
{
  "question": "1. 要用哪種方式修改設定模組（預計影響 config.py、loader.py、main.py）？",
  "header": "規劃方案",
  "multiSelect": false,
  "options": [
    {
      "label": "JSON 檔 (Recommended)",
      "description": "免安裝資料庫、可直接用記事本看，適合單機小工具"
    },
    {
      "label": "SQLite",
      "description": "支援大量資料查詢，但無法直接用記事本編輯"
    }
  ]
}
```

#### 5-3-2 Antigravity 的選項寫法（多檔案任務動態三題範例）

沒有獨立說明欄，所以**把說明寫進同一個字串**；當任務牽連多檔案且適合子代理時，一次問齊三題：

```json
{
  "questions": [
    {
      "question": "1. 規劃方案與影響檔案（預計修改 config.py、loader.py、main.py 共 3 檔）？",
      "is_multi_select": false,
      "options": [
        "(Recommended) JSON 檔 — 免安裝資料庫、可直接用記事本看，適合單機小工具",
        "SQLite — 支援大量資料查詢，但無法直接用記事本編輯"
      ]
    },
    {
      "question": "2. 自我迴圈驗證方式？",
      "is_multi_select": false,
      "options": [
        "(Recommended) 自動跑 py_compile 與 pytest 修到全過 — 改完自動執行測試，失敗自動修（最多 2 次），全過才回報",
        "只檢查語法，畫面由我手動實測 — AI 先跑 py_compile，UI 操作交給我確認"
      ]
    },
    {
      "question": "3. 是否使用子代理（本任務涉及跨檔案修改，適合改完後獨立挑錯）？",
      "is_multi_select": false,
      "options": [
        "(Recommended) 改完後派 1 個唯讀子代理挑錯審查 — 主對話負責改檔，完成後派 research 子代理檢查有無漏改或邊界錯誤（亦可調用 OpenCode CLI 並自選模型）",
        "不使用子代理 — 全程留在主對話處理，最省 token"
      ]
    }
  ]
}
```

### 5-4 記憶機制差異

| 項目 | Claude Code | Antigravity | Codex | OpenCode |
|---|---|---|---|---|
| 背景自動記憶 | 有，只存四類：使用者資訊、被糾正的回饋、專案背景、外部參照；**除錯修法通常不存** | 無 | `~/.codex/memories_*.sqlite` | 無 |
| 手動學習 | `/memory`（檢視與編輯） | `/learn`（先提案、核准後寫入） | 無對應 | 無對應 |
| 跨工具／跨電腦 | `~/.claude/projects/` 只在本機，不隨 Git 同步 | 寫進專案 `AGENTS.md` 才各家都讀、才同步 | 同左 | 同左 |

### 5-5 驗收：四個固定任務（不打任何指令，只講白話需求）

開新對話，直接用白話輸入需求（不打 `/plan`、`/grill-me`），記錄結果：

| 任務 | 預期表現 | 實測結果 |
|---|---|---|
| A：需求模糊的新功能 | 跳卡片（必問 ① 規劃方案、② 自我迴圈驗證），不先改檔 | |
| B：已明確指定的小修改（如改一句文字） | 不跳卡片，直接改檔並跑驗證 | |
| C：有兩種做法的單檔小修改 | 跳卡片（問 ① 規劃方案、② 自我迴圈驗證；不適合子代理故不問第 ③ 題） | |
| D：牽連 3 個以上檔案或大改動的任務 | 跳卡片（一次問齊 ① 規劃與影響檔案清單、② 自我迴圈驗證、③ 是否派子代理分工／審查） | |

判斷：A、C、D 若沒跳卡片就直接改檔，才需要評估用 Hook 強制（開發機與通用機的 Antigravity 已安裝 `ag_stop_card_guard.py` Stop Hook 自動偵測拉回補發）。

> 提問規則全文見 `global_rules.md` 開頭；經驗沉澱、停損、維護節奏見 `docs/rule_maintenance_sop.md` 第六～八節；每月重新查證步驟見 `docs/verification_sources.md` 第七節。

---

## 六、查證來源

**Claude Code**
- [Memory（CLAUDE.md、AGENTS.md、rules、auto memory）](https://code.claude.com/docs/en/memory)
- [Large codebases & permissions.deny paths](https://code.claude.com/docs/en/large-codebases)
- [Commands](https://code.claude.com/docs/en/commands)
- [Permission modes／Plan mode](https://code.claude.com/docs/en/permission-modes)
- [Agent SDK approvals（AskUserQuestion）](https://code.claude.com/docs/en/agent-sdk/approvals)
- [Troubleshooting（safeguards、/rewind）](https://code.claude.com/docs/en/troubleshooting)
- [Skills](https://code.claude.com/docs/en/skills)
- [Output styles](https://code.claude.com/docs/en/output-styles)
- [Hooks](https://code.claude.com/docs/en/hooks-guide)
- [Plugins](https://code.claude.com/docs/en/plugins)
- [Subagents](https://code.claude.com/docs/en/sub-agents)
- [Security（/sandbox）](https://code.claude.com/docs/en/security)
- [Changelog（v2.1.314～v2.1.330 等）](https://code.claude.com/docs/en/changelog)

**Antigravity**
- [Rules](https://antigravity.google/docs/rules/)
- [Slash commands（/plan、/grill-me、/learn）](https://antigravity.google/docs/slash-commands/)
- [/grill-me](https://antigravity.google/docs/commands/grill-me/)
- [/agy-customizations](https://antigravity.google/docs/commands/agy-customizations/)
- [/learn（Schema check、learning_proposal.md）](https://antigravity.google/docs/commands/learn/)
- [CLI Reference（/context、/skills reload）](https://antigravity.google/docs/cli/reference/)
- [Models & Thinking Level](https://antigravity.google/docs/models/)
- [Antigravity agent（模型正式名稱）](https://ai.google.dev/gemini-api/docs/antigravity-agent)
- [Gemini 3.8 Flash 上線公告](https://antigravity.google/blog/gemini-3-8-flash-in-google-antigravity/)
- [Gemini 4 Carbon 上線公告](https://antigravity.google/blog/gemini-4-carbon-in-google-antigravity/)
- [Agent skills](https://antigravity.google/docs/skills)
- [Plugins](https://antigravity.google/docs/plugins/)
- [Changelog（v2.28～v2.34.0、Dynamic Workflows、Gemini 4 Neon、Orchestrator (Neon)、MCP Apps）](https://antigravity.google/docs/changelog/)
- [Custom subagents](https://antigravity.google/docs/subagents)
- [Hooks](https://antigravity.google/docs/hooks)
- [Workflows to skills migration](https://antigravity.google/docs/migration/workflows-to-skills/)
- [CLI: Managing conversations](https://antigravity.google/docs/cli/conversations/)
- [Interactive UI Workflows（ask_question）](https://dev.to/googleai/elevating-antigravity-agent-skills-part-1-interactive-ui-workflows-6l2)
- [Gemini CLI 轉換公告](https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/)

**Codex**
- [Custom instructions with AGENTS.md](https://developers.openai.com/codex/guides/agents-md/)
- [Agent Skills](https://developers.openai.com/codex/skills/)
- [Config reference (`config.toml`)](https://developers.openai.com/codex/config-reference/)

**OpenCode（V2 官方文件，2026-11-22 複查）**
- [Instructions](https://opencode.ai/v2/docs/instructions/)
- [Config](https://opencode.ai/v2/docs/config/)
- [Permissions](https://opencode.ai/v2/docs/permissions/)
- [Agents](https://opencode.ai/v2/docs/agents/)
- [Commands](https://opencode.ai/v2/docs/commands/)
- [Skills](https://opencode.ai/v2/docs/skills/)
- [Plugins](https://opencode.ai/v2/docs/plugins/)
- [V1 to V2 migration](https://opencode.ai/v2/docs/migrate-v1/)
