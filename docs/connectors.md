# Connections and member authentication

This private repository distributes configuration and shared workflows. It does not grant access to Slack, GitHub, Notion, or Atlassian. Every member connects their own account and retains that account's permissions. A GitHub account needs an invitation to this repository before it can clone or install the private marketplace.

## What is available

| Connection | Official server | Setup in this repository |
| --- | --- | --- |
| GitHub | `https://api.githubcopilot.com/mcp/` | Generate the client configuration; provide your own token through an environment variable. |
| Notion | `https://mcp.notion.com/mcp` | Optional `notion` plugin; complete browser OAuth with your own Notion account. |
| Atlassian | `https://mcp.atlassian.com/v2/mcp` | Optional `atlassian` plugin; requires an existing Atlassian Cloud site and browser OAuth. |
| Slack | `https://mcp.slack.com/mcp` | Use an official native connector, or configure an approved internal Slack app separately. |

The `team-workflows` plugin has no bundled service connections. Install Notion and Atlassian separately only when useful. These plugins package the providers' official servers; they are maintained by this repository's owner and are not official provider plugins.

## GitHub

For Codex and Claude Code, use a personal access token restricted to the repositories and permissions you need. Each member creates their own token. Keep the value outside this repository and make the environment variable available to the process launching the AI client. Merely creating a `.env` file does not make the client load it.

Codex supports a credential reference, rather than a token value, in its configuration:

```toml
[mcp_servers.team-github]
url = "https://api.githubcopilot.com/mcp/"
bearer_token_env_var = "GITHUB_MCP_TOKEN"
http_headers = { "X-MCP-Readonly" = "true" }
```

Claude Code accepts an environment reference in its JSON configuration:

```json
{
  "mcpServers": {
    "team-github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {"Authorization": "Bearer ${GITHUB_MCP_TOKEN}", "X-MCP-Readonly": "true"}
    }
  }
}
```

For reading only, the official hosted server supports `https://api.githubcopilot.com/mcp/readonly`. The equivalent header is `X-MCP-Readonly: true`. Select read-only access when you only need code, issue, PR, or CI context. A write-capable token still has its original permissions outside this server.

VS Code's GitHub MCP connection supports browser OAuth; it does not require storing a PAT in a workspace file. Its MCP client is part of the GitHub Copilot experience; installing the editor alone does not enable an AI client.

After connecting, verify with a read operation against one repository you are allowed to access. A saved configuration is not proof that authentication or tool access succeeded.

