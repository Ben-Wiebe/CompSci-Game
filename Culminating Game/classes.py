from math import pi, sin, cos, atan2
from settings import *
import pygame
pygame.init()
    
class Player:
    def __init__(self, x, y, team, maxHealth, worldX = 1, worldY = 1):
        self.x              = x
        self.y              = y
        self.worldX         = worldX
        self.worldY         = worldY
        self.team           = team
        self.health         = maxHealth
        self.maxHealth      = maxHealth
        self.w              = 1.5
        self.h              = 1.5
        self.ms             = 0.12
        self.slow           = 1
        self.shotCooldown   = 0
        self.attackFrames   = 0
        self.attacking      = False
        self.weapon         = None
        self.computer       = True
        self.d              = [0, 0, 0, 0]
        self.screen         = None
        self.direction      = "DOWN"
        self.display        = False
        self.moveCount      = 0
        self.spec           = {"lifesteal" : 0, "missingHpHeal" : 0, "revive" : False, "currentHealthDmg" : 0, "missingHpDmg" : 0, "playerHpBonus" : 0}
        
        self.images         = { "UP"    : [pygame.transform.scale(pygame.image.load(r"resources\player\up{}".format(i) + ".png"),
                                                                  (int(TILE_WIDTH * self.w), int(TILE_HEIGHT * self.h))) for i in range(1,3)] ,
                                "DOWN"  : [pygame.transform.scale(pygame.image.load(r"resources\player\down{}".format(i) + ".png"),
                                                                  (int(TILE_WIDTH * self.w), int(TILE_HEIGHT * self.h))) for i in range(1,3)] ,
                                "RIGHT" : [pygame.transform.scale(pygame.image.load(r"resources\player\right{}".format(i) + ".png"),
                                                                  (int(TILE_WIDTH * self.w), int(TILE_HEIGHT * self.h))) for i in range(1,5)] ,
                                "LEFT"  : [pygame.transform.scale(pygame.image.load(r"resources\player\left{}".format(i) + ".png"),
                                                                  (int(TILE_WIDTH * self.w), int(TILE_HEIGHT * self.h))) for i in range(1,5)] }

    def onHit(self, enemy, bullet):
        # Lifesteal
        self.health += bullet.dmg * (self.spec["lifesteal"] / 100)
        if self.health > self.maxHealth: self.health = self.maxHealth
        # More lifesteal the lower you are
        if self.health < self.maxHealth / 2: self.health += (self.maxHealth - self.health) * (self.spec["missingHpHeal"] / 100) * (bullet.dmg / 15)
        # More damage the higher health they are
        enemy.health -= enemy.health * (self.spec["currentHealthDmg"] / 100)
        # More damage the lower they are
        enemy.health -= (enemy.maxHealth - enemy.health) * (self.spec["missingHpDmg"] / 100)
        # More damage the more health you are
        enemy.health -= (self.maxHealth - self.health) * (self.spec["playerHpBonus"] / 100)

    def onDeath(self):
        if self.spec["revive"]:
            self.health = self.maxHealth / 2
            self.spec["revive"] = False
            return True

    def toggleDisplay(self):
        if self.display == True:    self.display = False
        else:                       self.display = True

class Enemy:
    def __init__(self, x, y, worldX, worldY, maxHealth, ms, armour, damage):
        self.x = x; self.worldX = worldX
        self.y = y; self.worldY = worldY
        self.attacking = False
        self.direction = "RIGHT"
        self.attackCount = 0
        self.ms = 0.05
        self.w = 2
        self.h = 2
        self.health = maxHealth
        self.maxHealth = maxHealth
        self.damage = damage
        self.slow = 1
        self.team = 10
        self.moveCount = 0

