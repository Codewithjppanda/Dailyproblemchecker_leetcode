import os
import smtplib
import requests
from datetime import datetime, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load credentials from environment
EMAIL_SENDER     = os.environ["EMAIL_SENDER"]
EMAIL_PASSWORD   = os.environ["EMAIL_PASSWORD"]
EMAIL_RECEIVER   = os.environ["EMAIL_RECEIVER"]
LEETCODE_SESSION = os.environ["LEETCODE_SESSION"]
CSRF_TOKEN       = os.environ["CSRF_TOKEN"]

# Any of these (case‐insensitive) count as “solved”
SOLVED_STATUSES = {"ac", "finished", "finish", "completed", "success"}

def make_leetcode_session():
    s = requests.Session()
    s.headers.update({
        "User-Agent":   "Mozilla/5.0",
        "Referer":      "https://leetcode.com",
        "Origin":       "https://leetcode.com",
        "Content-Type": "application/json",
        "Accept":       "application/json",
        "X-CSRFToken":  CSRF_TOKEN
    })
    s.cookies.set("LEETCODE_SESSION", LEETCODE_SESSION, domain=".leetcode.com")
    s.cookies.set("csrftoken", CSRF_TOKEN, domain=".leetcode.com")
    return s

def check_daily_challenge_status(session):
    payload = {
        "query": """
        query {
          activeDailyCodingChallengeQuestion {
            date
            userStatus
            question { title titleSlug }
          }
        }
        """,
        "variables": {}
    }
    resp = session.post("https://leetcode.com/graphql", json=payload)
    resp.raise_for_status()
    node = resp.json()["data"]["activeDailyCodingChallengeQuestion"]

    # Parse the date (either ms‐since‐epoch or ISO string)
    raw = node["date"]
    try:
        record_date = datetime.fromtimestamp(int(raw) / 1000, tz=timezone.utc).date()
    except (ValueError, TypeError):
        record_date = datetime.fromisoformat(raw).date()

    # Only act if it’s truly today’s challenge
    if record_date != datetime.now(timezone.utc).date():
        return None, None, None

    return node["userStatus"], node["question"]["title"], node["question"]["titleSlug"]

def send_email(subject, body):
    msg = MIMEMultipart()
    msg["From"]    = EMAIL_SENDER
    msg["To"]      = EMAIL_RECEIVER
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)

def main():
    session = make_leetcode_session()
    status, title, slug = check_daily_challenge_status(session)
    status_norm = status.lower() if status else None

    if status_norm in SOLVED_STATUSES:
        subject = "✅ LeetCode Daily Solved!"
        body    = f"You've solved today's problem:\n\n{title}\nhttps://leetcode.com/problems/{slug}/"
    elif status_norm:
        # Any other non‐None status (e.g. "notstart", "started", etc.) → not solved
        subject = "❌ LeetCode Daily NOT Solved!"
        body    = (
            f"You have NOT yet solved today's problem:\n\n"
            f"{title}\nhttps://leetcode.com/problems/{slug}/\n\n"
            "Please complete it before midnight!"
        )
    else:
        # status is None → we couldn't fetch today's challenge
        subject = "⚠️ LeetCode Check Failed!"
        body    = "Could not fetch today's challenge status. Check your session/CSRF token."

    send_email(subject, body)
    print("Email sent!")

if __name__ == "__main__":
    main()
