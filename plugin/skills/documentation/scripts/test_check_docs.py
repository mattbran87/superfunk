import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_docs import read_user_facing, extract_section, changed_files


def test_read_user_facing_yes():
    spec = "**Date:** 2026-08-28\n**User-Facing:** Yes\n"
    assert read_user_facing(spec) == "Yes"


def test_read_user_facing_no():
    spec = "**Date:** 2026-08-28\n**User-Facing:** No\n"
    assert read_user_facing(spec) == "No"


def test_read_user_facing_missing():
    spec = "**Date:** 2026-08-28\n**Status:** Approved\n"
    assert read_user_facing(spec) is None


def test_extract_section_finds_content():
    spec = "## Context\n\nSome context here.\n\n## Decision\n\nSome decision here.\n"
    assert extract_section(spec, "Context") == "Some context here."
    assert extract_section(spec, "Decision") == "Some decision here."


def test_extract_section_missing_returns_empty():
    spec = "## Context\n\nSome context here.\n"
    assert extract_section(spec, "Decision") == ""


def test_extract_section_last_section_to_end_of_file():
    spec = "## Context\n\nFirst.\n\n## Consequences\n\nLast section, no trailing header.\n"
    assert extract_section(spec, "Consequences") == "Last section, no trailing header."


def test_changed_files_detects_readme(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True)
    (repo / "file.txt").write_text("v1")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "base"], cwd=repo, check=True)
    base_sha = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True, check=True
    ).stdout.strip()

    (repo / "README.md").write_text("# Test")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "add readme"], cwd=repo, check=True)
    head_sha = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True, check=True
    ).stdout.strip()

    original_cwd = os.getcwd()
    os.chdir(repo)
    try:
        result = changed_files(base_sha, head_sha)
    finally:
        os.chdir(original_cwd)

    assert "README.md" in result


CHECK_DOCS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "check_docs.py")


def _init_repo(repo):
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True)


def _commit_all(repo, message):
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-q", "-m", message], cwd=repo, check=True)
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True, check=True
    ).stdout.strip()


def test_end_to_end_not_applicable(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _init_repo(repo)
    spec = repo / "spec.md"
    spec.write_text("**Date:** 2026-08-28\n**User-Facing:** No\n\n## Context\n\nInternal only.\n")
    base_sha = _commit_all(repo, "base")
    (repo / "other.py").write_text("x = 1")
    head_sha = _commit_all(repo, "change")

    result = subprocess.run(
        [sys.executable, CHECK_DOCS_PATH, str(spec), base_sha, head_sha],
        cwd=repo, capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "NOT_APPLICABLE" in result.stdout


def test_end_to_end_already_updated(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _init_repo(repo)
    spec = repo / "spec.md"
    spec.write_text("**Date:** 2026-08-28\n**User-Facing:** Yes\n\n## Context\n\nSomething.\n")
    base_sha = _commit_all(repo, "base")
    (repo / "README.md").write_text("# Updated")
    head_sha = _commit_all(repo, "update readme")

    result = subprocess.run(
        [sys.executable, CHECK_DOCS_PATH, str(spec), base_sha, head_sha],
        cwd=repo, capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "ALREADY_UPDATED: README.md" in result.stdout


def test_end_to_end_action_needed(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _init_repo(repo)
    spec = repo / "spec.md"
    spec.write_text(
        "**Date:** 2026-08-28\n**User-Facing:** Yes\n\n"
        "## Context\n\nUsers hit a bug.\n\n"
        "## Decision\n\nFix the bug this way.\n\n"
        "## Consequences\n\nUsers see correct behavior now.\n"
    )
    base_sha = _commit_all(repo, "base")
    (repo / "fix.py").write_text("x = 2")
    head_sha = _commit_all(repo, "fix")

    result = subprocess.run(
        [sys.executable, CHECK_DOCS_PATH, str(spec), base_sha, head_sha],
        cwd=repo, capture_output=True, text=True
    )
    assert result.returncode == 1
    assert "ACTION_NEEDED" in result.stdout
    assert "Users hit a bug." in result.stdout
    assert "Fix the bug this way." in result.stdout
    assert "Users see correct behavior now." in result.stdout
