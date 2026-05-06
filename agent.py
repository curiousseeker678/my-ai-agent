"""
agent.py — The Brain of Your Local AI Agent
============================================
This is the main file you run. It:
  1. Listens for your input
  2. Decides which skill to use
  3. Loads the skill files (Direction + Blueprints)
  4. Runs the solution script (Solutions)
  5. Calls the AI with everything loaded
  6. Prints the result

Run it with:  python agent.py
Stop it with: type 'exit' or press Ctrl+C
"""

import os
import json
import subprocess
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic

# ─────────────────────────────────────────
# 1. SETUP
# ─────────────────────────────────────────

# Load your API key from the .env file
load_dotenv()

# Connect to the AI
client = Anthropic()

# Tell the agent where your skills live
SKILLS_DIR  = Path("./skills")
DATA_DIR    = Path("./sample-data")


# ─────────────────────────────────────────
# 2. SKILL LOADER  (loads Direction + Blueprints)
# ─────────────────────────────────────────

def load_skill(skill_name: str) -> str:
    """
    Reads the SKILL.md and all reference files for a given skill.
    This becomes the system prompt — telling the AI exactly how to behave.
    """
    skill_path = SKILLS_DIR / skill_name

    # Check the skill exists
    if not skill_path.exists():
        raise FileNotFoundError(
            f"Skill '{skill_name}' not found in {SKILLS_DIR}. "
            f"Available skills: {[d.name for d in SKILLS_DIR.iterdir() if d.is_dir()]}"
        )

    # --- Direction: load SKILL.md ---
    skill_md = skill_path / "SKILL.md"
    system_prompt = skill_md.read_text(encoding="utf-8")
    print(f"  ✓ Direction loaded:   {skill_md}")

    # --- Blueprints: load all .md files in references/ ---
    refs_dir = skill_path / "references"
    if refs_dir.exists():
        for ref_file in sorted(refs_dir.glob("*.md")):
            system_prompt += f"\n\n---\n### Reference: {ref_file.name}\n"
            system_prompt += ref_file.read_text(encoding="utf-8")
            print(f"  ✓ Blueprints loaded:  {ref_file}")

    return system_prompt


# ─────────────────────────────────────────
# 3. SOLUTION RUNNER  (runs the Python script)
# ─────────────────────────────────────────

def run_solution(skill_name: str, data: str) -> dict:
    """
    Runs the fetch_bugs.py script from the skill's scripts/ folder.
    This is your Solutions layer — precise, repeatable data processing.
    Returns structured JSON the AI can reason over.
    """
    script_path = SKILLS_DIR / skill_name / "scripts" / "fetch_bugs.py"

    if not script_path.exists():
        # No script for this skill — just return raw data
        return json.loads(data)

    print(f"  ✓ Solutions running:  {script_path}")

    result = subprocess.run(
        ["python", str(script_path), "--data", data],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"  ⚠ Script error: {result.stderr}")
        return json.loads(data)   # fall back to raw data

    return json.loads(result.stdout)


# ─────────────────────────────────────────
# 4. TOOL: READ BUGS  (your data source)
# ─────────────────────────────────────────

def read_bugs() -> str:
    """
    Tool: reads bug data from sample-data/bugs.json.
    In a real setup, this is where you'd call JIRA, a database,
    or any internal system instead.
    """
    bugs_file = DATA_DIR / "bugs.json"

    if not bugs_file.exists():
        raise FileNotFoundError(
            f"No bug data found at {bugs_file}. "
            "Create sample-data/bugs.json to get started."
        )

    print(f"  ✓ Tool (data):        {bugs_file}")
    return bugs_file.read_text(encoding="utf-8")


# ─────────────────────────────────────────
# 5. SKILL ROUTER  (decides which skill to use)
# ─────────────────────────────────────────

def detect_skill(user_input: str) -> str:
    """
    Looks at what you typed and picks the right skill.
    As you add more skills, add more keywords here.
    """
    text = user_input.lower()

    triage_keywords = [
        "triage", "bugs", "backlog", "digest",
        "morning", "what's open", "attention", "check bugs"
    ]

    if any(word in text for word in triage_keywords):
        return "bug-triage"

    # Default — add more skills here as you build them
    # e.g. "release" → "release-notes"
    # e.g. "pr" or "review" → "pr-reviewer"
    return "bug-triage"


# ─────────────────────────────────────────
# 6. MAIN AGENT  (orchestrates everything)
# ─────────────────────────────────────────

def run_agent(user_input: str) -> str:
    """
    The full pipeline:
      Direction + Blueprints → Solutions → Tool → AI → Output
    """
    print("\n── Running agent pipeline ──────────────────")

    # Step 1: pick the right skill
    skill_name = detect_skill(user_input)
    print(f"  ✓ Skill detected:     {skill_name}")

    # Step 2: load Direction + Blueprints (system prompt)
    system_prompt = load_skill(skill_name)

    # Step 3: Tool — read the bug data
    raw_data = read_bugs()

    # Step 4: Solutions — run the processing script
    structured_data = run_solution(skill_name, raw_data)

    # Step 5: Tool — call the AI with everything loaded
    print(f"  ✓ Tool (AI):          Claude API")
    print("── Generating digest ───────────────────────\n")

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1000,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": (
                    f"{user_input}\n\n"
                    f"Here is the structured bug data:\n"
                    f"{json.dumps(structured_data, indent=2)}"
                )
            }
        ]
    )

    return response.content[0].text


# ─────────────────────────────────────────
# 7. ENTRY POINT  (the interactive loop)
# ─────────────────────────────────────────

def main():
    print("╔════════════════════════════════════════╗")
    print("║        Local AI Agent — Ready          ║")
    print("╠════════════════════════════════════════╣")
    print("║  Try typing:  morning triage           ║")
    print("║               what bugs need attention ║")
    print("║               check the backlog        ║")
    print("║  To quit:     exit                     ║")
    print("╚════════════════════════════════════════╝\n")

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ("exit", "quit", "q"):
                print("Agent: Goodbye!")
                break

            result = run_agent(user_input)
            print(f"\nAgent:\n{result}\n")
            print("─" * 45 + "\n")

        except FileNotFoundError as e:
            print(f"\n⚠ Setup error: {e}\n")

        except KeyboardInterrupt:
            print("\n\nAgent: Goodbye!")
            break

        except Exception as e:
            print(f"\n⚠ Something went wrong: {e}\n")


if __name__ == "__main__":
    main()
