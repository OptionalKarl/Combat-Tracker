import unittest
from unittest.mock import MagicMock
from character import Character

class TestCharacterService(unittest.TestCase):

    def test_update_character(self):
        data = {
            "character_token": "token",
            "name": "test",
            "ac": 10,
            "class": "Barbarian",
            "initiative": 15
        }

        character = Character()

        character.update = MagicMock(return_value={"ID" : 1,
            "character_token": "token",
            "name": "test",
            "ac": 10,
            "class": "Barbarian",
            "initiative": 15
        })

        # Call the method
        result = character.update(data)

        # Assertions
        character.update.assert_called_once_with({
            "character_token": "token",
            "name": "test",
            "ac": 10,
            "class": "Barbarian",
            "initiative": 15
        })

    def test_get_character(self):
        data = "1"

        character = Character(data)

        character.get = MagicMock(return_value={"ID": 1,"character_token" : "1", "name": "Test1", "AC": 10, "class": "Barbarian", "Initiative": 15})

        result = character.get(data)

        character.get.assert_called_once_with("1")
        self.assertEqual(result, {"ID": 1,"character_token" : "1", "name": "Test1", "AC": 10, "class": "Barbarian", "Initiative": 15})


if __name__ == '__main__':
    unittest.main()
