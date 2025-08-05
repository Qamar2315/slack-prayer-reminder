import google.generativeai as genai
import json
import time
import config

genai.configure(api_key=config.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash-lite')

def generate_motivational_messages():
    """Generates a motivational message for each prayer using Gemini AI."""
    prayer_list = ", ".join(config.PRAYERS_IN_ORDER)
    prompt = f"""
    You are an inspiring Islamic scholar. Your task is to generate a short, beautiful, and motivational reminder message for each of the five daily prayers: {prayer_list}.
    The message should be unique for each prayer and encourage performing it on time.
    Your response MUST be a valid JSON object where keys are the prayer names (e.g., "Fajr", "Dhuhr") and values are the generated motivational strings.
    Do not include any other text or explanations outside of the JSON object.

    Example format:
    {{
        "Fajr": "Message for Fajr...",
        "Dhuhr": "Message for Dhuhr...",
        "Asr": "Message for Asr...",
        "Maghrib": "Message for Maghrib...",
        "Isha": "Message for Isha..."
    }}
    """

    for attempt in range(3): # Retry up to 3 times
        try:
            print("Attempting to generate motivational messages with Gemini AI...")
            response = model.generate_content(prompt)
            # Clean the response to ensure it's valid JSON
            cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
            messages = json.loads(cleaned_response)
            
            # Validate that we got all prayers
            if all(prayer in messages for prayer in config.PRAYERS_IN_ORDER):
                print("Successfully generated and parsed motivational messages.")
                return messages
            else:
                print("Generated JSON is missing some prayers. Retrying...")

        except (json.JSONDecodeError, Exception) as e:
            print(f"Error generating/parsing messages (Attempt {attempt + 1}/3): {e}")
            time.sleep(5) # Wait before retrying
            
    print("Failed to generate motivational messages after 3 attempts.")
    print("Using default messages as fallback.")
    return config.DEFAULT_MESSAGES 