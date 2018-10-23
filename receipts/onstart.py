from .processors.pickup import start_pickup


def on_startup():
    start_pickup()

