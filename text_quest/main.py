"""
The main game execution.
"""

from core import GameCoordinator
import logging
from logger_config import setup_logging


def main():
    setup_logging(log_level=logging.ERROR, log_file="logs/text_quest.log")
    game = GameCoordinator()
    game.run_game()


if __name__ == "__main__":
    main()
