# Coding agent 功能對照表

> 整併自：原 coding_agent_features.md、lightweight_llm_improvement.md、interactive_question_rules.md（2026-10-31 併入第五節）；原始版本已移至資源回收筒或可查 Git 歷史。
> 範圍：只收**寫程式用的 coding agent**（Claude Code、Antigravity、Codex、OpenCode）；聊天介面（claude.ai、Gemini Apps、ChatGPT 網頁版）不在本表。
> 用途：設計 `global_rules.md`、`templates/` 規則與安裝腳本的依據。**每一列都有查證日期**；最後一次全面查證超過 1 個月就要重新查。
> 最後全面查證：2026-10-28（最後整併：2026-10-31）
> 標記：「—」查無對應功能；「⚠」只有第三方來源、本機實測或尚未查證。

---

## 一、納入的 coding agent

| 代號 | 工具 | 全域規則安裝位置 | 官方文件 |
|---|---|---|---|
| `claude` | Claude Code（CLI、桌面 App、IDE） | `~/.claude/CLAUDE.md`；開發機另設 `~/.claude/settings.json`（兩者都讀＋`permissions.deny`） | https://code.claude.com/docs/en/ |
| `antigravity` | Antigravity（App、IDE、CLI `agy`） | `~/.gemini/GEMINI.md` | https://antigravity.google/docs/ |
| `codex` | OpenAI Codex（CLI `codex`、桌面 App、IDE） | `~/.codex/AGENTS.md` | https://developers.openai.com/codex/ |
| `opencode` | OpenCode V2（TUI、桌面 App、Web） | `~/.config/opencode/AGENTS.md`；另設 `~/.config/opencode/opencode.jsonc` | https://opencode.ai/v2/docs/ |

> Gemini CLI 自 2026-06-18 起對 AI Pro、AI Ultra 與免費個人帳號停止服務，後繼者為 Antigravity CLI（`agy`）；企業授權與付費 API Key 不受影響（已查證，2026-05-19 Google 官方部落格）。本表不收 Gemini CLI。

---

## 二、功能對照

### 2-1 規則檔（每次對話都載入）

