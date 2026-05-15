#!/usr/bin/env python3
"""Small Comfy Cloud inspection helper."""

from __future__ import annotations

import argparse
import json
import os
import sys
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen


BASE_URL = "https://cloud.comfy.org"


def api_get(path: str, params: dict[str, str | int] | None = None) -> object:
    key = os.environ.get("COMFY_API_KEY")
    if not key:
        raise SystemExit("COMFY_API_KEY is not set")

    url = f"{BASE_URL}{path}"
    if params:
        url = f"{url}?{urlencode(params)}"

    request = Request(url, headers={"X-API-Key": key})
    with urlopen(request) as response:
        return json.loads(response.read().decode())


def print_json(value: object) -> None:
    json.dump(value, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def cmd_running_jobs(_: argparse.Namespace) -> None:
    print_json(api_get("/api/jobs", {"status": "pending,in_progress", "limit": 100}))


def cmd_jobs(args: argparse.Namespace) -> None:
    print_json(api_get("/api/jobs", {"limit": args.limit}))


def cmd_assets(args: argparse.Namespace) -> None:
    print_json(api_get("/api/assets", {"limit": args.limit}))


def cmd_saved_workflows(_: argparse.Namespace) -> None:
    print_json(api_get("/api/userdata", {"dir": "workflows"}))


def cmd_workflow(args: argparse.Namespace) -> None:
    path = args.path
    if not path.startswith("workflows/"):
        path = f"workflows/{path}"
    print_json(api_get(f"/api/userdata/{quote(path, safe='')}"))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Inspect Comfy Cloud account state.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    running = subparsers.add_parser("running-jobs", help="List pending and in-progress jobs.")
    running.set_defaults(func=cmd_running_jobs)

    jobs = subparsers.add_parser("jobs", help="List recent jobs.")
    jobs.add_argument("--limit", type=int, default=20)
    jobs.set_defaults(func=cmd_jobs)

    assets = subparsers.add_parser("assets", help="List recent assets.")
    assets.add_argument("--limit", type=int, default=20)
    assets.set_defaults(func=cmd_assets)

    saved = subparsers.add_parser("saved-workflows", help="List saved workflow files.")
    saved.set_defaults(func=cmd_saved_workflows)

    workflow = subparsers.add_parser("workflow", help="Read one saved workflow JSON file.")
    workflow.add_argument("path", help="Workflow filename or workflows/<filename>.json path.")
    workflow.set_defaults(func=cmd_workflow)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
