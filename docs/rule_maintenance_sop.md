# 規則檔整理與 Harness 稽核 SOP

> 整併自：原 rule_cleanup_plan、rule_cleanup_round2_plan、improvement_list_done、harness_improvement（2026-10-29）；原始版本已刪除，需要時查 Git 歷史。
> 用途：規則越加越多、同一件事寫在好幾個檔案、AI 開始漏看時，照這份流程整理。可交給任何 coding agent 執行。
> 原則：**先盤點、再稽核、經確認才動手、每次只改一批。**
> 最後整理：2026-10-31

---

## 一、什麼時候要做

- 規則檔超過 200 行、或 AI 開始只遵守前半段。
- 同一件事在 3 個以上檔案各寫一份，改一處漏三處。
- 工具改版，舊規則已與實際行為不符。
- 每個月一次；或每完成一個專案一次。

---

## 二、單一來源原則

每一種資訊只留**一個**地方，其他地方用一句指引指過去。

| 資訊類型 | 唯一來源 |
|---|---|
| 每次對話都要遵守的硬性限制、AI 推斷不出來的事實 | `global_rules.md`（200 行內） |
| 各家工具功能、版本、載入機制 | `docs/coding_agent_features_table.md` |
| 查表、清單、操作步驟 | `README.md` |
| 公司專案規則 | `templates/AGENTS_company.md` 標記區塊 |
| 逆向分析規則 | `templates/AGENTS_reverse.md` 標記區塊 |
| 只適用某台電腦 | `machine_rules/<代號>.md` |
| 進度、決策、踩過的坑 | `PROGRESS.md` |
| 原理、研究、長期參考 | `docs/`（本目錄其他文件） |

判斷順序：**能放專案就不放全域；能放 docs 就不放常駐檔。**

### 2-1 docs 維護規則

- **事實只有一份** → `coding_agent_features_table.md`；**查證只有一份** → `verification_sources.md`；**流程只有一份** → 本檔。
- 改事實先改對照表，再改依賴它的規則；改查證同步更新查證日。
- 新增文件前先問「能不能併進現有 5 份？」能就不新增。
- docs 是參考資料，不整份貼進常駐規則檔，常駐檔只留一行指標。

---

## 三、六步流程

### 起手提示詞

```text
請讀 docs/rule_maintenance_sop.md，從 Step 1 開始；先只做盤點和稽核報告，不要修改任何檔案；報告給我確認後才進入 Step 5。
```

### 任務開頭範本

- **目標**：一句話說明要做什麼
- **驗收標準**：怎樣算做完（可執行的指令或畫面預期）
- **目標執行環境**：執行在哪台電腦（開發機／管制機／同事電腦）
- **限制（不可更動的部分）**：業務限制與技術依賴
- **先給計畫再動手**：列出預計變動的檔案與做法，等核准再改

```mermaid
flowchart LR
    A["1 盤點<br/>列出所有規則檔"] --> B["2 稽核<br/>A～J 逐項檢查"]
    B --> C["3 報告<br/>只提案不改檔"]
    C --> D["4 確認<br/>使用者勾選項目"]
    D --> E["5 套用<br/>一次一檔＋備份"]
    E --> F["6 驗證<br/>跑指令＋實測"]
```

### Step 1：盤點（只讀不改）

列出所有規則相關檔案：路徑、行數、載入時機（每次常駐／按需）、內容類型。

```powershell
Get-ChildItem -Path . -Recurse -File -Include CLAUDE.md,AGENTS.md,SKILL.md |
  ForEach-Object {
    $n = (Get-Content -LiteralPath $_.FullName).Count
    "{0,5}  {1}" -f $n, $_.FullName
  }
```

> PowerShell 5.1 讀 UTF-8 檔案時，必要時加 `-Encoding UTF8`，否則中文行數可能算錯。

### Step 2：稽核

照 `docs/ai_agent_engineering.md` 第六節的 A～J 清單逐項檢查，每項回答「通過／部分／未通過／不適用」，附檔名與行號。

### Step 3：報告（停在這裡等確認）

報告固定五段：

1. 盤點結果表。
2. 稽核總表：項目／結果／證據／嚴重度／查證狀態。
3. 建議修改清單：編號、現況（引用原文不超過 3 行）、問題、可直接貼用的新文字、風險與回復方式、來源。
4. 待使用者決定（與現有規則衝突或需要取捨）。
5. 查不到或無法確認的事項（誠實列出，不補成事實）。

