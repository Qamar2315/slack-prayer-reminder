import requests
from datetime import date
import config

def fetch_prayer_times(method=None, school=None):
    """
    Fetches today's prayer times from the AlAdhan API.
    
    Args:
        method: Optional calculation method (0-23, 99). Default uses config.METHOD
        school: Optional school parameter
                - None: Use default from config.SCHOOL
                - 0: Shafi (standard)
                - 1: Hanafi
    """
    today_str = date.today().strftime("%d-%m-%Y")
    url = f"http://api.aladhan.com/v1/timings/{today_str}"
    params = {
        "latitude": config.LATITUDE,
        "longitude": config.LONGITUDE,
        "method": method if method is not None else config.METHOD,
        "school": school if school is not None else config.SCHOOL
    }
    
    try:
        print(f"Attempting to fetch prayer times from AlAdhan API...")
        if method is not None:
            print(f"Using calculation method: {method}")
        else:
            print(f"Using calculation method: {config.METHOD}")
        
        school_name = "Hanafi" if params["school"] == 1 else "Shafi"
        print(f"Using {school_name} school")
        
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

def fetch_prayer_times_comparison():
    """
    Fetches prayer times using both Shafi and Hanafi methods for comparison.
    Returns a dictionary with both sets of timings.
    """
    print("Fetching prayer times for comparison (Shafi vs Hanafi)...")
    
    # Fetch with Shafi method (school=0)
    shafi_timings = fetch_prayer_times(school=0)
    
    # Fetch with Hanafi method (school=1)
    hanafi_timings = fetch_prayer_times(school=1)
    
    return {
        "shafi": shafi_timings,
        "hanafi": hanafi_timings
    }

def get_calculation_methods():
    """
    Returns a dictionary of available calculation methods.
    """
    return {
        0: "Jafari / Shia Ithna-Ashari",
        1: "University of Islamic Sciences, Karachi",
        2: "Islamic Society of North America", 
        3: "Muslim World League",
        4: "Umm Al-Qura University, Makkah",
        5: "Egyptian General Authority of Survey",
        7: "Institute of Geophysics, University of Tehran",
        8: "Gulf Region",
        9: "Kuwait",
        10: "Qatar",
        11: "Majlis Ugama Islam Singapura, Singapore",
        12: "Union Organization islamic de France",
        13: "Diyanet İşleri Başkanlığı, Turkey",
        14: "Spiritual Administration of Muslims of Russia",
        15: "Moonsighting Committee Worldwide",
        16: "Dubai (experimental)",
        17: "Jabatan Kemajuan Islam Malaysia (JAKIM)",
        18: "Tunisia",
        19: "Algeria",
        20: "KEMENAG - Kementerian Agama Republik Indonesia",
        21: "Morocco",
        22: "Comunidade Islamica de Lisboa",
        23: "Ministry of Awqaf, Islamic Affairs and Holy Places, Jordan",
        99: "Custom"
    } 