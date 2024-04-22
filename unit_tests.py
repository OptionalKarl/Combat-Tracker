import unittest
from character_queries import get_next_combatant, check_for_char, update_char, insert_char
import sqlite3

class TestMessages(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE character (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        Character_token TEXT,
                        Name TEXT,
                        AC INTEGER,
                        Class TEXT,
                        Initiative INTEGER
            )
        ''')
        self.conn.commit()

    def tearDown(self):
        self.conn.close()

    def test_get_next_combatant(self):
        # Add test data
        self.cursor.execute('INSERT INTO character (character_token, name, AC, class, Initiative) VALUES ("1", "Test1", 10, "Barbarian", 15)')
        self.cursor.execute('INSERT INTO character (character_token, name, AC, class, Initiative) VALUES ("2", "Test2", 12, "Wizard", 20)')
        self.cursor.execute('INSERT INTO character (character_token, name, AC, class, Initiative) VALUES (3"", "Test3", 12, "Wizard", 100)')
        self.cursor.execute('INSERT INTO character (character_token, name, AC, class, Initiative) VALUES ("4", "Test4", 13, "Wizard", 100)')
        self.conn.commit()

        # Test with initiative 99
        result, new_init = get_next_combatant(99,self)
        self.assertEqual(result, [(2, "Test2", 12, "Wizard", 20)])
        self.assertEqual(new_init, 20)
    

        # Test with initiative 17
        result, newinit= get_next_combatant(17,self)
        self.assertEqual(result, [(1, "Test1", 10, "Barbarian", 15)])
        self.assertEqual(newinit, 15)

        # Test with initiative 15 (causing reset to 99)
        result, newinit = get_next_combatant(15,self)
        self.assertEqual(result, '"Message": "End of Round"')
        self.assertEqual(newinit, 99)

        # Test with initiative 101 (return multiple results)
        result, newinit = get_next_combatant(101,self)
        self.assertEqual(result, [(3, "Test3", 12, "Wizard", 100),(4, "Test4", 13, "Wizard", 100)])
        self.assertEqual(newinit, 100)

    def test_check_for_char(self):
        # Add test data
        self.cursor.execute('INSERT INTO character (character_token,  name, AC, class, Initiative) VALUES ("1", "Test1", 10, "Barbarian", 15)')
        self.conn.commit()

        # Test with existing character
        result, char_id = check_for_char("1",self)
        self.assertTrue(result)
        self.assertEqual(char_id, 1)

        # Test with non-existing character
        result, char_id = check_for_char("NonExistent",self)
        self.assertFalse(result)
        self.assertEqual(char_id, 0)

    def test_update_char(self):
        # Add test data
        self.cursor.execute('INSERT INTO character (character_token, name, AC, class, Initiative) VALUES ("1", "Test1", 10, "Barbarian", 15)')
        self.conn.commit()

        # Update character
        update_char("1", "Test1", 12, "Wizard", 20,self)

        # Retrieve updated character
        self.cursor.execute('SELECT * FROM character WHERE character_token = "1"')
        result = self.cursor.fetchone()
        self.assertEqual(result, (1,"1", "Test1", 12, "Wizard", 20))

    def test_insert_char(self):
        # Insert new character
        character_token = insert_char("Test2", 10, "Barbarian", 15,self)

        # Retrieve inserted character
        self.cursor.execute('SELECT * FROM character WHERE character_token = "{character_token}"'.format(character_token = character_token))
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertIsNotNone(character_token)

if __name__ == '__main__':
    unittest.main()
