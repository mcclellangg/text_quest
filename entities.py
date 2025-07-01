"""
Game entities:
- Player
- Rooms
- Items
"""

from dataclasses import dataclass, asdict


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
