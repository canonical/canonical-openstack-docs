from pathlib import Path
from conftest import run_cmd, write_file

def test_dependency_inserted_before_changed(tmp_repo: Path):
    changed = tmp_repo / "changed.txt"
    write_file(changed, "tests/snippets/fixture-with-dep.task.sh\n")
    plan = tmp_repo / "plan.txt"

    rc = run_cmd(
        ["python3", "ci/select-doc-pages.py",
         "--changed-file-list", str(changed),
         "--out", str(plan),
         "--repo-root", str(tmp_repo)],
        cwd=tmp_repo,
    )
    assert rc.returncode == 0, rc.stderr
    lines = plan.read_text().strip().splitlines()
    # Dep must appear first
    assert lines == [
        "tests/snippets/base-fixture.task.sh",
        "tests/snippets/fixture-with-dep.task.sh",
    ]

def test_dedup_when_both_changed(tmp_repo: Path):
    changed = tmp_repo / "changed.txt"
    write_file(changed,
               "tests/snippets/base-fixture.task.sh\n"
               "tests/snippets/fixture-with-dep.task.sh\n")
    plan = tmp_repo / "plan.txt"

    rc = run_cmd(
        ["python3", "ci/select-doc-pages.py",
         "--changed-file-list", str(changed),
         "--out", str(plan),
         "--repo-root", str(tmp_repo)],
        cwd=tmp_repo,
    )
    assert rc.returncode == 0
    lines = plan.read_text().strip().splitlines()
    assert lines == [
        "tests/snippets/base-fixture.task.sh",
        "tests/snippets/fixture-with-dep.task.sh",
    ]
