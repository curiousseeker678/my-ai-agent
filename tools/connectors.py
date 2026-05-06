"""
tools/connectors.py — External System Connectors
=================================================
These are your TOOLS — functions that connect the agent
to real systems like JIRA, Slack, email, databases, etc.

Right now they are STUBS — they return sample data so
you can run the agent without any real accounts.

When you're ready to connect to real systems, follow
the comments marked with: # REAL CONNECTION →
"""

import os
import json
from pathlib import Path


# ─────────────────────────────────────────
# TOOL 1: BUG DATA SOURCE
# ─────────────────────────────────────────

def get_bugs(source: str = "local") -> dict:
    """
    Fetches bug data from a source.
    Currently reads from sample-data/bugs.json (local).
    
    To connect to JIRA instead:
      1. pip install requests
      2. Set JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN in your .env
      3. Uncomment the REAL CONNECTION block below
    """

    if source == "local":
        # --- LOCAL FILE (default) ---
        bugs_file = Path("./sample-data/bugs.json")
        return json.loads(bugs_file.read_text())

    elif source == "jira":
        # REAL CONNECTION → JIRA
        # Uncomment and fill in when ready:
        #
        # import requests
        #
        # url   = os.getenv("JIRA_URL")           # e.g. https://yourco.atlassian.net
        # email = os.getenv("JIRA_EMAIL")          # e.g. you@yourco.com
        # token = os.getenv("JIRA_API_TOKEN")      # from id.atlassian.com/manage-profile/security
        #
        # response = requests.get(
        #     f"{url}/rest/api/3/search",
        #     params={"jql": "project=BUG AND status!=Done ORDER BY priority DESC"},
        #     auth=(email, token),
        #     headers={"Accept": "application/json"}
        # )
        # raw = response.json()
        #
        # # Map JIRA fields to our bug format
        # bugs = []
        # for issue in raw.get("issues", []):
        #     bugs.append({
        #         "id":        issue["key"],
        #         "title":     issue["fields"]["summary"],
        #         "desc":      issue["fields"].get("description", ""),
        #         "severity":  issue["fields"]["priority"]["name"].lower(),
        #         "status":    issue["fields"]["status"]["name"].lower(),
        #         "assignee":  issue["fields"].get("assignee", {}).get("emailAddress", ""),
        #         "component": issue["fields"].get("components", [{}])[0].get("name", ""),
        #         "created":   issue["fields"]["created"][:10]
        #     })
        # return {"bugs": bugs}

        print("JIRA not configured yet — using local data instead")
        return get_bugs(source="local")

    return get_bugs(source="local")


# ─────────────────────────────────────────
# TOOL 2: SLACK NOTIFICATION
# ─────────────────────────────────────────

def post_to_slack(message: str, channel: str = "#engineering") -> bool:
    """
    Posts a message to a Slack channel.
    Currently just prints to console (stub).

    To connect to real Slack:
      1. pip install slack-sdk
      2. Create a Slack app at api.slack.com
      3. Set SLACK_BOT_TOKEN in your .env
      4. Uncomment the REAL CONNECTION block below
    """

    # --- STUB (default) ---
    print(f"\n[Slack stub] Would post to {channel}:\n{message[:100]}...")
    return True

    # REAL CONNECTION → Slack
    # Uncomment and fill in when ready:
    #
    # from slack_sdk import WebClient
    # from slack_sdk.errors import SlackApiError
    #
    # slack = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
    #
    # try:
    #     slack.chat_postMessage(channel=channel, text=message)
    #     print(f"✓ Posted to Slack {channel}")
    #     return True
    # except SlackApiError as e:
    #     print(f"⚠ Slack error: {e.response['error']}")
    #     return False


# ─────────────────────────────────────────
# TOOL 3: EMAIL NOTIFICATION
# ─────────────────────────────────────────

def send_email(to: str, subject: str, body: str) -> bool:
    """
    Sends an email with the triage digest.
    Currently just prints to console (stub).

    To connect to real email:
      1. pip install sendgrid   (or use smtplib for Gmail)
      2. Set SENDGRID_API_KEY and FROM_EMAIL in your .env
      3. Uncomment the REAL CONNECTION block below
    """

    # --- STUB (default) ---
    print(f"\n[Email stub] Would send to: {to}")
    print(f"             Subject: {subject}")
    print(f"             Body preview: {body[:80]}...")
    return True

    # REAL CONNECTION → SendGrid
    # Uncomment and fill in when ready:
    #
    # import sendgrid
    # from sendgrid.helpers.mail import Mail
    #
    # sg = sendgrid.SendGridAPIClient(api_key=os.getenv("SENDGRID_API_KEY"))
    # mail = Mail(
    #     from_email=os.getenv("FROM_EMAIL"),
    #     to_emails=to,
    #     subject=subject,
    #     plain_text_content=body
    # )
    # response = sg.send(mail)
    # return response.status_code == 202


# ─────────────────────────────────────────
# TOOL 4: DATABASE (future use)
# ─────────────────────────────────────────

def save_digest_to_db(digest: str, date: str) -> bool:
    """
    Saves the triage digest to a database for historical records.
    Currently just saves to a local text file (stub).

    To connect to a real database:
      1. pip install psycopg2  (for PostgreSQL)
         or pip install pymysql  (for MySQL)
      2. Set DB_URL in your .env
      3. Replace the stub below
    """

    # --- STUB: save to local file instead ---
    output_dir = Path("./digest-history")
    output_dir.mkdir(exist_ok=True)

    filename = output_dir / f"digest-{date}.txt"
    filename.write_text(digest)
    print(f"\n[DB stub] Digest saved locally to: {filename}")
    return True
