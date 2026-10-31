# 查證狀態與來源總表

> 用途：集中管理「哪些說法有官方依據、哪些只是推測、哪些查不到」，方便每月重新查證，也避免同一件事在不同文件寫成不同版本。
> 說明：本表**沿用原文件在 2026-10-19～2026-10-28 的查證結果**，2026-10-29 整併、2026-10-31 增補部分來源。狀態改變時，同步更新來源文件與本表。
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
| `/doctor prompt-audit` | v2.1.283+；找過時、矛盾、引用不存在的內容 | 官方 | 同上 | 2026-10-28 |
| 隨需載入規則字元上限 | v2.1.309 起，200K 視窗為 40,000 字元，超過只取開頭 | 官方 | 同上 | 2026-10-28 |
| 自動記憶範圍 | 只存使用者資訊、被糾正的回饋、專案背景、外部參照；除錯修法通常不存；只存本機 | 官方 | 同上 | 2026-10-28 |
| `permissions.deny` 路徑 | 相對路徑以啟動資料夾為起點；跨資料夾要改用 `//` 絕對路徑；只涵蓋內建檔案工具 | 官方 | https://code.claude.com/docs/en/large-codebases 、https://horadecodar.com.br/impedir-claude-code-editar-arquivos/（二手） | 2026-10-25 |
| 被 deny 的檔案會從 Claude 的檔案列表中隱藏 | deny 的檔案在列表中不顯示 | 二手 | https://www.petefreitag.com/blog/claude-code-permissions/ | 2026-10-25 |
| `deny` 對 Bash 的效力 | `cat` 可能被擋，Python 一行指令仍可能讀到 | 二手 | https://www.developersdigest.tech/blog/keep-secrets-away-from-ai-coding-agents-2026 | 2026-10-25 |
| `.claudeignore` | 2026-10-22 實測無法阻止讀取或觸發審查 | 實測 | 本倉庫 `PROGRESS.md` 第五節 | 2026-10-22 |
| `/sandbox` 平台 | 只支援 macOS（Seatbelt）與 Linux／WSL2（bubblewrap + socat）；原生 Windows 不支援 | 官方 | https://code.claude.com/docs/en/security | 2026-10-25 |
| `AskUserQuestion` 工具與版本 | 官方確認為澄清問題工具（1-4題、2-4選項）；v2.0.21 起 | 官方（工具）／二手（v2.0.21 版本號） | https://code.claude.com/docs/en/agent-sdk/approvals ；claudelog.com、atcyrus.com（二手） | 2026-10-31 |

---

## 二、Antigravity

