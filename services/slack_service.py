import requests
import logging
import config
from datetime import datetime

def convert_to_12_hour_format(time_str):
    """Convert 24-hour time format (HH:MM) to 12-hour format with AM/PM."""
    try:
        # Parse the time string (e.g., "15:57")
        time_obj = datetime.strptime(time_str, "%H:%M")
        # Format as 12-hour with AM/PM
        return time_obj.strftime("%I:%M %p")
    except ValueError:
        # If parsing fails, return the original string
        return time_str

def send_reminder_message(prayer_name, prayer_time, message, verse, next_prayer):
    """Formats and sends a prayer reminder to Slack."""
    log = logging.getLogger(__name__)
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {config.SLACK_BOT_TOKEN}",
        "Content-Type": "application/json; charset=utf-8"
    }

    # Convert times to 12-hour format
    prayer_time_12hr = convert_to_12_hour_format(prayer_time)
    
    if next_prayer and next_prayer['time'] != 'tomorrow':
        next_prayer_time_12hr = convert_to_12_hour_format(next_prayer['time'])
        next_prayer_text = f"Next prayer is *{next_prayer['name']}* at *{next_prayer_time_12hr}*."
    else:
        next_prayer_text = "Next prayer is *Fajr* tomorrow, Insha'Allah."

    payload = {
        "channel": config.SLACK_CHANNEL_ID,
        "text": f"Reminder: It's almost time for {prayer_name} prayer!", # Fallback
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f":mosque: Reminder: {prayer_name} at {prayer_time_12hr}",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"_{message}_"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"A reminder from the Qur'an:\n\n>*{verse['arabic_text']}*\n>_{verse['urdu_text']}_\n\n`Quran {verse['chapter']}:{verse['verse']}`"
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f":clock1: {next_prayer_text}"
                    }
                ]
            }
        ]
    }

    try:
        log.info(f"Attempting to send {prayer_name} reminder to Slack...")
        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()
        if response_data.get("ok"):
            log.info(f"✅ Success! {prayer_name} reminder sent.")
            return True
        else:
            log.error(f"❌ Error sending message to Slack: {response_data.get('error')}")
            return False
    except requests.exceptions.RequestException as e:
        log.error(f"Connection Error sending to Slack: {e}")
        return False 