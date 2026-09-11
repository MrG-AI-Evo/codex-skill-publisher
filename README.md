# Codex Skill Publisher｜Skill 发布管家

A reusable Codex project and Skill for validating, packaging, documenting, and publishing Codex Skills to GitHub.

这是一个专门管理 Skill 发布流程的 Codex 项目。默认 GitHub 账号为 `MrG-AI-Evo`；明确要求发布时，默认创建公开仓库。只有明确说“只存储不发布”时，才会仅保存在本机且不进行任何远程操作。

## What it does｜功能

- 检查 `SKILL.md`、命名、占位内容、软链接和疑似凭据。
- 根据 Skill 内容生成清晰的英文仓库名、仓库简介和中英双语 README。
- 写明安装参数、调用名、使用示例、边界与兼容说明。
- 使用 GitHub CLI 创建或更新公开仓库并推送代码。
- 从公开仓库执行一次临时安装测试。
- 将成功发布的 Skill 登记到 `registry/skills.yaml`。
- “只存储不发布”的内容放入本地 `private-drafts/`，该目录不会进入 Git。

## One-time setup｜一次性设置

GitHub CLI 已安装后，只需登录一次：

```bash
gh auth login -h github.com --web --git-protocol https
```

认证信息由 GitHub CLI 和系统凭据存储管理，不写入本仓库。

## Install the publisher Skill｜安装发布 Skill

把下面这段发给 Codex：

```text
请使用 $skill-installer 安装这个公开 GitHub 仓库中的 Skill：
仓库：https://github.com/MrG-AI-Evo/codex-skill-publisher
路径：skills/github-skill-publisher
安装名：github-skill-publisher
```

安装后的调用名：

```text
$github-skill-publisher
```

## Use｜使用

把 Skill 文件夹交给 Codex，然后说：

```text
用 $github-skill-publisher 发布这个 Skill。
```

默认行为是发布为公开 GitHub 仓库。若暂时不希望上传：

```text
用 $github-skill-publisher 只存储这个 Skill，不发布。
```

如果仓库已经存在，发布器会先核对目标再更新，不会另外创建同名重复仓库。

## Security｜安全

本项目只保存公开用户名、发布偏好和仓库目录，不保存 GitHub 密码、访问令牌或 SSH 私钥。
