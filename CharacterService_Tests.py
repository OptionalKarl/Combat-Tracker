import unittest
from unittest.mock import MagicMock
from app import CharacterService

class TestCharacterService(unittest.TestCase):

    def test_update_character(self):
        # Mock request.json data
        data = {
            "character_token": "token",
            "name": "test",
            "ac": 10,
            "class": "Barbarian",
            "initiative": 15
        }

        # Create an instance of CharacterService
        character_service = CharacterService()

        # Mock the methods used inside update_character
        character_service.update_character = MagicMock(return_value={"ID" : 1,
            "character_token": "token",
            "name": "test",
            "ac": 10,
            "class": "Barbarian",
            "initiative": 15
        })

        # Call the method
        result = character_service.update_character (data)

        # Assertions
        character_service.update_character.assert_called_once_with({
            "character_token": "token",
            "name": "test",
            "ac": 10,
            "class": "Barbarian",
            "initiative": 15
        })

    def test_get_character(self):
        data = "1"

        character_service = CharacterService()

        character_service.get_character = MagicMock(return_value={"ID": 1,"character_token" : "1", "name": "Test1", "AC": 10, "class": "Barbarian", "Initiative": 15})

        result = character_service.get_character(data)

        character_service.get_character.assert_called_once_with("1")
        self.assertEqual(result, {"ID": 1,"character_token" : "1", "name": "Test1", "AC": 10, "class": "Barbarian", "Initiative": 15})


if __name__ == '__main__':
    unittest.main()
