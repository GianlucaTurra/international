from ninja import NinjaAPI
from players.api import router as players_router
import tournaments
from tournaments.api import router as tournaments_router

api = NinjaAPI()

api.add_router("/tournaments/", tournaments_router, tags=["tournaments"])
api.add_router("/players/", players_router, tags=["players"])
