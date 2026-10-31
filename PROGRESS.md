# PROGRESS　進度與交接

> 最後更新：2026-10-31（住家開發機）
> 新對話接手：先讀 `AGENTS.md` → 本檔 → `README.md`「三、檔案總覽」

## 一、目前階段

**維護中**。已完成：

1. 建立 coding agent 功能對照表 `docs/coding_agent_features_table.md`（2026-10-19 全面查證；2026-10-24 新增 Codex、OpenCode；2026-10-28 更新 OpenCode V2）
2. 建立每月重新查證流程（README「coding agent 功能查證」）與規則依據對照（對照表第三節）
3. 補強停損摘要與 `PROGRESS.md` 範本：新增「試過但無效的做法」一節（2026-10-19）
4. 新增規格檔範本 `templates/SPEC.md`，全域規則第 4、5 節加入 SPEC.md 的用法（2026-10-20）
5. 新增 Colab 筆記本排版規範 `templates/colab_notebook.md` 與骨架 `templates/colab_notebook.ipynb`；全域規則第 5 節「專案內資料夾」加指引（2026-10-20）
6. 新增「商業軟體式專案資料夾收納（根目錄極簡化）」規則、擴大支援 Codex 與 OpenCode、新增 AI 生圖規範（優先 Codex `$imagegen`／`codex-imagegen-bridge`，其次 Gemini `gemini-3.1-flash-image`／`agy-imagegen-bridge` 與 429 防鎖自保機制）（2026-10-24～2026-10-26）
7. 納入 OpenCode V2：安裝目的地加 `~/.config/opencode/AGENTS.md`，安裝腳本另建 `~/.config/opencode/opencode.jsonc`（工作區規則 `instructions` ＋ 敏感路徑／`git push` 權限）；對照表加 OpenCode 欄、README 與全域規則同步（2026-10-28）
8. 完成第一次 harness 稽核（A～J 稽核清單），套用 P1～P6：全域規則補上下文管理、驗收標準、大改動先給計畫、高風險變更獨立審查；修正 `permissions.deny` 跨資料夾措辭、`machine_rules` 引用、第 4 節重複句；`templates/PROGRESS.md` 補 commit 欄位（2026-10-29）
   - 稽核結論：C（上下文管理）、G（獨立審查）原本未通過，已補；E（強制機制）仍只有文字＋`permissions.deny`，hook 未採用；`feature_list.json` 不採用（與 `SPEC.md`、`PROGRESS.md` 重複）
   - 未採用：P7（月度稽核清單 `docs/harness_audit.md`）、P8（hook 強制擋 `git push`，需先查證格式並實測）
9. 技術文件整併與英文精確命名：整理為 5 份主文件（`ai_agent_engineering.md`、`coding_agent_features_table.md`、`claude_code_permissions_deny.md`、`rule_maintenance_sop.md`、`verification_sources.md`），過渡期索引檔與舊 `doc/` 目錄已移至資源回收筒或可查 Git 歷史（2026-10-29～2026-10-31）
10. 比對 AI Agent 實戰影片（子代理、權限與刪除、Loop Engineering）補強規則與文件：`global_rules.md` 補兩段式刪除、防間接提示詞注入與子代理安全邊界；`ai_agent_engineering.md` 補四問排查、人肉迴圈、核准疲勞可逆分流與子代理五問；`rule_maintenance_sop.md` 補固化三件套（2026-10-31）
11. 完成全專案一致性盤點與修正（12 項）：對齊 SOP「兩段式刪除」、對照表 `permissions.deny` 範例、`verification_sources.md` 狀態標示、`templates/.gitignore` 與三份 `AGENTS` 範本註解、`install.bat`／`install.sh` 檢查 `git push` 與開頭檢查，並清理過時檔案引用（2026-10-31）
12. 提問卡片全面取代手動指令（Vibe Coding 化）：取消日常手動打 `/plan /grill-me` 起手式，改由全域規則開頭與第 9 節強制觸發互動式提問卡片（門檻調整為 3 檔以上、跨檔案連動、單檔大改或有 2 種做法），並在卡片中動態整合「① 規劃方案與影響檔案、② 自我迴圈驗證方式、③ 合適時加問子代理」；完成 Downloads（10/31）版與本工作區獨有內容（Codex 支援、商業軟體式根目錄收納、AI 生圖與防鎖規範）之完整整合（2026-10-31）

