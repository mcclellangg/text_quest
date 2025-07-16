"""
Tests for Room class functionality.
"""

import pytest
from text_quest.entities import Room

def test_room_creation_and_modified_description():
    # Minimal room data with a conditional description for lamp presence
    room_data = {
        "id": "start_room",
        "name": "DUNGEON ENTRANCE",
        "base_description": "You stand alone in a dark damp basement.",
        "num_player_visits": 0,
        "connections_map": {"w": "armory"},
        "properties": {
            "conditional_descriptions": {
                "lamp_present": {
                    "condition": {
                        "type": "has_item",
                        "params": ["lamp"]
                    },
                    "description_modifier": "An old lamp sits on the workbench, casting flickering shadows on the walls."
                }
            }
        }
    }

    # Create Room object
    room = Room.from_dict(room_data)

    # Case 1: Lamp is present in the room
    desc_with_lamp = room.generate_modified_description(items_in_room=["lamp"])
    assert "An old lamp sits on the workbench" in desc_with_lamp

    # Case 2: Lamp is NOT present in the room
    desc_without_lamp = room.generate_modified_description(items_in_room=[])
    assert "An old lamp sits on the workbench" not in desc_without_lamp