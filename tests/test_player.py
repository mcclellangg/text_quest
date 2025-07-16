"""
Tests for Player class functionalities.
"""

import pytest
from text_quest.entities import Player

def test_player_moves_from_start_room_to_dark_maze_1():
    
    player_data = {
        "health": 100,
        "total_moves": 0,
        "inventory": [
            "blank_map"
        ],
        "current_location": "start_room"
    }

    # Create player
    player = Player.from_dict(player_data)
    
    # Case 1: Player is in 'start_room'
    assert player.get_current_location() == 'start_room'
    
    # Case 2: Player is in dark_maze_a
    assert player.set_current_location('dark_maze_a') == 'dark_maze_a'
    