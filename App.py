import google.generativeai as genai
from Certs.api import GEMINI_API_KEY, TOKEN

from flask import Flask, jsonify
from flask_cors import CORS

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

import json
import random
import time
import datetime

from Ship import Ship
from CrewMember import CrewMember
from TextManager import TextManager

#Gemini Config
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    'gemini-1.5-flash'
    #generation_config={"response_mime_type": "application/json"}
)

#Influx Config
influx_url = "http://localhost:8086"
influx_org = "my_org"
influx_bucket = "game_metrics"

client = InfluxDBClient(url=influx_url, token=TOKEN, org=influx_org)
write_api = client.write_api(write_options=SYNCHRONOUS)

#Flask Config
app = Flask(__name__)
CORS(app)

ship = Ship()
points_to_add = []

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

def add_to_story(story):
    point = Point("story") \
        .field("next_story_point", story)

    points_to_add.append(point)

def add_to_log(log, urgency):
    point = Point("log") \
        .field("next_log", log) \
        .field("urgency", urgency)

    points_to_add.append(point)

def add_to_ship():
    point = Point("ship") \
        .field("fuel", ship.get_fuel()) \
        .field("hull_integrity", ship.get_hull_integrity()) \
        .field("oxygen", ship.get_oxygen()) \
        .field("spare_parts", ship.get_spare_parts()) \
        .field("food", ship.get_food()) \
        .field("water", ship.get_water()) \
        .field("medical", ship.get_medical()) \
        .field("ammo", ship.get_ammo())

    points_to_add.append(point)

def add_to_crew(crewmate):
    point = Point("crewmates") \
        .field("name", crewmate.get_name()) \
        .field("health", crewmate.get_health()) \
        .field("sanity", crewmate.get_sanity()) \
        .field("status", crewmate.get_status()) \
        .field("hunger", crewmate.get_hunger()) \
        .field("job", crewmate.get_job())

    points_to_add.append(point)

def update_database():
    write_api.write(bucket=influx_bucket, org=influx_bucket, record=points_to_add)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)