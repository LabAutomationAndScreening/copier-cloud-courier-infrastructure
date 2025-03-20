"""Update any project files that point to a private package registry to use public ones.

Since the CI pipelines for testing these copier templates don't have access to private registries, we can't test installing from them as part of CI.

Seems minimal risk, since the only problem we'd be missing is if the pyproject.toml (or similar config files) had syntax errors that would have been
caught by pre-commit.
"""

import re
from pathlib import Path


def process_file(file_path: Path):
    # Read the entire file content
    content = file_path.read_text()

    # Regex to match a block starting with [[tool.uv.index]]
    # until the next block header (a line starting with [[) or the end of the file.
    pattern = re.compile(r"(\[\[tool\.uv\.index\]\].*?)(?=\n\[\[|$)", re.DOTALL)

    # Find all uv.index blocks.
    blocks = pattern.findall(content)

    # Check if any block contains "default = true"
    if not any("default = true" in block for block in blocks):
        print(f"No changes in: {file_path}")
        return

    # If at least one block contains "default = true", remove all uv.index blocks.
    new_content = pattern.sub("", content)

    # Ensure file ends with a newline before appending the new block.
    if not new_content.endswith("\n"):
        new_content += "\n"

    # Append the new block.
    new_block = '[[tool.uv.index]]\nname = "pypi"\nurl = "https://pypi.org/simple/"\n'
    new_content += new_block

    # Write the updated content back to the file.
    _ = file_path.write_text(new_content)
    print(f"Updated file: {file_path}")


def main():
    base_dir = Path(".")
    # Use rglob to find all pyproject.toml files recursively.
    for file_path in base_dir.rglob("pyproject.toml"):
        # Check if the file is at most two levels deep.
        # The relative path's parts count should be <= 3 (e.g. "pyproject.toml" is 1 part,
        # "subdir/pyproject.toml" is 2 parts, and "subdir/subsubdir/pyproject.toml" is 3 parts).
        if len(file_path.relative_to(base_dir).parts) <= 3:
            process_file(file_path)


if __name__ == "__main__":
    main()
