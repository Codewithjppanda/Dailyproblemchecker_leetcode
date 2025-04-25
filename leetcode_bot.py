import os
import smtplib
import requests
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# ─── Load credentials from .env ───────────────────────
load_dotenv()
LEETCODE_SESSION = os.getenv("LEETCODE_SESSION")
CSRF_TOKEN       = os.getenv("CSRF_TOKEN")
EMAIL_SENDER     = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD   = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER   = os.getenv("EMAIL_RECEIVER")

def make_leetcode_session():
    """
    Create a session with both cookies set manually.
    Avoids any forbidden GETs.
    """
    s = requests.Session()
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/117.0.0.0 Safari/537.36",
        "Referer":    "https://leetcode.com",
        "Origin":     "https://leetcode.com",
    })
    s.cookies.set("LEETCODE_SESSION", LEETCODE_SESSION, domain=".leetcode.com")
    s.cookies.set("csrftoken",       CSRF_TOKEN,       domain=".leetcode.com")
    return s

def check_daily_challenge_status(session):
    """
    Fetch today's activeDailyCodingChallengeQuestion.
    Return (userStatus, title, titleSlug) or (None, None, None).
    """
    payload = {
        "query": """
        query questionOfToday {
          activeDailyCodingChallengeQuestion {
            date
            userStatus
            question {
              title
              titleSlug
            }
          }
        }
        """,
        "variables": {}
    }

    resp = session.post("https://leetcode.com/graphql", json=payload)
    resp.raise_for_status()
    node = resp.json()["data"]["activeDailyCodingChallengeQuestion"]

    # Parse the date field which might be an int (ms) or a "YYYY-MM-DD" string
    raw = node.get("date")
    record_date = None

    # try int (milliseconds)
    try:
        ms = int(raw)
        record_date = datetime.fromtimestamp(ms / 1000).date()
    except (ValueError, TypeError):
        # try ISO string
        try:
            record_date = datetime.fromisoformat(raw).date()
        except Exception:
            pass

    if record_date != datetime.utcnow().date():
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

    if status == "AC":
        subject = "✅ LeetCode Daily Solved!"
        body    = f"You've solved today's problem:\n\n{title}\n" \
                  f"https://leetcode.com/problems/{slug}/"
    elif status:
        subject = "❌ LeetCode Daily NOT Solved!"
        body    = (
            f"You have NOT yet solved today's problem:\n\n"
            f"{title}\nhttps://leetcode.com/problems/{slug}/\n\n"
            "Please complete it before midnight!"
        )
    else:
        subject = "⚠️ LeetCode Check Failed!"
        body    = "Could not fetch today's challenge status. Check your session/CSRF token."

    send_email(subject, body)
    print("Email sent!")

if __name__ == "__main__":
    main()
