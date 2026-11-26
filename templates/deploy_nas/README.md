# NAS 容器部署與發布規範指南

> 本指南彙整系統部署至公司內網 NAS（Synology Container Manager / QNAP Container Station / Docker）的完整實務規範。
> 包含標準容器規則、GitSync 發布排除與線上資料庫保護、Port 規劃與操作流程。

---

## 一、標準專案目錄結構

需要部署至 NAS 的專案，建議採用以下標準目錄布局：

```text
<專案根目錄>/
├── deploy/
│   └── nas/
│       ├── Dockerfile              # NAS 容器建置設定 (Python 3.13 + 時區 + 中文字型)
│       ├── docker-compose.yml      # Compose 服務定義檔 (Port 映射、Volume 掛載)
│       ├── env.nas.example         # NAS 專案環境變數範例檔
│       └── README.md               # 專案專屬的 NAS 操作手冊
├── .dockerignore                   # Docker 映像檔建置排除規則
├── core/                           # 後端業務核心邏輯
├── static/                         # 前端靜態資源 (HTML / JS / CSS)
├── output/                         # 報表匯出與動態產出資料夾
├── logs/                           # 運行日誌目錄
├── requirements.txt                # 專案 Python 相依套件清單 (鎖定版本)
└── main.py                         # 系統伺服器主程式入口
```

> 註：上圖為既有多專案沿用的容器入口布局；若依全域規則第 5 節採根目錄極簡化（程式碼收進 `src/`），請對應調整 `docker-compose.yml` 掛載路徑與 `Dockerfile` 的 `CMD` 入口。

---

## 二、GitSync 發布規範（排除規則與資料庫保護）

專案發布至 NAS 建議一律透過 `GitSync` 的**「網頁發布」**分頁進行，兼具自動版本差異比對、發布前自動備份（`.backups/`）、線上資料庫保護與發布後提示。

在 `bundle.gitsync\config\GitSync_GUI.targets.json` 的配置規範如下：

```json
{
    "Name": "某系統（\\docker\\sample_project）",
    "Project": "my_workspace\\sample_project",
    "Subdir": "",
    "BackupName": "nas",
    "ServerPaths": [
        "\\\\<NAS_IP>\\docker\\sample_project",
        "\\\\<NAS_HOST>\\docker\\sample_project"
    ],
    "Url": "http://<NAS_IP>:<PORT>/",
    "ExcludeDirs": [
        "__pycache__",
        ".git",
        ".vscode",
        ".agents",
        ".venv",
        "runtime",
        "logs",
        "temp",
        "scratch",
        "output",
        "tests",
        "example",
        "portable",
        ".trash",
        ".backup"
    ],
    "ExcludeFiles": [
        ".server.pid",
        ".stopping",
        ".env",
        ".env.*",
        "PROGRESS.md",
        "*.pyc",
        "*.pyo",
        "*.log",
        "*.bak",
        "*.bak_*",
        "*.tmp",
        "*.zip",
        "*.lnk",
        "Thumbs.db",
        "desktop.ini",
        "~$*"
    ],
    "ProtectFiles": [
        "*.csv",
        "*.xlsx",
        "*.xls",
        "update_log.json",
        "presets.json"
    ],
    "RemindPatterns": [
        "*.py",
        "requirements.txt"
    ],
    "RemindText": "已更新 Python 程式碼或 requirements.txt：請至 NAS 的 Container Manager 重新建置／重啟容器以生效。若僅更新 static 網頁，瀏覽器按 Ctrl+F5 即可。"
}
```

### 規則重點說明：
1. **多伺服器路徑容錯 (`ServerPaths`)**：
   - 同時填寫 IP（`\\<NAS_IP>\docker\...`）與 NetBIOS 主機名稱（`\\<NAS_HOST>\docker\...`）。
   - Windows 網路認證是依主機名稱/IP 分開記錄；發布時 GitSync 會依序嘗試，避免單一路徑因名稱解析失敗而卡住。
2. **嚴格排除上傳清單 (`ExcludeDirs` / `ExcludeFiles`)**：
   - 排除版本庫（`.git`）、AI 與 IDE 設定（`.agents`, `.vscode`）。
   - 排除本機開發環境與快取（`.venv`, `runtime`, `__pycache__`, `*.pyc`）。
   - 排除機密檔案（`.env`, `.env.*`）：線上 NAS 應維持獨立的 `.env`，防止開發機本機金鑰或離線設定覆蓋線上正式設定。
   - 排除進度與日誌（`PROGRESS.md`, `*.log`, `output/`, `temp/`）。
