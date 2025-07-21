"""
Tests for Player class functionalities.
"""

import pytest
from text_quest.entities import Player

PLAYER_DATA = {
    "health": 100,
    "total_moves": 0,
    "inventory": ["blank_map"],
    "current_location": "start_room",
    "properties": {"in_darkness": False, "darkness_stacks": 0},
}


def test_player_moves_from_start_room_to_dark_maze_1():

    # Create player
    player = Player.from_dict(PLAYER_DATA)

    # Case 1: Player is in 'start_room'
    assert player.get_current_location() == "start_room"

    # Case 2: Player is in dark_maze_a
    assert player.set_current_location("dark_maze_a") == "dark_maze_a"


def test_darkness_property():
    player = Player.from_dict(PLAYER_DATA)
    assert player.properties.get("in_darkness") == False
