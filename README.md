# Team AI Connectors

A private personal repository of shared AI skills and connector configurations for mentors and students. Members use their own AI and service accounts; no GitHub organization is required.

**Start here: [Member quickstart](docs/quickstart.md).** The owner invites each member to [AtsushiHosaka/team-ai-connectors](https://github.com/AtsushiHosaka/team-ai-connectors), and members install only the tools they use.

## What is included

| Component | Purpose |
| --- | --- |
| `team-workflows` plugin | Four portable skills for everyday development |
| `sdd-lite` | Define a small task with observable acceptance criteria |
| `work-session` | Prepare session updates and send requested Slack notifications |
| `review-ready` | Prepare a PR handoff backed by actual checks |
| `reflection` | Reflect on evidence and choose one next experiment |
| Optional `notion` and `atlassian` plugins | Connect documentation and issue tracking through official MCP services |
| Connector exporter | Generate configuration snippets for Codex, Claude Code, and VS Code |
| Slack notification helper | Preview or send a short update through a configured incoming webhook |

Skills are reusable instructions. Connectors let an AI client access another service after authentication. Installing this repository does not grant access to anyone else's Slack, Notion, or GitHub account.

## Install the workflow plugin

Accept the private repository invitation first. With [GitHub CLI](https://cli.github.com/) installed:

```sh
gh auth login
gh auth setup-git
gh repo clone AtsushiHosaka/team-ai-connectors
cd team-ai-connectors
```

**Codex:** register this checkout, then launch Codex:

```sh
codex plugin marketplace add .
codex
```

Enter `/plugins`, choose the `team-ai-connectors` marketplace, and install `team-workflows`. Start a new session before using its skills. See the [official Codex plugin guide](https://learn.chatgpt.com/docs/plugins).

**Claude Code:** the [quickstart](docs/quickstart.md#optional-claude-code) gives the equivalent installation commands and eligibility note.

**ChatGPT on the web:** use native service plugins for Slack and other supported tools. This repository's Git marketplace installation instructions target local development clients; they do not promise arbitrary private-repository installation in ChatGPT web. See [supported plugin surfaces](https://learn.chatgpt.com/docs/plugins).

## Connect services

Start with Slack's native connection in the AI client, then add GitHub or documentation tools when needed. Each member completes their own sign-in and grants only the access they intend to use.

```sh
python3 scripts/configure.py list
python3 scripts/configure.py export --client codex --connectors notion github
```

The exporter prints a configuration snippet. Use `--client claude-code` or `--client vscode` for those clients. Add `atlassian` to the connector list if needed. `--output PATH` creates a new snippet file and rejects an existing file; **merge the snippet into your existing client configuration manually**.

GitHub snippets reference `GITHUB_MCP_TOKEN` and request read-only tools with `X-MCP-Readonly: true`. Set and export the token before launching the client. An `.env` file is not loaded automatically. OAuth services still require sign-in after configuration. See [connection details and provider references](docs/connectors.md).

The helper scripts and tests use Python 3.11 or later and need no additional Python packages. To run the checks locally: `python3 -m unittest discover -s tests -v`.

## Try one real task

Ask your AI client to use `sdd-lite` to define a small change. Implement it, use `review-ready` to explain the result and checks, then use `reflection` to choose one improvement for next time.

For a Slack update, explicitly ask for a notification and name its destination. The workflow does not post merely because a skill was loaded or an editor was opened. The [quickstart](docs/quickstart.md#send-an-optional-slack-update) also explains the webhook helper.

## Validation boundary

Configuration generation, skill packaging, and local checks can be verified without signing in to services. Actual Slack delivery, private GitHub access through MCP, and Notion/Atlassian OAuth must be checked with each member's accounts. This repository does not bundle credentials or preconfigured student records.
