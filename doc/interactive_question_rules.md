# 互動式選項卡片提問規則：讓輕量模型達到 Claude Code 同等提問體驗

> 用途：記錄 Claude Code、Antigravity、Codex、OpenCode 互動式選擇題工具的規格查證結果、結構差異，以及為了讓輕量主力模型（如 Gemini 3.8）主動跳出選項卡片而在 `global_rules.md` 制定的規範。
> 建立日期：2026-10-25

---

## 1. 背景與問題

- **分工現況**：Claude Code 與高階模型（如 Gemini Argon）因 token 成本較高，主要負責規劃與審查；日常寫程式的主力為省 token 的輕量模型（如 Gemini 3.8）。
- **遇到的問題**：
  1. 在開始規劃或修改程式碼前，Claude Code 常會主動跳出「互動式選項卡片」讓使用者勾選方案，體驗很好。
  2. 但切換到 Gemini 3.8 時，模型往往不會主動跳出選項卡片，而是直接動手改程式碼，或只在對話框裡用純文字問一句。
  3. 即使呼叫了 Antigravity 的選項卡片工具，選項文字也常過於簡略，缺少白話優缺點說明。

---

## 2. 工具規格查證與結構差異（事實 vs. 推測）

### 2-1. 已查證的事實（附來源）

| 項目 | Claude Code | Antigravity | Codex | OpenCode | 查證來源與日期 |
|---|---|---|---|---|---|
| **內建工具名稱** | `AskUserQuestion`（v2.0.21 起引入） | `ask_question` | `request_user_input`（預設於 Plan mode 啟用；一般模式需在 `~/.codex/config.toml` 設 `[features] default_mode_request_user_input = true`） | `question`（可在 `opencode.json` 設 `"permission": { "question": "allow" }`） | Claude Code：社群技術文件（`claudelog.com`、`atcyrus.com`）；Antigravity：系統原生工具定義 `declaration:default_api:ask_question`；Codex：本機 `codex features list` 實測與 GitHub `openai/codex`；OpenCode：官方文件 `opencode.ai/docs/tools/`（2026-10-25） |
| **單選／複選支援** | `multiSelect`（`boolean`） | `is_multi_select`（`boolean`） | 支援選項清單選擇 | 支援單選與複選 | 同上（2026-10-25） |
| **自由填寫（Other）** | 原生內建自由輸入欄位 | 原生內建 write-in 輸入欄位與 Submit/Skip 按鈕 | 支援自訂文字輸入 | 原生支援自訂文字輸入 | 同上（2026-10-25） |
| **推薦方案標示** | 第一項加上 `(Recommended)` | 系統提示明確規範：推薦項排第一並加上 `(Recommended)` 前綴 | 依提示詞排列於第一項並標示 `(Recommended)` | 依提示詞排列於第一項並標示 `(Recommended)` | 同上（2026-10-25） |
| **選項結構（關鍵差異）** | `options` 為物件陣列，**分成 `label`（短標題）與 `description`（詳細說明、優缺點與影響）兩個獨立欄位** | `options` 只是**單純的字串陣列（`ARRAY of STRING`），沒有獨立的 `description` 欄位**，且系統預設提示要求寫成使用者的簡短回答（`Format options as the user's direct response`） | 具標題、說明與選項清單 | 具 `header`、問題文字與選項清單 | 比對 JSON Schema 與官方文件確認（2026-10-25） |
| **如何強制觸發卡片** | 在規則或 Skill 明確寫出「禁止用純文字發問，必須呼叫工具名稱呈現選項」 | 在規則明確點名呼叫 `ask_question` 工具，並規定選項字串格式 | 規則點名工具名稱；未開 feature flag 時退回同格式編號選項 | 規則點名呼叫 `question` 工具 | 社群實踐（`filiphric.com`）與本專案規則設計（2026-10-25） |

#### 結構對照範例