3. **線上受保護檔案 (`ProtectFiles`)**：
   - 線上 NAS 常作為歷史資料庫或記錄即時業務數據（如 `*.csv`, `*.xlsx`, `update_log.json`）。
   - 發布時 GitSync 預設不勾選覆寫這些檔案，防止本機開發測試資料覆蓋線上同仁累積的正式資料。
4. **發布後智慧提醒 (`RemindPatterns` & `RemindText`)**：
   - 當發布檔案包含 `*.py` 或 `requirements.txt` 時，發布完成自動跳出彈窗，提醒工程師前往 NAS 重啟容器。若僅更動靜態網頁（HTML/CSS/JS），則告知僅需 Ctrl+F5 強制重新整理。

---

## 三、NAS 容器規格與設定原則

### 1. Dockerfile 規範
- **容器 Python 3.13**：以 `python:3.13-slim` 為基底（容器內部隔離，不受管制機本機 Python 3.11 限制）。
- **時區設定**：設定 `TZ=Asia/Taipei`，安裝 `tzdata` 並建立 `/etc/localtime` 軟連結，確保日誌與資料庫時間為 UTC+8（台灣標準時間）。
- **繁體中文字型**：安裝 `fonts-noto-cjk`（思源黑體），避免使用 Matplotlib、ReportLab 等匯出圖表或 PDF 報表時出現中文亂碼豆腐塊。
- **無快取安裝**：執行 `pip install --no-cache-dir -r requirements.txt` 並清除 apt 暫存目錄（`rm -rf /var/lib/apt/lists/*`），縮減鏡像體積。

### 2. Docker Compose 與連接埠規劃
- **連接埠 (Port) 防衝突**：
  - NAS 上通常同時運行多個系統。宿主機的預設 Port（如 `8080`）若已被其他系統使用，新建專案必須規劃獨立 Port（例如 `8081`、`8082` 等）。
  - Compose 寫法：`ports: - "8081:8080"`（外部 8081 映射至容器內部 8080）。
- **資料卷掛載 (Volumes)**：
  - 核心程式碼與靜態資源採目錄映射（`core/`, `static/`, `main.py`），日常小修補發布後重啟容器即可生效，免去每次重新 Build Image 的等待。
  - 資料目錄（`data/`, `output/`, `logs/`）掛載至宿主機，保障數據持久化。
  - `.env` 採唯讀掛載（`- ../../.env:/app/.env:ro`），確保設定檔安全性。

---

## 四、NAS 操作步驟 (以 Synology Container Manager 為例)

1. **首次建立專案**：
   - 透過 GitSync「網頁發布」將專案發布至 NAS（例如 `\\<NAS_IP>\docker\<project_name>`）。
   - **首次啟動前**：在 NAS 專案根目錄複製 `deploy/nas/env.nas.example` 為 `.env` 並填入線上設定，且確認 `core/`、`static/`、`data/`、`output/`、`logs/` 目錄已存在（避免 Docker 掛載時將缺漏的 `.env` 或目錄自動建為空資料夾）。
   - 登入 NAS DSM 網頁介面 ➔ 打開 **Container Manager**。
   - 點選 **專案 (Project)** ➔ **建立**：
     - 專案名稱：填寫專案名稱（全小寫連字號）。
     - 路徑：選擇發布的目錄下的 `deploy/nas`。
     - 來源：選擇現有的 `docker-compose.yml`。
   - 點選下一步完成建立並啟動。
2. **日常更新與維護**：
   - 透過 GitSync 發布新版本檔案。
   - 若僅修改靜態網頁（`static/`）：免重啟，瀏覽器按 `Ctrl+F5` 即可。
   - 若修改 Python 程式碼（`core/` 或 `main.py`）：在 Container Manager 專案點選 **重新啟動**。
   - 若修改了 `requirements.txt` 或 Dockerfile：在 Container Manager 專案點選 **動作** ➔ **建置 (Build)**，重新建置完成後再啟動。

---

## 五、特殊架構：反向中繼快遞模式

若專案需要存取受廠區防火牆限制的核心內部系統（NAS 無法直連，僅管制機可直連），且管制機受本機防火牆保護無法被主動連入：
- 請參閱獨立架構指南：[`REVERSE_RELAY_GUIDE.md`](./REVERSE_RELAY_GUIDE.md)。
