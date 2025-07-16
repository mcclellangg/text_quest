"""
Tests for Item class functionality using lamp.
"""

import pytest
from text_quest.entities import Item


def test_lamp_and_update_location():
    # Minimal room data with a conditional description for lamp presence
    lamp_data = {
        "id": "lamp",
        "name": "lamp",
        "description": "An old storm lantern bearing the stamp of 'Cloman Co-makers of reliable products'.",
        "current_location": "start_room",
    }

    # Create Lamp object
    lamp = Item.from_dict(lamp_data)

    # Case 1: Lamp is in 'start_room`
    lamp_in_start_room = lamp.get_current_location()
    assert lamp_in_start_room == "start_room"

    # Case 2: Lamp is in 'player_inventory'
    lamp_in_inventory = lamp.set_current_location(location="player_inventory")
    assert lamp_in_inventory == "player_inventory"