## 二、使用者已確認的事

- 功能對照表只收 coding agent（Claude Code、Antigravity、Codex、OpenCode），不收聊天介面；檔名用 `coding_agent_features_table.md`（2026-10-19；2026-10-24 擴充；2026-10-29 改名）
- 對照表每 1 個月重新查證一次（2026-10-19）
- 規則要讓各家 coding agent 都看得懂，預留新增其他 coding agent 的擴充性（2026-10-19）
- 啟用 Claude Code「兩者都讀」設定（`instructionFiles: claude-md-and-agents-md`），由 `install.bat`／`install.sh` 在開發機設定；fork 別人的專案保留原有 `CLAUDE.md`，自己的規則寫在 `AGENTS.md`（2026-10-19）
- 停損時摘要寫進 `PROGRESS.md`，只 commit `PROGRESS.md`、改壞的程式碼不 commit；最後一個正常運作的 commit 由使用者告知（2026-10-19）
- 不另加「審查先看 `git diff`」的獨立條文，併在停損條文的括號說明裡（2026-10-19）
- 「有沒有讀到 `AGENTS.md`」改由 Claude Code 開新對話時自行比對，寫在全域規則（寫在 `AGENTS.md` 會跟著被跳過）；`/memory` 留作人工確認（2026-10-19）
- Colab 筆記本排版：只針對 Colab；規則 `templates/colab_notebook.md` 與骨架 `templates/colab_notebook.ipynb` 都做；先用 pdf2epub 的 `layout_trial.ipynb`（雲端硬碟）試改一份，使用者看過試作版確認風格後定案；筆記本放專案的 `colab/`（2026-10-20）
- 開新專案一律先寫 `SPEC.md`（網頁或任何 coding agent 都可以寫），之後由使用者決定交給哪個 coding agent 寫程式；開發中保留當「要做什麼」的依據，第一版必做功能完成、使用者實測確認後，把內容搬到 README／AGENTS／PROGRESS 再刪除（2026-10-20）
- 同一類專案共用的規則寫成範本規則區塊、貼進每個專案，不放分類資料夾的 `AGENTS.md`（Antigravity 讀不到、也不會跨電腦同步）；分類資料夾的 `AGENTS.md` 只放不能進倉庫的資訊與 fork 規則（2026-10-21）
- 逆向範本合併「修改用」與「研究用」兩種專案，規則區塊分共通／修改檔案時／研究用三段；研究用專案也可以照「修改檔案時」改少數 byte（2026-10-21）
- 技術文件等參考檔案一律放 `docs/`，不用 `doc/`；全域規則第 5 節「專案內資料夾」加入這條，工作區所有專案統一改名（2026-10-22）
- 專案資料夾收納採「商業軟體式（根目錄極簡化）」：根目錄只留啟動器（`.bat`、`.cmd`、`.vbs`、`.exe`、`.sh`）、說明書、AI 規則檔與頂層環境設定；程式碼、素材（`assets/`）、設定（`config/`）、測試一律收進子資料夾（2026-10-24）
- 全域規則擴大安裝至 Codex（`~/.codex/AGENTS.md`）與 OpenCode（`~/.config/opencode/AGENTS.md`）；開發機使用四家（Claude Code、Antigravity、Codex、OpenCode），管制機無法使用 Claude Code 與 Codex（僅使用 Antigravity、OpenCode）（2026-10-24；2026-10-31 修正）
- AI 生圖優先使用 Codex 內建 `$imagegen`（其他 agent 透過 `codex-imagegen-bridge` 呼叫 `codex exec`），其次使用 Antigravity 內建 `gemini-3.1-flash-image`（其他 agent 透過 `agy-imagegen-bridge` 呼叫 `agy -p`），禁用第三方免費生圖或未授權付費 API；Gemini 批次生圖腳本強制間隔 15～20 秒與 60 秒退避機制（2026-10-24～2026-10-26）
- Colab 硬體加速器（GPU）規範：確立 L4（24GB，CP值最高/最省點數）、A100（40GB/80GB，極速）、G4（Blackwell 架構 RTX PRO 6000 Server 等級，最快旗艦）之算力分級與定位；明確標註「成片畫質與物理效果由模型與參數決定，L4/A100/G4 輸出品質完全一致，僅推論耗時與顯存不同」；已更新 `templates/colab_notebook.md` 與骨架 `templates/colab_notebook.ipynb`（2026-10-24）
- Claude Code 資安防凍結規則：`.claudeignore` 實測無效，改以 `settings.json` 的 `permissions.deny` 阻擋讀取 `google.cloud_oauth.relay`（不加通用檔名規則），保留敏感專案交由 Antigravity 等其他 agent 處理的分流原則；新建專案時跳出卡片選項詢問是否套用，既有專案有需要時再請 agent 建立；先寫進本倉庫 README 與安裝腳本範本（2026-10-24）
- 除錯後經驗沉澱規則：除錯或被糾正後，僅篩選外部資料/環境陷阱與測試破口，先提案經確認後補入專案 `AGENTS.md`，淘汰已根治舊坑維持 10 條／200 行上限（2026-10-25）
- 2026-10-25 改進清單核定事項（原清單已刪除，需要時查 Git 歷史）：(1) `~/.claude/settings.json` 範本與安裝腳本同時寫入新舊兩個外掛 ID（`agents-md@builtin` 與 `cc-plugin-agents-md@builtin`），安裝腳本僅在有安裝 `claude` CLI 時提示版本；(2) 本倉庫保留個人工具專案名稱 `google.cloud_oauth.relay` 與公開網域 `*.googleapis.com` 連線紀錄（於 `AGENTS.md` 註明例外），並將所有網路阻擋原因敘述統一簡化為「無法連線」及移除誇張用語。
- 納入 OpenCode V2（2026-10-28）：沿用同一份 `global_rules.md`，裝到 `~/.config/opencode/AGENTS.md`，並由安裝腳本建立 `opencode.jsonc` 指定工作區規則與權限；commit 署名用 `Co-authored-by: OpenCode <noreply@opencode.ai>`。
- harness 稽核第一輪只採用文字類改善 P1～P6；`feature_list.json` 不採用（改由 `SPEC.md` 功能清單＋`PROGRESS.md` 記錄）；hook 強制與月度稽核清單暫不採用（2026-10-29 使用者決定）。
- 技術文件整併為 5 份英文精確命名文件（`ai_agent_engineering.md`、`coding_agent_features_table.md`、`claude_code_permissions_deny.md`、`rule_maintenance_sop.md`、`verification_sources.md`）；刪除過渡期索引檔、舊主文件與封存目錄，舊檔需要時查 Git 歷史（2026-10-29～2026-10-31 使用者決定）。
- 管制機執行安裝腳本時維持現狀（照建 `~/.config/opencode/` 與 `~/.codex/` 設定檔）；`machine_rules/controlled.md` 第 8 行保留防毒產品名稱「Apex One」（2026-10-31 使用者決定）。
- 提問卡片全面取代背指令（推翻 2026-10-25「以 `/plan /grill-me` 為日常起手式」做法）：使用者只用白話講需求，不記斜線指令（指令僅留對照表第二節備查）；修改 3 個檔案以上、跨檔案連動、單檔大改、新規劃或有 2 種做法時一律先跳提問卡片（整併第 9 節大改動門檻），卡片採用「動態智慧加題」（必問 ① 規劃方案與預計影響檔案、② 自我迴圈驗證方式；任務適合子代理時動態加問 ③ 是否派子代理分工／唯讀挑錯）（2026-10-31 使用者決定）。
- 版本整合（2026-10-31 使用者決定）：以 Downloads 版（10/31）為基底，完整併入本工作區獨有的 3 項內容（Codex 第四家工具支援、商業軟體式根目錄收納、AI 生圖與 Gemini 429 防鎖規範）。

