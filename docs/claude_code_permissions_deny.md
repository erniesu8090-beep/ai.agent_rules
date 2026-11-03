# Claude Code 防凍結：禁止讀取特定專案與資安檔案

> 整併自：原 claude_code_block_cyber_files.md（2026-10-29）；原始版本已刪除，需要時查 Git 歷史。
> 目的：避免 Claude Code 讀到資安／逆向／網路代理相關內容時觸發安全機制、中斷整個對話；同時保留其他 coding agent 的處理路徑。
> 適用：Claude Code；其他工具（Antigravity、Codex、OpenCode）的對應設定見 `docs/coding_agent_features_table.md`。
> 最後整理：2026-10-31

---

## 一、給 coding agent 的執行指示（先看這段）

1. 先找使用者現有的規則檔（`AGENTS.md`、`CLAUDE.md` 或本倉庫的 `global_rules.md`）；找不到就停下來問，不要自己建立新檔。
2. **合併，不要覆蓋**：只補本檔第 3、4 節的內容；已有類似條文就更新，不要重複。
3. **不要讀取、開啟、搜尋、列出** `permissions.deny` 所列的路徑；需要資料夾名稱時問使用者，不要自己掃描。
4. **不要對含資安內容的資料夾執行 `/security-review`。**
5. 改 `.claude/settings.json` 時：已存在 → 只補 `permissions.deny` 缺少的項目；不存在 → 用第 4 節建立；改完確認 JSON 格式。
6. 資料夾名稱是佔位字，**必須先向使用者確認實際名稱**，不可猜測。
7. 完成後用白話回報：改了哪些檔、加了哪幾條、使用者要做哪些測試。

---

## 二、背景與事實

### 2-1 問題

Claude Code 讀到資安／駭客／逆向／網路代理相關程式碼時，可能出現：

```text
This request triggered cyber-related safeguards
```

然後停止回應。整個對話可能一起被擋，換題目也救不回來。

### 2-2 已查證

| 事實 | 來源 |
|---|---|
| 多位使用者回報，讀資安程式碼會被 `cyber-related safeguards` 中斷 | https://claudeissues.com/issue/68791-bug-cyber-safeguard-false-positive-blocks-security-review-skill-in-a-fresh-sessi |
| 全新對話只讓 Claude 讀含防外掛、低階 hook 的資料夾就被擋，不需攻擊性指令 | 同上 |
| 機制會看整段對話累積的內容，一次誤判可能擋掉整個對話 | https://claudeissues.com/issue/63751-bug-aup-cyber-safeguard-false-positives-on-legitimate-own-software-hardening-one |
| 官方說明防護刻意設得廣，有時會誤判正當資安工作 | https://arte.itlibra.com/en/articles/claude-code-safeguards-flagged-this-message |
| 有 Cyber Verification Program 可申請，但有人回報通過後仍被擋 | https://claudeissues.com/issue/86352-bug-claude-code-cybersecurity-safeguards-blocking-approved-cyber-verification-pr |
| `permissions.deny` 的 `Read(...)` 只涵蓋 Claude 內建檔案工具；相對路徑以**啟動資料夾**為起點，跨資料夾要改用 `//` 絕對路徑 | https://code.claude.com/docs/en/large-codebases |
| `deny` 對 Bash 效力有限：`cat` 可能被擋，改用 Python 一行指令仍可能讀到 | https://www.developersdigest.tech/blog/keep-secrets-away-from-ai-coding-agents-2026 |
| `/sandbox` 只支援 macOS 與 Linux／WSL2，原生 Windows 不支援，不能用來替代 Windows 的讀取阻擋 | https://code.claude.com/docs/en/security |
| 觸發後用 `/rewind` 退回、`/feedback` 回報、可申請 CVP | https://code.claude.com/docs/en/troubleshooting |

### 2-3 推測與查不到

- **推測**：用 `deny` 讓檔案內容不進入對話，可降低觸發機會；沒有查到直接驗證成效的來源。
- **推測**：檔名本身是否會被判斷，不確定。
- **查不到**：哪一種 `deny` 規則一定不會觸發凍結，官方沒有說明。
- **查不到**：多次觸發是否會停權，官方條款未見；目前只有使用者回報的推論。

---

## 三、要合併進規則檔的條文

