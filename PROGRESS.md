# PROGRESS　進度與交接

> 最後更新：2026-10-25（住家開發機）
> 新對話接手：先讀 `AGENTS.md` → 本檔 → `doc/coding_agent_features.md`

## 一、目前階段

**維護中**。已完成：

1. 建立 coding agent 功能對照表 `doc/coding_agent_features.md`（2026-10-19 全面查證；2026-10-24 新增 Codex、OpenCode）
2. 建立每月重新查證流程（README「coding agent 功能查證」）與規則依據對照（對照表第三節）
3. 補強停損摘要與 `PROGRESS.md` 範本：新增「試過但無效的做法」一節（2026-10-19）
4. 新增「商業軟體式專案資料夾收納」規則、擴大支援 OpenCode 與 Codex、新增 AI 生圖規範（優先 Codex `$imagegen`／`codex-imagegen-bridge`，其次 Gemini `gemini-3.1-flash-image` 或更高）（2026-10-24）

## 二、使用者已確認的事

- 功能對照表只收 coding agent（Claude Code、Antigravity、Codex、OpenCode），不收聊天介面；檔名用 `coding_agent_features.md`（2026-10-19；2026-10-24 擴充）
- 對照表每 1 個月重新查證一次（2026-10-19）
- 規則要讓各家 coding agent 都看得懂，預留新增其他 coding agent 的擴充性（2026-10-19）
- 啟用 Claude Code「兩者都讀」設定（`instructionFiles: claude-md-and-agents-md`），由 `install.bat`／`install.sh` 在開發機設定；fork 別人的專案保留原有 `CLAUDE.md`，自己的規則寫在 `AGENTS.md`（2026-10-19）
- 停損時摘要寫進 `PROGRESS.md`，只 commit `PROGRESS.md`、改壞的程式碼不 commit；最後一個正常運作的 commit 由使用者告知（2026-10-19）
- 不另加「審查先看 `git diff`」的獨立條文，併在停損條文的括號說明裡（2026-10-19）
- 「有沒有讀到 `AGENTS.md`」改由 Claude Code 開新對話時自行比對，寫在全域規則（寫在 `AGENTS.md` 會跟著被跳過）；`/memory` 留作人工確認（2026-10-19）
- 專案資料夾收納採「商業軟體式（根目錄極簡化）」：根目錄只留啟動器（`.bat`、`.cmd`、`.vbs`、`.exe`、`.sh`）、說明書、AI 規則檔与頂層環境設定；程式碼、素材、設定、測試一律收進子資料夾（2026-10-24）
- 全域規則擴大安裝至 Codex（`~/.codex/AGENTS.md`）與 OpenCode（`~/.config/opencode/AGENTS.md`），三台電腦皆有安裝（2026-10-24）
- AI 生圖優先使用 Codex 內建 `$imagegen`（其他 agent 透過 `codex-imagegen-bridge` 呼叫 `codex exec`），其次使用 Antigravity 內建 `gemini-3.1-flash-image`（或更高），禁用第三方免費生圖或未授權付費 API（2026-10-24）

## 三、待使用者決定（下次討論從這裡開始）

1. ~~要不要啟用 Claude Code 的「Project instructions：兩者都讀」設定？~~（已決定啟用，見第二節）
2. ~~本倉庫的 `PROGRESS.md` 要不要比照新範本補上「試過但無效的做法」？~~（已決定補上，2026-10-19）

## 四、已查證的重要發現

- 詳見 `doc/coding_agent_features.md`（每列附查證日期與第五節官方網址）。
- GitSync 的提交按鈕只提交勾選的檔案（`GitSync_GUI.ps1` 的 `BtnCommit`，2026-10-19 讀程式碼確認），所以可以只提交 `PROGRESS.md`。

## 五、試過但無效的做法（接手者不要重複）

- 目前沒有。

## 六、下一步

1. ~~住家開發機拉取後重新執行安裝腳本，確認讀得到 `AGENTS.md`。~~（2026-10-19 完成：已安裝；`settings.json` 原本就存在，手動合併設定並備份；新對話確認載入了新版全域規則與本倉庫 `AGENTS.md`）
2. 在一個有 `CLAUDE.md` 的 fork 專案開新對話，確認 `CLAUDE.md` 與 `AGENTS.md` 都有載入（住家開發機目前沒有這種專案：`reverse.projects` 的 `rea/`、`ghidra/` 都沒有 `CLAUDE.md`）。
3. 2026-11-19 前後重新查證對照表。
4. 各專案舊的 `PROGRESS.md` 不強制更新，下次交接時再補「試過但無效的做法」；逆向分析專案下次開工時，把 `AGENTS.md` 的逆向規則區塊換成 2026-10-19 版。

## 七、接手須知（環境與工具）

- 修改後的驗證方式見 `AGENTS.md`。

## 八、修訂紀錄

| 日期 | 電腦 | 內容 |
|---|---|---|
| 2026-10-19 | 公司開發機 | 建立本檔；新增 coding agent 功能對照表與查證流程 |
| 2026-10-19 | 公司開發機 | 啟用「兩者都讀」設定，安裝腳本寫入 settings.json；README 重寫 |
| 2026-10-19 | 住家開發機 | 停損摘要補上失敗修法與最後正常 commit；PROGRESS 範本新增「試過但無效的做法」；逆向範本交接條文對應修改 |
| 2026-10-19 | 住家開發機 | 「確認方法」改成 Claude Code 自行比對是否讀到 `AGENTS.md`；對照表、README 同步 |
| 2026-10-19 | 住家開發機 | 第 5 節 PROGRESS 提交規則註明停損例外；停損條文註明接手者在同一台電腦 |
| 2026-10-24 | 住家開發機 | 新增商業軟體式資料夾收納規則；擴大支援 Codex 與 OpenCode；新增 AI 生圖優先順序與 Codex CLI bridge 規則 |
| 2026-10-25 | 住家開發機 | 安裝 `agy` CLI 1.4.7 並實測 `agy -p` 呼叫 `image-generator` 子代理；建立全域 `codex-imagegen-bridge` 與 `agy-imagegen-bridge` 技能並同步更新規則檔 |
