#!/usr/bin/env python3
"""Antigravity Stop Hook (ag_stop_card_guard.py) 自動化單元測試。"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
HOOKS_DIR = REPO_ROOT / "templates" / "hooks"
SCRIPT_PATH = HOOKS_DIR / "ag_stop_card_guard.py"
if str(HOOKS_DIR) not in sys.path:
    sys.path.insert(0, str(HOOKS_DIR))

import ag_stop_card_guard as guard  # noqa: E402


def _write_transcript(tmp_dir: Path, records: list[dict]) -> Path:
    path = tmp_dir / "transcript.jsonl"
    lines = [json.dumps(r, ensure_ascii=False) for r in records]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _run_hook_cli(payload_raw: str) -> tuple[int, dict]:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT_PATH)],
        input=payload_raw,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )
    out = json.loads(proc.stdout) if proc.stdout.strip() else {}
    return proc.returncode, out


class TestAgStopCardGuard(unittest.TestCase):
    def test_1_real_missed_card_colon_tail(self) -> None:
        """命中：本對話第 1 回合真實漏發文本應回傳 decision=continue。"""
        content = (
            "已先檢查本機設定，先回報已查證的現況：\n"
            "1. 規則檔版本正常。\n\n"
            "請先幫我勾選以下三個問題，讓我精準對症下藥（找出根因再規劃解法）："
        )
        with tempfile.TemporaryDirectory() as td:
            tp = _write_transcript(
                Path(td),
                [
                    {"source": "USER_EXPLICIT", "type": "USER_INPUT", "content": "偶爾漏發圖卡"},
                    {"source": "MODEL", "type": "PLANNER_RESPONSE", "content": content},
                ],
            )
            payload = {
                "conversationId": "conv_test_01",
                "terminationReason": "NO_TOOL_CALL",
                "continuationActive": False,
                "transcriptPath": str(tp),
            }
            rc, out = _run_hook_cli(json.dumps(payload, ensure_ascii=False))
            self.assertEqual(rc, 0)
            self.assertEqual(out.get("decision"), "continue")
            self.assertIn("ask_question", out.get("reason", ""))

    def test_2_widget_pointer_without_tool(self) -> None:
        """命中：明確寫出透過下方卡片確認卻未呼叫工具應攔截。"""
        content = "以上分析完成，請透過下方卡片確認處理方向。"
        with tempfile.TemporaryDirectory() as td:
            tp = _write_transcript(
                Path(td),
                [
                    {"source": "USER_EXPLICIT", "type": "USER_INPUT", "content": "幫我規劃"},
                    {"source": "MODEL", "type": "PLANNER_RESPONSE", "content": content},
                ],
            )
            out = guard.evaluate_stop_payload(
                {
                    "terminationReason": "NO_TOOL_CALL",
                    "continuationActive": False,
                    "transcriptPath": str(tp),
                }
            )
            self.assertEqual(out.get("decision"), "continue")

    def test_3_plain_text_option_list_fallback(self) -> None:
        """命中：純文字選項清單替代圖卡且要求回覆編號應攔截。"""
        content = (
            "我有兩種做法可以處理：\n"
            "1. (Recommended) JSON 方案 — 免安裝資料庫\n"
            "2. SQLite 方案 — 支援大量查詢\n\n"
            "請問要採用哪一個方案？請回覆編號 1 或 2。"
        )
        with tempfile.TemporaryDirectory() as td:
            tp = _write_transcript(
                Path(td),
                [
                    {"source": "USER_EXPLICIT", "type": "USER_INPUT", "content": "怎麼存資料"},
                    {"source": "MODEL", "type": "PLANNER_RESPONSE", "content": content},
                ],
            )
            out = guard.evaluate_stop_payload(
                {
                    "terminationReason": "NO_TOOL_CALL",
                    "continuationActive": False,
                    "transcriptPath": str(tp),
                }
            )
            self.assertEqual(out.get("decision"), "continue")

    def test_4_already_called_tool_passes(self) -> None:
        """放行：已有 tool_calls 記錄時不應重複攔截。"""
        content = "請先幫我勾選以下三個問題："
        with tempfile.TemporaryDirectory() as td:
            tp = _write_transcript(
                Path(td),
                [
                    {"source": "USER_EXPLICIT", "type": "USER_INPUT", "content": "測試"},
                    {
                        "source": "MODEL",
                        "type": "PLANNER_RESPONSE",
                        "content": content,
                        "tool_calls": [{"name": "ask_question"}],
                    },
                ],
            )
            out = guard.evaluate_stop_payload(
                {
                    "terminationReason": "NO_TOOL_CALL",
                    "continuationActive": False,
                    "transcriptPath": str(tp),
                }
            )
            self.assertEqual(out, {})

    def test_5_normal_technical_explanation_passes(self) -> None:
        """放行：單純技術說明條列（未要求選擇方案）不誤攔。"""
        content = (
            "這個錯誤主要由兩個原因造成：\n"
            "1. 路徑使用了相對目錄。\n"
            "2. 編碼未指定 UTF-8。\n\n"
            "建議先檢查啟動目錄設定。"
        )
        self.assertIsNone(guard.detect_missing_card(content))

    def test_6_normal_completion_yes_no_passes(self) -> None:
        """放行：正常完工回報加簡單是非題不誤攔。"""
        content = "修改已完成並通過全部測試，需要我幫你 commit 嗎？"
        self.assertIsNone(guard.detect_missing_card(content))

    def test_7_phrase_inside_code_block_passes(self) -> None:
        """放行：程式碼區塊內含引導文字，或導語冒號後緊接程式碼區塊皆不誤攔。"""
        content = (
            "以下是範例文字，不要照寫：\n"
            "```markdown\n"
            "請選擇以下選項：\n"
            "```\n"
            "以上是需要注意的規則說明。"
        )
        self.assertIsNone(guard.detect_missing_card(content))

        content_trailing_code = (
            "請確認以下設定項目：\n"
            "```json\n"
            '{"enabled": true}\n'
            "```"
        )
        self.assertIsNone(guard.detect_missing_card(content_trailing_code))

    def test_8_continuation_active_prevents_loop(self) -> None:
        """放行：continuationActive 為 True 時不再觸發，防止無限迴圈。"""
        content = "請選擇以下方案："
        with tempfile.TemporaryDirectory() as td:
            tp = _write_transcript(
                Path(td),
                [
                    {"source": "USER_EXPLICIT", "type": "USER_INPUT", "content": "測試"},
                    {"source": "MODEL", "type": "PLANNER_RESPONSE", "content": content},
                ],
            )
            out = guard.evaluate_stop_payload(
                {
                    "terminationReason": "NO_TOOL_CALL",
                    "continuationActive": True,
                    "transcriptPath": str(tp),
                }
            )
            self.assertEqual(out, {})

    def test_9_fail_open_on_other_reasons_and_errors(self) -> None:
        """放行：非 NO_TOOL_CALL、損毀 JSON、不存在檔案、空 stdin 皆 Fail-Open 回傳 {}。"""
        self.assertEqual(
            guard.evaluate_stop_payload(
                {
                    "terminationReason": "USER_CANCELED",
                    "continuationActive": False,
                    "transcriptPath": "nonexistent.jsonl",
                }
            ),
            {},
        )
        for bad_input in ["", "   ", "{bad json", json.dumps({"terminationReason": "NO_TOOL_CALL", "transcriptPath": "no_such_file.jsonl"})]:
            rc, out = _run_hook_cli(bad_input)
            self.assertEqual(rc, 0)
            self.assertEqual(out, {})


if __name__ == "__main__":
    unittest.main()
