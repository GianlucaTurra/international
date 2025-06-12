from ninja import Schema

from players.schemas import PlayerOut


class StandingOut(Schema):
    player: PlayerOut
    matches_won: int
    games_won: int
    points: int