### Step 4：確認

- 用選擇題讓使用者勾選要採用的項目；不要自行全做。
- 有實測背景才寫下的規則，刪除或改寫前先問。

### Step 5：套用

1. 只處理勾選的項目。
2. 修改前備份：`<檔名>.<日期_時間>.bak`（或 `<檔名>.bak_YYYYMMDD`）。
3. **一次只改一個檔案**，改完立刻給 diff。
4. 編碼：文字檔 UTF-8；`.ps1` 含中文存 UTF-8 with BOM；`.bat`、`.vbs` 只用 ASCII。
5. 拆檔時：常駐檔留目錄與禁區，細節搬 `docs/`，常駐檔留一行指標。
6. 搬完確認規則條目數量沒有少。

### Step 6：驗證

- 規則檔能被工具載入：Claude Code 用 `/context` 或 `/memory`；其他工具查官方方式。
- 用一個小任務實測：先給計畫、做完實際執行、回報輸出。
- 有禁讀設定時，用**測試檔**驗證會被擋，不要拿真正的敏感檔測。
- 回報「還有哪些沒辦法驗證」。

---

## 四、去重與搬移的硬規則

1. **常駐檔只能變短，不能變長。** 每做完一項就檢查行數。
2. **交叉參照要重算**：刪段落後「見第 N 節」「見 README『XXX』」可能位移，全部重新確認。
3. **改一處要全域搜同義字串**：例如改了「讀不到工作區」，要搜 `讀不到`、`只到工作區根目錄`、`workspace root`。
4. **不要順手改無關內容**：只改與任務相關的檔案。
5. **不要為了縮短而刪掉關鍵字**：踩過坑的條件、例外、驗證方式，寧可留著。
6. **歷史紀錄不要改寫**：`PROGRESS.md` 修訂紀錄保留原樣；新決定用新的一列。整併後的原始檔不另建封存資料夾（Git 歷史可找回，2026-10-30 使用者決定）；清理時依全域規則第 8 節「兩段式刪除」先報完整路徑清單，經同意後移入資源回收筒或待刪除資料夾，由使用者自行清空。
7. **不可刪的查表區**：README 第一節的圖、查表區（開發用 CLI 清單、專案內資料夾、AI 生圖規範、Python 升級評估）被 `global_rules.md` 指向，整理時不可刪除或改章節名稱。

### 4-1 搬移後要檢查的殘留

```powershell
# 以本次整併為例：舊檔名不應再出現在現行文件中
Select-String -Path README.md,AGENTS.md,PROGRESS.md,global_rules.md,docs\*.md `
  -Pattern '舊檔名' -SimpleMatch
```

預期：只剩 `PROGRESS.md` 修訂紀錄的歷史引用。

---

## 五、這個倉庫的收尾驗證（每次改完都跑）

在 `D:\AI_Workspace\ai.agent_rules` 下：

```powershell
# 1. 公司資訊外洩（Git Bash）
grep -rnE '\\\\[A-Za-z0-9]|([0-9]{1,3}\.){3}[0-9]{1,3}|[0-9]{6}' --exclude-dir=.git .
# 預期：沒有輸出

# 2. install.bat 非 ASCII（Git Bash）
grep -nP '[^\x00-\x7F]' install.bat
# 預期：沒有輸出

