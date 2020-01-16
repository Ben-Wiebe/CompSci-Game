from math       import *
from random     import *
from settings   import *
from classes    import *
import caves
import pygame

# Determines the nearest value of a number from a list
def closestValue(lst, val): return min(range(len(lst)), key=lambda i : abs(lst[i]-val))

# Determines the nearest dictionary key to find a number
def closestKey(dictionary, val): return dictionary.get(val, dictionary[min(dictionary.keys(), key=lambda k: abs(k-val))])

# Determines the angle between 2 points
def getAngle(x1, y1, x2, y2):
    return atan2((y2 - y1), (x2 - x1))

# Creates the background for the loading screen using cellular automata
def loadingBackground():
    totalGenerations = []
    gen=''.join('01'[c in (38,39)]for c in range(RESOLUTION[0] // TILE_WIDTH))
    for r in gen: totalGenerations.append(list(gen)); gen=''.join('10'[gen[c-1:c+2] in ('111','000','100','01','01')] for c in range(RESOLUTION[0] // TILE_WIDTH))
    background = pygame.Surface((RESOLUTION[0], RESOLUTION[1]))
    for j, column in enumerate(totalGenerations):
        for k, row in enumerate(column):
            if int(row) == 1:   c = GREY
            else:               c = BROWN
            pygame.draw.rect(background, c, (j * TILE_WIDTH, k * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT))
    return background\

def getControls():
    def write(text, pos, fontSize=20):
        w.blit(pygame.font.SysFont("monospace", fontSize).render(str(text), False, WHITE),(pos[0], pos[1]))

    w = pygame.Surface((HALF_RES[0], HALF_RES[1]))
    w.fill(BLACK)

    write("CONTROLS:", (10, 10), fontSize=35)
    write("- X -       Toggle Minimap Display", (10, 40))
    write("- Y -       Toggle Weapon Pickup/Display", (10, 65))
    write("- B -       Pick Up Nearest Item", (10, 90))
    write("- Right Trigger/ZR -    Shoot Towards Cursor", (10, 115))
    write("- Left Trigger/ZL -     Move Cursor", (10, 140))
    write("- A -       Toggle Control Display", (10, 165))

    return w

def blitRotate(image, pos, angle):

    # calcaulate the axis aligned bounding box of the rotated image
    w, h       = image.get_size()
    originPos  = (w/2, h/2)
    box        = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]
    min_box    = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
    max_box    = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

    # calculate the translation of the pivot 
    pivot        = pygame.math.Vector2(originPos[0], -originPos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move   = pivot_rotate - pivot

    # calculate the upper left origin of the rotated image
    origin = (pos[0] - originPos[0] + min_box[0] - pivot_move[0], pos[1] - originPos[1] - max_box[1] + pivot_move[1])

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)

    # rotate and blit the image
    return rotated_image, origin
    
# Moves all bullets and checks if they collide with walls and players/enemies/bosses
def updateBullets(grid, bullets, players):
    def entityCollision(bullet, x, y):
        # Collision with players/enemies/bosses
        for player in players:
            hitbox = pygame.Rect((player.x * TILE_WIDTH, player.y * TILE_HEIGHT, player.w * TILE_WIDTH, player.h * TILE_HEIGHT))
            if hitbox.colliderect(((x - bullet.r) * TILE_WIDTH, (y - bullet.r) * TILE_HEIGHT, bullet.r * 2 * TILE_WIDTH, bullet.r * 2 * TILE_HEIGHT)) \
                and (bullet.team != player.team) and ((bullet.worldX, bullet.worldY) == (player.worldX, player.worldY)):
                player.health -= bullet.dmg
                player.health = min(player.health, player.maxHealth)
                return True
            
        for enemy in grid[bullet.worldX][bullet.worldY].enemies:
            hitbox = pygame.Rect((enemy.x * TILE_WIDTH, enemy.y * TILE_HEIGHT, enemy.w * TILE_WIDTH, enemy.h * TILE_HEIGHT))
            if hitbox.colliderect(((x - bullet.r) * TILE_WIDTH, (y - bullet.r) * TILE_HEIGHT, bullet.r * 2 * TILE_WIDTH, bullet.r * 2 * TILE_HEIGHT)) \
                and (bullet.team != enemy.team) and ((bullet.worldX, bullet.worldY) == (enemy.worldX, enemy.worldY)):
                enemy.health -= bullet.dmg
                return True

        for boss in grid[bullet.worldX][bullet.worldY].boss:
            hitbox = pygame.Rect((boss.x * TILE_WIDTH, boss.y * TILE_HEIGHT, boss.w * TILE_WIDTH, boss.h * TILE_HEIGHT))
            if hitbox.colliderect(((x - bullet.r) * TILE_WIDTH, (y - bullet.r) * TILE_HEIGHT, bullet.r * 2 * TILE_WIDTH, bullet.r * 2 * TILE_HEIGHT)) \
                and (bullet.team != boss.team) and ((bullet.worldX, bullet.worldY) == (boss.worldX, boss.worldY)):
                boss.health -= bullet.dmg
                return True

    # Collision with walls
    for bullet in bullets:
        area    = grid[bullet.worldX][bullet.worldY].collisionMap
        checks  = 2
        moveX   = bullet.dx * (bullet.speed / checks)
        moveY   = bullet.dy * (bullet.speed / checks)
        for i in range(checks):
            movedX = bullet.x + moveX
            movedY = bullet.y + moveY
            if entityCollision(bullet, movedX, movedY): bullets.remove(bullet); break
            elif int(movedX) > len(area) - 1 or int(movedY) > len(area[0]) - 1 or int(movedX) < 0 or int(movedY) < 0:
                bullets.remove(bullet); break
            elif bullet.age > bullet.range: bullets.remove(bullet); break
            elif bullet.bounces > bullet.maxBounces: bullets.remove(bullet); break
            if area[int(movedX)][int(bullet.y)] != 1:   bullet.x = movedX
            else:                                       bullet.collide('y'); break
            if area[int(bullet.x)][int(movedY)] != 1:   bullet.y = movedY
            else:                                       bullet.collide('x'); break
        bullet.age += 1

# Generates caves for each tile in the maze
def initializeRooms(grid):
    w = [x[:] for x in grid]
    for i, y in enumerate(grid):
        for j, x in enumerate(y):
            if x != 0 and x != 1:
                directions = []
                for k, l, direction in [(-1, 0, "LEFT"), (1, 0, "RIGHT"), (0, 1, "DOWN"), (0, -1, "UP")]:
                    if grid[i + k][j + l] == 0:
                        directions.append(direction)
                w[i][j] = Room(closestKey(DIFFICULTY_KEY, x), caves.generate(41, 24, directions), i, j)
    m = Minimap(w)
    # The tile in the very bottom right is where the boss spawns
    w[len(w)-2][len(w[0])-2].tileMap, w[len(w)-2][len(w[0])-2].collisionMap = map1, map1c
    w[len(w)-2][len(w[0])-2].boss = [Hastur(5, 5, len(w)-2, len(w[0])-2, 8, 8, 5000, 0.05, 30, 50)]
    w[len(w)-2][len(w[0])-2].enemies = []
    return w, m
