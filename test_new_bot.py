#!/usr/bin/env python3
"""
Test script to display prayer times based on University of Islamic Sciences, Karachi method.
This script fetches and displays prayer times in a clear, readable format.
Now includes comparison between Shafi and Hanafi Asr timings.
"""

import sys
import os
from datetime import datetime
import pytz

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def convert_to_12_hour_format(time_str):
    """Convert 24-hour time format (HH:MM) to 12-hour format with AM/PM."""
    try:
        time_obj = datetime.strptime(time_str, "%H:%M")
        return time_obj.strftime("%I:%M %p")
    except ValueError:
        return time_str

def display_calculation_methods():
    """Display available calculation methods."""
    print("📋 AVAILABLE CALCULATION METHODS:")
    print("=" * 70)
    
    try:
        from services.aladhan_service import get_calculation_methods
        methods = get_calculation_methods()
        
        print("ID | Method Name")
        print("-" * 50)
        for method_id, method_name in methods.items():
            current_marker = " ← CURRENT" if method_id == 1 else ""
            print(f"{method_id:2} | {method_name}{current_marker}")
        
        print("-" * 50)
        print("💡 To change method, update METHOD in config.py")
        print()
        
    except Exception as e:
        print(f"❌ Error displaying methods: {e}")

def display_prayer_times():
    """Fetch and display prayer times with detailed information."""
    print("🕌 Prayer Times - University of Islamic Sciences, Karachi Method")
    print("=" * 70)
    
    try:
        import config
        from services.aladhan_service import fetch_prayer_times, get_calculation_methods
        
        # Get current method name
        methods = get_calculation_methods()
        current_method_name = methods.get(config.METHOD, f"Method {config.METHOD}")
        
        # Get current school name
        school_name = "Hanafi" if config.SCHOOL == 1 else "Shafi"
        
        # Display configuration info
        print(f"📍 Location: {config.LATITUDE}, {config.LONGITUDE}")
        print(f"🕐 Timezone: {config.TIMEZONE}")
        print(f"📅 Date: {datetime.now(pytz.timezone(config.TIMEZONE)).strftime('%A, %B %d, %Y')}")
        print(f"🕐 Current Time: {datetime.now(pytz.timezone(config.TIMEZONE)).strftime('%I:%M:%S %p')}")
        print(f"⚙️  Calculation Method: {current_method_name} (Method {config.METHOD})")
        print(f"🕌 School: {school_name} (School {config.SCHOOL})")
        print()
        
        # Fetch prayer times
        print("📡 Fetching prayer times from AlAdhan API...")
        timings = fetch_prayer_times()
        
        if not timings:
            print("❌ Failed to fetch prayer times")
            return False
        
        print("✅ Prayer times fetched successfully!")
        print()
        
        # Display all prayer times
        print("🕐 PRAYER TIMES:")
        print("-" * 50)
        
        # Define prayer order for display
        prayer_order = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]
        
        for prayer in prayer_order:
            if prayer in timings:
                time_24hr = timings[prayer]
                time_12hr = convert_to_12_hour_format(time_24hr)
                
                # Add emoji based on prayer
                emoji_map = {
                    "Fajr": "🌅",
                    "Dhuhr": "☀️",
                    "Asr": "🌤️",
                    "Maghrib": "🌆",
                    "Isha": "🌙"
                }
                
                emoji = emoji_map.get(prayer, "🕌")
                print(f"{emoji} {prayer:8} | {time_24hr:5} | {time_12hr:8}")
        
        print("-" * 50)
        print()
        
        # Show configured prayers for reminders
        print("🔔 CONFIGURED FOR REMINDERS:")
        print("-" * 50)
        for i, prayer in enumerate(config.PRAYERS_IN_ORDER, 1):
            if prayer in timings:
                time_12hr = convert_to_12_hour_format(timings[prayer])
                print(f"{i}. {prayer} at {time_12hr}")
        
        print("-" * 50)
        print()
        
        # Show reminder timing
        print("⏰ REMINDER SETTINGS:")
        print("-" * 50)
        print(f"• Reminders sent {config.REMINDER_LEAD_TIME_MINUTES} minutes before prayer time")
        print(f"• Daily setup runs at 01:00 {config.TIMEZONE}")
        print(f"• Check frequency: Every minute")
        print("-" * 50)
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def display_asr_comparison():
    """Display comparison between Shafi and Hanafi Asr timings."""
    print("\n🕌 ASR PRAYER TIME COMPARISON (Shafi vs Hanafi)")
    print("=" * 70)
    
    try:
        import config
        from services.aladhan_service import fetch_prayer_times_comparison
        
        print("📡 Fetching prayer times for both methods...")
        comparison = fetch_prayer_times_comparison()
        
        if not comparison or not comparison["shafi"] or not comparison["hanafi"]:
            print("❌ Failed to fetch comparison data")
            return False
        
        shafi_timings = comparison["shafi"]
        hanafi_timings = comparison["hanafi"]
        
        print("✅ Comparison data fetched successfully!")
        print()
        
        # Display comparison table
        print("📊 ASR TIMING COMPARISON:")
        print("-" * 60)
        print(f"{'Method':<15} | {'24-Hour':<10} | {'12-Hour':<10} | {'Difference'}")
        print("-" * 60)
        
        # Get Asr times
        shafi_asr = shafi_timings.get("Asr", "N/A")
        hanafi_asr = hanafi_timings.get("Asr", "N/A")
        
        if shafi_asr != "N/A" and hanafi_asr != "N/A":
            shafi_12hr = convert_to_12_hour_format(shafi_asr)
            hanafi_12hr = convert_to_12_hour_format(hanafi_asr)
            
            # Calculate difference
            try:
                shafi_time = datetime.strptime(shafi_asr, "%H:%M")
                hanafi_time = datetime.strptime(hanafi_asr, "%H:%M")
                
                if hanafi_time > shafi_time:
                    diff_minutes = int((hanafi_time - shafi_time).total_seconds() / 60)
                    diff_text = f"+{diff_minutes} minutes"
                else:
                    diff_minutes = int((shafi_time - hanafi_time).total_seconds() / 60)
                    diff_text = f"-{diff_minutes} minutes"
            except:
                diff_text = "N/A"
            
            print(f"{'Shafi (Default)':<15} | {shafi_asr:<10} | {shafi_12hr:<10} | -")
            print(f"{'Hanafi':<15} | {hanafi_asr:<10} | {hanafi_12hr:<10} | {diff_text}")
        else:
            print("❌ Could not retrieve Asr times for comparison")
        
        print("-" * 60)
        print()
        
        # Show explanation
        print("📖 EXPLANATION:")
        print("-" * 50)
        print("• Shafi Method: Asr begins when shadow = 1x object height")
        print("• Hanafi Method: Asr begins when shadow = 2x object height")
        print("• Hanafi Asr typically starts later than Shafi Asr")
        print("• The difference is usually 15-30 minutes depending on location")
        print("-" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Comparison error: {e}")
        return False

def round_to_quarter_hour(time_str):
    """Round time to nearest quarter hour (00, 15, 30, 45 minutes)."""
    try:
        # Parse the time string (e.g., "09:05")
        time_obj = datetime.strptime(time_str, "%H:%M")
        
        # Get total minutes since midnight
        total_minutes = time_obj.hour * 60 + time_obj.minute
        
        # Round to nearest quarter hour (15 minutes)
        rounded_minutes = round(total_minutes / 15) * 15
        
        # Convert back to hours and minutes
        hours = rounded_minutes // 60
        minutes = rounded_minutes % 60
        
        # Format back to HH:MM
        return f"{hours:02d}:{minutes:02d}"
    except ValueError:
        return time_str

def test_quarter_hour_rounding():
    """Test quarter-hour rounding for Asr and Isha prayer times."""
    print("\n⏰ QUARTER-HOUR ROUNDING TEST (Asr & Isha)")
    print("=" * 70)
    
    try:
        import config
        from services.aladhan_service import fetch_prayer_times
        
        print("📡 Fetching prayer times from AlAdhan API...")
        timings = fetch_prayer_times()
        
        if not timings:
            print("❌ Failed to fetch prayer times")
            return False
        
        print("✅ Prayer times fetched successfully!")
        print()
        
        # Test quarter-hour rounding
        print("🔄 QUARTER-HOUR ROUNDING:")
        print("-" * 60)
        print(f"{'Prayer':<8} | {'Original':<10} | {'Rounded':<10} | {'12-Hour'}")
        print("-" * 60)
        
        # Test with actual prayer times
        for prayer in ["Asr", "Isha"]:
            if prayer in timings:
                original_time = timings[prayer]
                rounded_time = round_to_quarter_hour(original_time)
                rounded_12hr = convert_to_12_hour_format(rounded_time)
                
                print(f"{prayer:8} | {original_time:<10} | {rounded_time:<10} | {rounded_12hr}")
        
        print("-" * 60)
        print()
        
        # Test with sample times to show the rounding logic
        print("🧪 SAMPLE ROUNDING EXAMPLES:")
        print("-" * 60)
        print(f"{'Original':<10} | {'Rounded':<10} | {'12-Hour':<10} | {'Logic'}")
        print("-" * 60)
        
        sample_times = [
            "09:05",   # Should round to 09:00
            "09:07",   # Should round to 09:00
            "09:08",   # Should round to 09:15
            "09:22",   # Should round to 09:15
            "09:23",   # Should round to 09:30
            "09:37",   # Should round to 09:30
            "09:38",   # Should round to 09:45
            "09:52",   # Should round to 09:45
            "09:53",   # Should round to 10:00
            "15:44",   # Should round to 15:45
            "15:46",   # Should round to 15:45
            "15:47",   # Should round to 15:45
            "15:48",   # Should round to 15:45
            "15:49",   # Should round to 15:45
            "15:50",   # Should round to 15:45
            "15:51",   # Should round to 15:45
            "15:52",   # Should round to 15:45
            "15:53",   # Should round to 16:00
        ]
        
        for time_str in sample_times:
            rounded = round_to_quarter_hour(time_str)
            rounded_12hr = convert_to_12_hour_format(rounded)
            
            # Explain the logic
            time_obj = datetime.strptime(time_str, "%H:%M")
            total_minutes = time_obj.hour * 60 + time_obj.minute
            quarter = round(total_minutes / 15)
            logic = f"({total_minutes}min → {quarter} quarters)"
            
            print(f"{time_str:<10} | {rounded:<10} | {rounded_12hr:<10} | {logic}")
        
        print("-" * 60)
        print()
        
        # Show what would be saved to database
        print("💾 DATABASE SAVE PREVIEW:")
        print("-" * 50)
        for prayer in ["Asr", "Isha"]:
            if prayer in timings:
                original_time = timings[prayer]
                rounded_time = round_to_quarter_hour(original_time)
                rounded_12hr = convert_to_12_hour_format(rounded_time)
                
                print(f"• {prayer}: {original_time} → {rounded_time} ({rounded_12hr})")
        
        print("-" * 50)
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Quarter-hour test failed: {e}")
        return False

def test_timezone_conversion():
    """Test timezone conversion functionality."""
    print("\n🕐 TESTING TIMEZONE CONVERSION:")
    print("-" * 50)
    
    try:
        import config
        
        # Test current time in different formats
        local_tz = pytz.timezone(config.TIMEZONE)
        now = datetime.now(local_tz)
        
        print(f"Current time in {config.TIMEZONE}:")
        print(f"• 24-hour: {now.strftime('%H:%M:%S')}")
        print(f"• 12-hour: {now.strftime('%I:%M:%S %p')}")
        print(f"• Full: {now.strftime('%A, %B %d, %Y at %I:%M:%S %p')}")
        
        # Test some sample prayer times
        sample_times = ["05:30", "12:15", "15:45", "18:30", "20:15"]
        print(f"\nSample time conversions:")
        for time_24hr in sample_times:
            time_12hr = convert_to_12_hour_format(time_24hr)
            print(f"• {time_24hr} → {time_12hr}")
        
        print("-" * 50)
        return True
        
    except Exception as e:
        print(f"❌ Timezone test failed: {e}")
        return False

def main():
    """Main function to run the prayer time display."""
    print("🧪 Prayer Time Display Test (with Hanafi Asr comparison)")
    print("=" * 70)
    
    # Test 0: Display available calculation methods
    display_calculation_methods()
    
    # Test 1: Display prayer times
    success1 = display_prayer_times()
    
    # Test 2: Asr comparison
    success2 = display_asr_comparison()
    
    # Test 3: Quarter-hour rounding test
    success3 = test_quarter_hour_rounding()
    
    # Test 4: Timezone conversion
    success4 = test_timezone_conversion()
    
    print("\n" + "=" * 70)
    if success1 and success2 and success3 and success4:
        print("✅ All tests completed successfully!")
        print("\n📋 Summary:")
        print("• Prayer times are fetched from AlAdhan API")
        print("• Times are displayed in both 24-hour and 12-hour formats")
        print("• Hanafi vs Shafi Asr comparison is available")
        print("• Quarter-hour rounding for Asr & Isha is tested")
        print("• Timezone handling is working correctly")
        print("• University of Islamic Sciences, Karachi method is being used")
        print("\n💡 Configuration Options:")
        print("   • METHOD in config.py: Calculation method (0-23, 99)")
        print("   • SCHOOL in config.py: 0 = Shafi, 1 = Hanafi")
        print("\n💡 To use Hanafi method in your bot:")
        print("   Update config.py: SCHOOL = 1 (for Hanafi)")
        print("   Update config.py: SCHOOL = 0 (for Shafi, current)")
        print("   Or use school=1 in fetch_prayer_times() for Hanafi")
        print("   Or use school=0 in fetch_prayer_times() for Shafi")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\n🔧 Troubleshooting:")
        print("1. Check your internet connection")
        print("2. Verify the latitude/longitude in config.py")
        print("3. Make sure all dependencies are installed")
        print("4. Check if the AlAdhan API is accessible")

if __name__ == "__main__":
    main() 