"""
Game entities:
- Player
- Rooms
- Items
"""

from dataclasses import dataclass, asdict
from typing import List, Optional


@dataclass
class Item:
    id: str
    name: str
    description: str
    current_location: str

    @classmethod
    def from_dict(cls, item_data: dict):
        return cls(**item_data)

    def to_dict(self):
        return asdict(self)

    def get_description(self):
        return self.description

    def get_current_location(self):
        return self.current_location

    def update_current_location(self, location: str):
        """Updates current_location of item to one of below values:
        - 'room_id'
        - 'player_inventory'
        """
        self.current_location = location


@dataclass
class Player:
    health: int
    total_moves: int
    inventory: list
    current_location: str

    @classmethod
    def from_dict(cls, player_data: dict):
        return cls(**player_data)

    def to_dict(self):
        return asdict(self)

    def get_total_moves(self):
        return self.total_moves

    def get_current_location(self):
        "Returns 'room_id' for current room."
        return self.current_location

    def get_inventory_items_by_id(self) -> List[str]:
        """
        Example return -> ['lamp', 'sword', 'trophy']
        NOTE: currently inventory is a list of items referenced by their id. This will need to be changed to support future functionalities
        (player inspecting item, displaying item by name).
        """
        return self.inventory

    def update_current_location(self, room_id: str):
        self.current_location = room_id

    def add_item_to_inventory(self, item):
        self.inventory.append(item.id)
        print(f"{item.id} added to pack.")

    def remove_item_from_inventory(self, item):
        if item in self.inventory:
            print(f"{item.id} removed from pack.")

    def increment_total_moves(self, n: int = 1):
        """Increments total moves taken by player by given number (n) or 1."""
        self.total_moves += n


@dataclass
class Room:
    id: str
    name: str
    base_description: str
    num_player_visits: int
    connections_map: dict
    properties: dict

    # Define condition functions as a class variable
    condition_functions = None

    @classmethod
    def _initialize_condition_functions(cls):
        """Initialize condition functions - call this once when setting up the class"""
        cls.condition_functions = {
            "has_item": cls._has_item,
            "visit_count_less": cls._visit_count_less,
        }

    def _has_item(self, item_name: str, items_in_room: List[str]) -> bool:
        """Check if a specific item is present in the room"""
        return item_name in items_in_room

    def _visit_count_less(self, n: int, items_in_room: List[str]) -> bool:
        """Check if player has visited less than n (number) times"""
        return self.num_player_visits < n

    def generate_modified_description(
        self, items_in_room: Optional[List[str]] = None
    ) -> str:
        """Generate dynamic description based on conditions"""
        if items_in_room is None:
            items_in_room = []

        description = self.base_description

        # Get conditional descriptions from properties
        conditional_descriptions = self.properties.get("conditional_descriptions", {})

        for condition_name, condition_data in conditional_descriptions.items():
            if isinstance(condition_data, dict) and "condition" in condition_data:
                condition_config = condition_data["condition"]
                modifier = condition_data["description_modifier"]

                if self._evaluate_condition(condition_config, items_in_room):
                    description += " " + modifier

        return description

    def _evaluate_condition(
        self, condition_data: dict, items_in_room: List[str]
    ) -> bool:
        """Evaluate a condition based on its configuration"""
        if not isinstance(condition_data, dict):
            return False

        condition_type = condition_data.get("type")
        params = condition_data.get("params", [])

        if condition_type in self.condition_functions:
            try:
                return self.condition_functions[condition_type](
                    self, *params, items_in_room
                )
            except Exception as e:
                print(f"Error evaluating condition '{condition_type}': {e}")
                return False

        return False

    @classmethod
    def from_dict(cls, room_data: dict):
        if cls.condition_functions is None:
            cls._initialize_condition_functions()

        return cls(**room_data)

    def to_dict(self):
        return asdict(self)

    def get_base_description(self):
        return self.base_description

    def get_name(self):
        return self.name

    def get_id(self) -> str:
        """Returns room_id, ex: -> 'start_room'"""
        return self.id

    def display_room(self, items_in_room: List[str]):
        """Displays in following format when rooms are first entered.
        ROOM NAME
        You are in a dark, dank room.
        """
        print(self.get_name())
        print(self.generate_modified_description(items_in_room=items_in_room))

    def validate_direction(self, direction: str):
        """Check connections map for attempted direction and return True if player can travel to that room."""
        try:
            self.connections_map[direction]
            return True
        except KeyError as e:
            print(f"Unable to move: {direction} The way is blocked!")
            return False

    def get_adjacent_room_id(self, direction: str):
        return self.connections_map[direction]

    def increment_num_player_visits(self, n=1):
        self.num_player_visits += n
