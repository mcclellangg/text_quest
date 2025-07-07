"""
Core components for running the game.
- GameCoordinator
"""

from config import BASE_DIR, GAME_FILE_DIR, TUTORIAL_GAME_FILENAME
from copy import deepcopy
from entities import Item, Player, Room
import json
import logging
from pathlib import Path
import sys
from typing import List


PROMPT = "> "


class GameCoordinator:
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.game_data = (
            self.load_game_from_file(filename=TUTORIAL_GAME_FILENAME, dir="game_files")
            or {}
        )
        # Game State
        self.player = Player.from_dict(self.game_data["player"])
        self.current_room = Room.from_dict(self.game_data["rooms"]["start_room"])
        self.item_map = self.load_game_items()

        self.logger.info("GameCoordinator initialized.")

    # CommandProcessor
    def get_args_from_user(self) -> List[str]:
        """Expects user to pass two cmds separated by a space and returns a list."""
        return input(PROMPT).split(" ")

    def validate_args(self, args: List[str]) -> bool:
        """Ensures args are not blank or greater than expected length.
        NOTE: Onus is on user to pass valid args only.
        """
        if len(args) == 0 or args == [""]:
            print(f"Blank command, please enter a valid command")
            return False
        elif args[0] == "q":
            print("Exiting game ...")
            sys.exit()
        elif len(args) > 2:
            print(f"Functionality not yet implemented, please enter 1 or 2 args.")
            return False
        else:
            return True

    def process_args(self, args):
        """Routes args to handler based on args[0] via dispatch table."""
        arg_to_function = {
            "save": self.handle_save,
            "load": self.handle_load,
            "restart": self.handle_restart,
            "look": self.handle_look,
            "take": self.handle_take,
            # "move": self.handle_move_cmd,
            # "stats": self.display_player_stats
        }

        try:
            func_to_call = arg_to_function[args[0]]
            return func_to_call(args)
        except KeyError as e:
            self.logger.error(f"Invalid cmd ERROR: {args[0], {e}}")
            return e

    # arg handlers
    def handle_load(self, args):
        try:
            filename = args[1]
            return self.load_game_from_file(filename=filename, dir="save_files")
        except IndexError as e:
            self.logger.error(
                print(f"Invalid cmd ERROR: Please provide filename to load")
            )
            return e

    def load_game_from_file(self, filename: str, dir: str = "save_files"):
        """Updates state of current game from filename and directory provided."""
        load_file_path = Path(BASE_DIR) / dir / f"{filename}.json"

        try:
            with open(load_file_path, mode="r", encoding="utf-8") as f:
                game_data = json.load(f)
                self.game_data = game_data
                self.logger.info(f"Game loaded: {filename}\n")
                # print(f"Game loaded: {filename}\n")
                self.post_load_game_file_processing()
                return game_data
        except Exception as e:
            print(f"ERROR: {e}")
            return e

    def load_game_items(self):
        game_items = deepcopy(self.game_data["items"])
        return {
            item_id: Item.from_dict(item_dict)
            for item_id, item_dict in game_items.items()
        }

    def post_load_game_file_processing(self):
        "Update game state (item_map, player, current_room), and display current room"
        self.player = Player.from_dict(self.game_data["player"])
        current_room_id = self.player.get_current_location()
        self.current_room = Room.from_dict(self.game_data["rooms"][current_room_id])
        self.item_map = self.load_game_items()
        self.current_room.display_room()

    def handle_restart(self, args):
        get_user_validation = input(
            "WARNING: Unsaved progress will be lost, Are you sure you want to RESTART? (y/n): "
        )

        if get_user_validation in ["y", "Y", "yes", "YES"]:
            self.game_data = self.load_game_from_file(
                filename=TUTORIAL_GAME_FILENAME, dir="game_files"
            )
            self.logger.info("Game restarted")
            # print("Game restarted")
        else:
            print("Very well, continue on ...")

    def handle_save(self, args):
        if len(args) > 1:
            return self.save_game_to_file(filename=args[1])
        else:
            return self.save_game_to_file()

    def save_game_to_file(
        self, filename: str = "PROT01", dir: str = "save_files"
    ) -> str:
        file_path = Path(BASE_DIR) / dir / f"{filename}.json"

        try:
            with open(file_path, mode="w", encoding="utf-8") as f:
                json.dump(self.game_data, f, indent=4, sort_keys=True)
                self.logger.info(f"Game save: {file_path}")
                return file_path
        except Exception as e:
            self.logger.error(f"Save game error: {file_path}, {e}")
            return e

    # handle player cmds
    def handle_look(self, args):
        # validate
        if len(args) == 1:
            print(self.current_room.get_base_description())
        elif len(args) == 2:
            target = args[1]
            self.generate_description(target=target)
        else:
            self.logger.error(f"ERROR-Unexpected args passed: {args}")

    def generate_description(self, target):
        """Handles basic descriptions for items.
        NOTE: anything you know exists can be 'looked' for.
        """
        if target in self.item_map:
            print(self.item_map[target].get_description())
        else:
            self.logger.info(
                "Only 'item' objects are currently supported, please try again."
            )

    def handle_take(self, args):
        if len(args) == 1:
            print(
                "Take what? Me out, on me, to the ball game? None of which will work mind you."
            )
        elif len(args) == 2:
            target = args[1]
            # if valid target perform take actions and update game state
            print(f"execute take cmds for {target}")
        else:
            self.logger.error(f"ERROR-Unexpected args passed: {args}")

    # Run game
    def run_game(self):
        while True:
            args = self.get_args_from_user()
            if self.validate_args(args=args):
                self.process_args(args=args)
            else:
                self.logger.error("Invalid cmd, try again.")