```markdown
## 資安相關檔案處理規則（避免對話被安全機制中斷）

背景：讀取資安／駭客／逆向／網路代理相關檔案，可能觸發 Claude 的安全機制，導致整個對話中斷。

1. 不要讀取、開啟、搜尋、列出 `.claude/settings.json` 的 `permissions.deny` 所列路徑與檔案。
2. 不要使用 `/security-review` 掃描含資安內容的資料夾。
3. 不要用 Bash（`cat`、`type`、Python 等）繞過 deny 規則讀取受限檔案。
4. 需要受限資料夾的名稱或內容時，先詢問使用者，由使用者決定要不要貼出。
5. 明顯涉及網路代理、隧道、網路規避、低階 hook 的專案，一律交給 Claude Code 以外的 agent（例如 Antigravity）處理。
6. 若出現「safeguards flagged this message」或「cyber-related safeguards」：
   - 立刻停止重試同一個動作。
   - 告知使用者按 `Esc` 兩次，或輸入 `/rewind` 退回觸發前的檢查點，再換做法。
   - 不要讀取任何疑似造成問題的檔案來「找原因」。
   - 可用 `/feedback` 回報誤判，或申請 Cyber Verification Program。
7. 建議把這類檔案放在 Claude 工作目錄之外；碰不到最保險。
```

---

## 四、`.claude/settings.json` 設定

### 4-1 範本

```json
{
  "permissions": {
    "deny": [
      "Read(./**/google.cloud_oauth.relay/**)"
    ]
  }
}
```

> `./` 相對路徑以**啟動 Claude Code 時所在的資料夾**為起點，不是倉庫根目錄。跨資料夾保護尚待實測；請勿在含敏感專案的上層目錄啟動 Claude Code。

### 4-2 白話說明

| 規則 | 意思 |
|---|---|
| `Read(./**/<資料夾>/**)` | 整個資料夾與底下所有檔案，Claude 的內建讀檔工具都不能讀 |

### 4-3 合併規則

- 已有 `settings.json` → 只補 `permissions.deny` 缺少的項目，其他設定原樣保留。
- 已有 `permissions.allow` 或其他欄位 → 不動。
- 改完確認 JSON 逗號、括號正確；重新啟動 Claude Code 才生效。

### 4-4 已否決的做法（不要用）

- `Read(./**/exploit*)`
- `Read(./**/payload*)`
- `Read(./**/*.pcap)`

原因：通用檔名太廣，會誤擋正常的分析說明、測試腳本或範例檔。2026-10-24 決議**不加通用檔名規則**，只精準阻擋特定敏感專案資料夾。

---

## 五、設定後怎麼驗收

1. 重新啟動 Claude Code（設定要重開才載入）。
2. 輸入 `/permissions`，確認 deny 規則有出現。
3. 請 Claude 讀一個被擋的檔案 → 預期回「被拒絕」。
4. 請 Claude 讀一個正常程式檔 → 預期可正常讀取（確認沒有誤擋）。
5. 從「敏感專案所在資料夾」與「另一個不相干專案資料夾」各開一次，重複第 3、4 步；兩邊都應一致。
6. 若仍被擋或凍結，把完整錯誤訊息貼出來，再判斷原因。

---

## 六、已知限制（如實告知，不要誇大）

- **啟動資料夾限制（最重要）**：`Read(./**/<資料夾>/**)` 的 `./` 以啟動資料夾為起點；從別的專案啟動可能擋不到。Windows 磁碟機搭配 `//` 絕對路徑的寫法查無官方範例，**跨資料夾保護尚待實測**。
- `deny` 只管 Claude 內建讀檔工具，**不保證**擋得住 Bash／Python 繞道。
- 使用者自己貼進對話的內容，不受設定保護。
- 這套做法的成效屬**推測**，需要實測確認。
- `/sandbox` 在原生 Windows 不支援，不能替代讀取阻擋。
- 資安工作屬正當需求時，可申請 Cyber Verification Program；但已有通過後仍被擋的回報，不保證有效。
- 觸發後按一次 `Esc` 只是中斷目前動作；要退回檢查點請按 `Esc` 兩次或輸入 `/rewind`。

---

## 七、變更紀錄與來源

| 日期 | 內容 |
|---|---|
| 2026-10-22 | 首次實測 `.claudeignore` 無法阻止讀取，改採 `permissions.deny` |
| 2026-10-24 | 建立阻擋規則與 `settings.json` 範本；決議不加通用檔名規則 |
| 2026-10-25 | 補官方相對路徑起點、`/sandbox` 平台限制、`/rewind` 與 CVP 處置 |
| 2026-10-29 | 整併為精簡實戰版，原文封存至 `docs/archive/claude_code_block_cyber_files_2026-10-25.md` |
| 2026-10-31 | 原始封存檔刪除，未收錄的二手來源移至 verification_sources.md |

主要來源：Claude Code 官方 large codebases、security、troubleshooting 文件，以及第 2-2 節列出的問題回報頁。官方文件改版時，先重新查證再改本檔。
