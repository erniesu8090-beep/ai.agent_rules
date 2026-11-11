# PROGRESS　進度與交接

> 最後更新：2026-11-10（住家開發機）
> 新對話接手：先讀 `AGENTS.md` → 本檔 → `README.md`「三、檔案總覽」

## 一、目前階段

**維護中**。已完成：

1. 建立 coding agent 功能對照表 `docs/coding_agent_features_table.md`（2026-10-19 全面查證；2026-10-24 新增 Codex、OpenCode；2026-10-28 更新 OpenCode V2；2026-11-02～11-03 新增 Plugins 與四大工具子代理跨模型調度對照）
2. 建立每月重新查證流程（README「coding agent 功能查證」）與規則依據對照（對照表第三節）
3. 補強停損摘要與 `PROGRESS.md` 範本：新增「試過但無效的做法」一節（2026-10-19）
4. 新增規格檔範本 `templates/SPEC.md`，全域規則第 4、5 節加入 SPEC.md 的用法（2026-10-20）
5. 新增 Colab 筆記本排版規範 `templates/colab_notebook.md` 與骨架 `templates/colab_notebook.ipynb`；全域規則第 5 節「專案內資料夾」加指引（2026-10-20）
6. 管制機防毒行為監控與視窗相容：新增 VBS 限制（禁止呼叫 `Shell.Application`）、GUI 啟動優先使用 `.cmd` 搭配 `start`、桌面工具完工收納與 PDF 手冊、Tkinter 高 DPI 與動態尺寸規則（2026-10-20～2026-10-21）
7. 新增「商業軟體式專案資料夾收納（根目錄極簡化）」規則、擴大支援 Codex 與 OpenCode、新增 AI 生圖規範（優先 Codex `$imagegen`／`codex-imagegen-bridge`，其次 Gemini `gemini-3.1-flash-image`／`agy-imagegen-bridge` 與 429 防鎖自保機制）（2026-10-24～2026-10-26）
8. 納入 OpenCode V2：安裝目的地加 `~/.config/opencode/AGENTS.md`，安裝腳本另建 `~/.config/opencode/opencode.jsonc`（工作區規則 `instructions` ＋ 敏感路徑／`git push` 權限）；對照表加 OpenCode 欄、README 與全域規則同步（2026-10-28）
9. 完成第一次 harness 稽核（A～J 稽核清單），套用 P1～P6：全域規則補上下文管理、驗收標準、大改動先給計畫、高風險變更獨立審查；修正 `permissions.deny` 跨資料夾措辭、`machine_rules` 引用、第 4 節重複句；`templates/PROGRESS.md` 補 commit 欄位（2026-10-29）
   - 稽核結論：C（上下文管理）、G（獨立審查）原本未通過，已補；E（強制機制）仍只有文字＋`permissions.deny`，hook 未採用；`feature_list.json` 不採用（與 `SPEC.md`、`PROGRESS.md` 重複）
   - 未採用：P7（月度稽核清單 `docs/harness_audit.md`）、P8（hook 強制擋 `git push`，需先查證格式並實測）