class Voidling(Enemy):
    images      = { "RIGHT" : [pygame.transform.scale(pygame.image.load(r"resources\enemies\voidling\right{}".format(i) + ".png"),
                                                      (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,4)] ,
                    "LEFT"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\voidling\left{}".format(i) + ".png"),
                                                      (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,4)] }
    
    attackingImages = { "RIGHT" : [pygame.transform.scale(pygame.image.load(r"resources\enemies\voidling\attackright{}".format(i) + ".png"),
                                                          (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,7)] ,
                        "LEFT"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\voidling\attackleft{}".format(i) + ".png"),
                                                          (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,7)] }
  
    def AI(self, grid, bullets, players):
        targeted = False
        for p in players:
            if not targeted and not self.attacking:
                if (p.worldX, p.worldY) == (self.worldX, self.worldY):
                    targeted = True
                    self.moveCount += 0.1
                    angle = atan2((self.y - p.y), (self.x - p.x))

                    if ((self.x - p.x) ** 2) + ((self.y - p.y) ** 2) > 3:
                        if p.y < self.y:
                            if not grid.collisionMap[int((self.y + (self.h / 2)) - (self.h / 2))][int(self.x + (self.w / 2))]:
                                self.y -= self.ms * self.slow
                                
                        elif p.y > self.y:
                            if not grid.collisionMap[int((self.y + (self.h / 2)) + (self.h / 2))][int(self.x + (self.w / 2))]:
                                self.y += self.ms * self.slow

                        if p.x < self.x:
                            self.direction = "LEFT"
                            if not grid.collisionMap[int(self.y + (self.h / 2))][int((self.x + (self.w / 2)) - (self.w / 2))]:
                                self.x -= self.ms * self.slow

                        elif p.x > self.x:
                            self.direction = "RIGHT"
                            if not grid.collisionMap[int(self.y + (self.h / 2))][int((self.x + (self.w / 2)) + (self.w / 2))]:
                                self.x += self.ms * self.slow
                    else:
                        self.attacking = True; self.attackCount = 0

        if self.attacking:
            self.attackCount += 0.5
            if self.attackCount >= 6:
                hitbox = pygame.Rect(((self.x + (self.w * DIRECTION_KEY[self.direction][0])) * TILE_WIDTH, (self.y + (self.h * DIRECTION_KEY[self.direction][1])) * TILE_HEIGHT),
                                     (self.w * TILE_WIDTH, self.h * TILE_HEIGHT))
                for p in players:
                    if hitbox.colliderect((p.x * TILE_WIDTH, p.y * TILE_HEIGHT, p.w * TILE_HEIGHT, p.h * TILE_WIDTH)):
                        p.health -= self.damage
                self.attacking = False
            
class Bullet:
    def __init__(self, pos, worldPos, dmg, a, t, speed, bulletRange, maxBounces, r):
        self.x, self.y      = pos
        self.worldX, self.worldY                        = worldPos
        self.dmg            = dmg;          self.speed      = speed
        self.angle          = a
        self.dx, self.dy    = cos(self.angle), sin(self.angle)
        self.team           = t
        self.r              = r
        self.age            = 0
        self.range          = bulletRange
        self.bounces        = 0;            self.maxBounces = maxBounces

    def collide(self, axis):
        if axis == "x":
            self.angle = -self.angle
            self.dx, self.dy    = cos(self.angle), sin(self.angle)
        if axis == "y":
            self.angle = -(pi + self.angle)
            self.dx, self.dy    = cos(self.angle), sin(self.angle)
        self.bounces += 1

class Weapon:
    def __init__(self, weapon, wType):
        self.w      = weapon
        self.wType  = wType

