import sqlite3
import json
import random
from datetime import datetime, timedelta
import config
import pytz  # Import the timezone library

class DatabaseService:
    def __init__(self, db_file, quran_ar_file, quran_ur_file):
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file, check_same_thread=False)
        # Create a timezone object from the configuration
        self.local_tz = pytz.timezone(config.TIMEZONE)
        self._load_quran(quran_ar_file, quran_ur_file)

    def _load_quran(self, ar_file, ur_file):
        """Loads Quran JSON files into memory."""
        print("Loading Quran data...")
        with open(ar_file, 'r', encoding='utf-8') as f:
            self.quran_arabic = json.load(f)
        with open(ur_file, 'r', encoding='utf-8') as f:
            self.quran_urdu = json.load(f)
        print("Quran data loaded successfully.")

    def init_db(self):
        """Initializes the database table."""
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_prayers (
                prayer_name TEXT PRIMARY KEY,
                prayer_time TEXT NOT NULL,
                reminder_message TEXT NOT NULL,
                reminder_sent INTEGER NOT NULL DEFAULT 0
            )
        ''')
        self.conn.commit()
        print("Database initialized.")

    def clear_and_save_prayers(self, timings, messages):
        """Clears old data and saves new daily prayer times and messages."""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM daily_prayers")
        print("Cleared previous day's prayer data.")
        
        for prayer in config.PRAYERS_IN_ORDER:
            message = messages.get(prayer, config.DEFAULT_MESSAGES.get(prayer, f"Time for {prayer} prayer."))
            cursor.execute('''
                INSERT INTO daily_prayers (prayer_name, prayer_time, reminder_message, reminder_sent)
                VALUES (?, ?, ?, 0)
            ''', (prayer, timings[prayer], message))
        
        self.conn.commit()
        print("Saved new prayer times and messages for the day.")

    def get_prayers_to_remind(self):
        """Fetches prayers that are due for a reminder and haven't been sent."""
        cursor = self.conn.cursor()
        
        # --- FIX 1: USE LOCAL TIMEZONE FOR COMPARISON ---
        # Get the current time in the bot's configured local timezone
        now = datetime.now(self.local_tz)
        
        reminder_start_time = (now + timedelta(minutes=config.REMINDER_LEAD_TIME_MINUTES)).strftime("%H:%M")
        
        cursor.execute('''
            SELECT prayer_name, prayer_time, reminder_message FROM daily_prayers
            WHERE prayer_time <= ? AND reminder_sent = 0
        ''', (reminder_start_time,))
        
        prayers = cursor.fetchall()
        return [{"name": p[0], "time": p[1], "message": p[2]} for p in prayers]

    def mark_as_sent(self, prayer_name):
        """Marks a prayer reminder as sent."""
        cursor = self.conn.cursor()
        cursor.execute("UPDATE daily_prayers SET reminder_sent = 1 WHERE prayer_name = ?", (prayer_name,))
        self.conn.commit()
        print(f"Marked {prayer_name} reminder as sent.")

    def get_next_prayer(self, current_prayer_name):
        """Finds the next prayer in the sequence, correctly handling the end of the day."""
        # --- FIX 2: HANDLE THE LAST PRAYER IN THE CONFIGURED LIST ---
        # If the current prayer is the last one in our list, the next is always Fajr.
        if current_prayer_name == config.PRAYERS_IN_ORDER[-1]:
            return {"name": "Fajr", "time": "tomorrow"}
        
        try:
            current_index = config.PRAYERS_IN_ORDER.index(current_prayer_name)
            # This is safe now because we already handled the last prayer case.
            next_prayer_name = config.PRAYERS_IN_ORDER[current_index + 1]

            cursor = self.conn.cursor()
            cursor.execute("SELECT prayer_time FROM daily_prayers WHERE prayer_name = ?", (next_prayer_name,))
            result = cursor.fetchone()
            if result:
                return {"name": next_prayer_name, "time": result[0]}
        except (ValueError, IndexError):
            # This will now only catch genuine errors, like a misconfigured list.
            return None
        return None

    def get_random_verse(self):
        """Selects a random verse from the loaded Quran data."""
        chapter_key = random.choice(list(self.quran_arabic.keys()))
        verse_index = random.randint(0, len(self.quran_arabic[chapter_key]) - 1)
        
        arabic_verse = self.quran_arabic[chapter_key][verse_index]
        urdu_verse = self.quran_urdu[chapter_key][verse_index]

        return {
            "chapter": arabic_verse['chapter'],
            "verse": arabic_verse['verse'],
            "arabic_text": arabic_verse['text'],
            "urdu_text": urdu_verse['text']
        }

    def has_today_data(self):
        """Check if we have prayer data for today."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM daily_prayers")
        count = cursor.fetchone()[0]
        return count > 0

    def initialize_with_defaults(self, timings):
        """Initialize the database with prayer times and default messages."""
        print("Initializing database with prayer times and default messages...")
        self.clear_and_save_prayers(timings, config.DEFAULT_MESSAGES) 