10. 技術文件整併與英文精確命名：整理為 5 份主文件（`ai_agent_engineering.md`、`coding_agent_features_table.md`、`claude_code_permissions_deny.md`、`rule_maintenance_sop.md`、`verification_sources.md`）（2026-10-29～2026-10-31）
11. 比對 AI Agent 實戰影片（子代理、權限與刪除、Loop Engineering）補強規則與文件：`global_rules.md` 補兩段式刪除、防間接提示詞注入與子代理安全邊界；`ai_agent_engineering.md` 補四問排查、人肉迴圈、核准疲勞可逆分流與子代理五問；`rule_maintenance_sop.md` 補固化三件套（2026-10-31）
12. 完成全專案一致性盤點與修正（12 項）：對齊 SOP「兩段式刪除」、對照表 `permissions.deny` 範例、`verification_sources.md` 狀態標示、`templates/.gitignore` 與三份 `AGENTS` 範本註解、`install.bat`／`install.sh` 檢查 `git push` 與開頭檢查，並清理過時檔案引用（2026-10-31）
13. 提問卡片全面取代手動指令（Vibe Coding 化）：取消日常手動打 `/plan /grill-me` 起手式，改由全域規則開頭與第 9 節強制觸發互動式提問卡片（門檻調整為 3 檔以上、跨檔案連動、單檔大改或有 2 種做法），並在卡片中動態整合「① 規劃方案與影響檔案、② 自我迴圈驗證方式、③ 合適時加問子代理」（2026-10-31）
14. 完成各家 coding agent「Plugins 插件體系」與「四大工具子代理跨模型調度」全面查證與對照表補齊（2026-11-02～2026-11-03）：查證 Claude Code、Antigravity（v2.28.2 Marketplace、Partner 插件、Accounts OAuth）、Codex 與 OpenCode V2（`@opencode/plugin`、原生異質多模型子代理），更新 `docs/coding_agent_features_table.md`、`docs/ai_agent_engineering.md`、`docs/verification_sources.md`。
15. 全域規則瘦身與個人環境拆分、雙向完整融合住家開發機（11/03 版）與管制機版本（2026-11-03）：將個人四機表格、GitSync 與 `.bundle` 跨機同步、Python 3.11 細節及 `google.cloud_oauth.relay` 拆至 `machine_rules/personal.md`，安裝腳本新增 `general`（通用／同事）模式；納入 OpenCode CLI 子代理選模型卡片與 `< nul` 防卡死規範；同時完整保留四家工具（含 Codex）安裝、商業軟體收納／PDF 手冊／Tkinter 高 DPI、管制機 VBS `Shell.Application` 防毒攔截與 AI 生圖規範，且最長的 `controlled` 合成後規則壓在 200 行上限內。
16. 沉澱 LLM 工具手腳架構與 Skill 實戰心得（2026-11-03）：於 `docs/ai_agent_engineering.md` 完整梳理 Rules/CLI/MCP/Skills/Plugins/Custom Agents 之 Token 代價與定位對照表，記錄免記指令語意自動路由（Semantic Triggering）、全域集中派發與漸進式揭露零污染機制、防過度工程防線，以及社群 Spec-Plan-Build 指令流 vs. 本倉庫規則自動攔截流之架構演進；同步更新 `docs/coding_agent_features_table.md` 2-2-1 節子代理定位。
17. 管制機部署 OpenCode CLI 與桌面 App 實測（2026-11-03～11-04）：實測確認管制機能連線 npm registry（`registry.npmjs.org`，HTTP 200）與 OpenCode 免費模型端點（`api.opencode.ai`，HTTP 200，但 `openrouter.ai` 與 `github.com` 連不上）；以系統內建 `tar.exe` 解壓獨立二進位檔 `@opencode/cli-windows-x64`（v2.2.5）至 `%LOCALAPPDATA%\Programs\opencode\bin` 並設 User PATH；OpenCode 桌面 App 實測確認載入 `~/.config/opencode/AGENTS.md`（自動辨識 `THIS MACHINE: controlled`），且 `DeepSeek V4.1 Flash Free` + `High` 連線正常。
18. OpenCode 子代理 Skill 化、強制鎖定 `--agent plan` 唯讀與動態工作池（Worker Pool，線上上限 3 個）（2026-11-04）：移除全域規則中的 OpenRouter 條文；將具體 CLI 指令與安全規範抽離為獨立 Skill `templates/skills/opencode-runner/SKILL.md`（預設帶入 `opencode/deepseek-v4.1-flash-free#high` 與 `--agent plan` 唯讀鎖定），並採用「階梯式錯峰啟動（間隔 5～10 秒）＋ 線上並行上限 3 個（Worker Pool）」動態遞補機制；由 `install.bat` 與 `install.sh` 的 `:deploy_skills` 自動派發至各 Agent 全域技能目錄。
19. 跨機同步規則精簡與快取命中（Prompt Caching）強化（2026-11-04）：將 `machine_rules/personal.md` 跨機同步長文字精簡為 1 條核心指引；`global_rules.md` 第 9 節明訂「除錯後經驗沉澱」於任務收尾時寫入專案 `AGENTS.md`；三份專案範本（`templates/AGENTS*.md`）將「已知的坑」移至全檔最末尾（公司與逆向範本置於標記區塊結束之後）。
20. 雙向完整融合管制機 11/04 版、獨立 `SKILL.md` 與本工作區版本（2026-11-05）：完整合入 `opencode-runner` Skill 動態工作池、`--agent plan` 唯讀鎖定、安裝腳本四家工具全域 Skill 自動派發、快取命中設計、LLM 工具手腳架構與管制機實測紀錄，同時 100% 保留四家工具（含 Codex）支援、商業軟體收納／PDF 手冊／Tkinter 高 DPI、VBS 防毒限制與 AI 生圖規範。
21. 合成規則排版與同主題列點精簡（2026-11-06）：在不刪減任何規則、實測結論與日期的前提下，整併 `global_rules.md`（135 → 67 行）、`machine_rules/personal.md`（23 → 19 行）與 `machine_rules/controlled.md`（32 → 22 行），使最長的 `controlled` 合成後規則從 195 行降至 113 行（預留 87 行空間）。
22. 打包與分發 Google Flow 跨專案生圖與生片技能（2026-11-07）：建立 `templates/skills/google-flow-bridge/SKILL.md`，支援自動偵測工作區路徑、免 API Key 直接消耗 Google Flow 點數與每日配額生成 Nano Banana 2K 圖片、Veo 720p 影片、Extend 接續生成與分鏡故事板管線；同步由安裝機制派發至四大 Agent 全域技能目錄（`~/.claude/skills/`、`~/.codex/skills/`、`~/.config/opencode/skills/`、`~/.gemini/config/skills/`）。
23. 收錄 Three.js r170 現代 Web 3D 與互動檢視器技能（2026-11-08）：建立 `templates/skills/threejs/SKILL.md`，收錄最新繁中文件（r170）、現代 ES Module / Import Map 單檔架構、本地 3D 模型載入（GLTF/GLB 自適應相機視距）、材質光影與記憶體防洩漏（dispose）規範；同步納入四大 Agent 全域技能派發機制。
24. 收錄 Gemini Web 網頁版免費額度生圖技能（`gemini-web-imagegen`）並列為生圖第三優先備援（2026-11-08）：建立 `templates/skills/gemini-web-imagegen/`（含 `SKILL.md` 與 `scripts/gemini_web_gen.py`），整合 `gemini-webapi` 2.x 與 Chromium CDP 無頭自動提取 `__Secure-1PSID`／`__Secure-1PSIDTS` 機制，支援跨專案 2K 文生圖與 Image-to-Image 改圖，並由安裝腳本統一派發至四大 Agent 全域技能目錄。
25. 雙向融合 GitHub 遠端技能更新與管制機規則精簡版（2026-11-09）：合入 Google Flow、Three.js、Gemini Web 生圖三大通用技能；保留管制機 11/06 規則排版精簡成果（`global_rules.md` 67 行），合成後維持 113 行且無衝突完成同步。
<<<<<<< HEAD
26. 規則與技能一致性盤點與清理（2026-11-09）：移除 `google-flow-bridge/SKILL.md` 硬編碼個人帳號路徑與 `gemini_web_gen.py`／`gemini-web-imagegen/SKILL.md` 的硬編碼磁碟代號，改為動態推算與檢查 `gemini_webapi` 套件；同步補齊 `coding_agent_features_table.md` 與 `verification_sources.md` 的生圖備援對照，並更新 `AGENTS.md`／`rule_maintenance_sop.md` 的技能安裝驗證預期行數（20 行 skills）。
=======
26. 技能全面解耦與雙庫分工定案（2026-11-10）：將 templates/skills/ 舊目錄徹底解耦移出（移入 _pending_delete/），Web 3D 技能 threejs 正式移入獨立技能母本庫 ai.agent_skills/project/threejs/；install.bat 與 install.sh 精簡並改為自動偵測連動呼叫 ai.agent_skills\deploy_global_skills，實現「規則掌管思想邊界、技能掌管外掛手腳」之乾淨對稱雙庫架構。
>>>>>>> refs/remotes/colab/main