- **Claude Code (`AskUserQuestion`) 的選項結構**（天生有獨立說明欄）：
  ```json
  {
    "question": "要用哪種方式儲存設定？",
    "header": "設定儲存",
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

- **Antigravity (`ask_question`) 的選項結構**（只有單一字串，需靠規則強制把說明寫進字串裡）：
  ```json
  {
    "questions": [
      {
        "question": "要用哪種方式儲存設定？",
        "is_multi_select": false,
        "options": [
          "(Recommended) JSON 檔 — 免安裝資料庫、可直接用記事本看，適合單機小工具",
          "SQLite — 支援大量資料查詢，但無法直接用記事本編輯"
        ]
      }
    ]
  }
  ```

### 2-2. 原本規則的缺口（已確認）

檢查 2026-10-25 修改前的 `global_rules.md`：
1. 開頭「提問先行」只寫「先停下來問使用者，確認後再動手」，**完全沒有提到「選項卡片」或工具名稱**，因此模型用純文字發問也算合規。
2. 第 4 節「規劃先行」只寫「開新專案或大幅改架構前，先說明建議的語言、框架、需要安裝的東西與理由，等使用者確認後再開始撰寫」，一般規劃新功能或修改現有程式碼並未強制使用互動式選項卡片。
3. 沒有規定選項字串必須包含「`方案名稱 — 白話做法、優缺點與影響`」，導致在 Antigravity 上呼叫 `ask_question` 時容易只出現簡短名詞，缺乏決策資訊。

### 2-3. 推測與查不到的部分

- **推測（無官方數據支持）**：不同模型（如 Claude 與 Gemini 3.8）在未強制點名工具時，主動呼叫互動式問答工具的頻率差異，可能與模型本身的訓練偏好或省 token 傾向有關；此點並無 Google 或 Anthropic 官方報告證實。
- **查不到**：查無官方「調整模型主動呼叫 `ask_question` 機率」的獨立設定參數，唯一可控做法是在載入的規則檔（`global_rules.md`）中明確規定觸發條件與工具名稱。

---

## 3. 制定的規則條文（已寫入 `global_rules.md`）

為了彌補上述缺口與工具欄位差異，並遵守 `AGENTS.md`「條列、簡短、不重複」的原則，在 `global_rules.md` 開頭寫入完整規定，第 4 節則以簡短參照呼應：

### 3-1. `global_rules.md` 開頭醒目區塊

```markdown
> **提問先行與互動式選項卡片（重要）**：開始新規劃、修改現有程式碼，或遇到需求／規格不明確、有 2 種以上做法且會影響結果時，**先讀完相關檔案盤點問題，停下來向使用者提問，確認後再動手**，嚴禁自行假設。提問時**禁止只用純文字問句，必須呼叫互動式選擇題工具**（Antigravity 用 `ask_question`、Claude Code 用 `AskUserQuestion`、OpenCode 用 `question`、Codex 用 `request_user_input`）跳出選項卡片，並遵守：(1) 把所有待確認問題整理在同一次呼叫中一次問齊（可含多題，可複選的題目開啟 `is_multi_select`／`multiSelect`）；(2) 最推薦的方案排第一項並標示 `(Recommended)`；(3) 每個選項都寫明「`方案名稱 — 白話做法、優缺點與影響`」（彌補 `ask_question` 無獨立說明欄位的限制）；(4) 若當前環境無該工具，才退回在對話中列出同樣格式的編號選項（1 / 2 / 3）。**唯一例外**：使用者已明確指定具體改法（如單純改文字、調按鈕位置等無歧義的小修改），或不影響結果的內部細節（如變數命名），直接執行即可，不必提問。
```

### 3-2. `global_rules.md` 第 4 節「規劃先行」第一點（簡短參照，不重複細節）

```markdown
- 開新專案、規劃新功能或修改現有程式碼前（除非使用者已明確指定改法），依開頭「提問先行與互動式選項卡片」規定，先讀完相關檔案並呼叫選擇題工具跳出選項卡片（含推薦方案、語言／框架、需要安裝的東西與白話優缺點），等使用者點選確認後再開始撰寫。
```

### 3-3. 設計重點對照

| 規則要求 | 解決什麼問題 |
|---|---|
| **先讀完相關檔案盤點問題，再同一次呼叫問齊（可多題／複選）** | 避免模型沒看程式碼就瞎問，或問一題、改一點、又問一題 |
| **禁止只用純文字問句，必須呼叫互動式選擇題工具** | 堵住輕量模型「只打字發問就算遵守提問先行」的漏洞 |
| **首項標示 `(Recommended)`** | 讓非工程師使用者一眼看出最推薦哪個方案 |
| **每個選項寫明「`方案名稱 — 白話做法、優缺點與影響`」** | 彌補 Antigravity `ask_question` 沒有獨立 `description` 欄位的限制，達到與 Claude Code 相同的閱讀體驗 |
| **無該工具時退回同格式編號選項（1 / 2 / 3）** | 在不支援卡片 UI 的環境（如純文字介面、網頁聊天或未開啟 feature flag 的 Codex 一般模式）仍能維持相同選項品質 |
| **唯一例外：已明確指定具體改法的小修改（如改文字、調按鈕位置）** | 避免連毫無歧義的簡單指令都要跳卡片干擾工作流程 |

---

## 4. 關聯更新檔案

- `global_rules.md`：更新開頭「提問先行與互動式選項卡片」與第 4 節「規劃先行」。
- `doc/coding_agent_features.md`：
  - 第二節「強制執行與記憶」新增「互動式選擇題卡片工具」一列，記錄四家工具的功能與結構差異。
  - 第三節「依賴本表的規則」新增對應列，未來工具改版時可連動檢查。
- `README.md`：第三節「檔案總覽」加入 `doc/interactive_question_rules.md` 說明。
- `PROGRESS.md`：記錄使用者確認事項與修訂紀錄。

---

## 5. 變更紀錄

| 日期 | 內容 |
|---|---|
| 2026-10-25 | 初版：整理四家 coding agent 選擇題工具查證結果、結構差異與 `global_rules.md` 強化規則，收納於 `doc/interactive_question_rules.md` |
