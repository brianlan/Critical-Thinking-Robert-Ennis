import argparse
import dataclasses
import itertools
import os
import re
import signal
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from loguru import logger

from scripts.bilingual_export.align import (
    build_aligned_document,
    parse_markdown,
    AlignedRow,
    AlignedDocument,
    AlignedSection,
)


TRANSLATOR_MODEL_POOL = itertools.cycle(
    [
        "zhipuai-coding-plan/glm-5-turbo",
        "ark-coding-plan/doubao-seed-2.0-lite",
        "ollama-cloud/deepseek-v4-flash",
        "tencent-coding-plan/kimi-k2.5",
        "opencode-go/deepseek-v4-flash",
        "opencode/deepseek-v4-flash-free",
    ]
)
DEFAULT_TIMEOUT_SECONDS = 300
DEFAULT_MAX_RETRIES = 2


def parent_ensured_path(path: str | Path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    return Path(path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="desc")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="Repository root containing FullText-en and FullText-zh-sense.",
    )
    parser.add_argument("--chapter-filename", type=str, help="file name of the chapter to be optimized.")
    parser.add_argument("-o", "--output", type=parent_ensured_path, help="Optimized Chinese translation output path.")
    parser.add_argument("--num-workers", type=int, default=0)
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=DEFAULT_TIMEOUT_SECONDS,
        help="Timeout for each LLM submission attempt.",
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=DEFAULT_MAX_RETRIES,
        help="Retries after the first failed LLM submission.",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Show detailed progress")
    parser.add_argument("--startover", action="store_true", default=False)

    return parser.parse_args()


def run_llm_command(command: list[str], timeout_seconds: int) -> subprocess.CompletedProcess[str]:
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=os.name == "posix",
    )
    try:
        stdout, stderr = process.communicate(timeout=timeout_seconds)
    except subprocess.TimeoutExpired as exc:
        kill_llm_process(process)
        stdout, stderr = process.communicate()
        raise subprocess.TimeoutExpired(command, timeout_seconds, output=stdout, stderr=stderr) from exc

    return subprocess.CompletedProcess(command, process.returncode, stdout, stderr)


def kill_llm_process(process: subprocess.Popen[str]) -> None:
    if os.name == "posix":
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGKILL)
            return
        except ProcessLookupError:
            return
        except OSError as exc:
            logger.warning("Failed to kill opencode process group, killing process directly: {}", exc)

    try:
        process.kill()
    except ProcessLookupError:
        pass


def optimize_row(
    row: AlignedRow,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    max_retries: int = DEFAULT_MAX_RETRIES,
) -> AlignedRow:
    total_attempts = max_retries + 1
    prompt = f"英文原文：{row.english_block.source_text} 现有翻译：{row.chinese_block.source_text}"
    for attempt in range(1, total_attempts + 1):
        model = next(TRANSLATOR_MODEL_POOL)
        command = [
            "opencode",
            "run",
            "--pure",
            "-m",
            model,
            "--agent",
            "snippet-translation-coordinator",
            prompt,
        ]
        try:
            result = run_llm_command(command, timeout_seconds)
        except subprocess.TimeoutExpired:
            logger.warning(
                "opencode timed out after {}s on attempt {}/{}",
                timeout_seconds,
                attempt,
                total_attempts,
            )
            continue

        if result.returncode != 0:
            logger.error(
                "opencode failed on attempt {}/{}: {}",
                attempt,
                total_attempts,
                result.stderr.strip(),
            )
            continue

        match = re.search(r"<translation>(.*?)</translation>", result.stdout, re.DOTALL)
        if not match:
            logger.warning("No <translation> tag found in output on attempt {}/{}", attempt, total_attempts)
            continue

        optimized = match.group(1).strip()
        original = row.chinese_block
        optimized_block = dataclasses.replace(original, content=optimized) if original else None
        return dataclasses.replace(row, chinese_block=optimized_block)

    logger.error("All {} opencode attempts failed, keeping original", total_attempts)
    return row


def count_written_sections(output: Path) -> int:
    """Count how many sections have been written by parsing the output file."""
    if not output.exists():
        return 0
    parsed = parse_markdown(output)
    return len(parsed.sections)


def build_section_markdown(section: AlignedSection, lang="chinese") -> str:
    parts = (
        [row.chinese_block.content for row in section.rows if row.chinese_block]
        if lang == "chinese"
        else [row.english_block.content for row in section.rows if row.english_block]
    )
    return "\n\n".join(parts) + "\n\n" if parts else ""


def optimize_doc(
    doc: AlignedDocument,
    output: Path,
    num_workers: int = 0,
    lang="chinese",
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    max_retries: int = DEFAULT_MAX_RETRIES,
) -> None:
    n_done = count_written_sections(output)
    with open(output, "a", encoding="utf-8") as f:
        for section in doc.sections:
            if section.index < n_done:
                continue
            logger.info("Section {}/{}: {}", section.index + 1, len(doc.sections), section.anchor)

            rows = list(section.rows)
            if num_workers > 0:
                with ThreadPoolExecutor(max_workers=num_workers) as executor:
                    optimized = dict(
                        zip(
                            rows,
                            executor.map(
                                lambda row: optimize_row(row, timeout_seconds, max_retries),
                                rows,
                            ),
                        )
                    )
            else:
                optimized = {row: optimize_row(row, timeout_seconds, max_retries) for row in rows}

            optimized_section = dataclasses.replace(section, rows=tuple(optimized[row] for row in section.rows))
            f.write(build_section_markdown(optimized_section, lang))
            f.flush()


def main(args) -> None:
    if args.startover and args.output.exists():
        args.output.unlink()

    doc = build_aligned_document(args.repo_root, args.chapter_filename)
    optimize_doc(
        doc,
        output=args.output,
        num_workers=args.num_workers,
        timeout_seconds=args.timeout_seconds,
        max_retries=args.max_retries,
    )


if __name__ == "__main__":
    main(parse_args())
