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
import datetime
from datetime import datetime

from Ship import Ship
from CrewMember import CrewMember

#Gemini Config
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    'gemini-2.5-flash',generation_config=GenerationConfig(response_mime_type="application/json")
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
    if random.randint(0, 2) == 1:
        ship.decrease_fuel()
        decrease_fuel_log()
    ship.increase_date()

    for crewmate in crew:
        crewmate.decrease_hunger(random.randint(10,20))
        if crewmate.get_hunger() < 50:
            crewmate.set_health(crewmate.get_health() - 5)
        elif crewmate.get_hunger() > 50 and crewmate.get_health() < 95:
            crewmate.set_health(crewmate.get_health() + 5)

    crew_string = ""

    for i in crew:
        crew_string += i.get_crew_context()

    if random.randint(0,3) == 0:
        warning = [drift_off_course, crew_injury, alien_attack, mechanical_failure, asteroid_strike]
        disaster = random.choice(warning)
        disaster()

    response = ask_gemini_prompt(
        f"""
        The user has passed to the next day, generate a brief summary of some
        events that could have happened, nothing serious or eventful, can be funny or waffle
        
        It must be a summary from an external point of view with no connection to the people involved in the ship.
        Taking the current state of ship and crew into account. It could be helpful to comment on any crew or 
        ship stats getting low 
        
        { ship.get_ai_context() }
        { crew_string }
        
        Return a JSON object with this exact key:"
        {{
            "message": "your message to the player to begin the game and give them some backstory"
        }}
        """
    )

    add_to_story(response["message"])
    add_to_ship()
    add_to_crew(crew)

def drift_off_course():
    add_to_log("You're drifting off course towards a black hole", "CRITICAL")

def crew_injury():
    person = random.choice(crew)
    person.set_status("Injured")
    add_to_crew(crew)
    add_to_log(person.get_name() + " has been injured", "warning")

def alien_attack():
    add_to_log("You are being threatened by aliens", "CRITICAL")

def mechanical_failure():
    add_to_log("There has been a mechanical failure", "warning")

def asteroid_strike():
    if ship.get_hull_integrity() > 45:
        ship.set_hull_integrity(ship.get_hull_integrity() - 45)
    else:
        ship.set_hull_integrity(0)

    add_to_log("You have been hit by asteroids", "CRITICAL")

def decrease_fuel_log():
    if ship.get_fuel() > 30:
        add_to_log("Fuel level decreased", "Normal")
    elif ship.get_fuel() > 10:
        add_to_log("Fuel level low", "Warning")
    else:
        add_to_log("Fuel very low", "CRITICAL")

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

@app.route("/cook_food", methods=["POST"])
def cook_food():
    for crewmate in crew:
        if crewmate.get_hunger() < 75:
            crewmate.set_hunger(crewmate.get_hunger() + 25)
        else:
            crewmate.set_hunger(100)
    ship.set_food(ship.get_food() - 5)

    add_to_ship()
    add_to_crew(crew)

    add_to_log("Kitchen is a little smokey", "normal")

    thread = threading.Thread(target=main_loop())
    thread.start()

    return jsonify({"status": "received"})

@app.route("/repair_ship", methods=["POST"])
def repair_ship():
    if ship.get_hull_integrity() < 90 and ship.get_spare_parts() > 10:
        ship.set_hull_integrity(ship.get_hull_integrity() + 10)
        ship.set_spare_parts(ship.get_spare_parts() - 10)

    if ship.get_hull_integrity() < 90:
        add_to_log("Hull integrity is low", "warning")
    elif ship.get_hull_integrity() < 80:
        add_to_log("Hull integrity is very low", "CRITICAL")
    else:
        add_to_log("Hull integrity is safe", "normal")

    add_to_ship()

    thread = threading.Thread(target=main_loop())
    thread.start()

    return jsonify({"status": "received"})

@app.route("/defend_ship", methods=["POST"])
def defend_ship():
    if ship.get_ammo() > 10:
        ship.set_ammo(ship.get_ammo() - 10)
    else:
        ship.set_ammo(0)

    if ship.get_ammo() < 40:
        add_to_log("Ammo is low", "warning")
    elif ship.get_ammo() < 20:
        add_to_log("Ammo is very low", "CRITICAL")

    add_to_ship()

    thread = threading.Thread(target=main_loop())
    thread.start()

    return jsonify({"status": "received"})

@app.route("/heal_crew", methods=["POST"])
def heal_crew():
    if ship.get_medical() > 20:
        ship.set_medical(ship.get_medical() - 20)
    else:
        ship.set_medical(0)

    if ship.get_medical() < 10:
        add_to_log("Medical supplies are very low", "CRITICAL")
    elif ship.get_medical() < 30:
        add_to_log("Medical supplies are low", "warning")

    for crewmate in crew:
        if crewmate.get_health < 80:
            crewmate.set_health(crewmate.get_health() + 20)
        else:
            crewmate.set_health(100)

    add_to_ship()
    add_to_crew(crew)

    thread = threading.Thread(target=main_loop())
    thread.start()

    return jsonify({"status": "received"})

@app.route("/replace_filters", methods=["POST"])
def replace_filters():
    if ship.get_spare_parts() > 5:
        ship.set_spare_parts(ship.get_spare_parts() - 5)
        if ship.get_water() < 85:
            ship.set_water(ship.get_water() + 15)
        else:
            ship.set_water(100)

    add_to_ship()

    thread = threading.Thread(target=main_loop())
    thread.start()

    return jsonify({"status": "received"})

@app.route("/correct_course", methods=["POST"])
def correct_course():
    if ship.get_fuel() > 15:
        ship.set_fuel(ship.get_fuel() - 15)
    else:
        ship.set_fuel(0)

    if ship.get_fuel() < 10:
        add_to_log("Fuel is very low", "CRITICAL")
    elif ship.get_fuel() < 40:
        add_to_log("Fuel is low", "warning")

    add_to_ship()

    thread = threading.Thread(target=main_loop())
    thread.start()

    return jsonify({"status": "received"})

if __name__ == '__main__':
    clear_database()

    response = ask_gemini_prompt(BEGIN_GAME)
    add_to_story(response["message"])
    add_to_ship()
    add_to_log("All systems are good", "normal")
    init_crew(response["crew"])

    app.run(host='0.0.0.0', port=5000)