## 二、使用者已確認的事

- 收錄 Three.js 繁中文件與指引為通用技能（Skill）（2026-11-08）：依 CS2680 與「能不放全域就不放」原則，不寫入 `global_rules.md` 避免無關對話浪費 Token，採用通用技能 `templates/skills/threejs/SKILL.md`，在使用者提到「Three.js」、「Web 3D」、「WebGL 渲染」時才觸發，並由安裝腳本統一派發至四大 Agent 全域技能目錄。

- 雙庫解耦與 threejs 技能遷移定案（2026-11-10 使用者確認）：確立 ai.agent_rules（思想邊界憲法）與 ai.agent_skills（工具手腳母本）獨立雙庫對稱架構；templates/skills/ 舊目錄徹底移出至 _pending_delete/，threejs 技能遷入 ai.agent_skills/project/threejs/ 作為專案備用母本，並由 install.bat 與 install.sh 自動偵測連動呼叫 deploy_global_skills，實現單一入口一鍵安裝。

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
- Windows Python Tkinter 視窗工具：啟用高 DPI 感知（`SetProcessDpiAwareness(1)`）、原生 `vista` 佈景主題與動態尺寸計算（`update_idletasks()` + `winfo_reqwidth()`／`winfo_reqheight()`），避免高縮放比例下文字模糊或被截斷（2026-10-21）
- 技術文件等參考檔案一律放 `docs/`，不用 `doc/`；全域規則第 5 節「專案內資料夾」加入這條，工作區所有專案統一改名（2026-10-22）
- 專案資料夾收納採「商業軟體式（根目錄極簡化）」：根目錄只留啟動器（`.bat`、`.cmd`、`.vbs`、`.exe`、`.sh`）、說明書、AI 規則檔與頂層環境設定；程式碼、素材（`assets/`）、設定（`config/`）、測試一律收進子資料夾；桌面工具完工時操作手冊 PDF 放根目錄、`AGENTS.md` 設 Windows 隱藏（2026-10-21、2026-10-24）
- 全域規則擴大安裝至 Codex（`~/.codex/AGENTS.md`）與 OpenCode（`~/.config/opencode/AGENTS.md`）；開發機使用四家（Claude Code、Antigravity、Codex、OpenCode），管制機無法使用 Claude Code 與 Codex（僅使用 Antigravity、OpenCode）（2026-10-24；2026-10-31 修正）
- AI 生圖優先使用 Codex 內建 `$imagegen`（其他 agent 透過 `codex-imagegen-bridge` 呼叫 `codex exec`；管制機因無法連線 Codex 生圖，直接走第二優先），其次使用 Antigravity 內建 `gemini-3.1-flash-image`（其他 agent 透過 `agy-imagegen-bridge` 呼叫 `agy -p`），禁用第三方免費生圖或未授權付費 API；Gemini 批次生圖腳本強制間隔 15～20 秒與 60 秒退避機制（2026-10-24～2026-10-27）
- Colab 硬體加速器（GPU）規範：確立 L4（24GB，CP值最高/最省點數）、A100（40GB/80GB，極速）、G4（Blackwell 架構 RTX PRO 6000 Server 等級，最快旗艦）之算力分級與定位；明確標註「成片畫質與物理效果由模型與參數決定，L4/A100/G4 輸出品質完全一致，僅推論耗時與顯存不同」；已更新 `templates/colab_notebook.md` 與骨架 `templates/colab_notebook.ipynb`（2026-10-24）
- Claude Code 資安防凍結規則：`.claudeignore` 實測無效，改以 `settings.json` 的 `permissions.deny` 阻擋讀取 `google.cloud_oauth.relay`（不加通用檔名規則），保留敏感專案交由 Antigravity 等其他 agent 處理的分流原則；新建專案時跳出卡片選項詢問是否套用，既有專案有需要時再請 agent 建立；先寫進本倉庫 README 與安裝腳本範本（2026-10-24）
- 除錯後經驗沉澱規則：除錯或被糾正後，僅篩選外部資料/環境陷阱與測試破口，先提案經確認後補入專案 `AGENTS.md`，淘汰已根治舊坑維持 10 條／200 行上限（2026-10-25）
- 2026-10-25 改進清單核定事項（原清單已刪除，需要時查 Git 歷史）：(1) `~/.claude/settings.json` 範本與安裝腳本同時寫入新舊兩個外掛 ID（`agents-md@builtin` 與 `cc-plugin-agents-md@builtin`），安裝腳本僅在有安裝 `claude` CLI 時提示版本；(2) 本倉庫保留個人工具專案名稱 `google.cloud_oauth.relay` 與公開網域 `*.googleapis.com` 連線紀錄（於 `AGENTS.md` 註明例外），並將所有網路阻擋原因敘述統一簡化為「無法連線」及移除誇張用語。
- 納入 OpenCode V2（2026-10-28）：沿用同一份 `global_rules.md`，裝到 `~/.config/opencode/AGENTS.md`，並由安裝腳本建立 `opencode.jsonc` 指定工作區規則與權限；commit 署名用 `Co-authored-by: OpenCode <noreply@opencode.ai>`。
- harness 稽核第一輪只採用文字類改善 P1～P6；`feature_list.json` 不採用（改由 `SPEC.md` 功能清單＋`PROGRESS.md` 記錄）；hook 強制與月度稽核清單暫不採用（2026-10-29 使用者決定）。
- 技術文件整併為 5 份英文精確命名文件（`ai_agent_engineering.md`、`coding_agent_features_table.md`、`claude_code_permissions_deny.md`、`rule_maintenance_sop.md`、`verification_sources.md`）；刪除過渡期索引檔、舊主文件與封存目錄，舊檔需要時查 Git 歷史（2026-10-29～2026-10-31 使用者決定）。
- 管制機執行安裝腳本時維持現狀（照建 `~/.config/opencode/` 與 `~/.codex/` 設定檔）；`machine_rules/controlled.md` 保留防毒產品名稱「Apex One」（2026-10-31 使用者決定）。
- 提問卡片全面取代背指令（推翻 2026-10-25「以 `/plan /grill-me` 為日常起手式」做法）：使用者只用白話講需求，不記斜線指令（指令僅留對照表第二節備查）；修改 3 個檔案以上、跨檔案連動、單檔大改、新規劃或有 2 種做法時一律先跳提問卡片（整併第 9 節大改動門檻），卡片採用「動態智慧加題」（必問 ① 規劃方案與預計影響檔案、② 自我迴圈驗證方式；任務適合子代理時動態加問 ③ 是否派子代理分工／唯讀挑錯）（2026-10-31 使用者決定）。
- 對照表 2-2 節新增 Plugins 列與 2-2-1 四大工具子代理跨模型調度對照，完整收錄查證網址（2026-11-02～2026-11-03 使用者要求）。
- OpenCode CLI 子代理評估與部署（2026-11-03 使用者決定）：已在住家開發機安裝全域 CLI `@opencode/cli`（v2.2.5），確認可透過 `opencode run --auto --model <模型>` 作為非互動式背景子代理（具第二視角審查、不耗主力 token）。
- OpenCode 調用提問卡片與防卡死規則（2026-11-03 使用者決定）：當使用者提出調用 OpenCode 時，強制跳出卡片選擇執行模型：(1) `(Recommended) OpenCode Free (DeepSeek V4.1 Flash Free)`（免費免額度，適合一般唯讀審查與檢查）、(2) `OpenRouter (DeepSeek V4.1 Flash 1017)`（走 OpenRouter 帳號，最新 1017 版本），指令一律強制帶 `--auto` 並以 `cmd /c` 包裹、末尾帶 `< nul` 立即關閉 stdin 管道避免卡死。
- `global_rules.md` 通用化瘦身與個人環境拆分、雙向融合（2026-11-03 使用者決定）：為方便分享給同事且避免同事 AI 誤認電腦為 Win10 22H2 管制機，將個人四機環境表格、跨機 `.bundle`／GitSync 流程、個人專案領域、Python 3.11 補充與 `google.cloud_oauth.relay` 拆入 `machine_rules/personal.md`；安裝腳本新增 `general`（通用／同事）模式（僅載入 `global_rules.md` 與通用設定），`home`／`dev`／`controlled` 則自動附加 `personal.md`（管制機再附加 `controlled.md`），並完整保留四家工具（含 Codex）與管制機實測規範，所有模式合成後均維持在 200 行內。
- OpenCode 子代理 Skill 化、強制 `--agent plan` 唯讀與動態工作池（2026-11-04 使用者決定）：(1) 因管制機無法連線 OpenRouter API，從全域規則移除 OpenRouter 選項，改為提問說明中的自選模型提醒（非 Recommended）；(2) 調用細節封裝為獨立 Skill `templates/skills/opencode-runner/SKILL.md`，預設為 `opencode/deepseek-v4.1-flash-free#high` 並強制帶 `--agent plan` 鎖定唯讀模式；(3) 多子代理調用採用「階梯式錯峰啟動（間隔 5～10 秒）＋ 線上並行上限 3 個（Worker Pool）」動態遞補模式，兼顧防範 429 併發限速與最小化等待時間；(4) 由 `install.bat` 與 `install.sh` 自動將 `templates/skills/` 派發至各 Agent 全域技能目錄（`~/.claude/skills/`、`~/.gemini/config/skills/`、`~/.codex/skills/`、`~/.config/opencode/skills/`）。
- 跨機同步規則精簡與快取命中強化規則（2026-11-04 使用者決定）：將 `machine_rules/personal.md` 跨機同步長文字精簡為 1 條核心指引；`global_rules.md` 第 9 節明訂經驗沉澱於任務收尾時寫入專案 `AGENTS.md`（避免對話中途改常駐規則破壞快取）；三份專案範本 `templates/AGENTS*.md` 將「已知的坑」移至全檔最末尾（公司與逆向範本放在標記區塊結束之後）。

