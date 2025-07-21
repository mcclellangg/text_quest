"""
Tests for key functionalities of TUTORIAL_GAME.
- Ensure GameCoordinator loads the tutorial game and can start the game loop.
"""

import pytest

# Import GameCoordinator from the correct module path
from text_quest.core import GameCoordinator


def test_game_loads_and_starts(monkeypatch):
    # Patch input to simulate user entering 'q' to immediately exit the game loop
    monkeypatch.setattr("builtins.input", lambda _: "q")

    # Instantiate GameCoordinator (should load TUTORIAL_GAME.json)
    game = GameCoordinator()

    # Ensure player and current_room are loaded correctly
    assert game.player.get_current_location() == "start_room"
    assert game.current_room.get_id() == "start_room"

    # Run the game loop (should exit immediately due to 'q' input)
    with pytest.raises(SystemExit):
        game.run_game()