| 功能 | Claude Code | Antigravity | Codex | OpenCode | 查證日 |
|---|---|---|---|---|---|
| 全域規則 | `~/.claude/CLAUDE.md`；組織 managed CLAUDE.md | `~/.gemini/AGENTS.md`、`~/.gemini/GEMINI.md`、`~/.gemini/config/AGENTS.md`、`~/.gemini/config/GEMINI.md`；模組化 `~/.gemini/config/rules/*.md`（需 frontmatter）；CLI 另讀 `~/.gemini/antigravity-cli/rules/*.md` | `~/.codex/AGENTS.override.md` 或 `~/.codex/AGENTS.md` | `~/.config/opencode/AGENTS.md`（系統層另讀 `/etc/opencode`、`%ProgramData%\opencode`） | 2026-10-28 |
| 專案／目錄規則 | `CLAUDE.md`、`.claude/CLAUDE.md`、`CLAUDE.local.md`，目前資料夾與所有上層全部串接；子資料夾的檔案讀到該資料夾檔案時才載入 | 任一目錄的 `AGENTS.md`、`GEMINI.md`，或 `<dir>/.agents/` 底下；累加，衝突時較具體的目錄優先 | 從 Git／專案根目錄往下到目前資料夾，依序合併 `AGENTS.override.md` 或 `AGENTS.md` | 任一目錄的 `AGENTS.md`，由遠而近合併；子資料夾的檔案讀到該資料夾時才載入 | 2026-10-28 |
| 讀 `AGENTS.md` | v2.1.277 起原生讀取，但路徑上有 `CLAUDE.md`／`.claude/CLAUDE.md`／`CLAUDE.local.md` 時**全部跳過、不提示**（`~/.claude/CLAUDE.md` 不算）。可在 `~/.claude/settings.json` 設 `instructionFiles: "claude-md-and-agents-md"` 改成兩者都讀（專案層無效；v2.1.285 前外掛 ID 為 `agents-md@builtin`，v2.1.285 起亦支援 `cc-plugin-agents-md@builtin`，或用 `/config`） | 原生常駐 | 原生常駐（預設不讀 `CLAUDE.md`，除非在 `config.toml` 設 `project_doc_fallback_filenames`） | **唯一格式**：只讀 `AGENTS.md`，不讀 `CLAUDE.md`（V2 官方明訂無 fallback） | 2026-10-28 |
| AI 看得出載入哪些規則 | 是：每個規則檔附完整路徑（「Contents of <路徑>」），可自行比對；人工確認用 `/memory`（需 v2.1.280+ 才會列出直接讀入的 `AGENTS.md`） | ⚠ 未查證 | `/status` 可檢視目前載入設定 | ⚠ 未查證；查無 `/memory` 類指令，靠開新對話自行比對 | 2026-10-28 |
| 往上找規則的範圍 | 一直到磁碟根目錄 | 只到工作區根目錄（workspace root，不會超過）；2026-10-10 實測開啟 Git 倉庫時只到該倉庫根目錄 | 只到 Git／專案根目錄 | 從工作區往上找到**家目錄**；工作區在家目錄以外時只到專案根目錄（`D:\AI_Workspace` 屬此類，要另用 `instructions` 指定） | 2026-10-28 |
| 引用其他檔 | `@path`，展開嵌入，最多 4 層；程式碼區塊內不展開 | `@[label](path)` 展開嵌入；`@filename` 只轉成絕對路徑 | — | 不支援 `@` 展開；改用 `opencode.jsonc` 的 `instructions`（相對路徑、glob、`~/`、絕對路徑、HTTP(S)） | 2026-10-28 |
| 模組化規則 | `.claude/rules/*.md`，遞迴掃描；frontmatter `paths` 限定檔案 | 工作區 `.agents/rules/*.md`、全域 `~/.gemini/config/rules/*.md`（CLI 為 `~/.gemini/antigravity-cli/rules/*.md`），只掃第一層；`trigger` 必填（`always_on`／`model_decision`／`glob`／`manual`），缺少或寫錯**靜默丟棄** | 子目錄放 `AGENTS.md`（註：`~/.codex/rules/*.rules` 是指令執行的白名單規則，不是文字規則） | 巢狀 `AGENTS.md`（按需載入）＋ `instructions` 陣列 | 2026-10-28 |
| 容量限制 | 建議每檔 200 行內；隨需載入規則（子資料夾 `CLAUDE.md`、`paths` 限定規則）v2.1.309 起單檔有字元上限（200K 視窗為 40,000 字元），超過只取開頭 | 每檔 24,000 bytes（含展開後），超過截斷；常駐規則合計 20,000 tokens，超過時最大的檔改成指標 | 預設合計 32 KiB（`project_doc_max_bytes = 32768`），超過靜默截斷 | —（查無上限，只受模型上下文限制） | 2026-10-28 |
| 規則自我檢查 | `/doctor prompt-audit`（v2.1.283+）：找過時、矛盾、引用不存在的內容，只出報告 | — | — | — | 2026-10-28 |

### 2-2 按需載入與流程

