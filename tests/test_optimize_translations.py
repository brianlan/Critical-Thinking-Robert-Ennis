import subprocess
import sys

import pytest

from scripts.bilingual_export.align import AlignedRow, Block
from scripts import optimize_translations


def make_row() -> AlignedRow:
    english = Block(
        index=0,
        block_type="paragraph",
        source_text="Original English.",
        content="Original English.",
        section_anchor="section",
        section_level=2,
        line_start=1,
        line_end=1,
    )
    chinese = Block(
        index=0,
        block_type="paragraph",
        source_text="原始译文。",
        content="原始译文。",
        section_anchor="section",
        section_level=2,
        line_start=1,
        line_end=1,
    )
    return AlignedRow(
        section_index=0,
        section_anchor="section",
        row_index=0,
        status="matched",
        english_block=english,
        chinese_block=chinese,
    )


def completed(stdout: str = "", stderr: str = "", returncode: int = 0) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(["opencode"], returncode, stdout, stderr)


def test_parse_args_defaults_timeout_and_retries(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "argv", ["optimize_translations.py"])

    args = optimize_translations.parse_args()

    assert args.timeout_seconds == 300
    assert args.max_retries == 2


def test_optimize_row_returns_translation_on_first_attempt(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = []

    def fake_run(command: list[str], timeout_seconds: int) -> subprocess.CompletedProcess[str]:
        calls.append((command, timeout_seconds))
        return completed("<translation>优化译文。</translation>")

    monkeypatch.setattr(optimize_translations, "run_llm_command", fake_run)

    optimized = optimize_translations.optimize_row(make_row(), timeout_seconds=12, max_retries=2)

    assert optimized.chinese_block.content == "优化译文。"
    assert len(calls) == 1
    assert calls[0][0][:3] == ["opencode", "run", "--pure"]
    assert calls[0][1] == 12


def test_optimize_row_retries_timeout_then_succeeds(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = []
    responses = [
        subprocess.TimeoutExpired(["opencode"], 12),
        completed("<translation>重试成功。</translation>"),
    ]

    def fake_run(command: list[str], timeout_seconds: int) -> subprocess.CompletedProcess[str]:
        calls.append((command, timeout_seconds))
        response = responses.pop(0)
        if isinstance(response, subprocess.TimeoutExpired):
            raise response
        return response

    monkeypatch.setattr(optimize_translations, "run_llm_command", fake_run)

    optimized = optimize_translations.optimize_row(make_row(), timeout_seconds=12, max_retries=2)

    assert optimized.chinese_block.content == "重试成功。"
    assert len(calls) == 2


def test_optimize_row_retries_nonzero_exit_then_succeeds(monkeypatch: pytest.MonkeyPatch) -> None:
    responses = [
        completed(stderr="failed", returncode=1),
        completed("<translation>恢复成功。</translation>"),
    ]

    def fake_run(command: list[str], timeout_seconds: int) -> subprocess.CompletedProcess[str]:
        return responses.pop(0)

    monkeypatch.setattr(optimize_translations, "run_llm_command", fake_run)

    optimized = optimize_translations.optimize_row(make_row(), timeout_seconds=12, max_retries=2)

    assert optimized.chinese_block.content == "恢复成功。"


def test_optimize_row_retries_missing_translation_tag_then_succeeds(monkeypatch: pytest.MonkeyPatch) -> None:
    responses = [
        completed("plain output"),
        completed("<translation>标签恢复。</translation>"),
    ]

    def fake_run(command: list[str], timeout_seconds: int) -> subprocess.CompletedProcess[str]:
        return responses.pop(0)

    monkeypatch.setattr(optimize_translations, "run_llm_command", fake_run)

    optimized = optimize_translations.optimize_row(make_row(), timeout_seconds=12, max_retries=2)

    assert optimized.chinese_block.content == "标签恢复。"


def test_optimize_row_returns_original_after_all_attempts_fail(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = []

    def fake_run(command: list[str], timeout_seconds: int) -> subprocess.CompletedProcess[str]:
        calls.append((command, timeout_seconds))
        return completed("plain output")

    monkeypatch.setattr(optimize_translations, "run_llm_command", fake_run)
    row = make_row()

    optimized = optimize_translations.optimize_row(row, timeout_seconds=12, max_retries=2)

    assert optimized is row
    assert len(calls) == 3


def test_run_llm_command_kills_process_group_on_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    created = {}
    killed = {}

    class FakeProcess:
        pid = 1234
        returncode = -9

        def __init__(self, command, stdout, stderr, text, start_new_session):
            created["command"] = command
            created["stdout"] = stdout
            created["stderr"] = stderr
            created["text"] = text
            created["start_new_session"] = start_new_session
            self.communicate_calls = 0

        def communicate(self, timeout=None):
            self.communicate_calls += 1
            if self.communicate_calls == 1:
                raise subprocess.TimeoutExpired(created["command"], timeout)
            created["communicate_after_kill"] = True
            return "partial stdout", "partial stderr"

    monkeypatch.setattr(optimize_translations.os, "name", "posix")
    monkeypatch.setattr(optimize_translations.subprocess, "Popen", FakeProcess)
    monkeypatch.setattr(optimize_translations.os, "getpgid", lambda pid: 4321)

    def fake_killpg(process_group_id: int, sig: int) -> None:
        killed["process_group_id"] = process_group_id
        killed["signal"] = sig

    monkeypatch.setattr(optimize_translations.os, "killpg", fake_killpg)

    with pytest.raises(subprocess.TimeoutExpired) as exc_info:
        optimize_translations.run_llm_command(["opencode"], timeout_seconds=12)

    assert created["start_new_session"] is True
    assert killed == {"process_group_id": 4321, "signal": optimize_translations.signal.SIGKILL}
    assert created["communicate_after_kill"] is True
    assert exc_info.value.output == "partial stdout"
    assert exc_info.value.stderr == "partial stderr"
