#!/usr/bin/env python3
"""Preview a work update; send only with --send and SLACK_WEBHOOK_URL."""

import argparse
from http.client import HTTPException
import json
import os
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

EVENTS = {"started": "Started", "blocked": "Needs help", "review": "Ready for review", "completed": "Completed"}


def payload(event, summary, link=None):
    if not summary.strip() or len(summary) > 1000:
        raise ValueError("Use a nonempty summary of at most 1000 characters.")
    text = summary.strip().replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = f"[{EVENTS[event]}] {text}"
    if link:
        parsed = urlsplit(link)
        if (parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password
                or re.search(r"[\s<>|]", link)):
            raise ValueError("The related-work link must be an HTTPS URL without credentials.")
        text += f"\n<{link.replace('&', '&amp;')}|Related work>"
    return {"text": text}


def validate_webhook(url):
    message = "Set SLACK_WEBHOOK_URL to an official Slack incoming webhook URL."
    if any(char.isspace() or ord(char) < 32 or ord(char) == 127 for char in url):
        raise ValueError(message)
    try:
        parsed = urlsplit(url)
        valid = (parsed.scheme == "https" and parsed.hostname == "hooks.slack.com"
                 and not parsed.username and not parsed.password and not parsed.query and not parsed.fragment
                 and parsed.port in (None, 443)
                 and re.fullmatch(r"/services/[A-Za-z0-9_-]+/[A-Za-z0-9_-]+/[A-Za-z0-9_-]+", parsed.path))
    except ValueError:
        raise ValueError(message) from None
    if not valid:
        raise ValueError(message)


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def deliver(url, content):
    validate_webhook(url)
    request = Request(url, data=json.dumps(content).encode("utf-8"),
                      headers={"Content-Type": "application/json"}, method="POST")
    with build_opener(NoRedirect()).open(request, timeout=10) as response:
        if response.status != 200 or response.read(256).strip() != b"ok":
            raise ValueError("Slack did not confirm delivery. No automatic retry was made.")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--event", choices=tuple(EVENTS), required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--link")
    parser.add_argument("--send", action="store_true", help="Send to the webhook's preconfigured channel")
    args = parser.parse_args(argv)
    try:
        content = payload(args.event, args.summary, args.link)
        if not args.send:
            print(json.dumps(content, ensure_ascii=False, indent=2))
            return 0
        url = os.environ.get("SLACK_WEBHOOK_URL", "")
        if not url:
            raise ValueError("SLACK_WEBHOOK_URL is missing. No message was sent.")
        deliver(url, content)
        print("Slack confirmed delivery to the webhook's configured channel.")
    except HTTPError as exc:
        print(f"Slack rejected the notification (HTTP {exc.code}). No automatic retry was made.", file=sys.stderr)
        return 1
    except (URLError, TimeoutError, OSError, HTTPException):
        print("Delivery could not be confirmed. No automatic retry was made.", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
