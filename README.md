# Absence Notification Bot

A Telegram bot that reads employee absence data from Google Sheets and sends scheduled reports to a Telegram chat. Perfect for keeping your team informed about who's on vacation, sick leave, or otherwise unavailable.

## Features

- **Scheduled Reports**: Automatic daily reports at 10:00 AM on weekdays (Monday-Friday)
- **Friday Preview**: Additional "next week" preview report on Fridays
- **On-Demand Reports**: Manual report generation via `/report` command
- **Multiple Absence Types**: Supports Vacation, Sick Leave, and Other absence categories
- **Configurable Timezone**: Set your local timezone for accurate scheduling
- **Google Sheets Integration**: Easy data management through familiar spreadsheet interface

## Project Structure

```
absence-bot/
├── bot/                        # Python modules
│   ├── bot.py                  # Entry point - generates reports
│   ├── config.py               # Configuration from environment variables
│   ├── sheets.py               # Google Sheets API integration
│   ├── dates.py                # Date utilities and timezone handling
│   ├── logic.py                # Business logic for filtering absences
│   └── formatter.py            # Message formatting for Telegram
├── server/                     # Node.js server
│   └── index.js                # Telegram bot and cron scheduler
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
├── package.json                # Node.js dependencies
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Requirements

- **Python** 3.10 or higher
- **Node.js** 18 or higher
- **Google Cloud** account with Sheets API enabled
- **Telegram Bot** (created via @BotFather)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/absence-bot.git
cd absence-bot
```

### 2. Install Python Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Install Node.js Dependencies

```bash
npm install
```

### 4. Configure Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your actual values
```

## Configuration

### Telegram Bot Setup

1. Open Telegram and search for **@BotFather**
2. Send `/newbot` command
3. Enter a name for your bot (e.g., "Absence Notifier")
4. Enter a username (must end with `bot`, e.g., `my_absence_bot`)
5. Copy the token (format: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)
6. Paste into `TELEGRAM_BOT_TOKEN` in `.env`

### Getting Chat ID

**Option 1: Personal Chat (via @userinfobot)**
1. Search for **@userinfobot** in Telegram
2. Send any message
3. Copy the ID from the response

**Option 2: Group Chat (via @RawDataBot)**
1. Add **@RawDataBot** to your group
2. Find `"id"` in the `"chat"` section of the response
3. Group IDs are negative (e.g., `-1001234567890`)

**Option 3: Via API**
1. Add your bot to the target chat
2. Send a message in the chat
3. Open: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
4. Find `"chat":{"id":...}` in the response

### Google Sheets API Setup

#### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Note your project ID

#### Step 2: Enable Google Sheets API

1. Navigate to **APIs & Services** → **Library**
2. Search for **Google Sheets API**
3. Click **Enable**

#### Step 3: Create Service Account

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **Service Account**
3. Fill in:
   - Service account name: `sheets-bot`
   - Service account ID: (auto-generated)
4. Click **Create and Continue**
5. Skip the role selection
6. Click **Done**

#### Step 4: Download Credentials

1. Click on the created service account
2. Go to **Keys** tab
3. Click **Add Key** → **Create new key**
4. Select **JSON** and click **Create**
5. Rename the downloaded file to `credentials.json`
6. Place it in the project root directory

#### Step 5: Share Spreadsheet with Service Account

1. Open `credentials.json` and copy the `client_email` value
2. Open your Google Spreadsheet
3. Click **Share**
4. Paste the service account email
5. Set permission to **Viewer**
6. Click **Send**

#### Step 6: Get Spreadsheet ID

1. Open your spreadsheet in browser
2. URL format: `https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit`
3. Copy the `SPREADSHEET_ID` portion
4. Paste into `.env`

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `TELEGRAM_BOT_TOKEN` | Yes | Bot token from @BotFather |
| `CHAT_ID` | Yes | Target chat ID for messages |
| `SPREADSHEET_ID` | Yes | Google Sheets document ID |
| `GOOGLE_APPLICATION_CREDENTIALS` | Yes | Path to credentials.json |
| `SHEET_NAME` | No | Sheet/tab name (default: `Absences`) |
| `TIMEZONE` | No | Timezone (default: `Europe/Moscow`) |

## Google Sheets Structure

Create a sheet named **Absences** (or specify a custom name in `SHEET_NAME`) with the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| Type | Absence type | Vacation, Sick, Other |
| Employee | Full name | John Smith |
| Start | Start date (DD.MM.YYYY) | 20.01.2025 |
| End | End date (DD.MM.YYYY) | 31.01.2025 |
| Working days | Number of work days | 8 |
| Calendar days | Total calendar days | 12 |

### Example Data

| Type | Employee | Start | End | Working days | Calendar days |
|------|----------|-------|-----|--------------|---------------|
| Vacation | John Smith | 20.01.2025 | 31.01.2025 | 8 | 12 |
| Sick | Jane Doe | 22.01.2025 | 24.01.2025 | 3 | 3 |
| Other | Bob Wilson | 25.01.2025 | 25.01.2025 | 1 | 1 |

### Absence Type Classification

| Type | Description | Report Section |
|------|-------------|----------------|
| `Vacation` | Planned time off, holidays | Grouped under "Vacation" |
| `Sick` | Sick leave, medical absence | Grouped under "Sick Leave" |
| `Other` | Training, business trips, etc. | Grouped under "Other" |

## Running the Bot

```bash
npm start
```

The bot will:
- Start listening for commands
- Send automatic reports at 10:00 AM on weekdays
- Respond to `/report` command anytime

## Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Display bot information |
| `/report` | Generate and send report immediately |
| `/help` | Show available commands |

## Report Format Example

### Monday-Thursday Report

```
🌴 Absence Report

📅 Today

🏖 Vacation
    • John Smith
      20.01.2025 – 31.01.2025 (12 days)

🤒 Sick Leave
    • Jane Doe
      22.01.2025 – 24.01.2025 (3 days)
```

### Friday Report (with Next Week Preview)

```
🌴 Absence Report

📅 Today

🏖 Vacation
    • John Smith
      20.01.2025 – 31.01.2025 (12 days)

📆 Next Week

🏖 Vacation
    • John Smith
      20.01.2025 – 31.01.2025 (12 days)
    • Alice Brown
      27.01.2025 – 31.01.2025 (5 days)
```

### No Absences Report

```
🌴 Absence Report

✅ Everyone is present today!
```

## Filtering Logic

### Today's Absences

An absence is shown in "Today" section if:
```
Start Date ≤ Today ≤ End Date
```

### Next Week Absences (Friday only)

An absence is shown in "Next Week" section if it intersects with the next work week (Monday-Friday):
```
Start Date ≤ Next Friday AND End Date ≥ Next Monday
```

This includes absences that:
- Start and end within next week
- Start before next week and continue into it
- Start during next week and end after
- Completely span next week

## Troubleshooting

### Bot doesn't respond to commands

- Verify `TELEGRAM_BOT_TOKEN` is correct
- Ensure bot is added to the chat (for groups)
- Check that the bot has message permissions

### Google Sheets access error

- Verify spreadsheet is shared with the service account email
- Check that `SPREADSHEET_ID` is correct
- Confirm Google Sheets API is enabled in your project
- Ensure `credentials.json` path is correct

### Scheduled messages not sending

- Verify `TIMEZONE` setting matches your location
- Ensure Node.js process is running
- Check that today is a weekday (Mon-Fri)

### "Missing required environment variables" error

- Verify `.env` file exists in project root
- Check all required variables are filled in
- Ensure no extra spaces around values

## License

This project is licensed under the MIT License - see below for details.

```
MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
