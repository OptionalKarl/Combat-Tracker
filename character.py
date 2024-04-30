import json
from character_queries import check_for_char, update_char, insert_char, get_char

class Character:
    def __init__(self, character_token = None, name = None, ac= None, char_class= None, initiative= None):

        if name is not None and len(name) > 32:
            raise ValueError("Name exceeds maximum length of 32 characters")
        
        # Validate char_class length (optional)
        if char_class is not None and len(char_class) > 32:
            raise ValueError("Character class exceeds maximum length of 32 characters")


        self.character_token = character_token
        self.name = name
        self.ac = ac
        self.char_class = char_class
        self.initiative = initiative
        
    def update(self, data):
        
        try:
            character_data = json.loads(data)
            character = Character(**character_data)
        except ValueError:
            return [500, "Data items not valid"]
        except Exception as e:
            return [500, str(e)]
        



        # Call database-related functions to update or insert character
        try:
            char_exists, char_id = check_for_char(character.name)
            if char_exists:
                update_char(char_id, character.name, character.ac, character.char_class, character.initiative)
                return [200,'Character updated successfully"']
            else:
                insert_char(character.name, character.ac, character.char_class, character.initiative)
                return [200,'"message": "Character created successfully"']
        except Exception as e:
            return [500, str(e)]

    def get(self, data):
        # Validate input data
        if 'character_token' not in data or not isinstance(data['character_token'], str):
            return [400,"Invalid character token"]

        character_token = data.get('character_token')

        # Call database-related function to retrieve character
        try:
            character = get_char(character_token)
            return [200, character]
        except Exception as e:
            return [500, str(e)]