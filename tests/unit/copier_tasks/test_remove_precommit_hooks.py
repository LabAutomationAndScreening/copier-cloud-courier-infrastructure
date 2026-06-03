import re
import shutil
import subprocess
from pathlib import Path

from .helpers import run_copier_task

_EXIT_CODE_INVALID_REGEX = 2
_PROJECT_ROOT = Path(__file__).resolve().parents[3]
_SCRIPT_PATH = _PROJECT_ROOT / "src" / "copier_tasks" / "remove_precommit_hooks.py"


class TestRemovePrecommitHooksViaSubprocess:
    def _run_script(self, *, hook_id_regex: str, target_file: Path) -> subprocess.CompletedProcess[str]:
        return run_copier_task(_SCRIPT_PATH, "--hook-id-regex", hook_id_regex, "--target-file", str(target_file))

    def test_When_run_with_matching_hook__Then_hook_removed(self, tmp_path: Path) -> None:
        source_config = _PROJECT_ROOT / ".pre-commit-config.yaml"
        config_path = tmp_path / ".pre-commit-config.yaml"
        _ = shutil.copyfile(source_config, config_path)
        original = config_path.read_text(encoding="utf-8")
        assert "id: check-json5" in original
        assert "id: trailing-whitespace" in original

        result = self._run_script(hook_id_regex=r"^\s*-\s+id:\s+check-json5\s*$", target_file=config_path)

        assert result.returncode == 0
        assert "Removed 1 matching hook" in result.stdout

        updated = config_path.read_text(encoding="utf-8")
        assert "id: check-json5" not in updated
        assert "id: trailing-whitespace" in updated

    def test_When_run_with_no_matching_hook__Then_file_unchanged(self, tmp_path: Path) -> None:
        source_config = _PROJECT_ROOT / ".pre-commit-config.yaml"
        config_path = tmp_path / ".pre-commit-config.yaml"
        _ = shutil.copyfile(source_config, config_path)
        original = config_path.read_text(encoding="utf-8")

        result = self._run_script(hook_id_regex=r"^\s*-\s+id:\s+nonexistent-hook-xyz\s*$", target_file=config_path)

        assert result.returncode == 0
        assert "No matching hooks found" in result.stdout
        assert config_path.read_text(encoding="utf-8") == original

    def test_When_target_file_does_not_exist__Then_exits_with_error(self, tmp_path: Path) -> None:
        nonexistent_path = tmp_path / "does-not-exist.yaml"

        result = self._run_script(hook_id_regex=r"^\s*-\s+id:\s+some-hook\s*$", target_file=nonexistent_path)

        assert result.returncode != 0

    def test_When_invalid_regex_provided__Then_exits_with_code_2(self, tmp_path: Path) -> None:
        config_path = tmp_path / ".pre-commit-config.yaml"
        _ = config_path.write_text("repos: []\n", encoding="utf-8")

        result = self._run_script(hook_id_regex="[invalid-regex", target_file=config_path)

        assert result.returncode == _EXIT_CODE_INVALID_REGEX
        assert "Invalid regex pattern" in result.stdout

    def test_When_multiple_hooks_match__Then_all_removed_and_count_reported(self, tmp_path: Path) -> None:
        source_config = _PROJECT_ROOT / ".pre-commit-config.yaml"
        config_path = tmp_path / ".pre-commit-config.yaml"
        _ = shutil.copyfile(source_config, config_path)

        hook_id_regex = r"^\s*-\s+id:\s+check-"
        original = config_path.read_text(encoding="utf-8")
        expected_removed = sum(1 for line in original.splitlines() if re.match(hook_id_regex, line))
        assert expected_removed > 1

        result = self._run_script(hook_id_regex=hook_id_regex, target_file=config_path)

        assert result.returncode == 0
        assert f"Removed {expected_removed} matching hook(s)" in result.stdout

        updated = config_path.read_text(encoding="utf-8")
        assert "id: check-" not in updated
        assert "id: trailing-whitespace" in updated
