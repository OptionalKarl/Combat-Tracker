import sqlite3;
import uuid;

def connect_to_database():
    conn = sqlite3.connect('Tracker.db')
    cursor = conn.cursor()
    return conn, cursor

def insert_campaign(campaign, connection = None):
    try:
        if connection == None:
            conn, cursor = connect_to_database()
        else:
            conn = connection.conn
            cursor = connection.cursor
        campaign.campaign_token = str(uuid.uuid4())
        query = '''
                INSERT INTO campaign (Campaign_token, Name, Setting, Description)
                VALUES ({Campaign_token}, {Name}, {Setting}, {Description});
                '''.format (Campaign_token = campaign.campaign_token, Name = campaign.name, Setting = campaign.setting, Description = campaign.description)
        cursor.execute(query)
        conn.commit()
        if connection == None:
            conn.close()
        return campaign.campaign_token
    except Exception as e:
        print(f"Error in insert_campaign: {e}")
        raise e