import requests
from datetime import date
import config

def fetch_prayer_times():
    """Fetches today's prayer times from the AlAdhan API."""
    today_str = date.today().strftime("%d-%m-%Y")
    url = f"http://api.aladhan.com/v1/timings/{today_str}"
    params = {
        "latitude": config.LATITUDE,
        "longitude": config.LONGITUDE,
        "method": config.METHOD
    }
    
    try:
        print("Attempting to fetch prayer times from AlAdhan API...")
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        if data.get('code') == 200:
            print("Successfully fetched prayer times.")
            return data['data']['timings']
        else:
            print(f"API Error: {data.get('status', 'Unknown error')}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Connection Error fetching prayer times: {e}")
        return None 