## 三、待使用者決定（下次討論從這裡開始）

- （目前無待決定事項）

## 四、已查證的重要發現

- 詳見 `docs/coding_agent_features_table.md`（每列附查證日期與第六節官方網址）。
- GitSync 的提交按鈕只提交勾選的檔案（`GitSync_GUI.ps1` 的 `BtnCommit`，2026-10-19 讀程式碼確認），所以可以只提交 `PROGRESS.md`。
- 管制機對外網路實測（2026-10-22，測試方式：`curl.exe -I`／`Test-NetConnection`）：
  - 核心端點對照實測結果：
    - `generativelanguage.googleapis.com`（Gemini 核心模型）：可連（HTTP 404）
    - `cloudaicompanion.googleapis.com`（AI 寫程式助理專用端點）：可連（HTTP 404）
    - `www.googleapis.com`（Google 核心 API 基礎架構）：可連（HTTP 404）
    - `dl.google.com`（下載伺服器）：可連（HTTP 302）
    - `script.google.com`（GAS 中繼）：可連
    - `oauth2.googleapis.com`（OAuth 授權端點）：管制機無法連線。
  - **意義**：管制機本地 Antigravity 的模型連線可直接連通 Google 官方伺服器，僅 OAuth 換證端點無法連線。
- **Anthropic Claude 安全審查機制與風控查證（2026-10-22、2026-10-25 更新）**：
  - 查證證實：Anthropic 自動化安全審查器對「網路代理 / 隧道中繼 / 網路規避 / 低階 hook」等內容極度敏感，讀到會出現 `This request triggered cyber-related safeguards` 並凍結對話（多次觸發有無帳號風險為使用者回報推論，官方條款查不到，列入月度查證；詳見 `docs/claude_code_permissions_deny.md`）。
  - 確立處置規則：敏感專案（目前為 `google.cloud_oauth.relay`）一律交由 **Claude Code 以外的 coding agent（如：Antigravity）** 處理；技術阻擋改用 `.claude/settings.json` 的 `permissions.deny`（阻擋 `Read(./**/google.cloud_oauth.relay/**)`；注意 `./` 相對路徑以啟動資料夾為起點，跨資料夾保護尚待實測），並在 `global_rules.md` 第 4、8 節明定新建專案詢問機制、禁止 Bash 繞道讀取、禁止 `/security-review` 與觸發錯誤時的處置步驟。

