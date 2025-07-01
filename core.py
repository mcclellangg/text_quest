"""
Core components for running the game.
- GameCoordinator
"""

from config import BASE_DIR, GAME_FILE_DIR, TUTORIAL_GAME_FILENAME
import json
import logging
from pathlib import Path


PROMPT = "> "


class GameCoordinator:
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.game_data = (
            self.load_game_from_file(filename=TUTORIAL_GAME_FILENAME, dir="game_files")
            or {}
        )
        self.logger.info("GameCoordinator initialized.")

    def load_game_from_file(self, filename: str, dir: str = "save_files"):
        """Updates state of current game from filename and directory provided."""
        load_file_path = Path(BASE_DIR) / dir / f"{filename}.json"

        try:
            with open(load_file_path, mode="r", encoding="utf-8") as f:
                game_data = json.load(f)
                self.game_data = game_data
                print(f"Game loaded: {filename}\n")
                self.post_load_game_file_processing()
                return game_data
        except Exception as e:
            print(f"ERROR: {e}")
            return e

    def post_load_game_file_processing(self):
        pass

    def run_game(self):
        print(self.game_data["rooms"])
