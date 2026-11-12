#!/usr/bin/env python3
"""Publish a new Zenodo version of the dataset when the data has changed enough.

Usage:
  python3 scripts/zenodo.py            # decide, and publish if needed (needs ZENODO_TOKEN)
  python3 scripts/zenodo.py --dry-run  # decide only; public API, no token

A new version is published when, compared with the latest version on Zenodo:
  - the security incidents changed, or
  - at least MIN_RATING_CHANGES models changed their overall rating, or
  - anything changed and the latest version is at least MAX_AGE_DAYS old.
Archiving every small edit would bury the record in near-identical snapshots.

Standard library only.
"""

import csv
import datetime as dt
import hashlib
import io
import json
import os
import pathlib
import sys
import urllib.error
import urllib.request

API = "https://zenodo.org/api"
CONCEPT_ID = "24104206"
FILES = ["wallets.csv", "wallets.json", "security-incidents.csv", "security-incidents.json"]
MIN_RATING_CHANGES = 5
MAX_AGE_DAYS = 30
DATA = pathlib.Path(__file__).resolve().parent.parent / "data"


def request(method, url, token=None, body=None, raw=None, content_type="application/json"):
    headers = {"User-Agent": "walletinsights-data-zenodo/1.0"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    data = None
    if body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = content_type
    elif raw is not None:
        data = raw
        headers["Content-Type"] = "application/octet-stream"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            payload = resp.read()
    except urllib.error.HTTPError as err:
        detail = err.read().decode("utf-8", "replace")[:500]
        raise SystemExit(f"{method} {url} -> HTTP {err.code}: {detail}") from None
    return json.loads(payload) if payload else None


def download(url):
    req = urllib.request.Request(url, headers={"User-Agent": "walletinsights-data-zenodo/1.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read()


def md5(data):
    return "md5:" + hashlib.md5(data).hexdigest()


def overall_ratings(csv_bytes):
    rows = csv.DictReader(io.StringIO(csv_bytes.decode("utf-8")))
    return {r["slug"]: r["rating_overall"] for r in rows}


def decide(latest, local):
    remote = {f["key"]: f for f in latest["files"]}
    changed = [n for n in FILES if remote.get(n, {}).get("checksum") != md5(local[n])]
    if not changed:
        return False, "data identical to the latest Zenodo version"

    if any(n.startswith("security-incidents") for n in changed):
        return True, "security incidents changed"

    old = overall_ratings(download(remote["wallets.csv"]["links"]["self"]))
    new = overall_ratings(local["wallets.csv"])
    moved = sorted(s for s in new.keys() | old.keys() if old.get(s) != new.get(s))
    if len(moved) >= MIN_RATING_CHANGES:
        return True, f"{len(moved)} overall ratings changed"

    published = dt.date.fromisoformat(latest["metadata"]["publication_date"])
    age = (dt.date.today() - published).days
    if age >= MAX_AGE_DAYS:
        return True, f"data changed and the latest version is {age} days old"
    return False, f"{len(moved)} overall ratings changed, latest version {age} days old: below threshold"


def publish(latest, local, token):
    dep = f"{API}/deposit/depositions"
    current = request("GET", f"{dep}/{latest['id']}", token)
    draft_url = current["links"].get("latest_draft")
    if not draft_url or draft_url.rstrip("/").endswith(f"/{latest['id']}"):
        draft_url = request("POST", f"{dep}/{latest['id']}/actions/newversion", token)["links"]["latest_draft"]
    draft = request("GET", draft_url, token)

    for f in draft.get("files", []):
        request("DELETE", f"{draft_url}/files/{f['id']}", token)
    bucket = draft["links"]["bucket"]
    for name in FILES:
        request("PUT", f"{bucket}/{name}", token, raw=local[name])

    today = dt.date.today()
    metadata = draft["metadata"]
    metadata["version"] = today.strftime("%Y.%m.%d")
    metadata["publication_date"] = today.isoformat()
    request("PUT", draft_url, token, body={"metadata": metadata})
    done = request("POST", f"{draft_url}/actions/publish", token)
    return done.get("doi_url") or done["links"].get("html")


def main():
    dry_run = "--dry-run" in sys.argv
    local = {n: (DATA / n).read_bytes() for n in FILES}
    latest = request("GET", f"{API}/records/{CONCEPT_ID}")
    print(f"latest Zenodo version: {latest['metadata'].get('version')} ({latest['id']})")

    publish_now, reason = decide(latest, local)
    print(("publish: " if publish_now else "skip: ") + reason)
    if not publish_now or dry_run:
        return 0

    token = os.environ.get("ZENODO_TOKEN")
    if not token:
        raise SystemExit("ZENODO_TOKEN is not set")
    print("published:", publish(latest, local, token))
    return 0


if __name__ == "__main__":
    sys.exit(main())