| 主題 | 結論 | 狀態 | 來源 | 查證日 |
|---|---|---|---|---|
| 規則檔位置 | 全域 `~/.gemini/AGENTS.md`、`GEMINI.md`、`~/.gemini/config/*`、`~/.gemini/config/rules/*.md`；CLI 另讀 `~/.gemini/antigravity-cli/rules/*.md` | 官方 | https://antigravity.google/docs/rules/ | 2026-10-28 |
| 往上找規則範圍 | 只到工作區根目錄（workspace root），不會超過 | 官方 | 同上 | 2026-10-28 |
| 開啟 Git 倉庫的範圍 | 只到該倉庫根目錄 | 實測 | 2026-10-10 本機 | 2026-10-10 |
| 容量限制 | 每檔 24,000 bytes；常駐規則合計 20,000 tokens，超過時最大的檔改成指標 | 官方 | 同上 | 2026-10-28 |
| 模組化規則 | `trigger` 必填（`always_on`／`model_decision`／`glob`／`manual`），缺少或寫錯靜默丟棄 | 官方 | 同上 | 2026-10-28 |
| `/plan`、`/grill-me`、`/learn` | 規劃、一次一題訪談、先提案再寫入 | 官方 | https://antigravity.google/docs/slash-commands/ | 2026-10-25 |
| 舊 Workflows | 2026-10-19 起停止運作，用 `/migrate-workflows` 轉 Skills；新系統待公布 | 官方 | https://antigravity.google/docs/migration/workflows-to-skills/ | 2026-10-25 |
| `ask_question` 支援複選與自由填寫 | 是；`is_multi_select` | 官方 | https://dev.to/googleai/elevating-antigravity-agent-skills-part-1-interactive-ui-workflows-6l2 | 2026-10-25 |
| `ask_question` 選項格式 | `options` 為單一字串陣列，沒有獨立 `description` | 實測 | 本機 session JSON Schema | 2026-10-25 |
| 是否有背景自動記憶 | 無；只有手動 `/learn` | 官方 | Antigravity customizations 文件 | 2026-10-25 |
| Gemini 3.8 Flash 上線日 | 2026-09-01 | 官方 | https://antigravity.google/blog/gemini-3-8-flash-in-google-antigravity/ | 2026-10-25 |
| 模型正式名稱 gemini-3.8-flash／gemini-4-argon | 官方模型標籤與正式名稱 | 官方 | https://ai.google.dev/gemini-api/docs/antigravity-agent | 2026-10-25 |
| 規劃時不會主動跳提問卡片（需規則或 /plan /grill-me 觸發） | 規劃時預設不跳卡片，需靠指令或規則明確點名觸發 | 實測（使用者觀察） | 本機 | 2026-10-30 |
| Gemini 4 Argon 可用方案 | 需 Google AI Pro 以上 | 官方 | https://antigravity.google/docs/models/ | 2026-10-25 |
| Gemini CLI 停止服務 | 2026-06-18 起對 AI Pro、AI Ultra、免費個人帳號停止；企業與付費 API Key 例外 | 官方 | https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/ | 2026-10-25 |
| `agy -p` 呼叫 `image-generator` 子代理跨工具生圖 | 單純呼叫 `image-generator` 不執行 shell，圖片自動存入 `~/.gemini/antigravity-cli/brain/<對話ID>/`，免終端機權限確認 | 實測 | 2026-10-25 本機實測 `agy` v1.4.7 | 2026-10-25 |

---

## 三、Codex 與 OpenCode V2

| 主題 | 結論 | 狀態 | 來源 | 查證日 |
|---|---|---|---|---|
| Codex 規則檔與容量限制 | 全域 `~/.codex/AGENTS.md`；專案從 Git／專案根目錄往下合併 `AGENTS.md`（預設不讀 `CLAUDE.md`）；預設合計上限 32 KiB | 官方 | https://developers.openai.com/codex/guides/agents-md/ | 2026-10-24 |
| Codex 提問工具 `request_user_input` | 預設於 Plan mode 啟用；一般模式需在 `config.toml` 設 `[features] default_mode_request_user_input = true` | 實測／官方 | 本機 `codex features list` 與 GitHub `openai/codex` | 2026-10-25 |
| Codex `$imagegen` 跨工具呼叫 | 透過 `codex exec` 可走本機 ChatGPT 登入額度呼叫內建 `image_gen` 產圖 | 實測 | 本機 `codex-imagegen-bridge` 技能實測 | 2026-10-24 |
| OpenCode V2 規則檔格式 | 只讀 `AGENTS.md`，不讀 `CLAUDE.md`；無 fallback | 官方 | https://opencode.ai/v2/docs/instructions/ | 2026-10-28 |
| OpenCode V2 往上找規則範圍 | 找到家目錄；工作區在家目錄以外時只到專案根目錄 | 官方 | 同上 | 2026-10-28 |
| OpenCode V2 工作區規則 | 要用 `opencode.jsonc` 的 `instructions` 指定 | 官方 | https://opencode.ai/v2/docs/config/ | 2026-10-28 |
| OpenCode V2 權限 | `permissions` 的 `*` 會跨 `/`；可管 `external_directory` | 官方 | https://opencode.ai/v2/docs/permissions/ | 2026-10-28 |
| OpenCode V2 Hooks | 無宣告式 hooks，用 Plugin | 官方 | https://opencode.ai/v2/docs/plugins/ | 2026-10-28 |
| OpenCode V2 提問工具 | `question`，選項有 `label`／`description` | 官方 | https://opencode.ai/v2/docs/agents/ | 2026-10-28 |

---

## 四、安全機制與環境