| 功能 | Claude Code | Antigravity | Codex | OpenCode | 查證日 |
|---|---|---|---|---|---|
| 規劃與訪談 | Plan mode（見 permission-modes 文件） | `/plan`（訪談後產生可審閱的實作計畫）、`/grill-me`（一次一題、推薦答案排第一）；可組合 `/plan /grill-me 任務` | Plan mode（預設啟用 `request_user_input`） | 內建 `plan` agent（唯讀，不改專案檔；TUI 切換）＋自訂 `/plan` 指令 | 2026-10-28 |
| Skills | `~/.claude/skills/`、`.claude/skills/`；`/名稱` 或依描述自動 | 工作區 `.agents/skills/`；全域 App/IDE `~/.gemini/config/skills/`，CLI `~/.gemini/antigravity-cli/skills/`；`/名稱` 或自動 | 工作區 `.agents/skills/`；全域 `~/.codex/skills/`、`~/.agents/skills/`；`$名稱` 或依描述自動 | `~/.config/opencode/skills/`、`.opencode/skills/<id>/SKILL.md`；**相容讀** `~/.claude/skills/`、`.claude/skills/`、`.agents/skills/`；依描述自動或 `@skill-id` | 2026-10-28 |
| 手動流程 | Skill 設 `disable-model-invocation: true`；舊 `.claude/commands/` 仍可用 | 舊 Workflows 2026-10-19 起停止運作，用 `/migrate-workflows` 轉成 Skills（官方預告新系統另行公布，待追蹤） | 以 `$skill-name` 點名觸發 Skill | `.opencode/commands/*.md` 或 `commands` 設定（可指定 `agent`／`model`；`subagent: true` 背景執行） | 2026-10-28 |
| 子代理 | `~/.claude/agents/`、`.claude/agents/` | `.agents/agents/<name>.md`、全域 `~/.gemini/config/agents/` | `.toml` 子代理設定與內建平行子代理 | `~/.config/opencode/agents/`、`.opencode/agents/<name>.md`；`mode: subagent` | 2026-10-28 |
| 回應風格 | Output styles：`~/.claude/output-styles`、`.claude/output-styles`；`/output-style` | ⚠ 導覽列有「Personas」頁，未查證 | — | —（自訂 agent 的 `system` 可換系統提示） | 2026-10-28 |

### 2-3 強制執行與記憶

| 功能 | Claude Code | Antigravity | Codex | OpenCode | 查證日 |
|---|---|---|---|---|---|
| Hooks | `settings.json`；`PreToolUse` 可阻擋 | 工作區 `.agents/hooks.json`、全域 `~/.gemini/config/hooks.json`；`PreToolUse` 可 `deny` | `config.toml`／`hooks.json`；另 `~/.codex/rules/*.rules` 可設指令 `prefix_rule` 放行或阻擋 | 無宣告式 hooks；用 Plugin（`~/.config/opencode/plugins/`、`.opencode/plugins/*.ts`） | 2026-10-28 |
| 拒絕讀取特定路徑 | `settings.json` 的 `permissions.deny`（例：`Read(./**/<資料夾>/**)`，相對路徑以啟動資料夾為起點；跨資料夾可能需改用 `//` 絕對路徑，⚠ 尚待實測），只擋內建讀檔工具（對 Bash 繞道效力有限）；`.claudeignore` 於 2026-10-22 實測無效 | — | —（沙盒管寫入範圍，無宣告式讀檔黑名單） | `opencode.jsonc` 的 `permissions`：`{action:"read", resource:"*<資料夾>*", effect:"deny"}`（`*` 會跨 `/`）；`external_directory` 可管工作區外的路徑 | 2026-10-28 |
| 自動記憶 | `~/.claude/projects/<專案>/memory/MEMORY.md`（前 200 行／25KB 自動載入；只存使用者資訊、被糾正的回饋、專案背景、外部參照，除錯修法通常不存；只存該機器，不隨 Git 同步） | —（無背景自動記憶；僅手動 `/learn`，先提案、核准後寫入） | `~/.codex/memories_*.sqlite` | —（無背景自動記憶） | 2026-10-28 |
| 附加系統提示 | `--append-system-prompt` | — | `-c developer_instructions=...` | agent 的 `system` 欄位（會取代該 agent 的基礎系統提示） | 2026-10-28 |
| 互動式選擇題卡片 | `AskUserQuestion`（⚠ v2.0.21+ 為第三方來源；原生單選、複選 `multiSelect`、自由填寫；選項分 `label` 與 `description`） | `ask_question`（官方確認支援單選、複選 `is_multi_select`、自動附自由填寫；本機實測 `options` 為單一字串陣列，做法與優缺點要寫在同一字串） | `request_user_input`（預設於 Plan mode 啟用；一般模式需設 `[features] default_mode_request_user_input = true`） | `question`（原生單選／複選／自由填寫；選項有 `label` 與 `description`） | 2026-10-28 |

