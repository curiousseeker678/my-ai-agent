#!/usr/bin/env python3
"""
fetch_bugs.py — Solutions script for bug-triage skill

Reads bugs from artifact storage, filters and sorts them,
and outputs a structured JSON payload ready for digest generation.

Usage:
    python fetch_bugs.py --data '<raw_json_string>'

Output: JSON printed to stdout
"""

import json
import sys
import argparse
from datetime import datetime

SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%d %b %Y")
    except Exception:
        return datetime.now()

def days_open(date_str):
    created = parse_date(date_str)
    return (datetime.now() - created).days

def fetch_and_sort(raw_json: str) -> dict:
    data = json.loads(raw_json)
    bugs = data.get("bugs", [])

    # Exclude resolved
    active = [b for b in bugs if b.get("status") != "resolved"]

    # Sort: severity first, then unassigned first within same severity
    active.sort(key=lambda b: (
        SEVERITY_ORDER.get(b.get("severity", "low"), 99),
        0 if not b.get("assignee") else 1
    ))

    # Categorise
    needs_action = []
    in_progress  = []
    backlog      = []

    for bug in active:
        sev    = bug.get("severity", "low")
        status = bug.get("status", "open")
        comp   = bug.get("component", "")
        d_open = days_open(bug.get("created", ""))

        # Auth component treated as one severity higher
        effective_sev = sev
        if comp == "Auth" and sev == "high":
            effective_sev = "critical"

        bug["days_open"]     = d_open
        bug["effective_sev"] = effective_sev
        bug["escalate"]      = (effective_sev == "critical" and d_open > 1)

        if effective_sev == "critical" or (effective_sev == "high" and not bug.get("assignee")):
            needs_action.append(bug)
        elif status == "in-progress":
            in_progress.append(bug)
        else:
            backlog.append(bug)

    resolved_count = len([b for b in bugs if b.get("status") == "resolved"])

    return {
        "needs_action":   needs_action,
        "in_progress":    in_progress,
        "backlog":        backlog,
        "total_open":     len(active),
        "resolved_today": resolved_count,
        "oldest_bug":     active[-1] if active else None
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True, help="Raw JSON string from storage")
    args = parser.parse_args()
    result = fetch_and_sort(args.data)
    print(json.dumps(result, indent=2))
