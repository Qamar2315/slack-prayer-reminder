import schedule
import time
from datetime import datetime

import config
from services import aladhan_service, gemini_service, slack_service, db_service

# Initialize the database service
db = db_service.DatabaseService(
    config.DATABASE_FILE, 
    config.QURAN_ARABIC_FILE, 
    config.QURAN_URDU_FILE
)

def daily_setup_job():
    """
    Runs once daily to fetch prayer times and generate messages.
    """
    print("\n" + "="*50)
    print(f"[{datetime.now()}] Running daily setup job...")
    
    # 1. Fetch prayer times
    timings = aladhan_service.fetch_prayer_times()
    if not timings:
        print("Halting daily setup: Could not fetch prayer times.")
        return

    # 2. Generate motivational messages (with fallback to defaults)
    messages = gemini_service.generate_motivational_messages()
    if not messages:
        print("Error: No messages available. This should not happen with fallback defaults.")
        return

    # 3. Save everything to the database
    db.clear_and_save_prayers(timings, messages)
    print("Daily setup job completed successfully.")
    print("="*50 + "\n")

def initialize_if_needed():
    """
    Initialize the database with prayer times and default messages if no data exists.
    """
    if not db.has_today_data():
        print("No prayer data found for today. Initializing with defaults...")
        timings = aladhan_service.fetch_prayer_times()
        if timings:
            db.initialize_with_defaults(timings)
            print("Database initialized with prayer times and default messages.")
        else:
            print("Could not fetch prayer times for initialization.")


def check_and_send_reminders_job():
    """
    Runs every minute to check if a reminder needs to be sent.
    """
    # print(f"[{datetime.now().strftime('%H:%M:%S')}] Checking for due reminders...")
    
    due_prayers = db.get_prayers_to_remind()

    if not due_prayers:
        return # Nothing to do

    for prayer in due_prayers:
        print(f"--> Found due reminder for: {prayer['name']}")
        
        # 1. Get a random Quran verse
        verse = db.get_random_verse()
        
        # 2. Get the next prayer's info
        next_prayer = db.get_next_prayer(prayer['name'])

        # 3. Send the Slack message
        success = slack_service.send_reminder_message(
            prayer_name=prayer['name'],
            prayer_time=prayer['time'],
            message=prayer['message'],
            verse=verse,
            next_prayer=next_prayer
        )

        # 4. If sent successfully, update the database
        if success:
            db.mark_as_sent(prayer['name'])


def main():
    """Main function to start the bot."""
    print("--- Slack Prayer Reminder Bot ---")
    print("Initializing...")
    
    # Initialize the database schema if it doesn't exist
    db.init_db()

    # Initialize with defaults if no data exists
    initialize_if_needed()

    # Run the setup job once on startup to get today's data immediately
    daily_setup_job()

    # Schedule the jobs
    schedule.every().day.at("01:00").do(daily_setup_job)
    schedule.every().minute.do(check_and_send_reminders_job)

    print("Bot is now running. Waiting for scheduled jobs...")
    print(f"Reminders will be sent {config.REMINDER_LEAD_TIME_MINUTES} minutes before prayer time.")

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    # Ensure you have valid keys in your .env file before running
    if not config.SLACK_BOT_TOKEN or not config.GEMINI_API_KEY:
        raise ValueError("API keys for Slack and Gemini are missing. Please add them to your .env file.")
    main() 