## 五、試過但無效的做法（接手者不要重複）

- 以工作區與專案目錄的 `.claudeignore` 隔離敏感專案（2026-10-22 設定，實測無法阻止 Claude Code 讀取或觸發資安審查凍結；2026-10-24 改用 `settings.json` 的 `permissions.deny` 與規則條文限制）。

## 六、下一步

1. ~~住家開發機拉取後重新執行安裝腳本，確認讀得到 `AGENTS.md`。~~（2026-10-19 完成）
2. 在一個有 `CLAUDE.md` 的 fork 專案開新對話，確認 `CLAUDE.md` 與 `AGENTS.md` 都有載入（住家開發機目前沒有這種專案：`reverse.projects` 的 `rea/`、`ghidra/` 都沒有 `CLAUDE.md`）。
3. 2026-12-01 前後重新查證對照表（依每月的第 1 天原則排定，11/01 間隔太近略過）：
   - 官方更新紀錄查證：Claude Code `AskUserQuestion` 是否從 v2.0.21 起提供（目前標記第三方來源）。
   - 工具規範查證：Antigravity `ask_question` 工具參數是否公布獨立 `description` 欄位官方規範（目前標記本機實測）。
   - 風控條款查證：Claude safeguards 觸發多次是否有官方停權條款依據（目前標記推論）。
   - 新功能追蹤：Antigravity 是否新增類似 Auto Memory 的背景自動記憶機制；Antigravity 新 workflows 系統是否已公布。
   - 載入範圍查證：開啟分類資料夾當工作區時的規則載入範圍實測（是否僅到倉庫根目錄）。
