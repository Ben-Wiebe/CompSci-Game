import pygame
import sys
import os
from settings import *
pygame.init()

TILE_SIZE   = 35
WIDTH       = 32
HEIGHT      = 20

# DOWNLOAD ALL OF THE FILES THEN PUT THEM IN PROPER FOLDERS PLEASE CALEB PLEASE THIS IS VERY IMPORTANT

currentDifficulty = 1 # Make it so that you can change difficulty with buttons maybe? Right now it's only by pressing keys 1-6

screen  = pygame.display.set_mode(RESOLUTION, pygame.FULLSCREEN)

def updateTiles():
    t = [pygame.transform.scale(tile, (TILE_SIZE, TILE_SIZE)) for tile in tiles]
    return t

class Map:
    def __init__(self, w = WIDTH, h = HEIGHT):
        self.image          = pygame.Surface((TILE_SIZE * w, TILE_SIZE * h))
        self.tileMap        = [ [ 0 for x in range(h) ] for y in range(w) ]
        self.collisionMap   = [ [ 0 for x in range(h) ] for y in range(w) ]
        self.doors          = [False, False, False, False]

    def toggle(self, v):
        # Please tidy this up, I know there is a better way to do this but I can't think of the best way.
        if v == True: v = False
        elif v == False: v = True
        return v

class Tile:
    def __init__(self, image, tileType):
        self.image      = image
        self.tileType   = tileType

doorKey     = {0 : "UP", 1 : "DOWN", 2 : "LEFT", 3 : "RIGHT"}

tileIDs     = open("resources\TileIDs.txt", "r")
contents    = tileIDs.readlines()
tileIDs.close()
maps        = []
tiles       = []
for i in contents:
    # Separate the :(number) at the end of each tile name, as it is only needed for collision
    a = i.split(":")
    # Adds each tile to a class containing the resized tile along with the Tile's name then appends that to the list of all tiles
    tiles.append(Tile(pygame.transform.scale(pygame.image.load("resources\\" + a[0] + ".png").convert(), (TILE_SIZE, TILE_SIZE)), int(a[1][:-1])))

currentMap  = Map()

selected    = []
hold = True
borders     = False
# Arr, this be where the buttons be
tileSelection = [pygame.Rect((RESOLUTION[0] - 200, i * 15),(200, 15)) for i,c in enumerate(contents)]
doorSelection = [pygame.Rect((RESOLUTION[0] - 200, (i * 15) + 15 * (len(contents) + 2)),(200, 15)) for i,val in enumerate(currentMap.doors)]

def write(text, pos):
    screen.blit(pygame.font.SysFont("monospace", 12).render(str(text), True, WHITE), pos)

def draw(currMap, surface):
    screen.fill(BLACK)
    # You can look at my main program for a better way of doing the drawing to make it run better. Or don't. 
    for j, column in enumerate(currMap.tileMap):
        for k, row in enumerate(column):
            surface.blit(tiles[row].image, (j * TILE_SIZE, k * TILE_SIZE))
            if borders:
                pygame.draw.rect(screen, BLACK, (j * TILE_SIZE, k * TILE_SIZE, TILE_SIZE, TILE_SIZE), 2)

            for i in selected:
                pygame.draw.rect(screen, WHITE, (i[0] * TILE_SIZE, i[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE), 2)

    pygame.draw.rect(screen, GREY, (RESOLUTION[0] - 200, 0, 200, RESOLUTION[1]))
    # All tiles for selection
    for rect in tileSelection:
        pygame.draw.rect(screen, BLACK, rect, 1)
    for i,val in enumerate(contents):
        write(val[:-3], (RESOLUTION[0] - 195, i * 15))
    # All door directions for selection
    for rect in doorSelection:
        pygame.draw.rect(screen, BLACK, rect, 1)
    for i,val in enumerate(currentMap.doors):
        write("{}: {}".format(doorKey[i], val), (RESOLUTION[0] - 195, (i * 15) + (15 * (len(contents) + 2))))# + 15 * (len(contents) + 2)))

    # The write function thing below tells you what difficulty is on right now, all you need is an x/y position inside of the second brackets
    #write("Current Difficulty: {}".format(currentDifficulty), ())
    pygame.display.update()

def saveImage():
    # Up to the next bunch of hashtags is unnecessary, comment it out probably. All we need to save are the 2 text files.
    draw(currentMap, currentMap.image)
    pygame.image.save(currentMap.image, "resources\maps\{}".format(str(currentDifficulty))\
                      + "\{}.png".format("".join([doorKey[i] if currentMap.doors[i] else "" for i,status in enumerate(currentMap.doors)])))
    # # #
    # This bit opens the file based on your current difficulty, which you should make changeable
    tileMaps = open("resources\maps\{}.txt".format(str(currentDifficulty)), "a")
    # This writes the tilemap values, make it also write into a separate file the collision values as stored in map.collisionMap
    for i, row in enumerate(currentMap.collisionMap):
        tileMaps.write("".join([str(i) for i in row]) + "\n")
    # Prints the separator value, don't change this or you die irl
    tileMaps.write("@\n")
    tileIDs.close()

while True:
    # I mean... this is just for the buttons. Change stuff if you want, but it shouldn't matter
    events = pygame.event.get() 
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if event.button == 1:
                if pos[0] >= 0 and pos[0] < len(currentMap.tileMap) * TILE_SIZE and pos[0] >= 0 and pos[1] < len(currentMap.tileMap[0]) * TILE_SIZE:
                    s = (pos[0] // TILE_SIZE, pos[1] // TILE_SIZE)
                    # If you're holding down the shift key as you are clicking on boxes it will add to the selected list instead of replacing all the values with one
                    if not pygame.key.get_mods() & pygame.KMOD_SHIFT: selected = []
                    if not s in selected: selected.append(s)
                    else: selected.remove(s)

                else:
                    for i,rect in enumerate(tileSelection):
                        if rect.collidepoint(pos):
                            for n in selected:
                                currentMap.tileMap[n[0]][n[1]] = i
                                currentMap.collisionMap[n[0]][n[1]] = tiles[i].tileType
                            
                    for i,rect in enumerate(doorSelection):
                        if rect.collidepoint(pos):
                            currentMap.doors[i] = currentMap.toggle(currentMap.doors[i])

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                if borders: borders = False
                else: borders = True

            elif event.key == pygame.K_s:
                saveImage()

            elif event.key == pygame.K_1: currentDifficulty = 1
            elif event.key == pygame.K_2: currentDifficulty = 2
            elif event.key == pygame.K_3: currentDifficulty = 3
            elif event.key == pygame.K_4: currentDifficulty = 4
            elif event.key == pygame.K_5: currentDifficulty = 5
            elif event.key == pygame.K_6: currentDifficulty = 6

            elif event.key == pygame.K_j:
                print(currentMap.collisionMap)

    draw(currentMap, screen)
