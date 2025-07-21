from ninja import Schema

from players.schemas import PlayerOut


class StandingOut(Schema):
    player: PlayerOut
    matches_won: int
    matches_tied: int
    games_won: int
    games_tied: int
    opponents_match_winrate: float
    opponents_game_winrate: float
    points: int
