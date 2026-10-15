import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import tomllib
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


configure = module("configure")
slack = module("slack_notify")
packages = module("package_skills")


class ConfigurationTests(unittest.TestCase):
    def test_codex_snippet_is_valid_toml_and_keeps_token_as_reference(self):
        with patch.dict(os.environ, {"GITHUB_MCP_TOKEN": "private-test-value"}):
            rendered = configure.render("codex", ["notion", "github", "atlassian"])
        servers = tomllib.loads(rendered)["mcp_servers"]
        self.assertEqual(servers["team-github"]["bearer_token_env_var"], "GITHUB_MCP_TOKEN")
        self.assertEqual(servers["team-github"]["http_headers"]["X-MCP-Readonly"], "true")
        self.assertNotIn("private-test-value", rendered)
        self.assertEqual(len(servers), 3)

    def test_json_clients_use_their_own_schema_and_variable_syntax(self):
        claude = json.loads(configure.render("claude-code", ["github", "notion"]))
        vscode = json.loads(configure.render("vscode", ["github", "notion"]))
        self.assertEqual(claude["mcpServers"]["team-github"]["headers"]["Authorization"],
                         "Bearer ${GITHUB_MCP_TOKEN}")
        self.assertEqual(vscode["servers"]["team-github"]["headers"]["Authorization"],
                         "Bearer ${env:GITHUB_MCP_TOKEN}")

    def test_existing_configuration_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "settings.toml"
            target.write_text("existing unrelated settings", encoding="utf-8")
            with contextlib.redirect_stderr(io.StringIO()):
                code = configure.main(["export", "--client", "codex", "--connectors", "notion", "--output", str(target)])
            self.assertEqual(code, 2)
            self.assertEqual(target.read_text(), "existing unrelated settings")

    def test_slack_is_guided_and_cannot_be_exported_as_generic_oauth(self):
        with self.assertRaisesRegex(ValueError, "registered Slack app"):
            configure.render("codex", ["slack"])

    def test_duplicate_connector_has_only_one_entry(self):
        result = json.loads(configure.render("claude-code", ["notion", "notion"]))
        self.assertEqual(len(result["mcpServers"]), 1)

    def test_packages_are_uploadable_and_cannot_replace_existing_packages(self):
        with tempfile.TemporaryDirectory() as directory:
            archives = packages.build(directory)
            self.assertEqual(len(archives), 4)
            for path in archives:
                with zipfile.ZipFile(path) as archive:
                    self.assertIn(f"{path.stem}/SKILL.md", archive.namelist())
                    self.assertFalse(any(name.startswith("/") or ".." in Path(name).parts for name in archive.namelist()))
            with self.assertRaises(FileExistsError):
                packages.build(directory)


class SlackTests(unittest.TestCase):
    def test_preview_cannot_send_even_with_a_configured_webhook(self):
        with patch.dict(os.environ, {"SLACK_WEBHOOK_URL": "https://hooks.slack.com/services/TTEST/BTEST/secret"}), \
                patch.object(slack, "deliver") as deliver, contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(slack.main(["--event", "started", "--summary", "Working on a task"]), 0)
            deliver.assert_not_called()

    def test_send_requires_credentials_and_does_not_print_them(self):
        output = io.StringIO()
        with patch.dict(os.environ, {}, clear=True), patch.object(slack, "deliver") as deliver, \
                contextlib.redirect_stderr(output):
            self.assertEqual(slack.main(["--event", "started", "--summary", "Task", "--send"]), 2)
            deliver.assert_not_called()
        self.assertIn("missing", output.getvalue())

    def test_payload_escapes_mentions_and_rejects_injected_links(self):
        result = slack.payload("started", "Try <@U123> & inspect")
        self.assertIn("&lt;@U123&gt; &amp;", result["text"])
        with self.assertRaises(ValueError):
            slack.payload("started", "Task", "https://example.com/|<!channel>")

    def test_webhook_rejects_other_hosts_and_embedded_credentials(self):
        for url in ("https://hooks.slack.com.attacker.test/services/T/B/S", "http://hooks.slack.com/services/T/B/S",
                    "https://user:secret@hooks.slack.com/services/T/B/S", "https://hooks.slack.com/services/T/B/S?secret=x"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                slack.validate_webhook(url)

    def test_delivery_confirms_slack_response(self):
        with patch.object(slack, "build_opener") as opener:
            response = opener.return_value.open.return_value.__enter__.return_value
            response.status = 200
            response.read.return_value = b"ok"
            slack.deliver("https://hooks.slack.com/services/TTEST/BTEST/secret", {"text": "Task"})
            request = opener.return_value.open.call_args.args[0]
            self.assertEqual(request.get_method(), "POST")
            self.assertEqual(json.loads(request.data), {"text": "Task"})

    def test_invalid_webhook_cannot_leak_secret_in_failure_output(self):
        for url in ("https://hooks.slack.com/services/TTEST/BTEST/fake\n-secret",
                    "https://hooks.slack.com:fake-secret/services/TTEST/BTEST/key"):
            output = io.StringIO()
            with self.subTest(url="malformed webhook"), patch.dict(os.environ, {"SLACK_WEBHOOK_URL": url}), \
                    patch.object(slack, "build_opener") as opener, contextlib.redirect_stderr(output):
                self.assertEqual(slack.main(["--event", "started", "--summary", "Task", "--send"]), 2)
                opener.assert_not_called()
                self.assertNotIn("fake", output.getvalue())


if __name__ == "__main__":
    unittest.main()
