# GitHub Skill Publisher Project

This project packages and publishes Codex Skills for the GitHub account configured in `skills/github-skill-publisher/references/publisher-config.yaml`.

When the user explicitly asks to publish, upload, or push a Skill, use the workflow in `skills/github-skill-publisher/SKILL.md`. The configured default is a public repository. If the user says “只存储不发布”, “store only”, “draft only”, or an equivalent phrase, make no remote changes and store the material only under the ignored `private-drafts/` directory.

Never store passwords, tokens, cookies, SSH private keys, or credential exports in this project. Authentication must remain in GitHub CLI, macOS Keychain, or the SSH agent.

After a successful publication, update `registry/skills.yaml` with the Skill name, repository URL, invocation name, and publication status. Do not mark a Skill published until the public repository and its `SKILL.md` are readable and a temporary installation test succeeds.
