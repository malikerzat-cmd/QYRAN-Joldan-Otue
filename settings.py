import os

WIDTH, HEIGHT = 600, 720
CELL = 60
COLS = 10
FPS = 60
ASSETS = os.path.join(os.path.dirname(__file__), "assets")

def asset_path(name):
    return os.path.join(ASSETS, name)
