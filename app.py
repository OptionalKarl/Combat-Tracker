import json
import logging
from flask import Flask, request, jsonify, session
import uuid
from character_queries import check_for_char, update_char, insert_char, get_char
from Initiative_queries import get_next_combatant
from character import Character
from swagger_ui import api_doc

logging.basicConfig(filename='log.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

api_doc(app, config_path='docs\swagger.json', url_prefix='/api/doc', title='API doc')

guid = uuid.uuid4()
app.secret_key = str(guid).encode()


def before_first_request():
    session['current_initiative'] = 99


character = Character()

@app.route("/")
def home():
    app.logger.info('Home endpoint accessed')
    return "Home"

@app.route("/new-encounter", methods=["POST"])
def new_encounter():
    try:
        session['current_initiative'] = 99
        app.logger.info('Initiative reset successfully')
        return jsonify("Message: Initiative Reset"), 200
    except Exception as e:
        app.logger.error('Error occurred during initiative reset: %s', e)
        return jsonify({"error": str(e)}), 500

@app.route("/next-combatant", methods=["GET"])
def next():
    initiative = session.get('current_initiative', 99)
    try:
        result, new_init = get_next_combatant(initiative)
        session['current_initiative'] = new_init
        app.logger.info('Next combatant retrieved')
        return jsonify(result), 200
    except Exception as e:
        app.logger.error('Unable to get next combatant')
        return jsonify({"error": str(e)}), 500

@app.route("/single-character", methods=["POST", "GET"])
def single_character():
    if request.method == "POST":
        response = character.update(request.json)
        
    if request.method == "GET":
        response = character.get(request.json)
    if response[0] != 200:
        response[1] = jsonify({"error" : response[1]})

    return response[1] , response[0]

@app.route("/characters", methods=["POST", "GET"])
def characters():
    if request.method == "POST":
            response = character.bulk(request.json)

    if request.method == "GET":
            response = character.get_all()

    if response[0] != 200:
            response[1] = jsonify({"error" : response[1]})

    return response[1] , response[0]

if __name__ == "__main__":
    app.run(port=80, debug=True)
