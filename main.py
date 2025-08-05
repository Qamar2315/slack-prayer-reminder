import schedule
import time
from datetime import datetime
import logging  # Import logging

import config
from services import aladhan_service, gemini_service, slack_service, db_service

# --- Setup Logging ---
# This configuration forces logs to be unbuffered and appear immediately in systemd's journalctl
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)


# Initialize the database service
db = db_service.DatabaseService(
    config.DATABASE_FILE, 
    config.QURAN_ARABIC_FILE, 
    config.QURAN_URDU_FILE
)

def daily_setup_job():
    """Runs once daily to fetch prayer times and generate messages."""
    log.info("="*50)
    log.info(f"Running daily setup job...")
    
    timings = aladhan_service.fetch_prayer_times()
    if not timings:
        log.error("Halting daily setup: Could not fetch prayer times.")
        return

    messages = gemini_service.generate_motivational_messages()
    if not messages:
        log.error("Halting daily setup: No messages available, even with fallbacks.")
        return

    db.clear_and_save_prayers(timings, messages)
    log.info("Daily setup job completed successfully.")
    log.info("="*50)

def initialize_if_needed():
    """Initialize the database with prayer times if no data exists."""
    if not db.has_today_data():
        log.info("No prayer data found for today. Initializing with defaults...")
        timings = aladhan_service.fetch_prayer_times()
        if timings:
            db.initialize_with_defaults(timings)
            log.info("Database initialized with prayer times and default messages.")
        else:
            log.error("Could not fetch prayer times for initialization.")

def check_and_send_reminders_job():
    """Runs every minute to check if a reminder needs to be sent."""
    due_prayers = db.get_prayers_to_remind()

    if not due_prayers:
        return # Nothing to do, no log needed for this

    for prayer in due_prayers:
        log.info(f"--> Found due reminder for: {prayer['name']}")
        
        verse = db.get_random_verse()
        next_prayer = db.get_next_prayer(prayer['name'])

        success = slack_service.send_reminder_message(
            prayer_name=prayer['name'],
            prayer_time=prayer['time'],
            message=prayer['message'],
            verse=verse,
            next_prayer=next_prayer
        )

        if success:
            db.mark_as_sent(prayer['name'])

def main():
    """Main function to start the bot."""
    log.info("--- Slack Prayer Reminder Bot ---")
    log.info("Initializing...")
    
    db.init_db()
    initialize_if_needed()
    daily_setup_job()

    schedule.every().day.at("01:00").do(daily_setup_job)
    schedule.every().minute.do(check_and_send_reminders_job)

    log.info("Bot is now running. Waiting for scheduled jobs...")
    log.info(f"Operational timezone set to: {config.TIMEZONE}")
    log.info(f"Reminders will be sent {config.REMINDER_LEAD_TIME_MINUTES} minutes before prayer time.")

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    if not config.SLACK_BOT_TOKEN or not config.GEMINI_API_KEY:
        raise ValueError("API keys for Slack and Gemini are missing. Please add them to your .env file.")
    main() 