# Slack Prayer Reminder Bot

A production-ready, well-structured prayer reminder bot that sends beautiful, motivational reminders to Slack channels with Quran verses and AI-generated messages.

## 🚀 Features

- **Automated Prayer Reminders**: Sends reminders 10 minutes before each prayer time
- **AI-Generated Messages**: Uses Google Gemini AI to create unique motivational messages for each prayer
- **Quran Integration**: Includes random Quran verses (Arabic + Urdu) with each reminder
- **Beautiful Slack Messages**: Rich formatting with emojis, headers, and structured content
- **Database Persistence**: SQLite database to track prayer times and sent reminders
- **Production-Ready**: Proper error handling, logging, and scheduled jobs
- **Secure Configuration**: Environment variables for API keys

## 📁 Project Structure

```
slack-prayer-reminder/
├── main.py                 # Main application entry point and scheduler
├── config.py               # All configuration variables
├── requirements.txt        # Python dependencies
├── services/
│   ├── __init__.py
│   ├── aladhan_service.py    # Handles fetching prayer times
│   ├── slack_service.py      # Handles sending Slack messages
│   ├── gemini_service.py     # Handles generating motivational messages
│   └── db_service.py         # Handles all database interactions
├── data/
│   ├── quran.json           # Arabic Quran verses
│   └── ur.json              # Urdu Quran translations
└── prayer_times.db          # SQLite database (created automatically)
```

## 🛠️ Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root with your API keys:

```env
# --- SECRETS ---
GEMINI_API_KEY="AIzaSy...YOUR_GEMINI_KEY"
SLACK_BOT_TOKEN="xoxb-...YOUR_SLACK_TOKEN"
```

**⚠️ IMPORTANT**: 
- Replace the exposed tokens in your current code with new ones
- Never commit API keys to version control
- Use environment variables for all secrets

### 3. Configure Bot Settings

Edit `config.py` to customize:
- **Location**: Latitude/Longitude for prayer times
- **Channel**: Your Slack channel ID
- **Reminder Timing**: How many minutes before prayer to send reminders
- **Prayer Method**: Islamic calculation method (default: University of Islamic Sciences, Karachi)

### 4. Invite Bot to Channel

In your Slack channel, type:
```
/invite @YourBotName
```

### 5. Run the Bot

```bash
python main.py
```

## 🔧 How It Works

### Daily Setup Job (1:00 AM)
1. **Fetch Prayer Times**: Gets today's prayer times from AlAdhan API
2. **Generate Messages**: Uses Gemini AI to create motivational messages for each prayer
3. **Save to Database**: Stores everything in SQLite for the day

### Reminder Check Job (Every Minute)
1. **Check Due Reminders**: Looks for prayers due for reminders
2. **Get Quran Verse**: Selects a random verse from your Quran data
3. **Send Slack Message**: Formats and sends beautiful reminder with:
   - Prayer name and time
   - AI-generated motivational message
   - Random Quran verse (Arabic + Urdu)
   - Next prayer information

## 📊 Database Schema

```sql
CREATE TABLE daily_prayers (
    prayer_name TEXT PRIMARY KEY,
    prayer_time TEXT NOT NULL,
    reminder_message TEXT NOT NULL,
    reminder_sent INTEGER NOT NULL DEFAULT 0
);
```

## 🔒 Security Features

- **Environment Variables**: All secrets stored in `.env` file
- **Input Validation**: Proper error handling for API responses
- **Rate Limiting**: Built-in retry logic for API calls
- **Database Security**: SQLite with proper parameterized queries

## 🎨 Message Format

Each reminder includes:
- **Header**: Prayer name and time with mosque emoji
- **Motivational Message**: AI-generated unique message for each prayer
- **Quran Verse**: Random verse in Arabic and Urdu
- **Next Prayer Info**: Time of the next prayer

## 🚨 Troubleshooting

### Common Issues

1. **"API keys missing"**: Check your `.env` file exists and has correct keys
2. **"not_in_channel"**: Invite the bot to your Slack channel
3. **"Failed to fetch prayer times"**: Check internet connection and API status
4. **"Failed to generate messages"**: Verify Gemini API key and quota

### Logs

The bot provides detailed console output for:
- Daily setup progress
- Prayer time fetching
- Message generation
- Slack message sending
- Database operations

## 📝 Configuration Options

### Prayer Calculation Method
- `1`: University of Islamic Sciences, Karachi
- `2`: Islamic Society of North America
- `3`: Muslim World League
- `4`: Umm Al-Qura University, Makkah
- `5`: Egyptian General Authority of Survey

### Reminder Timing
Change `REMINDER_LEAD_TIME_MINUTES` in `config.py` to adjust when reminders are sent.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

---

**Note**: This bot is designed for personal or community use. Please respect prayer times and Islamic traditions when using this tool.