## 三、待使用者決定（下次討論從這裡開始）

- （目前無待決定事項）

## 四、已查證的重要發現

- 詳見 `docs/coding_agent_features_table.md`（每列附查證日期與第六節官方網址）。
- GitSync 的提交按鈕只提交勾選的檔案（`GitSync_GUI.ps1` 的 `BtnCommit`，2026-10-19 讀程式碼確認），所以可以只提交 `PROGRESS.md`。
- 管制機端點防毒行為監控（Apex One）：VBScript 呼叫 `Shell.Application`（`ShellExecute`）叫起外部程式會被端點防毒直接攔截並發出資安告警；啟動 GUI 程式優先使用 `.cmd`／`.bat` 的 `start`（2026-10-20 在管制機實測）。
- 管制機對外網路實測（2026-10-22、2026-10-27，測試方式：`curl.exe -I`／`Test-NetConnection`）：
  - 核心端點對照實測結果：
    - `generativelanguage.googleapis.com`（Gemini 核心模型）：可連（HTTP 404）
    - `cloudaicompanion.googleapis.com`（AI 寫程式助理專用端點）：可連（HTTP 404）
    - `www.googleapis.com`（Google 核心 API 基礎架構）：可連（HTTP 404）
    - `dl.google.com`（下載伺服器）：可連（HTTP 302）
    - `script.google.com`（GAS 中繼）：可連
    - `registry.npmjs.org`（npm 官方套件端點，2026-11-03 實測）：可連（HTTP 200）。
    - `api.opencode.ai`（OpenCode 官方免費模型端點，2026-11-03 實測）：可連（HTTP 200）。
    - `oauth2.googleapis.com`（OAuth 授權端點）：管制機無法連線。
    - `openrouter.ai`（OpenRouter 授權端點，2026-11-03 實測）：管制機無法連線（Proxy 連線逾時／ECONNREFUSED）。
    - `github.com`（GitHub 網站／API，2026-11-03 實測）：管制機無法連線（SSL 握手失敗）。
    - OpenAI / Codex 生圖服務：管制機無法連線（2026-10-27 實測），在管制機上生圖直接走 Antigravity `image-generator` 子代理。
  - **意義**：管制機本地 Antigravity 的模型連線可直接連通 Google 官方伺服器；OpenCode CLI 與桌面 App 可直連 npm 與官方免費模型端點（如 `deepseek-v4.1-flash-free#high`），僅 OAuth 換證端點、OpenRouter 與 Codex 生圖無法連線。
