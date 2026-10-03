# ai.agent_rules

> 寫給 AI 看的專案規則：維護全域規則檔與安裝腳本時遵守。

## 專案用途

存放所有電腦共用的全域 AI Agent 規則（`global_rules.md`），以及把它安裝到 Claude Code、Antigravity 的腳本。

## 目標執行環境

- 開發在：住家開發機／公司開發機
- 執行在：住家開發機、公司開發機、管制機（三台都要執行 `install.bat`）
- 取得方式：住家與公司開發機用 GitHub；管制機由公司開發機經 GitSync 的 `.bundle` 帶過去（管制機連不到 GitHub）

## 業務規則

- `global_rules.md` 是規則本體；安裝結果 = `global_rules.md` + 最後一行 `THIS MACHINE: <home|dev|controlled>`，寫到 `~/.claude/CLAUDE.md` 與 `~/.gemini/GEMINI.md`。
- 全域規則每次對話都會載入：條列、簡短、不重複；能放在工作區或專案規則的內容就不要放進全域。
- 本倉庫會推送到 GitHub：不得出現公司內部主機名稱、IP、內網路徑、員工編號、公司專案名稱、GitHub 帳號。這些資訊寫在工作區規則檔（例如 `D:\AI_Workspace` 底下）。
- 修改規則內容時，同步檢查 `README.md` 與 `templates/` 是否需要一起更新。

## 不可更動的部分

- 電腦代號 `home`、`dev`、`controlled`：規則內文與安裝腳本都依賴這三個代號。
- 安裝目的地：`~/.claude/CLAUDE.md`、`~/.gemini/GEMINI.md`。
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
   cmd /c "install.bat controlled < nul"   # 預期：兩行 [OK]
   cmd /c "install.bat controlled < nul"   # 預期：兩行 [SKIP]
   cmd /c "install.bat dev < nul"          # 預期：兩行 [BACKUP] + [OK]
   Get-Content "$t\.claude\CLAUDE.md" -Tail 1   # 預期：THIS MACHINE: dev
   Remove-Item -Recurse -Force $t
   ```
3. `install.bat` 沒有非 ASCII 字元：`grep -nP '[^\x00-\x7F]' install.bat` 沒有輸出。
