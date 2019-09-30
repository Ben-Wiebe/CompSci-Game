import pygame
pygame.init()

TILE_SIZE   = 12
WIDTH       = 60
HEIGHT      = 30

screen = pygame.display.set_mode(HALF_RES)

maps = []
tileID = []
currentMap = Map()

class Map:
    def __init__(self, w = WIDTH, h = HEIGHT):
        self.image      = pygame.Surface((TILE_SIZE * w, TILE_SIZE * h))
        self.tileMap    = [ [0 for x in range(h)] for y in range(w)]

    def update(self, WIDTH = WIDTH, HEIGHT = HEIGHT, TILE_SIZE = TILE_SIZE):
        self.image = pygame.Surface((TILE_SIZE * WIDTH, TILE_SIZE * HEIGHT))
        if 
        self.tileMap.append()

def draw(currMap):
    for j, column in enumerate():
        for k, row in enumerate(column):
            screen.blit()
