import google.generativeai as genai
from Certs.api import GEMINI_API_KEY

from flask import Flask, jsonify
from flask_cors import CORS

import datetime
import json

from Ship import Ship
from CrewMember import CrewMember
from TextManager import TextManager

DB_FILE = "state.json"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    'gemini-1.5-flash'
    #generation_config={"response_mime_type": "application/json"}
)

"""
CrewMates Table
Ship
Logs
Story
"""

app = Flask(__name__)
CORS(app)

ship = Ship()
text_manager = TextManager()


def ask_gemini(action):
    prompt = f"""
    You are the AI Computer dictating the story of a sci-fi spaceship game. 
    
    Current game Status: 
    - Fuel: {ship.get_fuel()}%
    - Hull Integrity: {ship.get_hull_integrity()}%
    - Oxygen: {ship.get_oxygen()}%
    - Supplies: {ship.get_supplies()}

    The Player just chose to: "{action}"

    Determine the outcome based on sci-fi tropes.
    - If Fuel is low, actions might fail.
    - If Hull is low, the ship is sparking.

    Return a JSON object with these exact keys:
    {{
        "log_entry": "A short, dramatic 1-sentence description of what happened.",
        "fuel_change": (integer, e.g. -10),
        "hull_change": (integer, e.g. 0 or -20 if damaged),
        "distance_change": (integer, positive to move forward)
    }}
    """

    try:
        response = model.generate_content(prompt)
        return json.loads(response.text)

    except Exception as e:
        print(f"Gemini Error: {e}")
        return {
            "log_entry": "AI Connection Offline. Manual Override.",
            "fuel_change": -5,
            "hull_change": 0,
            "distance_change": 0
        }



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)