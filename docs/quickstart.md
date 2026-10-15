# Member quickstart

Use your own accounts. Begin with the workflow plugin and Slack; add other services when a task needs them.

## 1. Get access to the repository

**Owner:** open [the repository](https://github.com/AtsushiHosaka/team-ai-connectors), choose **Settings → Collaborators → Add people**, and invite the member's GitHub username. This is a private repository under a personal account.

**Member:** create a [GitHub account](https://github.com/signup) if needed, then accept the invitation from GitHub or its email notification. Confirm that you can open the repository while signed in.

Install [GitHub CLI](https://cli.github.com/) if it is not available. In your terminal:

```sh
gh auth login
gh auth setup-git
gh repo clone AtsushiHosaka/team-ai-connectors
cd team-ai-connectors
```

Choose GitHub.com and complete the browser sign-in. Keep this checkout and reuse it; you do not need separate clones for different AI clients.

If cloning reports that the repository cannot be found, check the accepted invitation and the account shown by `gh auth status` before trying again.

## 2. Install the skills in your client

### Codex

If you have only used ChatGPT in a browser, first follow the [official Codex CLI installation guide](https://learn.chatgpt.com/docs/cli#getting-started) for your operating system and sign in. Then continue below.

From the repository directory:

```sh
codex plugin marketplace add .
codex
```

At the Codex prompt, enter `/plugins`. Choose `team-ai-connectors` and install `team-workflows`. Start a new session, then try:

```text
Use sdd-lite to turn this feature into a small, testable task: [your idea].
```

The same checkout also supports `codex plugin marketplace add AtsushiHosaka/team-ai-connectors` after private Git access is configured. Choose one registration route. The [official guide](https://learn.chatgpt.com/docs/plugins) describes the plugin browser; [marketplace setup](https://developers.openai.com/plugins/build/plugins) covers repository and local sources.

### Optional Claude Code

Consumer Claude requires users to be 18 or older. Members under 18 should use an eligible alternative rather than this optional path. See [Claude's consumer terms](https://www.anthropic.com/legal/consumer-terms).

Install Claude Code using its [official setup guide](https://code.claude.com/docs/en/setup) if the `claude` command is not already available.

Start Claude Code from this repository directory with `claude`, then enter:

```text
/plugin marketplace add .
/plugin install team-workflows@team-ai-connectors
```

Start a new session after installation. You can also add `AtsushiHosaka/team-ai-connectors` instead of `.` after private Git authentication is configured. See [Claude Code marketplaces](https://code.claude.com/docs/en/plugin-marketplaces).

For a Claude interface that supports custom skill uploads, create the individual skill ZIP files with:

```sh
python3 scripts/package_skills.py --output dist
```

Upload the relevant generated ZIP through that interface's skill settings. A skill ZIP contains instructions; it does not authenticate connectors. Feature availability depends on the account and client.

### ChatGPT on the web

Connect supported services through ChatGPT's native Plugins interface as described below. A GitHub repository is a distribution source for this project's local clients; having repository access does not automatically install these skills into a web chat. Check the [current supported surfaces](https://learn.chatgpt.com/docs/plugins) before choosing an installation route.

## 3. Connect Slack with your own account

**ChatGPT:** open **Plugins**, find **Slack**, install it, and complete **Connect** when prompted. Select the intended workspace and review the requested permissions. Then start a new chat. The [official plugin guide](https://learn.chatgpt.com/docs/plugins) lists Slack as a supported native plugin.

**Claude:** open its connectors settings, select Slack, and complete its browser authorization flow. See [Claude connectors](https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities). Claude Code can also use supported connectors already connected to the same Claude account; inspect `/mcp` to check availability. See [Claude Code connector reuse](https://code.claude.com/docs/en/mcp#use-mcp-servers-from-claudeai).

Each member signs in individually. Account, workspace, and administrator restrictions can affect availability; installing the shared skills does not bypass them.

First ask for a read-only check against a channel you can access:

```text
Use the Slack connection to find the latest message in #your-channel.
Return its link. Do not send a message.
```

Only treat the connection as working after the client returns a real accessible message. If no Slack tool is available, inspect the client's connection status rather than assuming a new bot or script is needed.

## 4. Add optional development connectors

Python 3.11 or later is needed for the repository helpers and local tests. On Windows, use `py -3` in place of `python3` if that is your installed Python command. List the available connector definitions:

```sh
python3 scripts/configure.py list
```

The optional `notion` and `atlassian` marketplace plugins provide their corresponding MCP connection setup. Install them through the same plugin browser only when you need them, then authenticate when prompted. In Claude Code, the install commands are:

```text
/plugin install notion@team-ai-connectors
/plugin install atlassian@team-ai-connectors
```

Alternatively, generate configuration snippets for the client you use:

```sh
python3 scripts/configure.py export --client codex --connectors notion github
python3 scripts/configure.py export --client claude-code --connectors notion github
python3 scripts/configure.py export --client vscode --connectors notion github atlassian
```

Choose the relevant command; you do not need all three. Without `--output`, the result appears in the terminal. To save a new snippet file:

```sh
python3 scripts/configure.py export --client codex --connectors notion github --output codex-connectors.toml
```

The exporter rejects an existing output file. It does not edit your client configuration. Merge the generated server entries into your existing configuration, preserving other settings:

| Client | Typical configuration | Section to merge |
| --- | --- | --- |
| Codex | `~/.codex/config.toml` | `mcp_servers` tables |
| Claude Code | Project `.mcp.json` | `mcpServers` entries |
| VS Code | Project `.vscode/mcp.json` | `servers` entries |

Choose either the plugin or the exported configuration for the same connector to avoid duplicate connections. Do not replace a whole configuration file with a snippet or put secret values in a committed file.

### Authenticate the connectors

**GitHub:** create a token with access only to the repositories and read operations you need. Set and export `GITHUB_MCP_TOKEN` in the environment before launching the AI client. The generated configuration refers to that variable; it does not contain a token, and a local `.env` file is not loaded automatically. A GUI client launched separately may not inherit a terminal's environment.

GitHub configuration requests read-only tools with the `X-MCP-Readonly: true` header. This is separate from `gh auth login`: authenticating the GitHub CLI does not populate `GITHUB_MCP_TOKEN`.

**Notion and Atlassian:** complete the browser OAuth flow from your client's MCP or connection settings after adding the server. Select the intended account and content access. For the exported Codex configuration, use `codex mcp login team-notion` or `codex mcp login team-atlassian`; for a plugin connection, follow its sign-in prompt. In Claude Code, inspect `/mcp`.

Verify each connection with one concrete read, such as reading this repository's README or finding a page you already have permission to open. Configuration generation alone does not prove authentication or live access.

## 5. Use the skills on one small task

1. Ask `sdd-lite` to define the outcome and acceptance criteria for a small change.
2. Implement the change in your normal editor or AI development client.
3. Ask `review-ready` to prepare a PR explanation using the actual diff and checks.
4. Ask `reflection` what the evidence shows and which one experiment to try next.

The skills respond in the language you use. They do not require a new planning system or publish work automatically.

## Send an optional Slack update

With a native Slack connector available, ask explicitly:

```text
Use work-session to post a start update to #your-development-channel.
My goal is [goal], and my first step is [step].
```

The client needs a confirmed destination and actual send capability. Merely loading the skill, opening an editor, or reading a Slack message does not authorize a post.

If you prefer a channel-specific incoming webhook, have the Slack workspace owner configure one and provide the secret through a secure channel. Set and export `SLACK_WEBHOOK_URL` locally. Its configured channel is the destination; the script does not select a different channel.

Preview a payload without sending:

```sh
python3 scripts/slack_notify.py --event started --summary "Starting the search feature"
```

Send deliberately by adding `--send`:

```sh
python3 scripts/slack_notify.py --event completed --summary "Search feature checks passed" --link "https://github.com/AtsushiHosaka/team-ai-connectors" --send
```

Events are `started`, `blocked`, `review`, and `completed`. Use a link to the actual task or PR when available. The webhook helper sends updates; it does not let the AI read Slack. Do not paste the webhook URL into chat, code, or Git commits.

## Update your checkout

From the existing checkout, run `git pull --ff-only` when your working tree is ready to update. For locally registered plugins, follow the client's reload or new-session prompt. Repository-backed marketplace installations have their own refresh controls; Codex provides `codex plugin marketplace upgrade team-ai-connectors`.

If a helper rejects an existing file, choose a fresh output filename and merge the result. If a service fails to connect, check the account, permissions, token environment, and connection status. Report the failed step and its error without sharing credentials.
