"""
Tests for Item class functionality using lamp.
"""

import pytest
from text_quest.entities import Item

LAMP_DATA = {
    "id": "lamp",
    "name": "lamp",
    "base_description": "An old storm lantern bearing the stamp of 'Cloman Co-makers of reliable products'.",
    "current_location": "start_room",
    "commands": ["on", "off", "inspect"],
    "properties": {
        "is_lit": False,
    },
    "property_constraints": {
        "is_lit": {
            "type": "bool",
            "toggleable": True,
            "description": "Whether the lamp is currently lit",
            "state_descriptions": {
                "true": "It glows with a warm, flickering light.",
                "false": "It sits dark and unlit.",
            },
        }
    },
    "cmd_to_config_map": {
        "on": {
            "property": "is_lit",
            "action_type": "toggle",
            "target_value": True,
            "prerequisites": [
                {
                    "property": "fuel_remaining",
                    "condition": "greater_than",
                    "value": 0,
                    "fail_message": "The lamp is out of fuel and cannot be lit.",
                }
            ],
            "already_message": "The lamp is already glowing brightly!",
            "success_message": "You turn on the lamp. It casts a warm, flickering light.",
        },
        "off": {
            "property": "is_lit",
            "action_type": "toggle",
            "target_value": False,
            "already_message": "The lamp is already off.",
            "success_message": "You extinguish the lamp. Darkness surrounds you.",
        },
    },
}


def test_lamp_and_update_location():
    # Minimal room data with a conditional description for lamp presence

    # Create Lamp object
    lamp = Item.from_dict(LAMP_DATA)

    # Case 1: Lamp is in 'start_room`
    lamp_in_start_room = lamp.get_current_location()
    assert lamp_in_start_room == "start_room"

    # Case 2: Lamp is in 'player_inventory'
    lamp_in_inventory = lamp.set_current_location(location="player_inventory")
    assert lamp_in_inventory == "player_inventory"


def test_lamp_inspect_command():
    lamp = Item.from_dict(LAMP_DATA)
    lamp_inspect_result = lamp.inspect_object()
    assert (
        lamp_inspect_result
        == "An old storm lantern bearing the stamp of 'Cloman Co-makers of reliable products'. It sits dark and unlit."
    )