- **OpenCode 桌面 App 規則載入實測（2026-11-04，截圖驗證）**：
  - OpenCode 桌面 App 在 Windows 啟動時會自動讀取 `~/.config/opencode/AGENTS.md`，開新對話直接依規則主動反映本機身分（`THIS MACHINE: controlled`）並嚴格遵循繁體中文與提問先行規則。
  - GUI 介面下切換 OpenRouter 模型（如 `deepseek-v4.1-flash-1017`）確切拋出 `ECONNREFUSED`（證實受限於公司防火牆阻擋），而切換 `DeepSeek V4.1 Flash Free` 搭配 `High` 思考深度連線暢通、正常對答。
- **Anthropic Claude 安全審查機制與風控查證（2026-10-22、2026-10-25 更新）**：
  - 查證證實：Anthropic 自動化安全審查器對「網路代理 / 隧道中繼 / 網路規避 / 低階 hook」等內容極度敏感，讀到會出現 `This request triggered cyber-related safeguards` 並凍結對話（多次觸發有無帳號風險為使用者回報推論，官方條款查不到，列入月度查證；詳見 `docs/claude_code_permissions_deny.md`）。
  - 確立處置規則：敏感專案（目前為 `google.cloud_oauth.relay`）一律交由 **Claude Code 以外的 coding agent（如：Antigravity）** 處理；技術阻擋改用 `.claude/settings.json` 的 `permissions.deny`（阻擋 `Read(./**/google.cloud_oauth.relay/**)`；注意 `./` 相對路徑以啟動資料夾為起點，跨資料夾保護尚待實測），並在 `global_rules.md` 第 4、8 節明定新建專案詢問機制、禁止 Bash 繞道讀取、禁止 `/security-review` 與觸發錯誤時的處置步驟。

