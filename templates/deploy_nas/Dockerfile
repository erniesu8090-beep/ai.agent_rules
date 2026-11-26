# ==============================================================================
# NAS Docker 容器建置腳本範本 (Python 3.13)
# 適用於 Synology Container Manager / QNAP Container Station / 標準 Docker
# ==============================================================================

FROM python:3.13-slim

WORKDIR /app

# 1. 設定台灣時區 (Asia/Taipei, UTC+8)
# 2. 安裝 tzdata (時區資料庫) 與 fonts-noto-cjk (Google 思源黑體，避免 Matplotlib / 報表中文方塊亂碼)
# 3. 清理 apt 快取以精簡映像檔體積
ENV TZ=Asia/Taipei
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && apt-get update && apt-get install -y --no-install-recommends \
    tzdata \
    fonts-noto-cjk \
    && rm -rf /var/lib/apt/lists/*

# 最佳化 Python 執行環境：關閉標準輸出緩衝區、避免產生 .pyc 檔案
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# 優先安裝套件相依性（利用 Docker 快取層機制，當套件清單無變更時可極速建置）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製專案其餘檔案（注意：.dockerignore 會自動排除 .git, .venv, logs, .env 等）
COPY . .

# 宣告容器對外預設服務埠（內部預設 8080，外部 Port 映射由 docker-compose.yml 決定）
EXPOSE 8080

# 預設啟動命令：以伺服器純背景模式啟動
CMD ["python", "main.py", "--server-only", "--host", "0.0.0.0", "--port", "8080"]
