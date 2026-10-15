#!/usr/bin/env python3
"""Generate credential-free MCP snippets without editing client settings."""

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "connectors" / "catalog.json"


def load_catalog():
    return json.loads(CATALOG.read_text(encoding="utf-8"))["connectors"]


def render(client, names):
    catalog = load_catalog()
    if not names:
        raise ValueError("Choose at least one connector.")
    selected = {}
    for name in dict.fromkeys(names):
        if name not in catalog:
            raise ValueError(f"Unknown connector: {name}")
        item = catalog[name]
        if item["mode"] != "remote":
            raise ValueError(f"{item['name']}: {item['reason']}")
        selected[f"team-{name}"] = item

    if client == "codex":
        lines = ["# Merge these tables into your existing Codex configuration.",
                 "# Authenticate each connector separately; no credentials are included."]
        for name, item in selected.items():
            lines.extend(["", f"[mcp_servers.{name}]", f"url = {json.dumps(item['url'])}"])
            if item["auth"] == "bearer-env":
                lines.append(f"bearer_token_env_var = {json.dumps(item['token_env'])}")
            headers = item.get("headers", {})
            if headers:
                values = ", ".join(f"{json.dumps(k)} = {json.dumps(v)}" for k, v in headers.items())
                lines.append(f"http_headers = {{ {values} }}")
        return "\n".join(lines) + "\n"

    if client not in ("claude-code", "vscode"):
        raise ValueError(f"Unsupported client: {client}")
    servers = {}
    for name, item in selected.items():
        config = {"type": "http", "url": item["url"]}
        headers = dict(item.get("headers", {}))
        if item["auth"] == "bearer-env":
            prefix = "env:" if client == "vscode" else ""
            headers["Authorization"] = "Bearer ${" + prefix + item["token_env"] + "}"
        if headers:
            config["headers"] = headers
        servers[name] = config
    key = "servers" if client == "vscode" else "mcpServers"
    return json.dumps({key: servers}, indent=2) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list", help="Show available connectors and authentication methods")
    export = commands.add_parser("export", help="Print a snippet, or write a new file")
    export.add_argument("--client", choices=("codex", "claude-code", "vscode"), required=True)
    export.add_argument("--connectors", nargs="+", required=True)
    export.add_argument("--output", type=Path, help="New file only; existing files are never replaced")
    args = parser.parse_args(argv)
    if args.command == "list":
        for name, item in load_catalog().items():
            print(f"{name:12} {item['auth']:18} {item['name']}")
        return 0
    try:
        content = render(args.client, args.connectors)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with args.output.open("x", encoding="utf-8") as handle:
                handle.write(content)
            print(f"Created {args.output}. Merge it into your settings, then authenticate.")
        else:
            print(content, end="")
    except (ValueError, OSError) as exc:
        print(f"Configuration not written: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
