# 腳本編碼與跨平台規範（`guidelines/script_encoding.md`）

> 本檔由 `global_rules.md` 第 7 節外移，撰寫或修改 `.bat`、`.vbs`、`.ps1`、`.sh` 及跨平台路徑／執行指令時遵守。

## 1. 路徑與一般文字檔

- **路徑**：不硬編碼磁碟代號（`C:\`、`D:\`）與反斜線，改用 `pathlib.Path` 並以程式所在位置推算專案路徑；檔名大小寫保持一致（Linux 區分大小寫）。
- **文字檔編碼**：`.py`、`.json`、`.md`、`.html`、`.csv` 等文字檔統一使用 UTF-8；Python 開檔明確指定 `encoding="utf-8"`（給 Excel 開啟的 CSV 使用 `utf-8-sig`）。
- **Python 內嵌多行 HTML/JS**：一律使用原始字串 `r"""..."""`（避免 `\r?\n`、`^\uFEFF` 等正規式被 Python 轉義成換行致 `<script>` 語法崩潰），產出後抽 `<script>` 以 `node --check` 驗證（2026-11-05 實測）。

## 2. Windows 腳本規範

| 副檔名 | 換行 | 編碼要求 | 語法與執行注意事項 |
|---|---|---|---|
| `.bat` / `.cmd` | CRLF | **預設僅用 ASCII（英文）**；確需中文存 **ANSI / Big5（CP950）**（禁 UTF-8） | 1. 開頭加 `cd /d "%~dp0"`，路徑變數加雙引號。<br>2. 用 CP950 時避開次位元組為 `\`、`\|`、`^` 的字（許、功、蓋）。<br>3. 雙擊啟動 `.ps1` 寫 `powershell -NoProfile -ExecutionPolicy Bypass -File`（管制機終端不可直接執行含 Bypass 的命令，詳見 `machine_rules/controlled.md`）。 |
| `.vbs` | CRLF | **僅用 ASCII** | `shell.Run` 啟 GUI 禁設 `0`（`SW_HIDE`）；防搶焦點與管制機防毒（禁呼 `Shell.Application`）限制下，啟 GUI 置頂優先用 `.cmd`／`.bat` 搭 `start`。 |
| `.ps1` | CRLF | 含中文必須存 **UTF-8 with BOM** | 管制機或同事機主控台為 Windows PowerShell 5.1（字碼頁 950），**禁用 PS7 語法**（`?.`、`??`、`&&`／`||`、三元 `a ? b : c`、`ConvertFrom-Json -AsHashtable`、`ForEach-Object -Parallel`）。 |

## 3. Linux 腳本與跨平台相容

- **`.sh`**：使用 **LF** 換行並賦予執行權限（`chmod +x`）。
- **跨平台分流**：Python 程式需同時支援 Windows 與 Linux 時，Windows 專屬指令（`taskkill`、`netstat`、`start`、`cmd.exe` 等）須以 `sys.platform` 分流並提供 Linux 對應實作。
