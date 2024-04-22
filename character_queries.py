import sqlite3;
import random;
import uuid;

def connect_to_database():
    conn = sqlite3.connect('Tracker.db')
    cursor = conn.cursor()
    return conn, cursor



def get_next_combatant(initiative, connection = None):
    try:
        if connection == None:
            conn, cursor = connect_to_database()
        else:
            conn = connection.conn
            cursor = connection.cursor
        query = ''' SELECT ID, name, AC, class, Initiative
                    FROM character
                    WHERE Initiative = (
                            SELECT MAX(Initiative)
                            FROM character
                            WHERE Initiative < {initiative}
                        );
                    '''.format(initiative = initiative)
        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) == 0:
            
            return '"Message": "End of Round"', 99
        else:
            newInit = [row[4] for row in result]
        if connection == None:
            conn.close() 
        return result, newInit[0]
    except Exception as e:
        print(f"Error in get_next_combatant: {e}")
        raise e

def check_for_char(token, connection = None):
    try:
        if connection == None:
            conn, cursor = connect_to_database()
        else:
            conn = connection.conn
            cursor = connection.cursor
        query = 'SELECT ID FROM character WHERE character_token = "{token}"'.format(token=token)
        cursor.execute(query)
        existing_character = cursor.fetchone()
        if connection == None:
            conn.close()
        if bool(existing_character):
            id = existing_character[0]
        else:
            id = 0
        return bool(existing_character), id
    except Exception as e:
        print(f"Error in check_for_char: {e}")
        raise e

def update_char(id, name, ac, char_class, initiative, connection = None):
    try:
        if connection == None:
            conn, cursor = connect_to_database()
        else:
            conn = connection.conn
            cursor = connection.cursor
        query = '''
            UPDATE character
            SET AC = {ac},name = "{name}", class = "{char_class}", initiative = {initiative}
            WHERE id = {id}
            '''.format(ac=ac, char_class=char_class, initiative=initiative, name=name,id=id)

        cursor.execute(query)
        conn.commit()
        if connection == None:
            conn.close()
    except Exception as e:
        print(f"Error in update_char: {e}")
        raise e

def insert_char(name, ac, char_class, initiative, connection = None):
    try:
        if connection == None:
            conn, cursor = connect_to_database()
        else:
            conn = connection.conn
            cursor = connection.cursor

        character_token = str(uuid.uuid4())
        query = '''
            INSERT INTO character (character_token, name, AC, class, Initiative)
            VALUES ("{character_token}", "{name}", {ac},"{char_class}", {init})
            '''.format(character_token=character_token, name=name, ac=ac, char_class=char_class, init=initiative)

        cursor.execute(query)
        conn.commit()
        if connection == None:
            conn.close()
        return character_token
    except Exception as e:
        print(f"Error in insert_char: {e}")
        raise e

def get_char(character_token, connection=None):
    if connection == None:
        conn, cursor = connect_to_database()
    else:
        conn = connection.conn
        cursor = connection.cursor
    query = '''
        Select * from character where character_token = {character_token}
        '''.format(character_token = character_token)
    try:
        cursor.execute(query)
        character = cursor.fetchone()
        if connection == None:
            conn.close()
        return character
    except Exception as e:
        print(f"Error in insert_char: {e}")
        raise e