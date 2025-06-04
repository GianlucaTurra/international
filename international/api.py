from ninja import NinjaAPI
from players.api import router as players_router
from tournaments.api import router as tournaments_router
from authentication.api import router as authentication_router
from ninja_jwt.routers.blacklist import blacklist_router
from ninja_jwt.routers.obtain import obtain_pair_router, sliding_router
from ninja_jwt.routers.verify import verify_router

api = NinjaAPI()

api.add_router("/tournaments/", tournaments_router, tags=["tournaments"])
api.add_router("/players/", players_router, tags=["players"])
# api.add_router("/authentication/", authentication_router, tags=["authentication"])
api.add_router("/token", obtain_pair_router, tags=["auth"])
api.add_router("/verify", verify_router, tags=["auth"])
api.add_router("/blacklist", blacklist_router, tags=["auth"])