| 主題 | 結論 | 狀態 | 來源 | 查證日 |
|---|---|---|---|---|
| Claude 資安防護會誤判 | 官方說明防護刻意設得廣，可能誤判正當資安工作 | 官方 | https://arte.itlibra.com/en/articles/claude-code-safeguards-flagged-this-message | 2026-10-25 |
| 讀資安檔會被凍結 | 多位使用者回報；不需攻擊性指令 | 二手 | https://claudeissues.com/issue/68791-bug-cyber-safeguard-false-positive-blocks-security-review-skill-in-a-fresh-sessi | 2026-10-25 |
| 一次誤判可能擋整個對話 | 有回報指機制會看整段對話累積內容 | 二手 | https://claudeissues.com/issue/63751-bug-aup-cyber-safeguard-false-positives-on-legitimate-own-software-hardening-one | 2026-10-25 |
| Cyber Verification Program | 可申請，但有人回報通過後仍被擋；官方處置（/rewind、/feedback、CVP）見 troubleshooting 文件 | 官方（處置）／二手（被擋回報） | https://code.claude.com/docs/en/troubleshooting （官方）；https://claudeissues.com/issue/86352-bug-claude-code-cybersecurity-safeguards-blocking-approved-cyber-verification-pr （二手） | 2026-10-31 |
| 多次觸發是否停權 | 官方條款未見；只有使用者回報推論 | **查不到** | 無 | 2026-10-25 |
| `deny` 能否一定防凍結 | 無官方說明 | **查不到** | 無 | 2026-10-25 |
| Python 3.11 安全更新 | 到 2027-10 結束 | 官方 | https://peps.python.org/pep-0664/ | 2026-10-25 |
| `google-colab-cli` 平台 | 只支援 Linux、macOS；Windows 不支援 | 官方 | https://pypi.org/project/google-colab-cli/ | 2026-10-27 |
| Colab G4 顯卡 | NVIDIA RTX PRO 6000 Blackwell Server Edition，96GB GDDR7 | 官方 | Colab 官方資源頁 | 2026-10-27 |
| Gemini 生圖高頻呼叫限流（HTTP 429） | 連續快速呼叫易觸發 RPM 上限與 429 `RESOURCE_EXHAUSTED` 暫時冷卻（5～15 分鐘）；批次腳本需加 15～20 秒間隔與 60 秒退避 | 實測 | 2026-10-26 批量生圖實測 | 2026-10-26 |

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
| 各家 harness 是否會主動觸發提問卡片 | 免記指令，由全域規則開頭強制點名提問卡片工具（整合規劃、迴圈驗證、動態子代理）；見對照表第五節 | 用四個固定任務實測 |
| `deny` 降低凍結機率的成效 | 標「推測」，不誇大 | 跨資料夾實測 |
| `deny` 跨資料夾保護 | 標「尚待實測」；避免在敏感專案上層啟動 | 從兩個不同資料夾啟動實測 |
| Windows 的 `//` 絕對路徑寫法 | 查無官方範例 | 查官方文件或實測 |
| 多次觸發 safeguards 是否停權 | 標「使用者回報推論」 | 每月查官方條款 |
| Antigravity 是否有背景自動記憶 | 目前查無 | 每月追蹤 |
| Antigravity 新 workflows 系統 | 尚未公布 | 每月追蹤 |
| `ask_question` 是否有獨立 `description` 欄位 | 本機實測沒有 | 每月查官方規範 |
| Antigravity、OpenCode 的 Hook／權限對應細節 | 部分未查證 | 需要時查官方文件 |
| Meta-Harness／OO-Harness 的實際可用性 | 當研究方向 | 有官方實作再評估 |

---

## 七、每月重新查證流程

1. 打開 `docs/coding_agent_features_table.md`，照第六節官方網址逐頁對照。
2. 只改有變動的列，更新該列與開頭的「最後全面查證」。
3. 對照第三節「依賴本表的規則」，修改受影響的規則檔。
4. 更新本表對應列與查證日。
5. 在 Claude Code 執行 `/doctor prompt-audit`（v2.1.283+）。
6. 照 `docs/rule_maintenance_sop.md` 第五節跑收尾驗證。

> 查證時**先查官方文件再寫，不憑記憶**；查不到就寫查不到，不要用推論補成事實。工具版本、設定欄位、日期都屬高風險資訊。
