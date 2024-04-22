import sqlite3

def table_exists(table_name, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    result = cursor.fetchone()
    return result is not None

conn = sqlite3.connect('Tracker.db')
cursor = conn.cursor()

if not table_exists('character', conn):
    cursor.execute('''
        CREATE TABLE character (
            ID Integer PRIMARY KEY,
            Name TEXT,
            AC INTEGER,
            Class TEXT,
            Initiative INTEGER
        )

    ''')
if not table_exists('campaign', conn):
    cursor.execute('''
        CREATE TABLE campaign (
            ID Integer PRIMARY KEY,
            Name TEXT,
            Setting TEXT,
            Description TEXT            
        )

    ''')

if not table_exists('campaign_character', conn):
    cursor.execute('''
        CREATE TABLE campaign_character (
            ID INTEGER PRIMARY KEY,
            campaign_ID INTEGER,
            character_ID INTEGER

        )

    ''')

if not table_exists('campaign_initiative', conn):
    cursor.execute('''
        CREATE TABLE campaign_initiative (
            ID INTEGER PRIMARY KEY,
            campaign_ID INTEGER,
            current_initiative INTEGER

        )

    ''')

conn.commit()
conn.close()