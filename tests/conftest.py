import os
import shutil
import subprocess
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]

@pytest.fixture
def tmp_repo(tmp_path: Path) -> Path:
    """Copies snippets and ci/ scripts into an isolated temp repo."""
    src = REPO_ROOT / "tests" / "snippets"
    dst = tmp_path
    shutil.copytree(src, dst / "tests/snippets", dirs_exist_ok=True)
    (dst / "ci").mkdir(exist_ok=True)
    for name in ["select-doc-pages.py", "run-doc-pages.py"]:
        shutil.copy2(REPO_ROOT / "ci" / name, dst / "ci" / name)
    return dst

def run_cmd(args, cwd: Path, env=None):
    env_vars = os.environ.copy()
    if env:
        env_vars.update(env)
    return subprocess.run(
        args,
        cwd=cwd,
        env=env_vars,
        text=True,
        capture_output=True,
        check=False,
    )

def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
