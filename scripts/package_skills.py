#!/usr/bin/env python3
"""Build one uploadable ZIP per skill for Claude.ai; no third-party dependencies."""

import argparse
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "plugins" / "team-workflows" / "skills"


def build(output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    result = []
    for skill in sorted(SKILLS.iterdir()):
        if not skill.is_dir() or not (skill / "SKILL.md").is_file():
            continue
        files = sorted(p for p in skill.rglob("*") if p.is_file())
        if skill.is_symlink() or any(p.is_symlink() for p in skill.rglob("*")):
            raise ValueError("Skill packages cannot include symbolic links.")
        target = output / f"{skill.name}.zip"
        with zipfile.ZipFile(target, "x", compression=zipfile.ZIP_DEFLATED) as archive:
            for path in files:
                archive.write(path, str(Path(skill.name) / path.relative_to(skill)))
        result.append(target)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    try:
        for path in build(args.output):
            print(path)
    except (OSError, ValueError) as exc:
        parser.exit(2, f"Packages not completed: {exc}\n")


if __name__ == "__main__":
    main()
