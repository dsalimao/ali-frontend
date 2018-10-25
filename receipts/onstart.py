from .processors.pickup import start_pickup
from .processors.delete import delete_all

def on_startup():
    start_pickup()
    # delete_all()

