#import firebase_admin
#from firebase_admin import credentials, firestore
from flask import Flask, jsonify
from flask_cors import CORS
import datetime

from Ship import Ship
from CrewMember import CrewMember

app = Flask(__name__)
CORS(app)

"""
#Firebase setup
cred = credentials.Certificate("certs/firebase-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
"""

ship = Ship()

@app.route("/data/telemetry", methods=["GET"])
def get_telemetry():
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)