---
name: github-skill-publisher
description: Publish, update, or locally store Codex Skills for the configured GitHub account. Use when the user asks to package a Skill, write its repository documentation, upload or publish it to GitHub, update an existing Skill repository, or explicitly store a Skill without publishing it.
---

# GitHub Skill Publisher

Turn a supplied Skill folder into a clean, documented, installable GitHub repository while preserving the user's intent and credentials.

## Resolve the requested mode

- Treat an explicit request to “发布”, “上传”, “push”, or “publish” a Skill as authorization to create or update the required GitHub repository. Use the configured public visibility unless the user explicitly requests another visibility.
- If the user says “只存储不发布”, “store only”, “draft only”, or equivalent, perform no remote writes. Copy the Skill into the configured local draft directory, validate it, and report its saved location.
- A request to review, analyze, or improve a Skill does not authorize publication.

Before publishing or storing, read [publisher-config.yaml](references/publisher-config.yaml). For a publication, also read [publishing-policy.md](references/publishing-policy.md). Read [readme-template.md](references/readme-template.md) only when creating or substantially revising repository documentation.

## Prepare the Skill

1. Locate the exact Skill folder and inspect all files that will be published. Preserve unrelated user files and edits.
2. Run `scripts/preflight_skill.py <skill-folder>`. Resolve validation errors before publication. Treat every `security_findings` item as a blocker until the suspicious material is excluded or the user confirms it is non-sensitive.
3. Use the `name` from `SKILL.md` as the invocation slug. Default the repository name to `<skill-name>-skill`, avoiding a duplicated `-skill` suffix.
4. Create a concise English display name and repository name. The README may be bilingual and should retain useful Chinese search terms when the Skill targets Chinese users.
5. Keep the Skill itself installable as one directory containing `SKILL.md`. A standalone repository may place the Skill at its root; a catalog repository may place it under `skills/<skill-name>`.

## Publish

1. Check `gh auth status -h github.com`. If authentication is invalid, stop before remote mutation and ask the user to complete `gh auth login -h github.com --web --git-protocol https`. Never request or print a token.
2. Search the configured account for the target repository name. If it exists, verify that it is the intended Skill repository and update it without discarding unrelated remote changes. If it does not exist, create it as public.
3. Generate or update the README using the repository template. Include the exact repository URL, Skill path, installation name, invocation example, behavior, limitations, and relevant search keywords.
4. Validate the Skill with the available official Skill validator. Run syntax or smoke tests for bundled scripts.
5. Commit only the prepared Skill repository files, then push the main branch. Set a concise repository description and relevant lowercase GitHub topics.
6. Confirm that the public `README.md` and `SKILL.md` are readable. Install the published Skill into a unique temporary directory using the official Skill installer, then validate the installed copy.
7. Only after all checks pass, update the publisher project's `registry/skills.yaml` and push that catalog update when the project repository is available.

Return the repository link, invocation name, exact copyable installation prompt, and a brief statement of the checks performed.

## Safety boundaries

- Never commit `.env` files, access tokens, passwords, cookies, SSH private keys, credential exports, or unrelated personal files.
- Do not overwrite or delete an existing repository, branch, release, or user file without explicit authorization.
- Do not claim publication succeeded until the remote repository and temporary installation test both succeed.
- Do not create multiple output variants or promotional assets unless the user asks for them.
