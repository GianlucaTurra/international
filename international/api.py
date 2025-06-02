from ninja import NinjaAPI
from players.api import router as players_router
from tournaments.api import router as tournaments_router
from authentication.api import router as authentication_router

api = NinjaAPI()

api.add_router("/tournaments/", tournaments_router, tags=["tournaments"])
api.add_router("/players/", players_router, tags=["players"])
api.add_router("/authentication/", authentication_router, tags=["authentication"])
