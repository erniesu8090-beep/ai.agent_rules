# Coding agent 功能對照表

> 範圍：只收**寫程式用的 coding agent**（目前：Claude Code、Antigravity、Codex、OpenCode）；聊天介面（claude.ai、Gemini Apps、ChatGPT 網頁版）不在本表。
> 用途：設計 `global_rules.md`、`templates/` 規則時的依據。各家工具常改版，**每一列都有查證日期**；最後一次全面查證超過 1 個月就要重新查（步驟見 README「coding agent 功能查證」）。
> 最後全面查證：2026-10-24
> 標記：「—」查無對應功能；「⚠」只有第三方來源或未查證。

## 一、目前納入的 coding agent

| 代號 | 工具 | 全域規則安裝位置（`install.bat`／`install.sh`） | 官方文件入口 |
|---|---|---|---|
| `claude` | Claude Code（CLI、桌面 App、IDE） | `~/.claude/CLAUDE.md`；開發機另設 `~/.claude/settings.json`（兩者都讀） | https://code.claude.com/docs/en/ |
| `antigravity` | Antigravity（App、IDE、CLI `agy`） | `~/.gemini/GEMINI.md` | https://antigravity.google/docs/ |
| `codex` | OpenAI Codex（CLI `codex`、桌面 App、IDE） | `~/.codex/AGENTS.md` | https://developers.openai.com/codex/ |
| `opencode` | OpenCode（CLI `opencode`、TUI、桌面 App） | `~/.config/opencode/AGENTS.md` | https://opencode.ai/docs/ |

> Gemini CLI：個人帳號 2026-06-18 起停止回應，後繼者為 Antigravity CLI（`agy`）。⚠ 只查到第三方報導，未找到 Google 官方公告。本表不收 Gemini CLI。

## 二、功能對照

新增 coding agent 時，在每張表加一欄（見第四節）。

### 規則檔（每次對話都載入）

| 功能 | Claude Code | Antigravity | Codex | OpenCode | 查證日期 |
|---|---|---|---|---|---|
| 全域規則 | `~/.claude/CLAUDE.md`；組織 managed CLAUDE.md | `~/.gemini/AGENTS.md`、`~/.gemini/GEMINI.md`、`~/.gemini/config/AGENTS.md`、`~/.gemini/config/GEMINI.md` | `~/.codex/AGENTS.override.md` 或 `~/.codex/AGENTS.md` | `~/.config/opencode/AGENTS.md`（若不存在則回退讀 `~/.claude/CLAUDE.md`） | 2026-10-24 |
| 專案／目錄規則 | `CLAUDE.md`、`.claude/CLAUDE.md`、`CLAUDE.local.md`，目前資料夾與所有上層全部串接；子資料夾的檔案讀到該資料夾檔案時才載入 | 任一目錄的 `AGENTS.md`、`GEMINI.md`，或 `<dir>/.agents/` 底下；累加，衝突時較具體的目錄優先 | 從 Git／專案根目錄往下到目前資料夾，依序合併 `AGENTS.override.md` 或 `AGENTS.md` | 從目前資料夾往上找專案根目錄的 `AGENTS.md`；也可在 `opencode.json` 的 `instructions` 指定 | 2026-10-24 |
| 讀 `AGENTS.md` | v2.1.277 起原生讀取，但路徑上有 `CLAUDE.md`／`.claude/CLAUDE.md`／`CLAUDE.local.md` 時**全部跳過、不提示**（`~/.claude/CLAUDE.md` 不算）。可在 `~/.claude/settings.json` 設 `instructionFiles: "claude-md-and-agents-md"` 改成兩者都讀（專案層設定無效） | 原生常駐 | 原生常駐（預設不讀 `CLAUDE.md`，除非在 `config.toml` 設 `project_doc_fallback_filenames`） | 原生常駐（無 `AGENTS.md` 時回退讀 `CLAUDE.md`；有 `AGENTS.md` 時不讀 `CLAUDE.md`） | 2026-10-24 |
| AI 看得出載入了哪些規則檔 | 是：每個規則檔附完整路徑交給 AI（「Contents of <路徑>」），AI 可自行比對有沒有讀到 `AGENTS.md`；人工確認用 `/memory` | ⚠ 未查證 | `/status` 可檢視目前載入設定 | ⚠ 未查證 | 2026-10-24 |
| 往上層找規則的範圍 | 一直到磁碟根目錄 | 只到 Git 倉庫根目錄（實測） | 只到 Git／專案根目錄 | 只到 Git／專案根目錄 | 2026-10-24 |
| 引用其他檔 | `@path`，展開嵌入，最多 4 層；程式碼區塊內不展開 | `@[label](path)` 展開嵌入；`@filename` 只轉成絕對路徑 | — | `opencode.json` 的 `"instructions": ["path/to/file.md"]` | 2026-10-24 |
| 模組化規則 | `.claude/rules/*.md`，遞迴掃描；frontmatter `paths` 限定檔案 | `.agents/rules/*.md`，只掃第一層（子資料夾要 `.agents/rules.json`）；`trigger` 必填（`always_on`／`model_decision`／`glob`／`manual`），缺少或寫錯**靜默丟棄** | 子目錄放 `AGENTS.md`（注：`~/.codex/rules/*.rules` 是指令執行的白名單規則，不是文字規則） | `opencode.json` 的 `instructions` 支援 glob 萬用字元 | 2026-10-24 |
| 容量限制 | 建議每檔 200 行內 | 每檔 24,000 bytes（含展開後），超過截斷；常駐規則合計 20,000 tokens，超過時最大的檔改成指標 | 預設合計 32 KiB（`project_doc_max_bytes = 32768`），超過靜默截斷 | 無硬性上限（依模型 context window） | 2026-10-24 |
| 規則自我檢查 | `/doctor prompt-audit`（v2.1.283+）：找過時、矛盾、引用不存在的內容，只出報告 | — | — | — | 2026-10-19 |

