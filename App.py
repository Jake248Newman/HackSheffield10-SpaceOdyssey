import google.generativeai as genai
from google.generativeai.types import GenerationConfig

from Certs.api import GEMINI_API_KEY, TOKEN

from flask import Flask, jsonify
from flask_cors import CORS

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

import json
import threading
import random
import time
import datetime
from datetime import datetime, timezone

from Ship import Ship
from CrewMember import CrewMember

#Gemini Config
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    'gemini-2.5-flash',
    generation_config=GenerationConfig(
        response_mime_type="application/json"
    )
)
safety_settings = {
        "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
        "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
        "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
        "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
    }

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
crew = []

BEGIN_GAME = """
    You are the AI tasked with creating the story for a space odyssey game, and maintaining the story as we go.
    
    To begin, you need to greet the player and create a short backstory for this game, it should be fun but with a 
    sense of danger, their mission is to complete the game by making it to the destination, they are
    the captain of a space ship travelling between planets on an intergalactic trip in the year 3025. 
    
    Some rules:
    -They are travelling between two planets, and the journey takes 12 years.
    -They are the captain of a ship
    -The ship has a crew of 10-20 people
    -The people should have roles from the following
        -One executive officer
        -One head of security
        -Some engineers
        -One or two pilots
        -One or two gunners (people who man the weapons when under attack)
        -One or two medics
        -One or two cooks
    -The story can contain having to fight off aliens, drifting near to a black hole after a previous incident
    and having to avoid that, being attacked by an asteroid, have mechanical leaks or failures and having 
    crew members falling ill or injured.
    
    Please make the response 150 words max. You should not tell them about their crew in detail.
        
    Return a JSON object with this exact key:
     {{
         "message": "your message to the player to begin the game and give them some backstory"
         "crew": "A list of lists of the crew members to be initialised, 
                 it needs to be one list per crew member, each containing a name and a job for that person"
     }}
    """

def init_crew(crew_members):
    for person in crew_members:
        new_member = CrewMember(person[0], person[1])
        crew.append(new_member)

    add_to_crew(crew)

def main_loop():
    if random.randint(0, 50) == 1:
        ship.decrease_fuel()
        decrease_fuel_log()
    ship.increase_date()

    #for crewmate in crew:
    #    crewmate

    response = ask_gemini_prompt("""The user has passed to the next day, generate a brief summary of some "
                                 "events that could have happened, nothing serious or eventful, can be funny or waffle"
                                 "Return a JSON object with this exact key:"
                                 {{
                                     "message": "your message to the player to begin the game and give them some backstory"
                                 }}"""
                                 )

    print(response["message"])
    add_to_story(response["message"])
    add_to_ship()

def decrease_fuel_log():
    if ship.get_fuel() > 30:
        add_to_log("Fuel level decreased", "Normal")
    elif ship.get_fuel() > 10:
        add_to_log("Fuel level low", "Warning")
    else:
        add_to_log("Fuel very low", "CRITICAL")

def ask_gemini_action(action):
     prompt = f"""
     You are the AI Computer dictating the story of a sci-fi spaceship game.

     Current game Status:
     - Fuel: {ship.get_fuel()}%
     - Hull Integrity: {ship.get_hull_integrity()}%
     - Oxygen: {ship.get_oxygen()}%

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

def ask_gemini_prompt(prompt):
    try:
        response = model.generate_content(prompt, safety_settings=safety_settings)
        return json.loads(response.text)

    except Exception as e:
        print(f"Gemini Error: {e}")

def add_to_story(story):
    point = Point("story") \
        .field("next_story_point", story)

    write_api.write(bucket=influx_bucket, org=influx_org, record=point)

def add_to_log(log, urgency):
    point = Point("log") \
        .field("urgency", urgency) \
        .field("log_message", str(log)) \
        .field("point", "Day " + str(ship.get_days()))

    write_api.write(bucket=influx_bucket, org=influx_org, record=point)

def add_to_ship():
    point = Point("ship") \
        .field("fuel", ship.get_fuel()) \
        .field("hull_integrity", ship.get_hull_integrity()) \
        .field("oxygen", ship.get_oxygen()) \
        .field("spare_parts", ship.get_spare_parts()) \
        .field("food", ship.get_food()) \
        .field("water", ship.get_water()) \
        .field("medical", ship.get_medical()) \
        .field("ammo", ship.get_ammo()) \
        .field("current_date", ship.get_date())

    write_api.write(bucket=influx_bucket, org=influx_org, record=point)

def add_to_crew(crewmates):
    clear_database(["crewmates"])

    for crew in crewmates:
        point = Point("crewmates") \
            .field("name", crew.get_name()) \
            .field("health", crew.get_health()) \
            .field("sanity", crew.get_sanity()) \
            .field("status", crew.get_status()) \
            .field("hunger", crew.get_hunger()) \
            .field("job", crew.get_job())

        write_api.write(bucket=influx_bucket, org=influx_org, record=point)

def clear_database(tables=None):
    if tables is None:
        tables = ["log", "story", "ship", "crewmates"]

    for i in tables:
        delete_api = client.delete_api()
        start_time = "1970-01-01T00:00:00Z"
        stop_time = datetime.now()
        predicate = f'_measurement="{i}"'

        try:
            delete_api.delete(
                start=start_time,
                stop=stop_time,
                predicate=predicate,
                bucket=influx_bucket,
                org=influx_org
            )
            print("Deletion request successfully sent.")

        except Exception as e:
            print(f"An error occurred during deletion: {e}")



@app.route("/next_day", methods=["POST"])
def next_day():
    thread = threading.Thread(target=main_loop())
    thread.start()

    return jsonify({"status": "received"})

@app.route("/cook_food", methods=["GET"])
def cook_food():
    pass

@app.route("/repair_ship", methods=["GET"])
def repair_ship():
    pass

@app.route("/defend_ship", methods=["GET"])
def defend_ship():
    pass

@app.route("/heal_crew", methods=["GET"])
def heal_crew():
    pass

if __name__ == '__main__':
    clear_database()

    response = ask_gemini_prompt(BEGIN_GAME)
    add_to_story(response["message"])
    add_to_ship()
    add_to_log("All systems are good", 1)
    init_crew(response["crew"])

    app.run(host='0.0.0.0', port=5000)