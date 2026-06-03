import argparse
import re
from pathlib import Path

# ruff: noqa: T201 # the hooks need to print to stdout to show anything

HOOK_ID_LINE = re.compile(r"^-\s+id:\s")


def _is_matching_hook_block(block_lines: list[str], hook_id_pattern: re.Pattern[str]) -> bool:
    return bool(hook_id_pattern.search(block_lines[0])) if block_lines else False


def remove_hook_blocks(config_path: Path, hook_id_pattern: re.Pattern[str]) -> int:
    text = config_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    output_lines: list[str] = []
    index = 0
    removed_count = 0

    while index < len(lines):
        line = lines[index]
        stripped = line.lstrip()
        indentation = len(line) - len(stripped)

        if HOOK_ID_LINE.match(stripped):
            block_start = index
            block_end = index + 1

            while block_end < len(lines):
                next_line = lines[block_end]
                next_stripped = next_line.lstrip()
                next_indentation = len(next_line) - len(next_stripped)
                if HOOK_ID_LINE.match(next_stripped) and next_indentation == indentation:
                    break
                if next_stripped and next_indentation < indentation:
                    break
                block_end += 1

            block_lines = lines[block_start:block_end]
            if _is_matching_hook_block(block_lines, hook_id_pattern):
                removed_count += 1
                index = block_end
                continue

            output_lines.extend(block_lines)
            index = block_end
            continue

        output_lines.append(line)
        index += 1

    if removed_count == 0:
        return 0

    trailing_newline = "\n" if text.endswith("\n") else ""
    _ = config_path.write_text("\n".join(output_lines) + trailing_newline, encoding="utf-8")
    return removed_count


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Remove matching hook blocks from a pre-commit config file.",
    )
    _ = parser.add_argument(
        "--hook-id-regex",
        required=True,
        dest="hook_id_regex",
        help="Regex to match a hook id line (e.g. '^\\s*-\\s+id:\\s+.*graphql[_-]lambda').",
    )
    _ = parser.add_argument(
        "--target-file",
        default=".pre-commit-config.yaml",
        dest="target_file",
        help="Path to the pre-commit config file (default: .pre-commit-config.yaml).",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    target_file = Path(args.target_file)

    try:
        hook_id_pattern = re.compile(args.hook_id_regex)
    except re.error as error:
        print(f"Invalid regex pattern for hook_id_regex: {error}")
        return 2

    if not target_file.exists():
        print(f"{target_file} not found; skipping hook removal.")
        return 1

    removed_count = remove_hook_blocks(target_file, hook_id_pattern)
    if removed_count > 0:
        print(f"Removed {removed_count} matching hook(s) from {target_file}.")
    else:
        print(f"No matching hooks found in {target_file}; no changes made.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