class Gun:
    def __init__(self, shots, name, rarity, speed, bulletRange, maxBounces, atkSpeed, deviation, dmg, r, slow, fireType, pos=(1, 1), state=1):
        self.shots      = shots
        self.name       = name
        self.rarity     = rarity
        self.speed      = speed
        self.range      = bulletRange
        self.maxBounces = maxBounces
        self.atkSpeed   = atkSpeed
        self.deviation  = deviation
        self.bulletDmg  = dmg
        self.fireType   = fireType
        self.r          = r
        self.slow       = slow
        self.pos        = pos
        self.state      = state
        self.rect           = (0.8,0.8)
        self.window     = self.initWindow()

    def initWindow(self):
        def write(text, pos):
            w.blit(pygame.font.SysFont('monospace', 9).render(str(text), False, RARITIES[self.rarity]),(pos[0], pos[1]))
        w = pygame.Surface((201, 120), pygame.SRCALPHA)
        w.fill(BLACKA)
        pygame.draw.rect(w, BLACK, (0, 0, 201, 120), 1)
        #w.set_alpha(100)
        
        write(self.name, (10, 10))
        write("Damage: {} (+{})".format(self.bulletDmg, round((self.bulletDmg * RARITY_SCALING[self.rarity]) - self.bulletDmg, 2)), (10, 25))
        write("Attacks per Second: {} (+{})".format(FPS_CAP / max(0.1, self.atkSpeed), FPS_CAP), (10, 40))
        write("Deviation: + or - {} Degrees".format(self.deviation), (10, 55))
        write("Weapon Type: {}".format(self.fireType), (10, 70))
        write("Bullet Size: {}".format(self.r), (10, 85))

        return w
    
tileIDs     = open("resources\TileIDs.txt", "r")
contents    = tileIDs.readlines()
tileIDs.close()
tiles       = []
for i in contents:
    # Takes out the :(number) at the end of each tile name, as it is only needed for collision
    a = i.split(":")
    # Adds each tile to a class containing the resized tile along with the Tile's name then appends that to the list of all tiles
    tiles.append((pygame.transform.scale(pygame.image.load("resources\\" + a[0] + ".png"), (TILE_WIDTH, TILE_HEIGHT)), int(a[1][:-1])))

def getTiles():
    return tiles

class Melee:
    def __init__(self):
        #self.w, self.h      = d
        self.atkSpeed       = 1
        self.image          = None
        self.rect           = (0.8, 0.8)#[(15, 15),(15, 15),(15, 15),(15, 15),(15, 15),(15, 15),(15, 15)]

class Room:
    def __init__(self, tileMap, tileCollision):
        self.tileMap                = tileMap
        self.image, self.overlay    = self.initRoom()
        self.collisionMap           = tileCollision
        self.difficulty             = None

    def initRoom(self):
        room    = pygame.Surface((len(self.tileMap[0]) * TILE_WIDTH, len(self.tileMap) * TILE_HEIGHT))
        overlay = [pygame.Surface((len(self.tileMap[0]) * TILE_WIDTH, len(self.tileMap) * TILE_HEIGHT), pygame.SRCALPHA),
                   pygame.Surface((len(self.tileMap[0]) * TILE_WIDTH, len(self.tileMap) * TILE_HEIGHT), pygame.SRCALPHA)]
        for j, column in enumerate(self.tileMap):
            for k, row in enumerate(column):
                tiles = getTiles()
                tile = tiles[row][0]
                if not row in [5,6,7,8]: room.blit(tiles[row][0], (j * TILE_WIDTH, k * TILE_HEIGHT))
                else:
                    overlay[0].blit(tiles[row][0], (j * TILE_WIDTH, k * TILE_HEIGHT))
                    if row == 5:    overlay[1].blit(tiles[6][0], (j * TILE_WIDTH, k * TILE_HEIGHT))
                    elif row == 6:  overlay[1].blit(tiles[5][0], (j * TILE_WIDTH, k * TILE_HEIGHT))
                    elif row == 7:  overlay[1].blit(tiles[8][0], (j * TILE_WIDTH, k * TILE_HEIGHT))
                    elif row == 8:  overlay[1].blit(tiles[7][0], (j * TILE_WIDTH, k * TILE_HEIGHT))

        return room,overlay