---

## 三、依賴本表的規則

工具改版、某一列變了，就檢查對應的規則要不要改。新增依賴工具行為的規則時，補一列。

| 規則（所在位置） | 依據的列 |
|---|---|
| 安裝腳本同時設定新舊外掛 ID「兩者都讀」；自己的專案不建 `CLAUDE.md`；fork 保留 `CLAUDE.md`（`global_rules.md` 第 5 節、`install.bat`、`install.sh`、README） | 讀 `AGENTS.md`；Antigravity、Codex 與 OpenCode V2 不讀 `CLAUDE.md` |
| Claude Code 開新對話自行比對有沒有讀到 `AGENTS.md`；`/memory` 需 v2.1.280+（`global_rules.md` 第 5 節、README） | AI 看得出載入了哪些規則檔 |
| 工作區規則要靠 `~/.config/opencode/opencode.jsonc` 的 `instructions` 指定才對 OpenCode 生效；四家都要遵守的規則放全域或專案（`global_rules.md` 第 5 節、`AGENTS.md`、README） | 往上層找規則的範圍、引用其他檔 |
| 安裝腳本建立 `opencode.jsonc`（`instructions` ＋ `permissions`），已存在只檢查（`install.bat`、`install.sh`、README） | 引用其他檔、拒絕讀取特定路徑 |
| 不建 `.agents/rules/`、`.claude/rules/`，只用 `AGENTS.md`（`global_rules.md` 第 5 節） | 模組化規則 |
| `global_rules.md` 200 行內（本倉庫 `AGENTS.md`） | 容量限制 |
| 安裝位置（`install.bat`、`install.sh`、`global_rules.md` 開頭） | 全域規則 |
| 資安防凍結阻擋讀取敏感專案與啟動資料夾限制（`global_rules.md` 第 8 節、`install.bat`、`install.sh`、README、`docs/claude_code_permissions_deny.md`） | 拒絕讀取特定路徑 |
| 免記指令全自動提問卡片：規劃／3 檔以上／跨檔案／單檔大改前強制呼叫選擇題卡片，整合「規劃方案＋自我迴圈驗證＋動態子代理」（`global_rules.md` 開頭與第 4、9 節、README、本表第五節） | 互動式選擇題卡片、子代理 |
| 除錯後篩選重要陷阱與漏掉的測試，先提案確認再補進專案 `AGENTS.md`，維持 10 條／200 行（`global_rules.md` 第 9 節、本表第五節） | 自動記憶、容量限制 |

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

使用者以 Claude Code 的 Vibe Coding 體驗為基準（只用白話講需求，不記 `/plan`、`/grill-me`、`/goal` 等指令）；其他 agent 缺的不是模型能力，而是 harness 沒有主動觸發的機制，所以一律用「**規則強制點名提問卡片工具＋卡片整合題目（規劃方案、自我迴圈驗證、動態子代理）**」取代手動打指令。

### 5-1 落差表

| 落差 | Claude Code（基準） | 其他 agent 常見表現 | 補強做法（免記指令，全靠提問卡片與規則） |
|---|---|---|---|
| 主動提問與規劃 | 動手前跳選擇題卡片，先給計畫等核准 | 直接改檔，或只在對話裡問一句 | 規則開頭強制點名工具（`ask_question`／`question`／`request_user_input`）：新規劃、修改 3 檔以上、跨檔案、單檔大改或有 2 種做法時，必跳卡片確認「① 規劃方案與影響檔案」 |
| 選項品質 | 標題＋說明＋優缺點 | 只有簡短名詞，缺決策資訊 | 固定選項格式：首項標 `(Recommended)`，每項寫「方案 — 白話做法、優缺點」 |
| 自我迴圈驗證 | 會主動跑測試並修到過 | 傾向「看起來完成」就交差 | 提問卡片必問「② 自我迴圈驗證方式」；任務開頭寫驗收標準，改完自動跑驗證修到過（最多兩次）並附輸出 |
| 子代理調度 | 大任務適時分工或獨立審查 | 不主動派，或亂派小任務浪費額度 | AI 先判斷任務是否合適（大範圍搜尋、平行改獨立檔、改完唯讀挑錯），合適時在卡片動態加問「③ 是否派子代理」；不合適時不問 |
| 記憶沉澱 | 被糾正時自動記下回饋 | 不會自動記；要人提醒 | 除錯後先提案，經同意才寫入專案 `AGENTS.md` |
| 規則遵循 | 長規則也能抓到重點 | 規則一長就漏看（各家都會，見 `ai_agent_engineering.md` 第五節） | 規則 200 行內、提問卡片規則放最開頭 |