4. 各專案舊的 `PROGRESS.md` 不強制更新，下次交接時再補「試過但無效的做法」；逆向分析專案下次開工時，把 `AGENTS.md` 的逆向規則區塊換成 2026-10-21 版。
5. Colab 排版規範：骨架只在本機用假的顯示函式測過進度表與失敗停止，還沒在 Colab 實跑；下次有專案用到 Colab 時實跑一次，確認 `StopRun` 不顯示錯誤追蹤、進度表會即時更新。
6. 待使用者實測驗收項目：
   - **實測 A（資安防凍結 `permissions.deny` 跨資料夾啟動）**：從「敏感專案所在資料夾（如 `google.cloud_oauth.relay`）」與「另一不相干專案資料夾」各開一次 Claude Code，請它讀取被擋資料夾檔案，預期兩邊皆回「被拒絕」；同時讀取正常檔案確認未誤擋。若跨資料夾無法擋住，需評估改為 `//` 絕對路徑規則。
   - **實測 B（免記指令提問卡片表現）**：開新對話直接用白話輸入需求（不打 `/plan`、`/grill-me`），測試四個任務：
     - 任務 A（需求模糊的新功能）：預期跳卡片（問 ① 規劃方案、② 自我迴圈驗證），不先改檔。
     - 任務 B（已明確指定的小修改如改一句文字）：預期不跳卡片，直接改檔。
     - 任務 C（有兩種做法的單檔修改）：預期跳卡片（問 ① 規劃方案、② 自我迴圈驗證；不適合子代理故不問第 ③ 題）。
     - 任務 D（牽連 3 個以上檔案或大改動）：預期跳卡片（一次問齊 ① 規劃與影響檔案清單、② 自我迴圈驗證、③ 是否派子代理分工／審查）。
7. OpenCode 驗收（2026-10-28 加入）：
   - 在專案資料夾開新對話，確認讀到全域規則（最後一行 `THIS MACHINE`）與專案 `AGENTS.md`；再開 `D:\AI_Workspace` 底下的專案，確認工作區 `AGENTS.md`（若存在）有載入（靠 `opencode.jsonc` 的 `instructions`）。
   - 確認提問卡片走 `question` 工具（需求模糊或有兩種做法時）。
8. 若之後要補 P8（hook 強制擋 `git push`）：先查 Claude Code `hooks` 與 Antigravity `.agents/hooks.json` 官方格式，在開發機實測後才寫進安裝腳本。
9. `global_rules.md`、安裝腳本與文件 2026-10-31 雙版本合併完成後：本機（住家開發機）完成驗證後重新執行 `install.bat`，並透過 GitSync 同步至公司開發機與管制機重新執行 `install.bat`。

## 七、接手須知（環境與工具）

- 修改後的驗證方式見 `AGENTS.md`。
- 規則放置原則見 `README.md` 第二節與全域規則第 5 節；跨專案共用文件放各參與專案 `docs/`。
- 分類資料夾本身不是 Git 倉庫、不跨電腦同步；Antigravity 找規則只到工作區根目錄（詳見 `docs/coding_agent_features_table.md`）。

## 八、修訂紀錄

