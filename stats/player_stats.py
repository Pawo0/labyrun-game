"""
This module contains the PlayerStats class.
"""

from dataclasses import asdict, dataclass
from typing import Dict, List, Optional


@dataclass
class GameRecord:
    """Represents a single game record for a player."""

    timestamp: str  # ISO format date and time
    player_name: str
    opponent_name: str
    maze_width: int
    maze_height: int
    win: bool
    game_time: float  # seconds


@dataclass
class PlayerStats:
    """Stores and manages statistics for a single player."""

    player_name: str
    games_played: int = 0
    games_won: int = 0
    total_game_time: float = 0.0
    avg_game_time: float = 0.0
    fastest_win: Optional[float] = None
    game_history: List[Dict] = None

    def __post_init__(self):
        if self.game_history is None:
            self.game_history = []

    def add_game(self, record: GameRecord) -> None:
        """Add a game record to the player's history.

        Args:
            record (GameRecord): GameRecord object containing game data.
        """
        # Update overall stats
        self.games_played += 1
        if record.win:
            self.games_won += 1
            if self.fastest_win is None or record.game_time < self.fastest_win:
                self.fastest_win = record.game_time

        self.total_game_time += record.game_time
        self.avg_game_time = self.total_game_time / self.games_played

        # Add to history
        self.game_history.append(asdict(record))

    def to_dict(self) -> Dict:
        """Convert player stats to dictionary for serialization.

        Returns:
            Dict: Dictionary representation of player stats.
        """
        return asdict(self)
