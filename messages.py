import sqlite3
from flask import session

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

def check_for_char(name, connection = None):
    try:
        if connection == None:
            conn, cursor = connect_to_database()
        else:
            conn = connection.conn
            cursor = connection.cursor
        query = 'SELECT ID FROM character WHERE name = "{name}"'.format(name=name)
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
            '''.format(id=id, ac=ac, char_class=char_class, initiative=initiative, name=name)

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
        query_select = 'Select Max(ID) from character'
        cursor.execute(query_select)
        result = cursor.fetchone()
        if bool(result[0]):
            newID = result[0]
        else:
            newID = 1

        query_insert = '''
            INSERT INTO character (ID, name, AC, class, Initiative)
            VALUES ({id}, "{name}", {ac},"{char_class}", {init})
            '''.format(id=newID, name=name, ac=ac, char_class=char_class, init=initiative)

        cursor.execute(query_insert)
        conn.commit()
        if connection == None:
            conn.close()
    except Exception as e:
        print(f"Error in insert_char: {e}")
        raise e

def get_char(id, connection=None):
    if connection == None:
        conn, cursor = connect_to_database()
    else:
        conn = connection.conn
        cursor = connection.cursor
    query = '''
        Select * from character where ID = {id}
        '''.format(id = id)
    try:
        cursor.execute(query)
        character = cursor.fetchone()
        if connection == None:
            conn.close()
        return character
    except Exception as e:
        print(f"Error in insert_char: {e}")
        raise e