| 日期 | 電腦 | 內容 |
|---|---|---|
| 2026-10-19 | 公司開發機 | 建立本檔；新增 coding agent 功能對照表與查證流程 |
| 2026-10-19 | 公司開發機 | 啟用「兩者都讀」設定，安裝腳本寫入 settings.json；README 重寫 |
| 2026-10-19 | 住家開發機 | 停損摘要補上失敗修法與最後正常 commit；PROGRESS 範本新增「試過但無效的做法」；逆向範本交接條文對應修改 |
| 2026-10-19 | 住家開發機 | 「確認方法」改成 Claude Code 自行比對是否讀到 `AGENTS.md`；對照表、README 同步 |
| 2026-10-19 | 住家開發機 | 第 5 節 PROGRESS 提交規則註明停損例外；停損條文註明接手者在同一台電腦 |
| 2026-10-20 | 公司開發機 | 新增 `templates/SPEC.md`；全域規則第 4、5 節與 README 加入 SPEC.md 的用法與刪除時機 |
| 2026-10-20 | 公司開發機 | 新增 Colab 筆記本排版規範與骨架；全域規則第 5 節、README 加指引 |
| 2026-10-21 | 公司開發機 | 公司範本 2026-10-21：跨專案規範審查改為「註明參與的專案才適用」，清單放各參與專案 `docs/`、內容相同、同時更新；README 同步 |
| 2026-10-21 | 住家開發機 | 逆向範本 2026-10-21：合併研究用規則（原本在 `reverse.projects/AGENTS.md`），分共通／修改檔案時／研究用；工作區規則只留不能進倉庫的資訊與 fork 規則，全域規則第 5 節、README 同步 |
| 2026-10-22 | 住家開發機 | 第七節彙整分類資料夾規則的制定方式、判斷順序、各分類現況與修改時要動的檔案 |
| 2026-10-22 | 住家開發機 | 本倉庫 `doc/` 改名為 `docs/`，所有引用一併修改；全域規則第 5 節與 README「專案內資料夾」加入 `docs/` 規定 |
| 2026-10-22 | 公司開發機 | 記錄管制機無法連線至 oauth2.googleapis.com 之實測結果與受影響範圍 |
| 2026-10-22 | 公司開發機 | 實測確認 generativelanguage、cloudaicompanion 等 AI 模型端點可連線，僅 OAuth 換證端點無法連線 |
| 2026-10-22 | 公司開發機 | 新增 AI 工具安全分流規範：涉網路穿透/代理之專案由 Claude Code 以外之 agent (如 Antigravity) 負責，配置 .claudeignore 隔離 |
| 2026-10-24 | 住家開發機 | 新增商業軟體式資料夾收納規則；擴大支援 Codex 與 OpenCode；新增 AI 生圖優先順序與 Codex CLI bridge 規則 |
| 2026-10-24 | 住家開發機 | 新增 Colab GPU (L4/A100/G4) 選項指引與特性說明至 templates/colab_notebook.md 與骨架，確立畫質相同僅耗時差異之核心原則 |
| 2026-10-24 | 住家開發機 | 依 `docs/claude_code_permissions_deny.md` 改寫 Claude 防凍結規則：移除無效的 `.claudeignore` 做法，改用 `settings.json` 的 `permissions.deny` 阻擋 `google.cloud_oauth.relay`、新建專案主動詢問是否套用 |
| 2026-10-25 | 住家開發機 | 安裝 `agy` CLI 1.4.7 並實測 `agy -p` 呼叫 `image-generator` 子代理；建立全域 `codex-imagegen-bridge` 與 `agy-imagegen-bridge` 技能並同步更新規則檔 |
| 2026-10-25 | 住家開發機 | 強化 `global_rules.md` 開頭與第 4 節「提問先行與互動式選項卡片」規則；新增 `global_rules.md` 第 9 節「除錯後經驗沉澱（先提案、確認後寫入）」規則；`settings.json` 同時寫入新舊外掛 ID |
| 2026-10-26 | 住家開發機 | 新增 Gemini 生圖頻率限制（RPM／429 冷卻）與防鎖自保機制說明至全域規則與 README |
| 2026-10-27 | 住家開發機 | 完成第一、二輪規則整理與精簡（P1～P8、C1～C9）：管制機清單移至 machine_rules、檔案與資料夾說明去重、資安與驗證精簡、README 與 docs 去重 |
| 2026-10-28 | 公司開發機 | 納入 OpenCode V2：安裝腳本加 `~/.config/opencode/AGENTS.md` 與 `opencode.jsonc`；對照表全面加 OpenCode 欄並補查證來源 |
| 2026-10-29 | 住家開發機 | 完成 harness 稽核（A～J）並套用 P1～P6：全域規則新增「先說清楚怎樣算做完」「大改動先給計畫」「高風險變更獨立審查」與「上下文管理」小節 |
| 2026-10-29 | 公司開發機 | 技術文件整併並改英文精確命名（`ai_agent_engineering.md`、`coding_agent_features_table.md`、`claude_code_permissions_deny.md`、`rule_maintenance_sop.md`、`verification_sources.md`） |
| 2026-10-31 | 公司開發機 | 技術文件整併為 5 份；lightweight 併入對照表第五節；刪除 00_index 與 docs/archive/ |
| 2026-10-31 | 住家開發機 | 依實戰影片補強規則與文件（M1～M5）：global_rules 補兩段式刪除、防提示詞注入與子代理邊界；ai_agent_engineering 補排查四問、人肉迴圈、核准疲勞與子代理五問；rule_maintenance_sop 補固化三件套；完成全專案一致性修正與提問卡片全面取代手動指令 |
| 2026-10-31 | 住家開發機 | 整合 Downloads 版（10/31）與本工作區版本（10/26）：以 10/31 版為基底，併入 Codex 支援、商業軟體式根目錄收納規則、AI 生圖優先順序與 Gemini 429 防鎖規範；舊 `doc/` 目錄依兩段式刪除移至資源回收筒，並通過全部 4 項收尾驗證 |
