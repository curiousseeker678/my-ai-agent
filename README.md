# My AI Agent — Local Setup

A beginner-friendly local AI agent that uses **Skills** and **Tools**
to automate your bug triage process.

No Git. No cloud. Just Python on your laptop.

---

## What's Inside

```
my-ai-agent/
│
├── skills/                   ← WHAT the agent knows (process rules)
│   └── bug-triage/
│       ├── SKILL.md          ← the workflow steps
│       ├── references/
│       │   └── triage-rules.md   ← your team's triage rules
│       └── scripts/
│           └── fetch_bugs.py     ← sorts & filters bug data
│
├── tools/                    ← HOW the agent connects to things
│   └── connectors.py         ← JIRA, Slack stubs (ready to fill in)
│
├── sample-data/
│   └── bugs.json             ← fake bugs to test with
│
├── agent.py                  ← the brain — run this
├── .env.example              ← copy this to .env and add your API key
├── requirements.txt          ← Python packages needed
└── README.md                 ← you are here
```

---

## Setup — 4 Steps

### Step 1 — Make sure Python is installed
Open a terminal and type:
```bash
python --version
```
You should see Python 3.8 or higher. If not, download it from python.org.

### Step 2 — Install dependencies
In the terminal, navigate to this folder:
```bash
cd my-ai-agent
pip install -r requirements.txt
```

### Step 3 — Add your API key
1. Copy `.env.example` and rename it to `.env`
2. Open `.env` in VS Code
3. Replace `your-api-key-here` with your real Anthropic API key
   (Get one free at console.anthropic.com)

Your `.env` should look like:
```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxx
```

### Step 4 — Run the agent
```bash
python agent.py
```

That's it! The agent will start and wait for your input.

---

## Try These Commands

Once the agent is running, type any of these:

```
morning triage
what bugs need attention today
check the backlog
triage bugs
```

The agent will read the sample bugs from `sample-data/bugs.json`
and generate a prioritised digest.

---

## How It Works (Plain English)

```
You type:  "morning triage"
    ↓
agent.py sees the word "triage"
    ↓
Loads skills/bug-triage/SKILL.md        ← Direction (the workflow)
Loads skills/bug-triage/references/     ← Blueprints (the rules)
Runs  skills/bug-triage/scripts/        ← Solutions (the logic)
    ↓
Reads sample-data/bugs.json             ← Tool (data source)
    ↓
Sends everything to Claude API          ← Tool (AI reasoning)
    ↓
Prints your triage digest
```

---

## Customise It

### Change the bugs being triaged
Edit `sample-data/bugs.json` — add your own bugs, change severities,
update assignees. The agent reads this file every time it runs.

### Change the triage rules
Edit `skills/bug-triage/references/triage-rules.md` — update severity
definitions, component owners, escalation rules. No coding required.

### Change the workflow
Edit `skills/bug-triage/SKILL.md` — change the steps the agent follows.

### Connect to real JIRA
Open `tools/connectors.py` — the JIRA function is stubbed out with
comments showing exactly what to fill in.

---

## Files You Should NOT Edit (Unless You Know Python)

- `agent.py` — the orchestration logic
- `skills/bug-triage/scripts/fetch_bugs.py` — the data processing script

---

## Common Errors

**`ModuleNotFoundError: No module named 'anthropic'`**
→ Run `pip install -r requirements.txt` again

**`AuthenticationError: invalid x-api-key`**
→ Check your `.env` file has the correct API key with no spaces

**`FileNotFoundError: bugs.json`**
→ Make sure you're running from inside the `my-ai-agent` folder

---

## What's Next

Once you're comfortable, try:
1. Editing the triage rules in `triage-rules.md`
2. Adding more bugs to `bugs.json`
3. Creating a second skill (e.g. `skills/release-notes/`)
4. Connecting to a real JIRA instance via `tools/connectors.py`
