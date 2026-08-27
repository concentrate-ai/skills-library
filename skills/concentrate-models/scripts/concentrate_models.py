#!/usr/bin/env python3
"""Query Concentrate AI's public live model catalog with no dependencies."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

API = "https://api.concentrate.ai/v1/models"


def fetch(path: str = "", params: dict[str, str] | None = None) -> Any:
    url = f"{API}{path}"
    if params:
        url += "?" + urlencode(params)
    request = Request(url, headers={"Accept": "application/json", "User-Agent": "concentrate-skills/1.0"})
    try:
        with urlopen(request, timeout=30) as response:
            return json.load(response)
    except HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Concentrate API returned {error.code}: {body}") from error
    except URLError as error:
        raise RuntimeError(f"Could not reach Concentrate API: {error.reason}") from error


def nested_supported(model: dict[str, Any], capability: str) -> bool:
    value: Any = model.get("capabilities", {})
    for part in capability.split("."):
        if not isinstance(value, dict):
            return False
        value = value.get(part)
    return bool(value.get("supported")) if isinstance(value, dict) else bool(value)


def list_models(args: argparse.Namespace) -> None:
    params: dict[str, str] = {}
    if args.author:
        params["author.slug"] = args.author
    if args.capability:
        params[f"supports.{args.capability}"] = "true"

    if args.provider:
        payload = fetch(f"/providers/{quote(args.provider, safe='')}/models", params)
        models = payload if isinstance(payload, list) else payload.get("data", [])
    else:
        payload = fetch("", params)
        models = payload.get("data", []) if isinstance(payload, dict) else payload

    if args.search:
        term = args.search.casefold()
        models = [
            model for model in models
            if term in " ".join(str(model.get(key, "")) for key in ("id", "slug", "display_name", "name", "owned_by")).casefold()
        ]

    if args.capability and not args.provider:
        normalized = {
            "input.image": "image_input",
            "input.file.pdf": "pdf_input",
            "text.format.json_schema": "structured_outputs",
            "thinking": "thinking",
        }.get(args.capability)
        if normalized:
            models = [model for model in models if nested_supported(model, normalized)]

    def provider_rows(model: dict[str, Any]) -> list[dict[str, Any]]:
        providers = model.get("providers", {})
        if not isinstance(providers, dict):
            return []
        if args.provider and args.provider in providers:
            return [providers[args.provider]]
        return list(providers.values())

    def max_limit(model: dict[str, Any], combined: str, native: str) -> int:
        direct = model.get(combined)
        if isinstance(direct, (int, float)):
            return int(direct)
        values = [row.get(native) for row in provider_rows(model)]
        return max((int(value) for value in values if isinstance(value, (int, float))), default=0)

    key = {
        "name": lambda m: str(m.get("display_name") or m.get("name") or m.get("id") or m.get("slug") or "").casefold(),
        "newest": lambda m: -(m.get("created") or m.get("release_date") or 0),
        "context": lambda m: -max_limit(m, "max_input_tokens", "context_window"),
        "output": lambda m: -max_limit(m, "max_tokens", "max_output_tokens"),
    }[args.sort]
    models.sort(key=key)
    if args.limit is not None and args.limit > 0:
        models = models[: args.limit]

    if args.json:
        print(json.dumps(models, indent=2))
        return

    print(f"{'MODEL':38} {'AUTHOR':14} {'CONTEXT':>12} {'OUTPUT':>12}  CAPABILITIES")
    for model in models:
        identifier = model.get("id") or model.get("slug") or "-"
        author = model.get("owned_by") or (model.get("author") or {}).get("slug") or "-"
        context = max_limit(model, "max_input_tokens", "context_window") or "-"
        output = max_limit(model, "max_tokens", "max_output_tokens") or "-"
        caps = model.get("capabilities", {})
        enabled = [name for name, value in caps.items() if isinstance(value, dict) and value.get("supported")]
        if not enabled:
            rows = provider_rows(model)
            checks = {
                "stream": lambda support: support.get("stream"),
                "tools": lambda support: support.get("tools", {}).get("function_calling"),
                "structured_outputs": lambda support: support.get("text", {}).get("format", {}).get("json_schema"),
                "image_input": lambda support: bool(support.get("input", {}).get("image")),
                "pdf_input": lambda support: bool(support.get("input", {}).get("file", {}).get("pdf")),
            }
            enabled = [
                name for name, check in checks.items()
                if any(check(row.get("supports", {})) for row in rows)
            ]
        print(f"{str(identifier):38.38} {str(author):14.14} {str(context):>12} {str(output):>12}  {','.join(enabled) or '-'}")


def price(provider: dict[str, Any], direction: str) -> str:
    node = provider.get("pricing", {}).get("tokens", {}).get(direction, {})
    usd = node.get("price", {}).get("USD")
    units = node.get("units")
    if usd is None:
        return "-"
    if units == 1000000:
        return f"${usd:g}/M"
    if units == 1000:
        return f"${usd:g}/k"
    return f"${usd:g}/{units or 'unit'}"


def summary(detail: dict[str, Any]) -> dict[str, Any]:
    providers = detail.get("providers", {})
    return {
        "model": detail.get("slug"),
        "name": detail.get("name"),
        "author": (detail.get("author") or {}).get("slug"),
        "providers": [
            {
                "slug": slug,
                "context_window": data.get("context_window"),
                "max_output_tokens": data.get("max_output_tokens"),
                "input_price": price(data, "input"),
                "output_price": price(data, "output"),
                "zdr": isinstance(data.get("zdr"), dict),
                "stream": data.get("supports", {}).get("stream"),
                "tools": data.get("supports", {}).get("tools", {}).get("function_calling"),
                "structured_output": data.get("supports", {}).get("text", {}).get("format", {}).get("json_schema"),
                "image_input": bool(data.get("supports", {}).get("input", {}).get("image")),
                "deprecated_at": data.get("deprecated_at"),
            }
            for slug, data in providers.items()
        ],
    }


def show_model(args: argparse.Namespace) -> None:
    detail = fetch(f"/{quote(args.model, safe='')}")
    print(json.dumps(detail if args.json else summary(detail), indent=2))


def compare_models(args: argparse.Namespace) -> None:
    rows = [summary(fetch(f"/{quote(model, safe='')}")) for model in args.models]
    if args.json:
        print(json.dumps(rows, indent=2))
        return
    print(f"{'MODEL':34} {'PROVIDERS':>9} {'MAX CONTEXT':>12} {'MAX OUTPUT':>12} {'ZDR PROVIDERS'}")
    for row in rows:
        providers = row.get("providers", [])
        contexts = [p.get("context_window") for p in providers if p.get("context_window") is not None]
        outputs = [p.get("max_output_tokens") for p in providers if p.get("max_output_tokens") is not None]
        zdr = ",".join(p.get("slug", "") for p in providers if p.get("zdr")) or "-"
        print(f"{str(row.get('model', '-')):34.34} {len(providers):>9} {str(max(contexts) if contexts else '-'):>12} {str(max(outputs) if outputs else '-'):>12} {zdr}")


def list_providers(args: argparse.Namespace) -> None:
    payload = fetch("/providers")
    providers = payload if isinstance(payload, list) else payload.get("data", [])
    if args.json:
        print(json.dumps(providers, indent=2))
        return
    for provider in providers:
        aliases = ", ".join(provider.get("aliases", []))
        print(f"{provider.get('slug', '-'):16} {provider.get('display_name', '-'):24} {aliases}")


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)

    listing = commands.add_parser("list", help="List or search live models")
    listing.add_argument("--search")
    listing.add_argument("--author")
    listing.add_argument("--provider")
    listing.add_argument("--capability", choices=["input.image", "input.file.pdf", "text.format.json_schema", "tools.function_calling", "stream"])
    listing.add_argument("--sort", choices=["name", "newest", "context", "output"], default="name")
    listing.add_argument("--limit", type=int, default=None, help="Limit number of returned models (default: all)")
    listing.add_argument("--json", action="store_true")
    listing.set_defaults(run=list_models)

    show = commands.add_parser("show", help="Show per-provider details for one model")
    show.add_argument("model")
    show.add_argument("--json", action="store_true")
    show.set_defaults(run=show_model)

    compare = commands.add_parser("compare", help="Compare model limits and ZDR providers")
    compare.add_argument("models", nargs="+")
    compare.add_argument("--json", action="store_true")
    compare.set_defaults(run=compare_models)

    providers = commands.add_parser("providers", help="List provider slugs and aliases")
    providers.add_argument("--json", action="store_true")
    providers.set_defaults(run=list_providers)
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        args.run(args)
        return 0
    except RuntimeError as error:
        print(error, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
