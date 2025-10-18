#!/usr/bin/env python3
"""
Builds an ordered execution plan of snippet scripts to run for docs CI.

Usage:
  python ci/select-doc-pages.py --changed-file-list changed.txt --out plan.txt [--repo-root .]

Dependency additions:
  In any *.task.sh file, add lines like:
      # @depends: tutorial/snippets/get-started-with-openstack.task.sh
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from pathlib import Path
import re
import sys
from typing import List

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Select doc snippet pages to run.")
    p.add_argument("--changed-file-list", required=True, type=Path)
    p.add_argument("--out", required=True, type=Path)
    p.add_argument("--repo-root", default=".", type=Path)
    return p.parse_args()


def normalize_path(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


@dataclass
class ExecutionPlan:
    """Represents the set of scripts to be executed."""
    scripts: List[Path] = field(default_factory=list)
    repo_root: Path = Path(".")
    _depends_re = re.compile(r"^\s*#\s*@depends:\s+(.+?)\s*$")

    @classmethod
    def from_changed_files(cls, path: Path, repo_root: Path) -> "ExecutionPlan":
        """Create a plan from a file listing changed paths."""
        if not path.is_file():
            raise FileNotFoundError(f"Changed file list not found: {path}")

        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        # Filter comments and empty lines
        task_strings = [
            ln.strip() for ln in lines if ln.strip() and not ln.strip().startswith("#")
        ]
        # Treat each changed entry as repo-relative and resolve to absolute
        task_paths = [(repo_root / Path(p)).resolve() for p in task_strings if p.endswith(".task.sh")]

        # Preserve order, drop duplicates
        unique_paths = list(dict.fromkeys(task_paths))
        return cls(scripts=unique_paths, repo_root=repo_root)

    def validate_paths_exist(self) -> None:
        """Ensure all scripts in the plan exist on disk."""
        missing = [str(p) for p in self.scripts if not p.is_file()]
        if missing:
            joined = "\n  - ".join(missing)
            raise FileNotFoundError(f"The following snippet files do not exist:\n  - {joined}")

    def _resolve_dep(self, raw_dep: str, relative_to: Path) -> Path:
        """Resolve a dependency path based on its format."""
        s = raw_dep.strip().strip("'\"")
        if s.startswith("/"):
            return Path(s).resolve()
        if s.startswith("./") or s.startswith("../"):
            return (relative_to.parent / s).resolve()
        return (self.repo_root / s).resolve()

    def _parse_direct_depends(self, script: Path) -> List[Path]:
        """Parse '# @depends:' lines from a single script file."""
        try:
            text = script.read_text(encoding="utf-8", errors="ignore")
        except FileNotFoundError:
            return []

        deps: List[Path] = []
        for line in text.splitlines():
            if m := self._depends_re.match(line):
                raw = m.group(1)
                # Only consider *.task.sh dependencies
                if raw.strip().strip("'\"").endswith(".task.sh"):
                    deps.append(self._resolve_dep(raw, relative_to=script))

        return list(dict.fromkeys(deps)) # De-dupe deps from same file

    def expand_dependencies(self) -> None:
        """
        Rebuilds the script list, inserting direct dependencies before each script.
        The final list is de-duplicated.
        """
        expanded_list: List[Path] = []
        for script in self.scripts:
            # Add dependencies first, then the script
            expanded_list.extend(self._parse_direct_depends(script))
            expanded_list.append(script)

        self.scripts = list(dict.fromkeys(expanded_list))

    def write(self, out_path: Path) -> None:
        """Write the final, normalized plan to a file."""
        out_path.parent.mkdir(parents=True, exist_ok=True)
        # Resolve all paths to be absolute
        resolved_scripts = [p.resolve() for p in self.scripts]
        normalized_paths = [normalize_path(p, self.repo_root) for p in resolved_scripts]
        out_path.write_text("\n".join(normalized_paths) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()

    try:
        plan = ExecutionPlan.from_changed_files(
            path=args.changed_file_list, repo_root=args.repo_root
        )
    except FileNotFoundError as e:
        print(f"[select-doc-pages] ERROR: {e}", file=sys.stderr)
        return 2

    if not plan.scripts:
        print("No *.task.sh files changed; writing empty plan.", file=sys.stderr)
        plan.write(args.out)
        return 0

    # Validate initial changed files
    plan.validate_paths_exist()

    # Expand with dependencies
    plan.expand_dependencies()

    # Check paths to ensure all dependencies exist on disk
    plan.validate_paths_exist()

    plan.write(args.out)

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"[select-doc-pages] ERROR: {exc}", file=sys.stderr)
        sys.exit(1)