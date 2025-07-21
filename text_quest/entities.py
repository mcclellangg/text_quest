"""
Game entities:
- Player
- Rooms
- Items
"""

from dataclasses import dataclass, asdict
from typing import Any, Callable, Dict, List, Optional


@dataclass
class Item:
    id: str
    name: str
    base_description: str
    current_location: str
    commands: List[str]
    properties: Dict[str, Any]
    property_constraints: Dict[str, Dict]
    cmd_to_config_map: Dict[str, Dict]

    # Command function registry
    command_functions: Dict[str, Callable] = None

    def __post_init__(self):
        """
        Initialize command functions after object creation.
        Needed because command_functions will be different on a per-instance level.
        """
        if not self.command_functions:
            self._initialize_command_functions()

    def _initialize_command_functions(self):
        # Shared command_functions
        self.command_functions = {
            "inspect": self.inspect_object,
            # "toggle_property": self.execute_property_command,
            # "set_property": self.execute_property_command,
            # "increment_property": self.execute_property_command
        }

        # Map specific commands based on action type
        # for cmd_name, cmd_config in self.cmd_to_config_map.items():
        #     if cmd_config.get("action_type") == "toggle":
        #         self.command_functions[cmd_name] = self.execute_property_command
        #     elif cmd_config.get("action_type") == "set_value":
        #         self.command_functions[cmd_name] = self.execute_property_command
        #     elif cmd_config.get("action_type") == "increment":
        #         self.command_functions[cmd_name] = self.execute_property_command

    @classmethod
    def from_dict(cls, item_data: dict):
        return cls(**item_data)

    def to_dict(self):
        data = asdict(self)
        data.pop("command_functions", None)
        return data

    def get_description(self):
        return self.base_description

    def generate_modified_description(self):
        """Get a dynamic description including property states."""
        base_description = self.base_description

        state_descriptions = []

        for prop_name, prop_value in self.properties.items():
            if prop_name in self.property_constraints:
                constraints = self.property_constraints[prop_name]

                if "state_descriptions" in constraints:
                    state_desc = self._format_property_description(
                        prop_value, constraints["state_descriptions"]
                    )
                    if state_desc:
                        state_descriptions.append(state_desc)

        if state_descriptions:
            return f"{base_description} {'\n'.join(state_descriptions)}"
        return base_description

    def _format_property_description(
        self, value: Any, state_descriptions: Dict
    ) -> Optional[str]:
        """Get appropriate state description based on property value"""
        if isinstance(value, bool):
            return state_descriptions.get("true" if value else "false")
        elif isinstance(value, (int, float)):
            # Handle numeric ranges
            for condition, description in state_descriptions.items():
                if condition.startswith("greater_than_"):
                    threshold = float(condition.split("_")[-1])
                    if value > threshold:
                        return description
                elif condition.startswith("less_than_"):
                    threshold = float(condition.split("_")[-1])
                    if value < threshold:
                        return description
                elif condition.startswith("equals_"):
                    threshold = float(condition.split("_")[-1])
                    if value == threshold:
                        return description
        return None

    def inspect_object(self):
        return self.generate_modified_description()

    # Property Managers
    def has_property(self, property_name: str) -> bool:
        """
        Returns boolean indicating existence of given property.
        """
        return property_name in self.properties

    def get_property_value(self, property_name: str) -> Any:
        return self.properties.get(property_name)

    def set_property(self, property_name: str, value: Any):
        """
        Set object property with type validation, constraints, and smart defaults.
        Uses property_constraints from the object definition.
        """
        if property_name not in self.properties:
            raise KeyError(f"Property '{property_name}' not found on object")

        current_value = self.properties[property_name]
        constraints = self.property_constraints[property_name]
        expected_type = constraints["type"]

        if expected_type == "int":
            if value is None:
                raise ValueError(f"Integer property '{property_name}' requires a value")
            new_value = int(value)

        self.properties[property_name] = new_value
        return new_value

    def get_current_location(self):
        return self.current_location

    def set_current_location(self, location: str):
        """Updates current_location of item to one of below values:
        - 'room_id'
        - 'player_inventory'
        """
        self.current_location = location
        return self.current_location


@dataclass
class Player:
    health: int
    total_moves: int
    inventory: list
    current_location: str
    properties: dict

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

    def _has_item_in_inventory(self, item_id: str) -> bool:
        """
        Checks that a given item_id is currently in player's inventory. Returns a boolean.
        """
        return item_id in self.inventory

    def get_inventory_items_by_id(self) -> List[str]:
        """
        Example return -> ['lamp', 'sword', 'trophy']
        NOTE: currently inventory is a list of items referenced by their id. This will need to be changed to support future functionalities
        (player inspecting item, displaying item by name).
        """
        return self.inventory

    def set_current_location(self, room_id: str):
        self.current_location = room_id
        return self.current_location

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
