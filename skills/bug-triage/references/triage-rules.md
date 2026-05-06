# Triage Rules & Output Format

## Severity Definitions

| Level    | Meaning                                              | Target Response |
|----------|------------------------------------------------------|-----------------|
| Critical | Production broken, data loss risk, auth failure      | Fix today       |
| High     | Major feature broken, incorrect financial data       | Fix this sprint |
| Medium   | Degraded experience, wrong error codes               | Schedule next   |
| Low      | Cosmetic, preference, minor UX inconsistency         | Backlog         |

## Escalation Rules

- **Critical + unassigned** → escalate to tech lead immediately
- **Critical + open > 1 day** → add ⚠️ ESCALATE flag in digest
- **High + unassigned** → flag for assignment in standup
- **Payments component** → always notify finance team regardless of severity
- **Auth component** → treat as one severity higher than logged

## Component Owners

| Component | Owner          | Slack Handle  |
|-----------|----------------|---------------|
| Auth      | sarah@dev.io   | @sarah        |
| Payments  | james@dev.io   | @james        |
| API       | priya@dev.io   | @priya        |
| UI        | tom@dev.io     | @tom          |

## Output Format

Use this exact structure for the digest:

```
🔴 NEEDS IMMEDIATE ACTION
─────────────────────────
[BUG-ID] Title
Severity: critical | Component: X | Assignee: Y or UNASSIGNED
→ One-line recommended action

🟡 IN PROGRESS
──────────────
[BUG-ID] Title
Severity: high | Component: X | Assignee: Y
→ Current status note

🔵 BACKLOG
──────────
[BUG-ID] Title — severity: medium/low

📊 SUMMARY
──────────
X open bugs | Y in progress | Z resolved today
Oldest open bug: [BUG-ID] — N days old
```

## Tone
- Direct and factual — no filler words
- Engineers read this at 9am, keep it scannable
- Use → for recommended actions, never bullet points within sections
