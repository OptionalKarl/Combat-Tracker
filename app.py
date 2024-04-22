import logging;
from flask import Flask, request, jsonify, session;
import uuid;
from character_queries import check_for_char, update_char, insert_char, get_char;
from Initiative_queries import get_next_combatant;
from swagger_ui import api_doc;


logging.basicConfig(filename='log.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

api_doc(app, config_path='config\swagger.json', url_prefix='/api/doc', title='API doc')


guid = uuid.uuid4()
app.secret_key = str(guid).encode()

def before_first_request():
    session['current_initiative'] = 99

@app.route("/")
def home():
    app.logger.info('Home endpoint accessed')
    return "Home"

@app.route("/new-encounter", methods = ["POST"])
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
        result,new_init = get_next_combatant(initiative)
        session['current_initiative'] = new_init
        app.logger.info('Next combatant retrieved')
        return jsonify(result), 200
    except Exception as e:
        app.logger.error('Unable to get next combatant')
        return jsonify({"error": str(e)}), 500

@app.route("/character", methods=["POST","GET"])
def characters():
    if request.method == "POST":
        return update_character()
    if request.method == "GET":
        return jsonify({"Message" : "Feature Build In Progress"})

def update_character():
    data = request.json

    required_fields = ['character_token','name', 'ac', 'class', 'initiative']
    for field in required_fields:
        if field not in data:
            app.logger.error(f"Missing required field: {field}")
            return jsonify({"error": f"Missing required field: {field}"}), 400

        if not isinstance(data['name'], str) or \
           not isinstance(data['ac'], int) or \
           not isinstance(data['class'], str) or \
           not isinstance(data['initiative'], int):
            app.logger.error("Invalid data types")
            return jsonify({"error": "Invalid data types"}), 400

        # Check field lengths
        if len(data['name']) > 32 or len(data['class']) > 32:
            app.logger.error("Name or class exceeds maximum length of 32 characters")
            return jsonify({"error": "Name or class exceeds maximum length of 32 characters"}), 400

    try:
        character_token = data.get('character_token')
        name = data.get('name')
        ac = data.get('ac')
        char_class = data.get('class')
        initiative = data.get('initiative')
    except Exception as e:
        app.logger.error('Unable to load character data: %s', str(e))
        return jsonify({"error": str(e)}), 400
    
    try:
        char_exists, id = check_for_char(name)
    except Exception as e:
        app.logger.error('Unable to check for character in DB: %s', str(e))
        return jsonify({"error": str(e)}), 500
    
    if char_exists:
        try:
            update_char(id, name, ac, char_class, initiative)
            app.logger.info('Character %s updated successfully', name)
            return jsonify({"message": "Character updated successfully"}), 200
        except Exception as e:
            app.logger.error('unable to update chracter: %s', e)
            return jsonify({"message": "Unable to update Character"}), 500
    else:
        try:
            token  = insert_char(character_token, name, ac, char_class, initiative)
            app.logger.info('New character %s added successfully', name)
            return jsonify({"message": "Character added successfully"}), 200
        except Exception as e:
            app.logger.error('New character failed to update: %s', e)
            return jsonify({"message": f"Character not added, character token: {token}"  }), 500

def get_character():
    data = request.json
    required_fields = ['id']
    for field in required_fields:
        if field not in data:
            app.logger.error(f"Missing required field: {field}")
            return jsonify({"error": f"Missing required field: {field}"}), 400
    if not isinstance(data['id'], int):
        app.logger.error("Invalid data types")
        return jsonify({"error": "Invalid data types"}), 400
    try:
            id = data.get('id')
    except Exception as e:
        app.logger.error('Unable to load character data: %s', str(e))
        return jsonify({"error": str(e)}), 400
    try:
        character = get_char(id)
        return jsonify(character)
    except Exception as e:
        app.logger.error('Unable to get character character in DB: %s', str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port = 80, debug=True)