## 五、試過但無效的做法（接手者不要重複）

- 在管制機上用 VBScript 啟動 GUI 程式：`shell.Run command, 0, False` 的參數 `0` 會隱藏視窗（SW_HIDE）；改用 `1` 則因父程序結束觸發 Windows 防止搶焦點機制被壓在底層；改用 `Shell.Application`（`ShellExecute`）則被端點防毒（Apex One）攔截。結論：需要啟動 GUI 程式並置頂顯示時，直接使用 `.cmd` 搭配 `start` 最相容穩定（2026-10-20 實測）。
- 以工作區與專案目錄的 `.claudeignore` 隔離敏感專案（2026-10-22 設定，實測無法阻止 Claude Code 讀取或觸發資安審查凍結；2026-10-24 改用 `settings.json` 的 `permissions.deny` 與規則條文限制）。
- 在 Windows 子進程或背景執行 OpenCode CLI 未關閉 stdin：OpenCode 會因等待 stdin EOF 而卡死（Empty log）；必須以 `cmd /c` 包裹並在末尾加 `< nul` 立即關閉 stdin 管道（2026-11-03 實測）。
- 在 Python 腳本內以一般三引號字串 `"""..."""` 內嵌含 JavaScript 的 HTML 範本：JS 正規表示式（如 `split(/\r?\n/)`、`replace(/^\uFEFF/, "")`）會被 Python 轉義成實體換行，導致瀏覽器載入時發生 `SyntaxError: Invalid regular expression: missing /` 讓整段 `<script>` 失效；必須使用原始字串 `r"""..."""` 並抽取 `<script>` 以 `node --check` 驗證語法（2026-11-05 實測）。

## 六、下一步

1. 在管制機雙擊 `install.bat`（選 `3` controlled）更新本機規則，並清空或刪除 `_pending_delete/` 資料夾；後續透過 GitSync / `.bundle` 同步回公司開發機與住家開發機重新執行 `install.bat`。
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
     - 任務 D（牽連 3 個以上檔案或大改動的任務）：預期跳卡片（一次問齊 ① 規劃與影響檔案清單、② 自我迴圈驗證、③ 是否派子代理分工／審查）。
