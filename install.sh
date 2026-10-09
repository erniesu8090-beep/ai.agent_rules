#!/usr/bin/env sh
# 安裝全域 AI Agent 規則（Linux / macOS）
#   global_rules.md + 本機標示 -> ~/.claude/CLAUDE.md（Claude Code）
#   global_rules.md + 本機標示 -> ~/.gemini/GEMINI.md（Antigravity）
# 既有檔案會先備份成 *.YYYYMMDD_HHMMSS.bak
# 用法：sh install.sh [home|dev|controlled]（不帶參數則詢問）
set -e
cd "$(dirname "$0")"
ts=$(date +%Y%m%d_%H%M%S)

machine="$1"
if [ -z "$machine" ]; then
    echo "這台是哪一台電腦？ [1] home 住家開發機  [2] dev 公司開發機  [3] controlled 管制機"
    printf "請輸入 1、2 或 3："
    read -r ans
    case "$ans" in
        1) machine=home ;; 2) machine=dev ;; 3) machine=controlled ;;
        *) echo "[ERROR] 請輸入 1、2 或 3"; exit 1 ;;
    esac
fi
case "$machine" in
    home|dev|controlled) ;;
    *) echo "[ERROR] 不認得的電腦代號：$machine"; exit 1 ;;
esac

src=$(mktemp)
tmp="$src"
trap 'rm -f "$tmp"' EXIT
{ cat global_rules.md; [ -f "machine_rules/$machine.md" ] && cat "machine_rules/$machine.md"; printf '\n---\nTHIS MACHINE: %s\n' "$machine"; } > "$src"

install_to() {
    dir="$1"
    dst="$dir/$2"
    mkdir -p "$dir"
    if [ -f "$dst" ]; then
        if cmp -s "$src" "$dst"; then
            echo "[SKIP] $dst 已是最新"
            return
        fi
        cp "$dst" "$dst.$ts.bak"
        echo "[BACKUP] $dst.$ts.bak"
    fi
    cp "$src" "$dst"
    echo "[OK] $dst"
}

install_to "$HOME/.claude" CLAUDE.md
install_to "$HOME/.gemini" GEMINI.md

# 工作區規則：本倉庫旁邊有 .workspace_rule 檔的資料夾，把 workspace_rules/<名稱>.md 複製成該資料夾的 AGENTS.md
for wsdir in ../*/; do
    [ -f "$wsdir.workspace_rule" ] || continue
    name=$(head -n 1 "$wsdir.workspace_rule" | tr -d ' \r\n')
    if [ ! -f "workspace_rules/$name.md" ]; then echo "[WARN] 找不到 workspace_rules/$name.md，略過 $wsdir"; continue; fi
    src="workspace_rules/$name.md"
    install_to "${wsdir%/}" AGENTS.md
done
echo "[DONE] 已安裝為 $machine，請重新啟動 Claude Code / Antigravity 以載入新規則"