### 按需載入與流程

| 功能 | Claude Code | Antigravity | Codex | OpenCode | 查證日期 |
|---|---|---|---|---|---|
| Skills | `~/.claude/skills/`、`.claude/skills/`；`/名稱` 或依描述自動 | 工作區 `.agents/skills/`；全域 App/IDE `~/.gemini/config/skills/`，CLI `~/.gemini/antigravity-cli/skills/`；`/名稱` 或自動 | 工作區 `.agents/skills/`；全域 `~/.codex/skills/`、`~/.agents/skills/`；`$名稱` 或依描述自動 | 工作區 `.opencode/skills/`、`.claude/skills/`、`.agents/skills/`；全域 `~/.config/opencode/skills/`；依描述自動 | 2026-10-24 |
| 手動流程 | Skill 設 `disable-model-invocation: true`；舊 `.claude/commands/` 仍可用 | Workflows 2026-10-19 起停止運作，用 `/migrate-workflows` 轉成 Skills | 以 `$skill-name` 點名觸發 Skill | `.opencode/commands/*.md`、全域 `~/.config/opencode/commands/*.md`；`/名稱` 觸發 | 2026-10-24 |
| 子代理 | `~/.claude/agents/`、`.claude/agents/` | `.agents/agents/<name>.md`、全域 `~/.gemini/config/agents/` | `.toml` 子代理設定與內建平行子代理 | `.opencode/agents/`、全域 `~/.config/opencode/agents/` 或 `opencode.json`；`@名稱` 呼叫 | 2026-10-24 |
| 回應風格 | Output styles：`~/.claude/output-styles`、`.claude/output-styles`；`/output-style` | ⚠ 導覽列有「Personas」頁，未查證 | — | 透過自訂 Agent prompt 切換 | 2026-10-24 |

### 強制執行與記憶

| 功能 | Claude Code | Antigravity | Codex | OpenCode | 查證日期 |
|---|---|---|---|---|---|
| Hooks | `settings.json`；`PreToolUse` 可阻擋 | 工作區 `.agents/hooks.json`、全域 `~/.gemini/config/hooks.json`；`PreToolUse` 可 `deny` | `config.toml`／`hooks.json`；另 `~/.codex/rules/*.rules` 可設指令 `prefix_rule` 放行或阻擋 | 透過 `.opencode/plugins/`（`@opencode-ai/plugin`）攔截 `tool.execute.before` 等事件 | 2026-10-24 |
| 自動記憶 | `~/.claude/projects/<專案>/memory/` | — | `~/.codex/memories_*.sqlite` | 透過外掛（如 `claude-mem`） | 2026-10-24 |
| 附加系統提示 | `--append-system-prompt` | — | `-c developer_instructions=...` | `opencode.json` 的 `instructions` | 2026-10-24 |
| 互動式選擇題卡片工具 | `AskUserQuestion`（v2.0.21+；`options` 含獨立 `label` 與 `description` 欄位，支援 `multiSelect`） | `ask_question`（`options` 為單純字串陣列無獨立 `description` 欄位，支援 `is_multi_select`） | `request_user_input`（預設於 Plan mode 啟用；一般模式需設 `[features] default_mode_request_user_input = true`） | `question`（支援 `header`、單複選與自訂輸入；可在 `opencode.json` 設 `"permission": { "question": "allow" }`） | 2026-10-25 |