7. OpenCode 驗收（2026-10-28 加入，2026-11-04 更新）：
   - 在專案資料夾開新對話，確認讀到全域規則（最後一行 `THIS MACHINE`）與專案 `AGENTS.md`；再開 `D:\AI_Workspace` 底下的專案，確認工作區 `AGENTS.md`（若存在）有載入（靠 `opencode.jsonc` 的 `instructions`）。
   - 確認提問卡片走 `question` 工具（需求模糊或有兩種做法時）。
   - 住家開發機、公司開發機與管制機三台均已完成 `@opencode/cli`（v2.2.5）部署，支援 `opencode run --agent plan` 與免費模型（如 `opencode/deepseek-v4.1-flash-free#high`、`opencode/glm-5.3-flash-free#high`）。管制機以免安裝獨立版運作，連線走官方 `api.opencode.ai`。
   - 待使用者手動以提示詞實測調用 OpenCode 做唯讀審查之穩定度與效果。
8. 若之後要補 P8（hook 強制擋 `git push`）：先查 Claude Code `hooks` 與 Antigravity `.agents/hooks.json` 官方格式，在開發機實測後才寫進安裝腳本。

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
| 2026-10-20 | 管制機 | 新增 VBS GUI 啟動限制與管制機 Shell.Application 防毒行為監控規則（global_rules、machine_rules、templates） |
| 2026-10-20 | 管制機 | 納入 OpenCode（對照表、global_rules、install.bat/sh、AGENTS.md、README） |
| 2026-10-21 | 公司開發機 | 公司範本 2026-10-21：跨專案規範審查改為「註明參與的專案才適用」，清單放各參與專案 `docs/`、內容相同、同時更新；README 同步 |
| 2026-10-21 | 住家開發機 | 逆向範本 2026-10-21：合併研究用規則（原本在 `reverse.projects/AGENTS.md`），分共通／修改檔案時／研究用；工作區規則只留不能進倉庫的資訊與 fork 規則，全域規則第 5 節、README 同步 |
| 2026-10-21 | 管制機 | 新增桌面工具完工收納、圖文操作手冊 PDF、Windows Tkinter 高 DPI 與動態尺寸規則（global_rules、README） |
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
| 2026-10-27 | 管制機 | 雙向合併 `ai.agent_rules-main`，納入 Codex、選項卡片提問規則、商業軟體收納與生圖規範，保留管制機防毒實測與 Tkinter 規則 |
| 2026-10-27 | 管制機 | 實測管制機無法連線 Codex 生圖，更新 machine_rules、global_rules、README 與本檔指引直接改走 Antigravity |
| 2026-10-28 | 公司開發機 | 納入 OpenCode V2：安裝腳本加 `~/.config/opencode/AGENTS.md` 與 `opencode.jsonc`；對照表全面加 OpenCode 欄並補查證來源 |
| 2026-10-29 | 住家開發機 | 完成 harness 稽核（A～J）並套用 P1～P6：全域規則新增「先說清楚怎樣算做完」「大改動先給計畫」「高風險變更獨立審查」與「上下文管理」小節 |
| 2026-10-29 | 公司開發機 | 技術文件整併並改英文精確命名（`ai_agent_engineering.md`、`coding_agent_features_table.md`、`claude_code_permissions_deny.md`、`rule_maintenance_sop.md`、`verification_sources.md`） |
| 2026-10-31 | 公司開發機 | 技術文件整併為 5 份；lightweight 併入對照表第五節；刪除 00_index 與 docs/archive/ |
| 2026-10-31 | 住家開發機 | 依實戰影片補強規則與文件（M1～M5）：global_rules 補兩段式刪除、防提示詞注入與子代理邊界；ai_agent_engineering 補排查四問、人肉迴圈、核准疲勞與子代理五問；rule_maintenance_sop 補固化三件套；完成全專案一致性修正與提問卡片全面取代手動指令 |
| 2026-10-31 | 住家開發機 | 整合 Downloads 版（10/31）與本工作區版本（10/26）：以 10/31 版為基底，併入 Codex 支援、商業軟體式根目錄收納規則、AI 生圖優先順序與 Gemini 429 防鎖規範；舊 `doc/` 目錄依兩段式刪除移至資源回收筒，並通過全部 4 項收尾驗證 |
| 2026-11-02 | 管制機 | 雙向融合住家 10/31 版與管制機 10/27 版：升級至 10/31 全部新規則與 5 份 `docs/` 技術文件，同時完整保留管制機 VBS `Shell.Application` 防毒攔截、Windows Tkinter 高 DPI 與動態尺寸、桌面工具完工收納 PDF 手冊及管制機 Codex 生圖限制；舊 `doc/` 與 `workspace_rules/` 依兩段式刪除移至 `_pending_delete/` |
| 2026-11-03 | 住家開發機 | 安裝 `@opencode/cli` 全域 CLI（v2.2.5）；新增調用 OpenCode 跳卡片選模型（Free 與 OpenRouter 1017，強制加 `--auto`）與 `< nul` 防 stdin 卡死規則；完成 Plugins 與四大工具子代理跨模型調度對照；拆分個人環境至 `machine_rules/personal.md` 並新增 `general` 通用安裝模式 |
| 2026-11-03 | 管制機 | 雙向完整融合住家 11/03 版與管制機 11/02 版：導入 `machine_rules/personal.md` 個人拆分架構、`general` 通用模式、OpenCode CLI 調用規範、Plugins 與子代理跨模型對照表，同時完整保留四家工具（含 Codex）安裝、商業軟體收納／PDF 手冊／Tkinter 高 DPI、管制機 VBS `Shell.Application` 防毒攔截與 AI 生圖規範，且 `controlled` 合成總行數壓在 200 行內 |
| 2026-11-03 | 公司開發機 | 安裝 `@opencode/cli` 全域 CLI（v2.2.5）；OpenCode 子代理參數鎖定 `#high` 思考深度；梳理 LLM 工具手腳定位表、免記指令語意路由（Semantic Triggering）與全域派發架構，更新 `ai_agent_engineering.md` 與 `coding_agent_features_table.md` |
| 2026-11-03 | 管制機 | 實測並以獨立二進位檔完成 OpenCode CLI（v2.2.5）部署，驗證端點連線（`api.opencode.ai` 可連、`openrouter.ai` 被擋）與免額度模型背景調用 |
| 2026-11-04 | 管制機 | 實測 OpenCode 桌面 App 確認載入 `~/.config/opencode/AGENTS.md`；強化快取命中設計（經驗沉澱於收尾寫入、三份 `templates/AGENTS*.md` 將已知的坑移至末尾）；精簡 `personal.md` 跨機同步條文；建置 `templates/skills/opencode-runner/SKILL.md`（強制 `--agent plan` 唯讀鎖定與動態工作池 Worker Pool 線上上限 3 個），並於 `install.bat`／`install.sh` 實裝全域 Skill 自動派發機制 |
| 2026-11-05 | 住家開發機 | 雙向完整融合 Downloads 11/04 版、獨立 `SKILL.md` 與本工作區版本：合入 `opencode-runner` 動態工作池、`--agent plan` 唯讀鎖定、四家工具全域 Skill 自動派發、快取命中設計、LLM 工具手腳架構與管制機實測紀錄，同時完整保留四家工具（含 Codex）支援、商業軟體收納／PDF 手冊／Tkinter 高 DPI、VBS 防毒限制與 AI 生圖規範，通過全部 4 項驗證並實裝至本機 |
| 2026-11-05 | 管制機 | `global_rules.md` 第 7 節補入「Python 內嵌多行 HTML/JS 範本一律使用原始字串 `r"""..."""` 並以 `node --check` 驗證 `<script>` 語法」規則（不增加行數，維持 137 行） |
| 2026-11-06 | 管制機 | 雙向融合 GitHub 遠端（住家 11/05 版含 opencode-runner）與管制機 11/05 原始字串規則更新；精簡 `global_rules.md`（67 行）、`personal.md`（19 行）與 `controlled.md`（22 行）排版與同主題列點，最長 `controlled` 合成規則降至 113 行 |
| 2026-11-07 | 住家開發機 | 打包與分發 Google Flow 技能（templates/skills/google-flow-bridge/SKILL.md）至四大 Agent 技能庫，支援 Nano Banana 2K 生圖、Veo 720p 生片、Extend 與 Storyboard |
| 2026-11-08 | 住家開發機 | 收錄 Three.js r170 技能（templates/skills/threejs/SKILL.md）與 Gemini Web 網頁版免費額度生圖技能（templates/skills/gemini-web-imagegen/），更新 global_rules 與 README 將 Gemini Web 列為生圖第三優先備援並派發至四大 Agent 全域技能庫 |
| 2026-11-09 | 管制機 | 雙向融合遠端 GitHub 11/07～11/08 新增技能（Google Flow、Three.js、Gemini Web 生圖）與管制機 11/06 規則精簡版，排除衝突完成同步並執行安裝腳本驗證 |
| 2026-11-09 | 管制機 | 完成全專案規則與通用技能一致性檢視與 5 項清理：移除技能內個人帳號與磁碟硬編碼、強化 `gemini-webapi` 環境偵測、補齊對照表與查證來源總表、更新技能驗證預期行數 |
| 2026-11-10 | 住家開發機 | 將技能母本徹底解耦移往獨立倉庫 ai.agent_skills，精簡 install.bat 與 install.sh 為自動連動部署，確立雙庫乾淨對稱分工 |
