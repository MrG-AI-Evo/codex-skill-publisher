# Publishing Policy

Apply this workflow only when the user asks to publish or update a Codex Skill.

## Defaults

- GitHub owner: read `publisher-config.yaml`.
- Visibility: public.
- Repository name: `<skill-name>-skill`; if the Skill name already ends in `-skill`, use it unchanged.
- Primary branch: `main`.
- Documentation: bilingual Chinese and English when useful to the intended audience.
- One Skill should normally have one standalone repository. A separate catalog may link to it but should not replace the standalone repository.

## Authorization boundary

“发布这个 Skill” authorizes the repository creation or update, documentation, commit, push, description, and topic changes needed for that Skill. It does not authorize deletion, transfer of ownership, force-push, visibility reduction, release publication, or changes to unrelated repositories.

“只存储不发布” forbids all GitHub writes. Save only under the configured ignored draft directory and do not add the draft to the publisher repository's Git index.

## Repository preparation

- Copy only files belonging to the Skill and its public documentation.
- Exclude credentials, machine-specific caches, temporary output, source photographs not intended for distribution, and unrelated workspace files.
- Preserve executable bits on helper scripts.
- Use a local Git identity based on the configured public account when the new repository lacks one. Prefer the account's GitHub noreply email.
- Do not rewrite an existing Git history unless the user explicitly requests it.

## GitHub CLI flow

Prefer GitHub CLI because it can create repositories and edit metadata as well as push Git content. Use `gh auth status -h github.com` before writes. A typical new-repository operation uses `gh repo create OWNER/REPO --public --source PATH --remote origin --push`, followed by `gh repo edit` for description and topics when needed.

If authentication is missing or invalid, ask the user to complete the browser-based login. Never accept a token in chat or place one in a command, README, config file, or Git remote URL.

## Verification gates

Publication is complete only when all applicable checks pass:

1. Skill preflight has no errors or unresolved secret warnings.
2. Official Skill validation passes.
3. Bundled scripts pass syntax checks or focused smoke tests.
4. Local Git status contains only intended files.
5. Remote default branch exists and the repository is publicly readable.
6. The README contains an exact installation prompt with repository, path, and installation name.
7. A clean temporary installation from the public repository succeeds.

Stop and ask for direction if an existing repository conflicts with the prepared content, authentication cannot be restored, or publishing would expose material that appears private.
