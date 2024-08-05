from .registration import registration_router
from .add_note import add_notes_router
from .my_notes import get_notes_route


all_routers = [registration_router, get_notes_route, add_notes_router]
