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

