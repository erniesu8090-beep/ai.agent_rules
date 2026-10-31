# ai.agent_rules

> 寫給 AI 看的專案規則：維護全域規則檔與安裝腳本時遵守。
> 接手工作前先讀 `PROGRESS.md`。

## 專案用途

存放所有電腦共用的全域 AI Agent 規則（`global_rules.md`），以及把它安裝到 Claude Code、Antigravity、Codex、OpenCode 的腳本。

## 目標執行環境

- 開發在：住家開發機／公司開發機
- 執行在：住家開發機、公司開發機、管制機（三台都要執行安裝腳本：Windows `install.bat`、Ubuntu `install.sh`）
- 取得方式：住家與公司開發機用 GitHub；管制機由公司開發機經 GitSync 的 `.bundle` 帶過去（管制機連不到 GitHub）

## 業務規則

- `global_rules.md` 是規則本體；安裝結果 = `global_rules.md` +（有的話）`machine_rules/<電腦代號>.md` + 最後一行 `THIS MACHINE: <home|dev|controlled>`，寫到 `~/.claude/CLAUDE.md`、`~/.gemini/GEMINI.md`、`~/.codex/AGENTS.md` 與 `~/.config/opencode/AGENTS.md`；開發機另外設定 `~/.claude/settings.json`；所有電腦另外設定 `~/.config/opencode/opencode.jsonc`（見「不可更動的部分」）。
- 全域規則每次對話都會載入：條列、簡短、不重複；能放在工作區或專案規則的內容就不要放進全域。
- 本倉庫會推送到 GitHub：不得出現公司內部主機名稱、IP、內網路徑、員工編號、公司專案名稱、GitHub 帳號。這些資訊寫在工作區規則檔（例如 `D:\AI_Workspace` 底下）。（例外：個人工具專案名稱 `google.cloud_oauth.relay` 與公開網域如 `*.googleapis.com` 的可否連線狀態，不含公司識別資訊，因安裝腳本需自動寫入 `settings.json` 故保留於本倉庫）
- 修改規則內容時，同步檢查 `README.md` 與 `templates/` 是否需要一起更新。
- 只有公司專案用得到的規則放 `templates/AGENTS_company.md` 的「公司專案規則」標記之間，不放全域；修改時更新該段開頭的「公司規則版本」日期，並提醒使用者把新版本合併到各公司專案（整段替換標記之間的內容）。
- Antigravity 往上找規則檔只到工作區根目錄（不會超過；2026-10-10 實測開啟 Git 倉庫時只到該 Git 倉庫根目錄）；Codex 只到 Git／專案根目錄；OpenCode 從工作區往上只找到家目錄（`D:\AI_Workspace` 在家目錄以外，要由 `opencode.jsonc` 的 `instructions` 指定），所以四個工具都要遵守的規則一律放 `global_rules.md`；公司工作區專用的規則以「公司專案（目標執行環境含管制機或同事電腦）的上一層資料夾」來指稱，不寫資料夾名稱。

- 規則要寫成各家 coding agent 都看得懂、都讀得到：共用內容只寫在 `AGENTS.md` 與 `global_rules.md`，不寫只有某一家才懂的語法（例如 `@` 引用）當作唯一來源；工具專屬的設定另外註明是哪一家。
- 依賴工具行為的規則（例如「自己的專案不建立 `CLAUDE.md`」），要能在 `docs/coding_agent_features_table.md` 第三節找到依據；新增這類規則時同步補上那一列。
- 新增 coding agent 時照 `docs/coding_agent_features_table.md` 第四節做。

## 撰寫規則的原則（依 Harvard CS2680 課程重點，2026-10-15）

- 全域規則每次對話都整份載入：`global_rules.md` 維持 200 行以內；新增前先問「這條是不是每次對話都需要」。
- 只在特定情境用到的內容，放到那個情境才會讀的地方：公司專案 → `templates/AGENTS_company.md`；逆向分析專案 → `templates/AGENTS_reverse.md`；只有某台電腦 → `machine_rules/`；查表、清單、操作步驟 → `README.md`。
- 該寫：硬性限制、AI 自己推斷不出來的事實（實測結果、踩過的坑，附日期）。不該寫：程式語言常識、長篇說明、機密。
- 規則要具體可執行（寫「做什麼、不做什麼」），不寫「盡量」「注意」這類無法判斷是否做到的話。
- 新增或修改後，通讀全部規則檔：同一件事不可在兩處寫成不同規定、交叉參照（「見第 N 節」）要正確、過時的規則要刪。
- 有實測日期或曾經出過問題才寫下的規則，刪除前先問使用者。
- 需要「強制」而不只是「提醒」的規則（例如禁止 git push），評估改用 Hook：Claude Code、Antigravity 與 Codex 都有，OpenCode 用 Plugin；設定檔位置與格式不同，要各寫一份（見 `docs/coding_agent_features_table.md`）；管制機的防毒也可能攔截 Hook 執行的腳本。

## 不可更動的部分

- 電腦代號 `home`、`dev`、`controlled`：規則內文與安裝腳本都依賴這三個代號。
- 安裝目的地：`~/.claude/CLAUDE.md`、`~/.gemini/GEMINI.md`、`~/.codex/AGENTS.md`、`~/.config/opencode/AGENTS.md`；開發機另外在 `~/.claude/settings.json` 不存在時建立（已存在只檢查、不改寫，避免弄壞使用者自己的設定）；所有電腦另外在 `~/.config/opencode/opencode.jsonc` 不存在時建立（規則同上）。
- 安裝前一定先備份既有檔案（`*.日期_時間.bak`），內容相同則略過。
- `install.bat` 只用 ASCII、CRLF 換行；`install.sh` 用 LF 換行；換行由 `.gitattributes` 保證，不可刪除。

## 修改後的驗證方式

1. 檢查公司資訊沒有外洩（在專案資料夾開 Git Bash）：
   `grep -rnE '\\\\[A-Za-z0-9]|([0-9]{1,3}\.){3}[0-9]{1,3}|[0-9]{6}' --exclude-dir=.git .`
   預期：沒有輸出（網路路徑、IP、六位數字如員工編號都不應出現）。
   另外對照工作區規則檔裡的公司主機、專案名稱人工確認；檢查用的關鍵字本身也不能寫進本倉庫。
2. 用假的使用者資料夾測試安裝，不會動到真正的設定（在專案資料夾開 PowerShell）：
   ```powershell
   $t = "$env:TEMP\agentrules_test"; Remove-Item -Recurse -Force $t -ErrorAction SilentlyContinue; New-Item -ItemType Directory $t | Out-Null
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
3. `install.bat` 沒有非 ASCII 字元：`grep -nP '[^\x00-\x7F]' install.bat` 沒有輸出。
4. 行數：`global_rules.md` 不超過 200 行（PowerShell：`(Get-Content global_rules.md -Encoding UTF8).Count`，一定要加 `-Encoding UTF8`，否則 PowerShell 5.1 用 Big5 讀檔，行數會算錯；Git Bash：`wc -l global_rules.md`）；超過時先精簡或搬移，再提交。
