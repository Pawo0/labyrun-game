"""
This module contains the StatsManager class.
"""

import json
import os
from datetime import datetime
from typing import Dict, Optional

from .player_stats import GameRecord, PlayerStats


class StatsManager:
    """This class manages player statistics and persists them to a JSON file."""

    def __init__(self, stats_file: str = "data/player_stats.json"):
        self.stats_file = stats_file
        self.players: Dict[str, PlayerStats] = {}
        self.game_start_time: Optional[float] = None

        # Load existing stats if file exists
        self._load_stats()

    def _load_stats(self) -> None:
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, "r", encoding="utf-8") as file:
                    data = json.load(file)

                for player_name, player_data in data.items():
                    # Create PlayerStats objects from loaded data
                    self.players[player_name] = PlayerStats(
                        player_name=player_name,
                        games_played=player_data.get("games_played", 0),
                        games_won=player_data.get("games_won", 0),
                        total_game_time=player_data.get("total_game_time", 0.0),
                        avg_game_time=player_data.get("avg_game_time", 0.0),
                        fastest_win=player_data.get("fastest_win"),
                        game_history=player_data.get("game_history", []),
                    )
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading stats: {str(e)}")
                # Create a new stats file if there was an error
                self.players = {}

    def save_stats(self) -> None:
        """Save all player stats to the JSON file."""
        data = {name: stats.to_dict() for name, stats in self.players.items()}

        try:
            os.makedirs(
                os.path.dirname(os.path.abspath(self.stats_file)), exist_ok=True
            )
            with open(self.stats_file, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
        except IOError as e:
            print(f"Error saving stats: {str(e)}")

    def get_player_stats(self, player_name: str) -> PlayerStats:
        """Get statistics for a specific player.

        Args:
            player_name (str): Name of the player

        Returns:
            PlayerStats: PlayerStats object for the player
        """
        if player_name not in self.players:
            self.players[player_name] = PlayerStats(player_name=player_name)
        return self.players[player_name]

    def start_game_timer(self) -> None:
        """Start the game timer when a game begins."""
        self.game_start_time = datetime.now().timestamp()

    def record_game_result(
        self, winner_name: str, loser_name: str, maze_width: int, maze_height: int
    ) -> None:
        """Record the result of a completed game.

        Args:
            winner_name (str): Name of the winning player
            loser_name (str): Name of the losing player
            maze_width (int): Width of the maze
            maze_height (int): Height of the maze
        """
        if self.game_start_time is None:
            print("Warning: Game timer was not started")
            game_time = 0.0
        else:
            game_time = datetime.now().timestamp() - self.game_start_time
            self.game_start_time = None  # Reset timer

        timestamp = datetime.now().isoformat()

        # Create game records
        winner_record = GameRecord(
            timestamp=timestamp,
            player_name=winner_name,
            opponent_name=loser_name,
            maze_width=maze_width,
            maze_height=maze_height,
            win=True,
            game_time=game_time,
        )

        loser_record = GameRecord(
            timestamp=timestamp,
            player_name=loser_name,
            opponent_name=winner_name,
            maze_width=maze_width,
            maze_height=maze_height,
            win=False,
            game_time=game_time,
        )

        # Get or create player stats objects
        winner_stats = self.get_player_stats(winner_name)
        loser_stats = self.get_player_stats(loser_name)

        # Update stats
        winner_stats.add_game(winner_record)
        loser_stats.add_game(loser_record)

        # Save to file
        self.save_stats()

    def get_leaderboard(self) -> list:
        """Get a sorted leaderboard of all players by win count.

        Returns:
            list: List of (player_name, wins, total_games) tuples
        """
        leaderboard = []
        for name, stats in self.players.items():
            leaderboard.append(
                {
                    "player_name": name,
                    "wins": stats.games_won,
                    "total_games": stats.games_played,
                    "win_rate": (
                        stats.games_won / stats.games_played
                        if stats.games_played > 0
                        else 0
                    ),
                    "avg_time": stats.avg_game_time,
                    "fastest_win": stats.fastest_win,
                }
            )

        # Sort by wins (descending), then by win rate (descending)
        return sorted(
            leaderboard,
            key=lambda x: (x["wins"], x["win_rate"] if x["total_games"] > 0 else 0),
            reverse=True,
        )
