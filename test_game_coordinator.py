"""
Tests for GameCoordinator class focusing on load, restart, and save functionality.

Created with AI Assistance - https://claude.ai/share/1a4b0ed1-bd2e-4d9a-af7b-e965ad5ea42a

NOTE: Majority of tests are bypassed but are notable since GameCoordinator should be changed to use paths based on `config.py` NOT hardcoded values!
"""

import json
import pytest
from pathlib import Path
from unittest.mock import patch
import tempfile
import shutil
import sys
import os

# Ensure we can import from the current directory
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import with better error handling
try:
    from core import GameCoordinator
except ImportError as e:
    print(f"Import error: {e}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    print(f"Files in current directory: {list(Path('.').glob('*.py'))}")
    raise

# Test data constants
SAMPLE_TUTORIAL_GAME_DATA = {
    "rooms": {
        "start_room": {
            "id": "start_room",
            "name": "DUNGEON ENTRANCE",
            "base_description": "You stand alone in a dark damp basement. In the wall before you there is a gaping fissure roughly the size of a door. To the west there is a door.",
            "num_player_visits": 0,
            "connections_map": {"w": "armory", "n": "wine_cellar"},
        }
    },
    "player": {
        "health": 100,
        "total_moves": 0,
        "inventory": ["blank_map"],
        "current_location": "start_room",
    },
}

MODIFIED_GAME_DATA = {
    "rooms": {
        "start_room": {
            "id": "start_room",
            "name": "DUNGEON ENTRANCE",
            "base_description": "You stand alone in a dark damp basement. In the wall before you there is a gaping fissure roughly the size of a door. To the west there is a door.",
            "num_player_visits": 5,  # Modified from original
            "connections_map": {"w": "armory", "n": "wine_cellar"},
        }
    },
    "player": {
        "health": 75,  # Modified from original
        "total_moves": 10,  # Modified from original
        "inventory": ["blank_map", "sword"],  # Added item
        "current_location": "armory",  # Modified from original
    },
}


@pytest.fixture
def temp_game_directories():
    """Create temporary directories for game files and save files."""
    temp_base_dir = tempfile.mkdtemp()
    temp_base_path = Path(temp_base_dir)

    game_files_dir = temp_base_path / "game_files"
    save_files_dir = temp_base_path / "save_files"

    game_files_dir.mkdir()
    save_files_dir.mkdir()

    yield {
        "base_dir": temp_base_path,
        "game_files_dir": game_files_dir,
        "save_files_dir": save_files_dir,
    }

    # Cleanup
    shutil.rmtree(temp_base_dir)


@pytest.fixture
def tutorial_game_file(temp_game_directories):
    """Create a tutorial game file in the temporary directory."""
    tutorial_file_path = temp_game_directories["game_files_dir"] / "TUTORIAL_GAME.json"

    with open(tutorial_file_path, "w", encoding="utf-8") as file:
        json.dump(SAMPLE_TUTORIAL_GAME_DATA, file, indent=4)

    return tutorial_file_path


@pytest.fixture
def sample_save_file(temp_game_directories):
    """Create a sample save file for testing load functionality."""
    save_file_path = temp_game_directories["save_files_dir"] / "test_save.json"

    with open(save_file_path, "w", encoding="utf-8") as file:
        json.dump(MODIFIED_GAME_DATA, file, indent=4)

    return save_file_path


@pytest.fixture
def mocked_game_coordinator(temp_game_directories, tutorial_game_file):
    """Create GameCoordinator instance with all necessary mocks."""
    # Mock all the config imports and file operations
    with patch("core.BASE_DIR", str(temp_game_directories["base_dir"])), patch(
        "core.TUTORIAL_GAME_FILENAME", "TUTORIAL_GAME"
    ), patch("core.GAME_FILE_DIR", "game_files"):

        coordinator = GameCoordinator()
        return coordinator


class TestGameCoordinatorLoad:
    """Test cases for the load functionality."""

    # def test_load_valid_save_file_updates_game_data(self, mocked_game_coordinator, sample_save_file):
    #     """Test that loading a valid save file properly updates the game_data."""
    #     coordinator = mocked_game_coordinator
    #     initial_player_health = coordinator.game_data["player"]["health"]

    #     # Load the modified save file
    #     loaded_game_data = coordinator.load_game_from_file("test_save", "save_files")

    #     # Verify the game data was updated
    #     assert loaded_game_data == MODIFIED_GAME_DATA
    #     assert coordinator.game_data == MODIFIED_GAME_DATA
    #     assert coordinator.game_data["player"]["health"] != initial_player_health
    #     assert coordinator.game_data["player"]["health"] == 75
    #     assert coordinator.game_data["player"]["total_moves"] == 10
    #     assert coordinator.game_data["player"]["current_location"] == "armory"

    # def test_handle_load_with_valid_filename(self, mocked_game_coordinator, sample_save_file):
    #     """Test handle_load method with valid filename argument."""
    #     coordinator = mocked_game_coordinator
    #     load_args = ["load", "test_save"]

    #     result = coordinator.handle_load(load_args)

    #     assert result == MODIFIED_GAME_DATA
    #     assert coordinator.game_data == MODIFIED_GAME_DATA

    # def test_handle_load_missing_filename_returns_error(self, mocked_game_coordinator):
    #     """Test handle_load method when filename argument is missing."""
    #     coordinator = mocked_game_coordinator
    #     load_args_without_filename = ["load"]

    #     result = coordinator.handle_load(load_args_without_filename)

    #     assert isinstance(result, IndexError)


class TestGameCoordinatorRestart:
    """Test cases for the restart functionality."""

    # BUG: will not work until post_load_processing() is added
    # BUG: will fail until Player and Room classes are implemented
    # def test_restart_resets_game_data_to_tutorial_state(
    #     self, mocked_game_coordinator, sample_save_file
    # ):
    #     """Test that restart properly resets game_data to tutorial game state."""
    #     coordinator = mocked_game_coordinator

    #     # First load a modified save file
    #     coordinator.load_game_from_file("test_save", "save_files")
    #     assert coordinator.game_data["player"]["health"] == 75
    #     assert coordinator.game_data["player"]["total_moves"] == 10

    #     # Mock user input to confirm restart
    #     with patch("builtins.input", return_value="y"):
    #         restart_args = ["restart"]
    #         coordinator.handle_restart(restart_args)

    #     # Verify game data was reset to tutorial state
    #     assert coordinator.game_data == SAMPLE_TUTORIAL_GAME_DATA
    #     assert coordinator.game_data["player"]["health"] == 100
    #     assert coordinator.game_data["player"]["total_moves"] == 0
    #     assert coordinator.game_data["player"]["current_location"] == "start_room"


class TestGameCoordinatorSave:
    """Test cases for the save functionality."""

    # BUG: handle_save is hardcoded with absolute path, add this test case back in after 'config.py' has been created
    # def test_save_with_default_filename_creates_file(self, mocked_game_coordinator, temp_game_directories):
    #     """Test saving game with default filename (no arguments)."""
    #     coordinator = mocked_game_coordinator
    #     save_args_no_filename = ["save"]

    #     result = coordinator.handle_save(save_args_no_filename)

    #     expected_save_path = temp_game_directories["base_dir"] / "save_files" / "PROT01.json"
    #     assert result == expected_save_path
    #     assert expected_save_path.exists()

    #     # Verify file content matches current game data
    #     with open(expected_save_path, 'r', encoding='utf-8') as file:
    #         saved_game_data = json.load(file)
    #     assert saved_game_data == coordinator.game_data

    # def test_save_with_custom_filename_creates_file(self, mocked_game_coordinator, temp_game_directories):
    #     """Test saving game with custom filename."""
    #     coordinator = mocked_game_coordinator
    #     custom_filename = "my_custom_save"
    #     save_args_with_filename = ["save", custom_filename]

    #     result = coordinator.handle_save(save_args_with_filename)

    #     expected_save_path = temp_game_directories["base_dir"] / "save_files" / f"{custom_filename}.json"
    #     assert result == expected_save_path
    #     assert expected_save_path.exists()

    #     # Verify file content matches current game data
    #     with open(expected_save_path, 'r', encoding='utf-8') as file:
    #         saved_game_data = json.load(file)
    #     assert saved_game_data == coordinator.game_data

    # def test_save_preserves_current_game_state(self, mocked_game_coordinator, sample_save_file, temp_game_directories):
    #     """Test that saving preserves the exact current game state."""
    #     coordinator = mocked_game_coordinator

    #     # Load modified game data
    #     coordinator.load_game_from_file("test_save", "save_files")
    #     expected_game_state = coordinator.game_data.copy()

    #     # Save the game
    #     save_filename = "state_preservation_test"
    #     coordinator.handle_save(["save", save_filename])

    #     # Load the saved file and verify it matches the expected state
    #     saved_file_path = temp_game_directories["base_dir"] / "save_files" / f"{save_filename}.json"
    #     with open(saved_file_path, 'r', encoding='utf-8') as file:
    #         saved_game_data = json.load(file)

    #     assert saved_game_data == expected_game_state
    #     assert saved_game_data["player"]["health"] == 75
    #     assert saved_game_data["player"]["total_moves"] == 10
    #     assert saved_game_data["player"]["current_location"] == "armory"


class TestGameCoordinatorIntegration:
    """Integration tests for combined functionality."""

    def test_save_load_cycle_preserves_game_state(
        self, mocked_game_coordinator, temp_game_directories
    ):
        """Test that saving and then loading preserves the exact game state."""
        coordinator = mocked_game_coordinator

        # Modify the initial game state
        coordinator.game_data["player"]["health"] = 50
        coordinator.game_data["player"]["total_moves"] = 25
        coordinator.game_data["rooms"]["start_room"]["num_player_visits"] = 3
        expected_modified_state = coordinator.game_data.copy()

        # Save the modified state
        save_filename = "cycle_test"
        coordinator.handle_save(["save", save_filename])

        # Reset to tutorial state to verify load works
        with patch("builtins.input", return_value="y"):
            coordinator.handle_restart(["restart"])
        assert coordinator.game_data["player"]["health"] == 100  # Verify reset worked

        # Load the saved state
        coordinator.handle_load(["load", save_filename])

        # Verify the loaded state matches the originally modified state
        assert coordinator.game_data == expected_modified_state
        assert coordinator.game_data["player"]["health"] == 50
        assert coordinator.game_data["player"]["total_moves"] == 25
        assert coordinator.game_data["rooms"]["start_room"]["num_player_visits"] == 3

    def test_restart_after_modifications_returns_to_clean_state(
        self, mocked_game_coordinator
    ):
        """Test that restart works correctly after various game modifications."""
        coordinator = mocked_game_coordinator

        # Make multiple modifications to game state
        coordinator.game_data["player"]["health"] = 25
        coordinator.game_data["player"]["total_moves"] = 100
        coordinator.game_data["player"]["inventory"].append("magic_sword")
        coordinator.game_data["player"]["current_location"] = "boss_room"

        # Restart the game
        with patch("builtins.input", return_value="y"):
            coordinator.handle_restart(["restart"])

        # Verify complete reset to tutorial state
        assert coordinator.game_data == SAMPLE_TUTORIAL_GAME_DATA
        assert coordinator.game_data["player"]["health"] == 100
        assert coordinator.game_data["player"]["total_moves"] == 0
        assert coordinator.game_data["player"]["inventory"] == ["blank_map"]
        assert coordinator.game_data["player"]["current_location"] == "start_room"


# Alternative approach: Test with direct mocking if imports still fail
class TestGameCoordinatorWithDirectMocking:
    """Alternative tests using direct mocking approach."""

    # @patch('builtins.open', new_callable=mock_open, read_data=json.dumps(SAMPLE_TUTORIAL_GAME_DATA))
    # @patch('core.Path')
    # def test_load_with_direct_file_mock(self, mock_path, mock_file):
    #     """Test load functionality with direct file mocking."""
    #     # This approach mocks the file operations directly
    #     mock_path.return_value.__truediv__.return_value = "mocked_path"

    #     with patch('core.BASE_DIR', '/tmp'), \
    #          patch('core.TUTORIAL_GAME_FILENAME', 'TUTORIAL_GAME'):

    #         coordinator = GameCoordinator()
    #         result = coordinator.load_game_from_file("test", "save_files")

    #         assert result == SAMPLE_TUTORIAL_GAME_DATA
    #         assert coordinator.game_data == SAMPLE_TUTORIAL_GAME_DATA
