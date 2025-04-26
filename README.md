```

---

### ✅ Updated `README.md`

```markdown
# 📬 LeetCode Daily Problem Checker Bot

This is a fully automated Python bot that checks whether you've solved the **LeetCode Daily Challenge** — and sends you a personalized email notification daily at **11:55 PM IST**.

> 🚀 Runs on **GitHub Actions**, so you don’t need to keep your laptop on — works from the cloud.

---

## 🔧 Built With

- 🐍 **Python** – for script logic and email sending (SMTP)
- ⚙️ **GitHub Actions** – to schedule daily execution at 11:55 PM IST
- 📬 **Gmail App Passwords** – for secure email authentication
- 🔐 **GitHub Secrets** – to store your credentials safely
- 🔎 **LeetCode GraphQL API** – to check your daily problem status via `activeDailyCodingChallengeQuestion`

---

## 📸 Example Email

> Here's what you get daily in your inbox:

![LeetCode Daily Email Screenshot](https://github.com/user-attachments/assets/65e066b7-ad02-48c0-ad06-a8521eb8c40c)

---

## 💡 Why This Project?

I wanted something that keeps me accountable with LeetCode daily challenges — without relying on streaks or pop-ups. So I built a fully cloud-based reminder system that emails me whether I’ve solved the problem or not.

Along the way, I learned:
- How to authenticate with LeetCode using cookies and CSRF tokens
- How to query LeetCode’s private GraphQL API
- How to automate cloud scripts using GitHub Actions
- How to secure sensitive info using GitHub Secrets

---

## 📁 Folder Structure

```bash
Dailyproblemchecker_leetcode/
├── leetcode_bot.py          # Main script
├── requirements.txt         # Dependencies
├── .github/workflows/
│   └── daily_check.yml      # GitHub Actions workflow file
```

---

## ⚙️ Setup Instructions

### 1. Fork or clone this repo

```bash
git clone https://github.com/Codewithjppanda/Dailyproblemchecker_leetcode.git
cd Dailyproblemchecker_leetcode
```

### 2. Create your `requirements.txt`

```txt
requests
```

### 3. Update your GitHub Secrets

Go to:  
`GitHub → Settings → Secrets → Actions → New Repository Secret`

Add the following:

| Key               | Value                         |
|------------------|-------------------------------|
| `EMAIL_SENDER`     | Your Gmail address             |
| `EMAIL_PASSWORD`   | Gmail App Password (not normal password) |
| `EMAIL_RECEIVER`   | Receiver email address         |
| `LEETCODE_SESSION` | Your session cookie from browser |
| `CSRF_TOKEN`       | Your `csrftoken` from browser  |

### 4. GitHub Workflow

The workflow is set to run:

```yaml
schedule:
  - cron: '25 18 * * *' # This runs daily at 11:55 PM IST
```

You can also run it manually from the **Actions** tab on GitHub.

---

## 🔗 Repository URL

[👉 View the repo](https://github.com/Codewithjppanda/Dailyproblemchecker_leetcode)

---

## 🛡️ Security Tips

- Never commit your `.env` file or credentials
- Always use GitHub Secrets for sensitive data
- Revoke leaked Gmail App Passwords immediately

---

## ⭐ Want to Support?

Give this repo a ⭐ if it helps you stay consistent with LeetCode!

---

## 📜 License

MIT License — free to use and modify.

---

## 🔥 Bonus Ideas (Pull Requests Welcome!)

- [ ] Add Discord/Telegram bot notification support
- [ ] Log daily statuses in a Google Sheet or CSV
- [ ] Send weekly summary email with streak insights

---

## 🤝 Let's Connect

Built by [@Codewithjppanda](https://github.com/Codewithjppanda) — feel free to fork, star, or suggest improvements!
```
