# Host bootstrap

The Skill has one data dependency: an authorized, read-capable Lark interface. The setup prompt depends on the host.

## Doubao Enterprise

Use the enterprise host's built-in Lark tool or its approved Lark CLI bridge. Do not ask the user to install a local CLI when the host already exposes the tool. If no Lark tool is available, show:

> 当前豆包企业版没有可用的 Lark 数据工具，暂时无法读取协作证据。请先启用企业版的飞书工具或 Lark CLI 桥接，再继续推荐环评人。

## Codex and Claude Code

Require the local `lark-cli` command. Check it before any Feishu read:

```bash
command -v lark-cli
lark-cli --help
lark-cli auth status --json --verify
```

When the command is missing, show:

> 当前宿主还没有安装 Lark CLI。这个 Skill 需要通过 Lark CLI 读取飞书会议、消息、任务、文档和 OKR 证据；请先安装或启用 Lark CLI，完成后优先运行 `lark-cli auth status --json --verify` 验证用户身份。当前 CLI 构建若没有 `auth` 子命令，再退回 `contact +get-user --as user` 与 `task +get-my-tasks --as user` 做只读兼容探测。

Do not silently substitute a browser search, bot identity, or manually guessed data. Do not auto-install packages unless the user explicitly asks for installation. Use the organization-approved installation method; the exact package source may differ by environment.

## Common post-install check

After installation or host-tool enablement, require:

1. `lark-cli --help` succeeds;
2. When supported, `lark-cli auth status --json --verify` reports the intended tenant, `identity: user`, and `verified: true`; otherwise `contact +get-user --as user` resolves the current user and `task +get-my-tasks --as user` remains a weaker read-only canary;
3. the required domain scopes are present for the requested sources;
4. only then start evidence retrieval.
