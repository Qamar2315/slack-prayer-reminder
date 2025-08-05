import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Slack Configuration ---
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = "C099J0CK77S" # Your channel ID

# --- Gemini AI Configuration ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- AlAdhan API Configuration ---
LATITUDE = 33.5210681
LONGITUDE = 73.1578097
METHOD = 1 # University of Islamic Sciences, Karachi

# --- Bot Configuration ---
# The order is important for determining the "next" prayer
PRAYERS_IN_ORDER = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]
REMINDER_LEAD_TIME_MINUTES = 10 # Send reminder 10 minutes before prayer
DATABASE_FILE = "prayer_times.db"
QURAN_ARABIC_FILE = "data/quran.json"
QURAN_URDU_FILE = "data/ur.json" 