# 3. 全域規則行數
(Get-Content global_rules.md -Encoding UTF8).Count
# 預期：≤ 200
```

```powershell
# 4. 假的使用者資料夾測安裝（不會動到真正設定）
$t = "$env:TEMP\agentrules_test"
Remove-Item -Recurse -Force $t -ErrorAction SilentlyContinue
New-Item -ItemType Directory $t | Out-Null
$env:USERPROFILE = $t
cmd /c "install.bat controlled < nul"   # 預期：4 行 [OK]（CLAUDE.md、GEMINI.md、.codex/AGENTS.md、.config/opencode/AGENTS.md）+ 1 行 opencode.jsonc [OK]
cmd /c "install.bat controlled < nul"   # 預期：5 行 [SKIP]
cmd /c "install.bat dev < nul"          # 預期：4 組 [BACKUP]+[OK] + settings.json [OK] + opencode.jsonc [SKIP]（前一次已建立）
cmd /c "install.bat dev < nul"          # 預期：6 行 [SKIP]
Get-Content "$t\.claude\CLAUDE.md" -Tail 1          # 預期：THIS MACHINE: dev
Get-Content "$t\.codex\AGENTS.md" -Tail 1           # 預期：THIS MACHINE: dev
Get-Content "$t\.config\opencode\AGENTS.md" -Tail 1 # 預期：THIS MACHINE: dev
Get-Content "$t\.config\opencode\opencode.jsonc"    # 預期：含 instructions 與 permissions
Remove-Item -Recurse -Force $t
```

> `install.bat` 若同時改到安裝目的地或設定內容，才需要跑第 4 項；只改 docs 可跳過，但要說明。

---

## 六、停損與交接

同一個問題修了兩次仍失敗：

1. 停止修改。
2. 把摘要寫進 `PROGRESS.md`：症狀、已排除的原因、試過的修法與結果、目前最可能的原因、最後一個正常運作的 commit、下一步建議。
3. **只 commit `PROGRESS.md`**，改壞的程式碼不 commit；回報時列出未提交的檔案，提醒提交時不要勾。
4. 最後一個正常 commit 由使用者告知，不要自己猜。

換電腦或換對話前：

- 更新 `PROGRESS.md` 的「最後更新」與修訂紀錄。
- 寫清楚下一步**只寫一件事**。
- 「試過但無效的做法」要留，接手者才不會重做。

---

## 七、經驗沉澱：只補真正的坑

| 要補 | 不要補 |
|---|---|
| 讀程式碼推斷不出的 API／環境陷阱 | 打字錯誤、語法錯誤 |
| 現有測試漏掉的破口 | 看程式碼就懂的架構 |
| 外部資料格式意外 | 已從根本修掉的問題 |

流程：先提案那一行 → 使用者同意 → 寫進專案 `AGENTS.md` 或 `tests/` → 刪掉已根治的舊坑 → 維持 10 條／200 行。

### 7-1 規則提案單欄位

日期｜發生什麼事｜原因判斷（標事實或推測）｜提議規則（一句話）｜放哪裡（常駐檔／docs／Hook／權限）｜怎麼驗證有效｜會不會與現有規則衝突。

### 7-2 重複性任務的固化三件套（消滅人肉迴圈）

衡量工作流設得好不好，看任務做完後手頭留下什麼。若同一類任務（如固定格式的報表、講義、資料轉換）未來還要重複做，或同一個錯誤已經靠人工抓過兩次以上，除了考慮寫入 `AGENTS.md`，應評估拆成三件套留存：

1. **風格／規格筆記（`docs/`）**：把背景知識、欄位定義或排版偏好寫成獨立參考檔，按需讀取，不塞爆常駐規則。
2. **技能包（`SKILL.md` 或 `scripts/`）**：把成功跑通的步驟固定成可重複呼叫的 SOP 或轉換腳本，下次不必從零交代。
3. **自動檢查程式（`tests/` 或檢查腳本）**：把「每次都要人眼挑錯的項目」寫成程式自動掃描（零違規才准交件），不再當人肉迴圈。

---

## 八、節奏

| 頻率 | 做什麼 |
|---|---|
| 每次 AI 犯錯 | 判斷是不是「讀程式碼推斷不出來的坑」；是才提案補規則 |
| 每完成一個功能 | commit；更新 `PROGRESS.md` |
| 每月 | 重新查證工具對照表、跑 `/doctor prompt-audit`、檢查規則行數 |
| 每季或大改版 | 用本 SOP 做一次 A～J 全面稽核 |

---

## 九、不要做的事

- 不要一次改 6、7 個檔案還不給 diff。
- 不要把「推測」寫成「事實」；查不到就寫查不到。
- 與現有規則衝突時，以現有規則為準，列入「待使用者決定」，不自行取捨。
- 不要讀取、輸出或寫入密碼、API Key、`.env` 內容；範例中的內網主機、IP、人名、員工編號一律用虛構值。
- 不要用通用檔名規則（`*exploit*`、`*payload*`）做安全阻擋。
- 不要為了讓測試通過而改測試或放寬判定。
- 不要在未經同意的情況下 `git push`、刪資料、改全域設定。
- 不要把任務檔（像本檔）放進每次對話都載入的規則檔，會白付上下文租金。
