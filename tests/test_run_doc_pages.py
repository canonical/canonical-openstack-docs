from pathlib import Path
from conftest import run_cmd, write_file

def test_dry_run_prints_assembled_scripts(tmp_repo: Path):
    """
    Checks that in dry-run mode, the script correctly assembles and prints
    the content of multiple docs-exec blocks from multiple files.
    """
    plan = tmp_repo / "plan.txt"
    write_file(plan,
               "tests/snippets/base-fixture.task.sh\n"
               "tests/snippets/fixture-multi-blocks.task.sh\n")

    rc = run_cmd(
        ["python3", "ci/run-doc-pages.py", "--plan", str(plan)],
        cwd=tmp_repo,
        env={"DOCS_DRY_RUN": "1"}, # Explicitly set dry-run mode
    )

    assert rc.returncode == 0, rc.stderr
    out = rc.stdout

    # Check for content
    assert "install base" in out
    assert "block one" in out

    # Check that the final line of output is the correct dry-run message
    last_line = out.strip().splitlines()[-1]
    assert "Nothing executed" in last_line

def test_dry_run_fails_on_structural_error(tmp_repo: Path):
    """
    Checks that the script fails (even in dry-run) if it finds a malformed
    block, because parsing happens before the dry-run check.
    """
    plan = tmp_repo / "plan.txt"
    write_file(plan, "tests/snippets/fixture-missing-end.task.sh\n")

    rc = run_cmd(
        ["python3", "ci/run-doc-pages.py", "--plan", str(plan)],
        cwd=tmp_repo,
        env={"DOCS_DRY_RUN": "1"}, # Explicitly set dry-run mode
    )

    # Structural errors should cause a failure with exit code 1.
    assert rc.returncode == 1

    # Check for the specific error messages
    assert "Missing [docs-exec:oops-end]" in rc.stderr
    assert "Aborting due to structural errors" in rc.stderr

def test_dry_run_handles_no_blocks_gracefully(tmp_repo: Path):
    """
    Checks that in dry-run mode, a file with no blocks is reported correctly
    and the process SUCCEEDS.
    """
    plan = tmp_repo / "plan.txt"
    write_file(plan, "tests/snippets/fixture-no-blocks.task.sh\n")

    rc = run_cmd(
        ["python3", "ci/run-doc-pages.py", "--plan", str(plan)],
        cwd=tmp_repo,
        env={"DOCS_DRY_RUN": "1"}, # Explicitly set dry-run mode
    )

    # A dry run should always succeed if there are no structural errors.
    assert rc.returncode == 0, rc.stderr

    # It should print the correct output for the file with no blocks.
    assert "NO docs-exec FOUND" in rc.stdout
    assert "(no [docs-exec:*] blocks found - this would be skipped in a real run)" in rc.stdout