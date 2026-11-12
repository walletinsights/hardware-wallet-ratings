#!/usr/bin/env python3
"""Refresh the dataset snapshot from walletinsights.io and regenerate the
ratings table in README.md.

Usage: python3 scripts/update.py

Standard library only. Exits non-zero if a download fails or a file does
not parse, so a broken site build never overwrites a good snapshot.
"""

import csv
import io
import json
import pathlib
import sys
import urllib.request

SITE = "https://walletinsights.io"
FILES = [
    "wallets.json",
    "wallets.csv",
    "security-incidents.json",
    "security-incidents.csv",
]
ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
README = ROOT / "README.md"
START = "<!-- ratings:start -->"
END = "<!-- ratings:end -->"


def fetch(name: str) -> bytes:
    req = urllib.request.Request(
        f"{SITE}/data/{name}",
        headers={"User-Agent": "walletinsights-data-update/1.0"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def validate(name: str, body: bytes) -> None:
    text = body.decode("utf-8")
    if name.endswith(".json"):
        doc = json.loads(text)
        rows = doc.get("wallets") or doc.get("incidents")
        if not rows or len(rows) != doc.get("count"):
            raise ValueError(f"{name}: count does not match rows")
    else:
        rows = list(csv.DictReader(io.StringIO(text)))
        if not rows:
            raise ValueError(f"{name}: no rows")


def ratings_table(wallets: list[dict]) -> str:
    current = [w for w in wallets if not w.get("discontinued")]
    current.sort(key=lambda w: (-w["rating_overall"], w["name"]))
    lines = [
        "| # | Model | Overall | Security | Recovery | Usability | Ecosystem | Privacy | Price, USD |",
        "|---:|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for i, w in enumerate(current, 1):
        price = w.get("price_usd")
        lines.append(
            f"| {i} | [{w['name']}]({w['review_url']}) | **{w['rating_overall']}** "
            f"| {w['rating_security']} | {w['rating_recovery']} | {w['rating_usability']} "
            f"| {w['rating_ecosystem']} | {w['rating_privacy']} "
            f"| {price if price is not None else '—'} |"
        )
    return "\n".join(lines)


def main() -> int:
    bodies = {}
    for name in FILES:
        body = fetch(name)
        validate(name, body)
        bodies[name] = body
    for name, body in bodies.items():
        (DATA / name).write_bytes(body)

    doc = json.loads(bodies["wallets.json"])
    readme = README.read_text(encoding="utf-8")
    head, rest = readme.split(START, 1)
    _, tail = rest.split(END, 1)
    note = f"_Snapshot of {doc['generated']}; discontinued models are in the data files but not in this table._"
    README.write_text(
        f"{head}{START}\n{note}\n\n{ratings_table(doc['wallets'])}\n{END}{tail}",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