## 三、依賴本表的規則

工具改版、上表某一列變了，就檢查對應的規則要不要改。新增依賴工具行為的規則時，補一列。

| 規則（所在位置） | 依據的列 |
|---|---|
| 安裝腳本設定「兩者都讀」；自己的專案不建 `CLAUDE.md`；fork 的專案保留 `CLAUDE.md`（`global_rules.md` 第 5 節、`install.bat`、`install.sh`、README） | 讀 `AGENTS.md`；Antigravity 與 Codex 預設不讀 `CLAUDE.md`，OpenCode 有 `AGENTS.md` 時不讀 `CLAUDE.md` |
| Claude Code 開新對話時自行比對有沒有讀到 `AGENTS.md`（`global_rules.md` 第 5 節「確認方法」） | AI 看得出載入了哪些規則檔 |
| 工作區規則只對 Claude Code 有效（`global_rules.md` 第 5 節、`AGENTS.md` 業務規則） | 往上層找規則的範圍（Antigravity、Codex、OpenCode 只到 Git 根目錄） |
| 不建 `.agents/rules/`、`.claude/rules/`，只用 `AGENTS.md`（`global_rules.md` 第 5 節） | 模組化規則（四家格式不互通，唯有 `AGENTS.md` 四家原生支援） |
| `global_rules.md` 200 行內（`AGENTS.md` 撰寫原則） | 容量限制（Antigravity 單檔 24KB、Codex 合計 32KB） |
| 安裝位置（`install.bat`、`install.sh`、`global_rules.md` 開頭） | 全域規則（`~/.claude/CLAUDE.md`、`~/.gemini/GEMINI.md`、`~/.codex/AGENTS.md`、`~/.config/opencode/AGENTS.md`） |
| 提問時強制呼叫互動式選擇題工具，且每個選項字串須寫明「`方案名稱 — 白話做法、優缺點與影響`」（`global_rules.md` 開頭與第 4 節、`doc/interactive_question_rules.md`） | 互動式選擇題卡片工具（Antigravity `ask_question` 的 `options` 僅為字串陣列，無獨立 `description` 欄位） |

## 四、新增 coding agent

1. 第一節加一列：代號、工具、全域規則位置、官方文件入口。
2. 第二節每張表加一欄；查不到的功能填「—」。
3. 第三節逐條檢查：新工具讀不讀得到 `AGENTS.md`、會不會被其他檔名蓋掉。
4. 改 `install.bat`、`install.sh`，多安裝一個目的地（安裝前備份的規定不變）。
5. 更新 README「各工具自動讀取的規則檔」、`global_rules.md` 開頭的安裝位置。

## 五、查證來源

**Claude Code**
- [Memory（CLAUDE.md、AGENTS.md、rules、auto memory）](https://code.claude.com/docs/en/memory)
- [Skills](https://code.claude.com/docs/en/skills)
- [Output styles](https://code.claude.com/docs/en/output-styles)
- [Hooks](https://code.claude.com/docs/en/hooks-guide)
- [Subagents](https://code.claude.com/docs/en/sub-agents)

**Antigravity**
- [Rules](https://antigravity.google/docs/rules)
- [Agent skills](https://antigravity.google/docs/skills)
- [Custom subagents](https://antigravity.google/docs/subagents)
- [Hooks](https://antigravity.google/docs/hooks)
- [Workflows to skills migration](https://antigravity.google/docs/migration/workflows-to-skills/)
- [CLI: Managing conversations](https://antigravity.google/docs/cli/conversations/)
- ⚠ Gemini CLI 停止服務（第三方）：[The New Stack](https://thenewstack.io/gemini-cli-antigravity-replacement/)

**Codex**
- [Custom instructions with AGENTS.md](https://developers.openai.com/codex/guides/agents-md/)
- [Agent Skills](https://developers.openai.com/codex/skills/)
- [Config reference (`config.toml`)](https://developers.openai.com/codex/config-reference/)

**OpenCode**
- [Rules (`AGENTS.md`)](https://opencode.ai/docs/rules/)
- [Agent Skills](https://opencode.ai/docs/skills/)
- [Agents](https://opencode.ai/docs/agents/)
- [Commands](https://opencode.ai/docs/commands/)
- [Plugins & Hooks](https://opencode.ai/docs/plugins/)
