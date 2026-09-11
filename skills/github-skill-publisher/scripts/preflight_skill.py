#!/usr/bin/env python3
"""Perform a dependency-free preflight check on a Codex Skill directory."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---(?:\s*\n|\s*\Z)", re.DOTALL)
PRIVATE_KEY_RE = re.compile(r"-----BEGIN (?:[A-Z0-9 ]+ )?PRIVATE KEY-----")
TOKEN_PATTERNS = (
    re.compile(r"\bgh[oprsu]_[A-Za-z0-9_]{30,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{30,}\b"),
)
SENSITIVE_FILENAMES = {
    ".env",
    "id_rsa",
    "id_ed25519",
    "credentials.json",
    "credentials.yaml",
    "credentials.yml",
}
SKIP_DIRECTORIES = {".git", "__pycache__", ".pytest_cache"}


def frontmatter_value(frontmatter: str, key: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(.+?)\s*$", frontmatter)
    if not match:
        return None
    value = match.group(1).strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        value = value[1:-1]
    return value.strip()


def inspect_skill(skill_dir: Path) -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []
    security_findings: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    skill_name: str | None = None

    if not skill_dir.is_dir():
        errors.append(f"Skill directory does not exist: {skill_dir}")
    elif not skill_md.is_file():
        errors.append("SKILL.md is missing")
    else:
        text = skill_md.read_text(encoding="utf-8")
        match = FRONTMATTER_RE.search(text)
        if not match:
            errors.append("SKILL.md does not start with valid YAML frontmatter")
        else:
            frontmatter = match.group(1)
            skill_name = frontmatter_value(frontmatter, "name")
            description = frontmatter_value(frontmatter, "description")
            if not skill_name:
                errors.append("Frontmatter name is missing")
            elif len(skill_name) > 64 or not NAME_RE.fullmatch(skill_name):
                errors.append("Skill name must be at most 64 characters using lowercase letters, digits, and hyphens")
            elif skill_dir.name != skill_name:
                warnings.append(f"Folder name '{skill_dir.name}' differs from Skill name '{skill_name}'")
            if not description:
                errors.append("Frontmatter description is missing")
        if "TODO" in text or "[TODO" in text:
            errors.append("SKILL.md contains unfinished TODO placeholders")

    if skill_dir.is_dir():
        for path in skill_dir.rglob("*"):
            relative = path.relative_to(skill_dir)
            if any(part in SKIP_DIRECTORIES for part in relative.parts):
                continue
            if path.is_symlink():
                errors.append(f"Symbolic link is not publishable: {relative}")
                continue
            if not path.is_file():
                continue
            if path.name in SENSITIVE_FILENAMES or path.suffix.lower() in {".pem", ".key", ".p12", ".pfx"}:
                security_findings.append(f"Potential credential file: {relative}")
            size = path.stat().st_size
            if size > 10 * 1024 * 1024:
                warnings.append(f"Large file over 10 MiB: {relative}")
            if size > 2 * 1024 * 1024:
                continue
            try:
                content = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if PRIVATE_KEY_RE.search(content):
                security_findings.append(f"Private key material detected: {relative}")
            if any(pattern.search(content) for pattern in TOKEN_PATTERNS):
                security_findings.append(f"GitHub token-like value detected: {relative}")

    if skill_dir.is_dir() and not (skill_dir / "agents" / "openai.yaml").is_file():
        warnings.append("agents/openai.yaml is absent; installation still works, but UI metadata is unavailable")

    repository_name = None
    if skill_name:
        repository_name = skill_name if skill_name.endswith("-skill") else f"{skill_name}-skill"

    return {
        "skill_directory": str(skill_dir),
        "skill_name": skill_name,
        "suggested_repository": repository_name,
        "errors": errors,
        "warnings": sorted(set(warnings)),
        "security_findings": sorted(set(security_findings)),
        "ok": not errors and not security_findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_directory", type=Path)
    args = parser.parse_args()
    result = inspect_skill(args.skill_directory.expanduser().resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
