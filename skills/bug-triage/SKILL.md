---
name: bug-triage
description: >
  Reads the bug tracker and produces a prioritised morning triage digest.
  Use this skill whenever the user says "morning triage", "triage bugs",
  "bug digest", "what bugs need attention", "check the backlog",
  "what's open", or asks for a summary of current bugs or issues.
  Always activate for any request to summarise, prioritise, or review bugs.
---

# Bug Triage Skill

Produces a clear, prioritised digest of open bugs so the team knows
exactly what to work on today. Takes ~30 seconds. No manual spreadsheet
scanning required.

## Workflow

### Step 1 — Load triage rules
Read `references/triage-rules.md` before doing anything else.
This tells you how to classify severity, who to escalate to, and
what the output format should look like.

### Step 2 — Read the bug data
The bugs live in the artifact storage under the key `bugs`.
The data shape is:
```json
{
  "bugs": [
    {
      "id": "BUG-001",
      "title": "...",
      "desc": "...",
      "severity": "critical | high | medium | low",
      "status": "open | in-progress | resolved",
      "assignee": "...",
      "component": "...",
      "created": "DD Mon YYYY"
    }
  ]
}
```

### Step 3 — Filter and sort
- Exclude bugs with status `resolved`
- Sort remaining bugs: critical → high → medium → low
- Within same severity, surface unassigned bugs first

### Step 4 — Generate the digest
Follow the output format in `references/triage-rules.md` exactly.
Produce three sections:
1. **Needs immediate action** — critical + unassigned high bugs
2. **In progress** — bugs actively being worked on
3. **Backlog** — assigned medium/low bugs not yet started

### Step 5 — Flag blockers
If any critical bug has been open for more than 1 day, add a
⚠️ ESCALATE flag and note the days open next to it.

### Step 6 — Recommend next action
End with one sentence per critical/high bug: what the on-call engineer
should do first thing today.

## Rules
- Never include resolved bugs in the digest
- Always show bug ID alongside the title
- Keep descriptions to one line — link to detail if needed
- If there are zero open bugs, say so clearly and congratulate the team
- Severity labels must match exactly: critical, high, medium, low
