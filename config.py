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
PRAYERS_IN_ORDER = ["Asr", "Maghrib", "Isha"]
REMINDER_LEAD_TIME_MINUTES = 3 # Send reminder 10 minutes before prayer
DATABASE_FILE = "prayer_times.db"
QURAN_ARABIC_FILE = "data/quran.json"
QURAN_URDU_FILE = "data/ur.json"

# --- Default Messages (used when AI generation fails) ---
DEFAULT_MESSAGES = {
    "Fajr": "As the first light of dawn breaks, let us begin our day with the remembrance of Allah. Fajr prayer connects us to the divine and sets the tone for a blessed day ahead.",
    "Dhuhr": "The sun reaches its zenith, and it's time for Dhuhr prayer. Let us pause from our worldly pursuits and turn our hearts towards Allah, seeking His guidance and mercy.",
    "Asr": "As the afternoon sun begins to set, let us perform Asr prayer. This is a time of reflection and gratitude for the blessings Allah has bestowed upon us throughout the day.",
    "Maghrib": "The sun has set, marking the time for Maghrib prayer. Let us give thanks for another day of life and seek Allah's forgiveness for our shortcomings.",
    "Isha": "As night falls and the day comes to an end, let us perform Isha prayer. This final prayer of the day helps us reflect on our actions and seek Allah's protection for the night ahead."
} 