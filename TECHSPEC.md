# TECHNICAL SPECIFICATION
## Local Telegram Bot for Employee Absence Notifications

---

## 1. Purpose

Develop a local Telegram bot that runs on schedule to:
- Read data from Google Sheets
- Analyze employee absences
- Generate text reports
- Send messages to a Telegram chat

The bot runs locally on a PC without server deployment.

---

## 2. Technology Stack

### Required
- Python 3.10+
- Node.js 18+
- Google Sheets API
- Telegram Bot API

### Libraries

**Python:**
- google-api-python-client
- google-auth
- google-auth-oauthlib
- python-dateutil
- pytz
- python-dotenv

**Node.js:**
- telegraf
- node-cron
- dotenv

---

## 3. Architecture (Local)

- User PC:
  - Visual Studio Code
  - Python runtime
  - Node.js runtime
- Python:
  - Business logic
  - Date handling
  - Google Sheets data processing
  - Message formatting
- Node.js:
  - Scheduler (cron)
  - Telegram message delivery
- Google Sheets:
  - Data source

---

## 4. Data Source — Google Sheets

Sheet: "Absences"

### Table Structure

| Column Name | Description |
|-------------|-------------|
| Type | Vacation / Sick / Other |
| Employee | First Name Last Name |
| Start | Start date (DD.MM.YYYY) |
| End | End date (DD.MM.YYYY) |
| Working days | Number of working days |
| Calendar days | Number of calendar days |

Allowed Type values:
- Vacation
- Sick
- Other

---

## 5. Trigger Logic

Message sending schedule:
- Monday – Thursday: 10:00
- Friday: 10:00

Timezone is configured via environment variable (TIMEZONE).

---

## 6. Date Definitions

- **Today** — current calendar date
- **Next week** — work week (Monday 00:00 – Friday 23:59) of the following calendar week

---

## 7. Business Logic

### 7.1 "Today" Logic

A record is considered active today if:

```
Start ≤ today ≤ End
```

---

### 7.2 "Next Week" Logic (Friday only)

The "Next Week" section is generated only on Fridays.

A record is included if it intersects with the next work week period.

Intersection criteria:

```
Start ≤ end of next week
AND
End ≥ start of next week
```

Includes absences that:
- Start and end within next week
- Start before next week and continue into it
- Start during next week and end after
- Completely cover next week

Excludes absences that:
- Ended before next week starts
- Start after next week ends

Calendar dates are used.
Logic applies only on Fridays.

---

## 8. Message Formatting

### Monday – Thursday

```
🌴 Absence Report

📅 Today

🏖 Vacation
    • First Last
      Start Date – End Date (X days)

🤒 Sick Leave
    • First Last
      Start Date – End Date (X days)
```

---

### Friday

```
🌴 Absence Report

📅 Today

🏖 Vacation
    • ...

🤒 Sick Leave
    • ...

📆 Next Week

🏖 Vacation
    • ...

🤒 Sick Leave
    • ...
```

---

## 9. Code Requirements

- Clean, modular code
- No hardcoded tokens
- Configuration via .env

Recommended structure:

```
bot/
├── config.py
├── sheets.py
├── dates.py
├── formatter.py
├── logic.py
└── bot.py

server/
└── index.js
```

---

## 10. Environment Variables

```
TELEGRAM_BOT_TOKEN
CHAT_ID
SPREADSHEET_ID
GOOGLE_APPLICATION_CREDENTIALS
SHEET_NAME
TIMEZONE
```

---

## 11. API Key Setup

### Telegram
1. Find @BotFather
2. Create a new bot
3. Get BOT TOKEN
4. Get CHAT_ID of target chat

### Google Sheets
1. Create project in Google Cloud
2. Enable Google Sheets API
3. Create Service Account
4. Download credentials.json
5. Share spreadsheet with service account
6. Copy SPREADSHEET_ID

---

## 12. Running

```bash
pip install -r requirements.txt
npm install
npm start
```

---

## 13. Acceptance Criteria

- Bot starts locally
- Messages are sent on schedule
- Date logic is correct
- Next week logic implements range intersection correctly