### 5-2 五個補強做法

| 對策 | 做法 | 為什麼有效 | 成本 |
|---|---|---|---|
| 1. 提問卡片取代背指令 | 直接講白話需求（不打 `/plan`、`/grill-me`）；規則強制動手前呼叫 `ask_question`／`AskUserQuestion`／`question`／`request_user_input` | 維持 Vibe Coding 體驗，不用記各家指令，模型也有明確工具可呼叫 | 幾行規則 |
| 2. 卡片整合「規劃＋迴圈驗證＋動態子代理」 | 卡片必問「① 規劃與影響檔案」「② 自我迴圈驗證方式」；任務合適時動態加問「③ 是否派子代理分工／審查」 | 一張卡片同時對齊做什麼、怎麼驗收、要不要派子代理；不合適子代理時不多問，避免核准疲勞 | 幾行規則 |
| 3. 固定選項格式 | 首項標 `(Recommended)`，每項寫「方案 — 白話做法、優缺點」 | 決策資訊不靠模型臨場發揮 | 幾行規則 |
| 4. 自我迴圈驗證到底 | 開頭寫「怎樣算做完」，改完自動跑驗證、沒過自己修（最多 2 次） | 把「感覺完成」變成自動閉環檢查 | 一次設定 |
| 5. 經驗沉澱先提案 | 只補讀程式碼推斷不出的坑，經同意才寫入 | 規則不會越長越失焦 | 每次一行 |

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
        "(Recommended) 改完後派 1 個唯讀子代理挑錯審查 — 主對話負責改檔，完成後派 research 子代理檢查有無漏改或邊界錯誤",
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

判斷：A、C、D 若沒跳卡片就直接改檔，才需要評估用 Hook 強制。Hook 能否擋住「未核准就改檔」尚未查證，要先實測。

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
- [Subagents](https://code.claude.com/docs/en/sub-agents)
- [Security（/sandbox）](https://code.claude.com/docs/en/security)

**Antigravity**
- [Rules](https://antigravity.google/docs/rules/)
- [Slash commands（/plan、/grill-me、/learn）](https://antigravity.google/docs/slash-commands/)
- [/grill-me](https://antigravity.google/docs/commands/grill-me/)
- [Models & Thinking Level](https://antigravity.google/docs/models/)
- [Antigravity agent（模型正式名稱）](https://ai.google.dev/gemini-api/docs/antigravity-agent)
- [Gemini 3.8 Flash 上線公告](https://antigravity.google/blog/gemini-3-8-flash-in-google-antigravity/)
- [Agent skills](https://antigravity.google/docs/skills)
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

**OpenCode（V2 官方文件，2026-10-28）**
- [Instructions](https://opencode.ai/v2/docs/instructions/)
- [Config](https://opencode.ai/v2/docs/config/)
- [Permissions](https://opencode.ai/v2/docs/permissions/)
- [Agents](https://opencode.ai/v2/docs/agents/)
- [Commands](https://opencode.ai/v2/docs/commands/)
- [Skills](https://opencode.ai/v2/docs/skills/)
- [Plugins](https://opencode.ai/v2/docs/plugins/)
- [V1 to V2 migration](https://opencode.ai/v2/docs/migrate-v1/)