Sources: [GitHub's Codex installation guide](https://github.com/github/github-mcp-server/blob/main/docs/installation-guides/install-codex.md), [GitHub's Claude installation guide](https://github.com/github/github-mcp-server/blob/main/docs/installation-guides/install-claude.md), [GitHub remote server and read-only options](https://github.com/github/github-mcp-server/blob/main/docs/remote-server.md), [GitHub's VS Code OAuth example](https://github.com/github/github-mcp-server#install-in-vs-code), [Claude environment expansion](https://code.claude.com/docs/en/mcp#environment-variable-expansion-in-mcpjson).

## Notion

Install `notion@team-ai-connectors` and complete the OAuth prompt in your client. Select the intended workspace. The connected client can read and update content available to your account; check the requested permissions during authorization.

For a direct Codex connection, run `codex mcp add notion --url https://mcp.notion.com/mcp`, then `codex mcp login notion`. For a direct Claude Code connection, run `claude mcp add --transport http notion https://mcp.notion.com/mcp`, then open `/mcp` to authenticate. Choose either the plugin or direct configuration for the same account and endpoint to avoid redundant connections.

Notion's hosted MCP currently requires interactive OAuth. This is a member connection, not an unattended CI credential. A personal or free Notion account does not imply that every provider feature or tool is included; check the permissions and capabilities shown in your own workspace.

Source: [Notion's official connection guide](https://developers.notion.com/guides/mcp/get-started-with-mcp).

## Atlassian: optional

Install `atlassian@team-ai-connectors` only if you already use Atlassian Cloud. Authorize your own account and select the intended Cloud site. This does not create Jira projects, Confluence spaces, or Atlassian accounts.

The recommended endpoint is `https://mcp.atlassian.com/v2/mcp`. The previous `/v1/sse` endpoint is no longer supported after June 30, 2026. OAuth respects the connected account's permissions and administrator policies.

For direct setup, run `codex mcp add atlassian --url https://mcp.atlassian.com/v2/mcp`, then `codex mcp login atlassian`; Claude Code supports `claude mcp add --transport http atlassian https://mcp.atlassian.com/v2/mcp`, followed by `/mcp` authentication. Use one installation path per client.

Source: [Atlassian's official server and setup instructions](https://atlassian.github.io/atlassian-mcp-server/).

## Slack: reading and notifications are separate

Slack's official MCP server requires a registered Slack app with a fixed app identity. Slack does not provide Dynamic Client Registration for this endpoint, and only Marketplace-published apps or internal apps may use it. Therefore this repository does not present the URL alone as a ready-to-authenticate connector.

For ChatGPT or Codex, install the official Slack plugin from the product's available plugin directory, then connect your own Slack account. Availability and workspace approval can depend on your account and workspace settings. For Claude, use the Slack connector at `claude.ai/customize/connectors`. When Claude Code is signed in with a supported claude.ai subscription, it can reuse connected claude.ai connectors; inspect `/mcp` to confirm the actual connection.

An administrator can instead create an internal Slack app, configure the required OAuth identity and redirect URLs, and authorize each member through a supported client. That setup needs real app details and is not completed by cloning this repository. Do not share one member's user token with the team.

Incoming webhooks support notifications to a configured channel. They do not search Slack or read school information. A webhook URL is a credential: keep it in a local environment variable or a GitHub Actions secret, never in source control. Posting still requires the user's instruction or the team's explicit automation authorization.

Sources: [Slack MCP access and authentication requirements](https://docs.slack.dev/ai/slack-mcp-server/), [Claude connector reuse](https://code.claude.com/docs/en/mcp#use-mcp-servers-from-claudeai), [Slack incoming webhooks](https://docs.slack.dev/messaging/sending-messages-using-incoming-webhooks/).

## Packaging and client boundaries

The OpenAI marketplace is `.agents/plugins/marketplace.json`; the Claude marketplace is `.claude-plugin/marketplace.json`. Both catalogs point to the same plugin directories. Installing a marketplace makes plugins discoverable; it does not automatically install every optional connection.

Each plugin has a portable root `plugin.json`; Notion and Atlassian each have one portable `mcp.json`. OpenAI's portable format discovers the root `mcp.json` automatically. Portable component discovery takes precedence over compatibility component declarations, so no OpenAI manifest points at the Claude `.mcp.json`. The additional `.claude-plugin/plugin.json` and `.mcp.json` files provide Claude compatibility; the latter uses Claude's `http` transport label for the same endpoint. Credentials are not embedded in either format.

Codex CLI and the supported desktop app can use repository marketplaces. The Codex IDE extension currently does not provide the plugin browser; use standalone skills and direct MCP configuration there. VS Code's own MCP setup belongs to its AI client and has a different configuration wrapper. Do not assume that installing into one AI client installs into every editor or chat application.

Personal repository installation is not a promise of arbitrary-repository installation on ChatGPT web. Use the supported local desktop/Codex route for this marketplace; use the official service plugins available to your ChatGPT account for ordinary web chats. Workspace marketplace import is a separate admin capability.

Sources: [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins), [OpenAI portable component precedence](https://developers.openai.com/plugins/deploy/submission), [Supported ChatGPT and Codex plugin surfaces](https://learn.chatgpt.com/docs/plugins), [Claude plugin reference](https://code.claude.com/docs/en/plugins-reference), [VS Code MCP setup](https://code.visualstudio.com/docs/agent-customization/mcp-servers).

Endpoint and format references were checked on October 15, 2026. Configuration validation alone does not establish a working member OAuth session or access to real team data.
