"""
Game entities:
- Player
- Rooms
- Items
"""

from dataclasses import dataclass, asdict


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

    def update_current_location(self, room_id: str):
        self.current_location = room_id

    def update_total_moves(self):
        self.total_moves += 1


@dataclass
class Room:
    id: str
    name: str
    base_description: str
    num_player_visits: int
    connections_map: dict

    @classmethod
    def from_dict(cls, room_data: dict):
        return cls(**room_data)

    def to_dict(self):
        return asdict(self)

    def get_base_description(self):
        return self.base_description

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id

    def display_room(self):
        """Displays in following format when rooms are first entered.
        ROOM NAME
        You are in a dark, dank room.
        """
        print(self.get_name())
        print(self.get_base_description())

    def validate_direction(self, direction: str):
        # NOTE: error should be handled at a higher level, but for prototype purposes this is fine.
        try:
            self.connections_map[direction]
            return True
        except KeyError as e:
            print(f"Unable to move: {direction} The way is blocked!")
            return False

    def get_adjacent_room_id(self, direction: str):
        return self.connections_map[direction]

    def update_num_player_visits(self):
        self.num_player_visits += 1
