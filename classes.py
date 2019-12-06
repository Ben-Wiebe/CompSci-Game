from math import pi, sin, cos, atan2
from random import choice, randint
import copy
from settings import *
import pygame
pygame.init()

bulletImages = {"leaf"  : [pygame.transform.scale(pygame.image.load(r"resources\bullets\leaf.png"), (round(TILE_WIDTH / 1.5), round(TILE_HEIGHT / 1.5))),
                           pygame.transform.scale(pygame.image.load(r"resources\bullets\leaf.png"), (round(TILE_WIDTH / 1.5), round(TILE_HEIGHT / 1.5)))] ,
                ""      : [] }
class Player:# Player class
    players = 0
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
        self.display        = False
        self.weapon         = None
        self.movedRooms     = False
        self.direction      = "RIGHT"
        self.moveCount      = 0
        # Special attributes. Unused as of now
        self.spec           = {"lifesteal" : 0, "missingHpHeal" : 0, "revive" : False, "currentHealthDmg" : 0, "missingHpDmg" : 0, "playerHpBonus" : 0}
        
        self.images         = { "UP"    : [pygame.transform.scale(pygame.image.load(r"resources\player\{}up{}".format("",i) + ".png"),
                                                                  (int(TILE_WIDTH * self.w), int(TILE_HEIGHT * self.h))) for i in range(1,3)] ,
                                "DOWN"  : [pygame.transform.scale(pygame.image.load(r"resources\player\{}down{}".format("",i) + ".png"),
                                                                  (int(TILE_WIDTH * self.w), int(TILE_HEIGHT * self.h))) for i in range(1,3)] ,
                                "RIGHT" : [pygame.transform.scale(pygame.image.load(r"resources\player\{}right{}".format("",i) + ".png"),
                                                                  (int(TILE_WIDTH * self.w), int(TILE_HEIGHT * self.h))) for i in range(1,5)] ,
                                "LEFT"  : [pygame.transform.scale(pygame.image.load(r"resources\player\{}left{}".format("",i) + ".png"),
                                                                  (int(TILE_WIDTH * self.w), int(TILE_HEIGHT * self.h))) for i in range(1,5)] }

##        # Lifesteal
##        self.health += bullet.dmg * (self.spec["lifesteal"] / 100)
##        if self.health > self.maxHealth: self.health = self.maxHealth
##        # More lifesteal the lower you are
##        if self.health < self.maxHealth / 2: self.health += (self.maxHealth - self.health) * (self.spec["missingHpHeal"] / 100) * (bullet.dmg / 15)
##        # More damage the higher health they are
##        enemy.health -= enemy.health * (self.spec["currentHealthDmg"] / 100)
##        # More damage the lower they are
##        enemy.health -= (enemy.maxHealth - enemy.health) * (self.spec["missingHpDmg"] / 100)
##        # More damage the more health you are
##        enemy.health -= (self.maxHealth - self.health) * (self.spec["playerHpBonus"] / 100)

    def onDeath(self):
        if  self.spec["revive"]:
            self.health = self.maxHealth / 2
            self.spec["revive"] = False
            return True

    def toggleDisplay(self):
        # Toggles the minimap display
        if self.display == True:    self.display = False
        else:                       self.display = True

    def checkFloor(self, m, players, activeFrames):
        # Checks which tiles the player is standing on
        tiles = [(int(self.x), int(self.x + self.w)), (int(self.y), int(self.y + self.h))]
        damage = False
        wp = m[self.worldX][self.worldY]
        if self.movedRooms:
            self.movedRooms = False
            for i in range(tiles[0][0], tiles[0][1] + 1):
                for j in range(tiles[1][0] + 1, tiles[1][1] + 1):
                    if i >=0 and j >= 0 and i < len(wp.tileMap) - 1 and j < len(wp.tileMap[0]) - 1:
                        pos = wp.tileMap[i][j]
                        if not pos == 0: self.movedRooms = True
                
        for i in range(tiles[0][0], tiles[0][1] + 1):
            for j in range(tiles[1][0] + 1, tiles[1][1] + 1):
                #if i >=0 and j >= 0 and i < len(wp.tileMap) - 1 and j < len(wp.tileMap[0]) - 1:
                    pos = wp.tileMap[i][j]
                    
                    if pos in [5,6,7,8]: self.slow = 0.6
                    elif pos in [2, 3, 4] and (pos + int(activeFrames / 2) % 3) == 4: damage = True
                    elif pos in [5, 6]: damage = True
                    
                    if not self.movedRooms:
                        # Moves your player's room if you're on a doorway
                        if pos == 20:
                            count = 0
                            for p in players:
                                if (p.worldX, p.worldY) == (self.worldX, self.worldY): count += 1
                            if count == 1: m[self.worldX][self.worldY].unloadRoom()
                            self.worldY -= 2
                            if not m[self.worldX][self.worldY].image: m[self.worldX][self.worldY].loadRoom()
                            self.y = len(wp.tileMap[0]) - 3
                            self.movedRooms = True
                            return
                        elif pos == 21:
                            count = 0
                            for p in players:
                                if (p.worldX, p.worldY) == (self.worldX, self.worldY): count += 1
                            if count == 1: m[self.worldX][self.worldY].unloadRoom()
                            self.worldY += 2
                            if not m[self.worldX][self.worldY].image: m[self.worldX][self.worldY].loadRoom()
                            self.y = 0
                            self.movedRooms = True
                            return
                        elif pos == 22:
                            count = 0
                            for p in players:
                                if (p.worldX, p.worldY) == (self.worldX, self.worldY): count += 1
                            if count == 1: m[self.worldX][self.worldY].unloadRoom()
                            self.worldX -= 2
                            if not m[self.worldX][self.worldY].image: m[self.worldX][self.worldY].loadRoom()
                            self.x = len(wp.tileMap) - 3
                            self.movedRooms = True
                            return
                        elif pos == 23:
                            count = 0
                            for p in players:
                                if (p.worldX, p.worldY) == (self.worldX, self.worldY): count += 1
                            if count == 1: m[self.worldX][self.worldY].unloadRoom()
                            self.worldX += 2
                            if not m[self.worldX][self.worldY].image: m[self.worldX][self.worldY].loadRoom()
                            self.x = 0
                            self.movedRooms = True
                            return
                    
        if damage: self.health -= 0.5
        
class Boss:
    # Boss class
    def __init__(self, x, y, worldX, worldY, w, h, maxHealth, ms, armour, damage, gun=None):
        self.x              = x
        self.y              = y
        self.worldX         = worldX
        self.worldY         = worldY
        self.w              = w
        self.h              = h
        self.maxHealth      = maxHealth
        self.health         = maxHealth
        self.ms             = ms
        self.armour         = armour
        self.damage         = damage
        self.gun            = gun
        self.slow           = 1
        self.team           = 10
        self.moveCount      = 0
        self.attacking      = False
        self.direction      = "RIGHT"
        self.attackCount    = 0
        self.attacks        = 0

class Hastur(Boss):
    #Inherits the boss class for our first boss
    images              = { "UP"    : [pygame.transform.scale(pygame.image.load(r"resources\bosses\hastur\up{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 8), int(TILE_HEIGHT * 8))) for i in range(1,3)] ,
                            "DOWN"  : [pygame.transform.scale(pygame.image.load(r"resources\bosses\hastur\down{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 8), int(TILE_HEIGHT * 8))) for i in range(1,3)] ,
                            "RIGHT" : [pygame.transform.scale(pygame.image.load(r"resources\bosses\hastur\right{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 8), int(TILE_HEIGHT * 8))) for i in range(1,3)] ,
                            "LEFT"  : [pygame.transform.scale(pygame.image.load(r"resources\bosses\hastur\left{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 8), int(TILE_HEIGHT * 8))) for i in range(1,3)] }

    attackingImages     = { "UP"    : [pygame.transform.scale(pygame.image.load(r"resources\bosses\hastur\attack_up{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 8), int(TILE_HEIGHT * 8))) for i in range(1,4)] ,
                            "DOWN"  : [pygame.transform.scale(pygame.image.load(r"resources\bosses\hastur\attack_down{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 8), int(TILE_HEIGHT * 8))) for i in range(1,4)] ,
                            "RIGHT" : [pygame.transform.scale(pygame.image.load(r"resources\bosses\hastur\attack_right{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 8), int(TILE_HEIGHT * 8))) for i in range(1,4)] ,
                            "LEFT"  : [pygame.transform.scale(pygame.image.load(r"resources\bosses\hastur\attack_left{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 8), int(TILE_HEIGHT * 8))) for i in range(1,4)] }

    def AI(self, mapList, bullets, players, enemies, activeFrames):
        grid = mapList.collisionMap
        sortedPlayers = sorted(players, key=lambda p: ((self.x - p.x) ** 2) + ((self.y - p.y) ** 2), reverse=False)
        for p in sortedPlayers:
            if (p.worldX, p.worldY) == (self.worldX, self.worldY): break
        if not self.attacking:
            if (p.worldX, p.worldY) == (self.worldX, self.worldY):
                if round(activeFrames, 2) % 10 in [0, 1]:
                    # 8 directional shots around hastur
                    for angle in [pi / 4, pi / 2, (3 * pi) / 4, pi, (5 * pi) / 4, (3 * pi) / 2, (7 * pi) / 4, 2 * pi]:
                        bullets.append(Bullet((self.x + (self.w / 2), self.y + (self.h / 2)), (self.worldX, self.worldY), 25,
                                          (angle + atan2((p.y - self.y), (p.x - self.x)) * (pi / 180)),
                                          self.team, 0.12, 100, 3, 0.4))
                self.moveCount += 0.2
                angle = atan2((self.y - p.y), (self.x - p.x))
                if p.y < self.y + (self.h / 2):
                    self.direction = "UP"
                    if grid[int(self.x + (self.w / 2))][int((self.y + (self.h / 2)) - (self.h / 2))] != 1:
                        self.y -= self.ms * self.slow

                elif p.y > self.y + (self.h / 2):
                    self.direction = "DOWN"
                    if grid[int(self.x + (self.w / 2))][int((self.y + (self.h / 2)) + (self.h / 2))] != 1:
                        self.y += self.ms * self.slow

                if p.x < self.x + (self.w / 2):
                    self.direction = "LEFT"
                    if grid[int((self.x + (self.w / 2)) - (self.w / 2))][int(self.y + (self.h / 2))] != 1:
                        self.x -= self.ms * self.slow

                elif p.x > self.x + (self.w / 2):
                    self.direction = "RIGHT"
                    if grid[int((self.x + (self.w / 2)) + (self.w / 2))][int(self.y + (self.h / 2))] != 1:
                        self.x += self.ms * self.slow
                        
                if ((self.x + (self.w / 2) - p.x) ** 2) + ((self.y + (self.h / 2) - p.y) ** 2) < 20:
                    self.attacking = True
                    self.attackCount = 0
                    mapList.meleeRects.append(AttackRect((self.x + (self.w // 2) * DIRECTION_KEY[self.direction][0]) * TILE_WIDTH,
                                                         (self.y + (self.h // 2) * DIRECTION_KEY[self.direction][1]) * TILE_HEIGHT,
                                                         self.worldX, self.worldY,
                                                         self.w * 0.8 * TILE_WIDTH, self.h * TILE_HEIGHT, self.team, 20, range(25, 40), 40, ORANGE))

        if self.attacking:
            self.attackCount += 0.05
            if self.attackCount >= 4:
                self.attacking = False
    
class Enemy:
    # General enemy class
    def __init__(self, maxHealth, ms, armour, damage, gun=None):
        self.x = 0; self.worldX = 0
        self.y = 0; self.worldY = 0
        self.attacking          = False
        self.idling             = False
        self.direction          = "RIGHT"
        self.attackCount        = 0
        self.ms                 = ms
        self.w                  = 2
        self.h                  = 2
        self.weapon             = gun
        self.health             = maxHealth
        self.maxHealth          = maxHealth
        self.damage             = damage
        self.slow               = 1
        self.team               = 10
        self.moveCount          = 0
        self.lastMove           = [1, 1]
        self.attacks            = 0

    def onDeath(self): pass

# Several enemy classes inheriting the general enemy class
class Voidling(Enemy):
    images              = { "RIGHT" : [pygame.transform.scale(pygame.image.load(r"resources\enemies\voidling\right{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,4)] ,
                            "LEFT"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\voidling\left{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,4)] ,
                            "UP"    : [pygame.transform.scale(pygame.image.load(r"resources\enemies\voidling\up{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,4)] ,
                            "DOWN"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\voidling\down{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,4)] }

    attackingImages     = { "RIGHT" : [pygame.transform.scale(pygame.image.load(r"resources\enemies\voidling\attackright{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,7)] ,
                            "LEFT"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\voidling\attackleft{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,7)] ,
                            "UP"    : [pygame.transform.scale(pygame.image.load(r"resources\enemies\voidling\attackup{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,7)] ,
                            "DOWN"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\voidling\attackdown{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,7)] }

    def AI(self, mapList, bullets, players, enemies, activeFrames):
        def closestKey(dictionary, val): return dictionary.get(val, dictionary[min(dictionary.keys(), key=lambda k: abs(k-val))])
        grid = mapList.collisionMap
        sortedPlayers = sorted(players, key=lambda p: ((self.x - p.x) ** 2) + ((self.y - p.y) ** 2), reverse=False)
        for p in sortedPlayers:
            if (p.worldX, p.worldY) == (self.worldX, self.worldY): break
        if not self.attacking:
            if (p.worldX, p.worldY) == (self.worldX, self.worldY):
                self.moveCount += 0.2
                angle = atan2((p.y - self.y), (p.x - self.x)) * (180 / pi)
                angle %= 360
                self.direction = closestKey(DIRECTIONS, angle)
                angle *= (pi / 180)
                moveX = cos(angle) * self.ms * self.slow
                moveY = sin(angle) * self.ms * self.slow
                if grid[int((self.x + (self.w / 2)) + moveX)][int(self.y + (self.h / 2))] != 1: self.x += moveX
                if grid[int(self.x + (self.w / 2))][int((self.y + (self.h / 2)) + moveY)] != 1: self.y += moveY

                if ((self.x - p.x) ** 2) + ((self.y - p.y) ** 2) < 4:
                    self.attacking = True
                    self.attackCount = 0
                    if self.direction in "LEFT RIGHT":
                        mapList.meleeRects.append(AttackRect((self.x + (self.w // 2) * DIRECTION_KEY[self.direction][0]) * TILE_WIDTH,
                                                             (self.y + (self.h // 2) * DIRECTION_KEY[self.direction][1]) * TILE_HEIGHT,
                                                             self.worldX, self.worldY,
                                                             self.w * 0.8 * TILE_WIDTH, self.h * 0.8 * TILE_HEIGHT, self.team, 40, range(15, 25), 25, PURPLE))
                    elif self.direction in "UP DOWN":
                        mapList.meleeRects.append(AttackRect(self.x * TILE_WIDTH,
                                                             (self.y + ((self.h // 2) * DIRECTION_KEY[self.direction][1])) * TILE_HEIGHT,
                                                             self.worldX, self.worldY,
                                                             self.w * 0.8 * TILE_WIDTH, self.h * TILE_HEIGHT, self.team, 40, range(15, 25), 25, PURPLE))

        if self.attacking:
            self.attackCount += 0.25
            if self.attackCount >= 12:
                self.attacking = False

class Goblin(Enemy):
    images              = { "RIGHT" : [pygame.transform.scale(pygame.image.load(r"resources\enemies\goblin\right{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,3)] ,
                            "LEFT"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\goblin\left{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,3)] ,
                            "UP"    : [pygame.transform.scale(pygame.image.load(r"resources\enemies\goblin\up{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,3)] ,
                            "DOWN"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\goblin\down{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,3)] }

    attackingImages     = { "RIGHT" : [pygame.transform.scale(pygame.image.load(r"resources\enemies\goblin\attackright{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,3)] ,
                            "LEFT"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\goblin\attackleft{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,3)] ,
                            "UP"    : [pygame.transform.scale(pygame.image.load(r"resources\enemies\goblin\attackup{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,3)] ,
                            "DOWN"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\goblin\attackdown{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,3)] }

    def AI(self, mapList, bullets, players, enemies, activeFrames):
        def closestKey(dictionary, val): return dictionary.get(val, dictionary[min(dictionary.keys(), key=lambda k: abs(k-val))])
        grid = mapList.collisionMap
        sortedPlayers = sorted(players, key=lambda p: ((self.x - p.x) ** 2) + ((self.y - p.y) ** 2), reverse=False)
        for p in sortedPlayers:
            if (p.worldX, p.worldY) == (self.worldX, self.worldY): break
        if not self.attacking:
            if (p.worldX, p.worldY) == (self.worldX, self.worldY):
                self.moveCount += 0.2
                angle = atan2((p.y - self.y), (p.x - self.x)) * (180 / pi)
                angle %= 360
                self.direction = closestKey(DIRECTIONS, angle)
                angle *= (pi / 180)
                moveX = cos(angle) * self.ms * self.slow
                moveY = sin(angle) * self.ms * self.slow
                if grid[int((self.x + (self.w / 2) + ((self.w / 2) * DIRECTION_KEY[self.direction][0])) + moveX)] \
                   [int(self.y + (self.h / 2))] != 1: self.x += moveX
                if grid[int(self.x + (self.w / 2))] \
                   [int((self.y + (self.h / 2) + ((self.h / 2) * DIRECTION_KEY[self.direction][1])) + moveY)] != 1: self.y += moveY

                if ((self.x - p.x) ** 2) + ((self.y - p.y) ** 2) < 4.5:
                    self.attacking = True
                    self.attackCount = 0
                    if self.direction in "LEFT RIGHT":
                        mapList.meleeRects.append(AttackRect((self.x + (self.w // 2) * DIRECTION_KEY[self.direction][0]) * TILE_WIDTH,
                                                             (self.y + (self.h // 2) * DIRECTION_KEY[self.direction][1]) * TILE_HEIGHT,
                                                             self.worldX, self.worldY,
                                                             self.w * 0.8 * TILE_WIDTH, self.h * 0.8 * TILE_HEIGHT, self.team, 15, range(15, 20), 20, GREEN))
                    elif self.direction in "UP DOWN":
                        mapList.meleeRects.append(AttackRect(self.x * TILE_WIDTH,
                                                             (self.y + ((self.h // 2) * DIRECTION_KEY[self.direction][1])) * TILE_HEIGHT,
                                                             self.worldX, self.worldY,
                                                             self.w * 0.8 * TILE_WIDTH, self.h * TILE_HEIGHT, self.team, 15, range(15, 20), 20, GREEN))

        if self.attacking:
            self.attackCount += 0.1
            if self.attackCount >= 3:
                self.attacking = False

class WillOTheWisp(Enemy):
    images              = { "RIGHT" : [pygame.transform.scale(pygame.image.load(r"resources\enemies\willothewisp\right{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 1), int(TILE_HEIGHT * 1.5))) for i in range(1,3)] ,
                            "LEFT"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\willothewisp\left{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 1), int(TILE_HEIGHT * 1.5))) for i in range(1,3)] ,
                            "UP"    : [pygame.transform.scale(pygame.image.load(r"resources\enemies\willothewisp\right{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 1), int(TILE_HEIGHT * 1.5))) for i in range(1,3)] ,
                            "DOWN"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\willothewisp\left{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 1), int(TILE_HEIGHT * 1.5))) for i in range(1,3)] }

    attackingImages     = { "RIGHT" : [pygame.transform.scale(pygame.image.load(r"resources\enemies\willothewisp\attackright{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 1), int(TILE_HEIGHT * 1.5))) for i in range(1,3)] ,
                            "LEFT"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\willothewisp\attackleft{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 1), int(TILE_HEIGHT * 1.5))) for i in range(1,3)] ,
                            "UP"    : [pygame.transform.scale(pygame.image.load(r"resources\enemies\willothewisp\attackup{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 1), int(TILE_HEIGHT * 1.5))) for i in range(1,3)] ,
                            "DOWN"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\willothewisp\attackdown{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 1), int(TILE_HEIGHT * 1.5))) for i in range(1,3)] }

    def AI(self, mapList, bullets, players, enemies, activeFrames):
        self.w = 1
        self.h = 2
        def closestKey(dictionary, val): return dictionary.get(val, dictionary[min(dictionary.keys(), key=lambda k: abs(k-val))])
        grid = mapList.collisionMap
        sortedPlayers = sorted(players, key=lambda p: ((self.x - p.x) ** 2) + ((self.y - p.y) ** 2), reverse=False)
        for p in sortedPlayers:
            if (p.worldX, p.worldY) == (self.worldX, self.worldY): break
        if not self.attacking:
            if (p.worldX, p.worldY) == (self.worldX, self.worldY):
                self.moveCount += 0.5
                angle = atan2((p.y - self.y), (p.x - self.x)) * (180 / pi)
                angle %= 360
                self.direction = closestKey(DIRECTIONS, angle)
                angle *= (pi / 180)
                moveX = cos(angle) * self.ms * self.slow
                moveY = sin(angle) * self.ms * self.slow
                if grid[int((self.x + (self.w / 2) + ((self.w / 2) * DIRECTION_KEY[self.direction][0])) + moveX)] \
                   [int(self.y + (self.h / 2))] != 1: self.x += moveX
                if grid[int(self.x + (self.w / 2))] \
                   [int((self.y + (self.h / 2) + ((self.h / 2) * DIRECTION_KEY[self.direction][1])) + moveY)] != 1: self.y += moveY

                if ((self.x - p.x) ** 2) + ((self.y - p.y) ** 2) < 2.5:
                    self.attacking = True
                    self.attackCount = 0
                    if self.direction in "LEFT RIGHT":
                        mapList.meleeRects.append(AttackRect((self.x + (self.w * 0.8) * DIRECTION_KEY[self.direction][0]) * TILE_WIDTH,
                                                             (self.y + (self.h * 0.9) * DIRECTION_KEY[self.direction][1]) * TILE_HEIGHT,
                                                             self.worldX, self.worldY,
                                                             self.w * 0.8 * TILE_WIDTH, self.h * 0.5 * TILE_HEIGHT, self.team, 15, range(15, 20), 20, WHITE))
                    elif self.direction in "UP DOWN":
                        mapList.meleeRects.append(AttackRect(self.x * TILE_WIDTH,
                                                             (self.y + ((self.h * 0.5) * DIRECTION_KEY[self.direction][1])) * TILE_HEIGHT,
                                                             self.worldX, self.worldY,
                                                             self.w * 0.8 * TILE_WIDTH, self.h * 0.6 * TILE_HEIGHT, self.team, 15, range(15, 20), 20, WHITE))

        if self.attacking:
            self.attackCount += 0.1
            if self.attackCount >= 3:
                self.attacking = False

class Saladmander(Enemy):
    # This guy shots healing shots for the players
    images              = { "RIGHT" : [pygame.transform.scale(pygame.image.load(r"resources\enemies\saladmander\right{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,3)] ,
                            "LEFT"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\saladmander\left{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,3)] ,
                            "UP"    : [pygame.transform.scale(pygame.image.load(r"resources\enemies\saladmander\up{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,3)] ,
                            "DOWN"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\saladmander\down{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,3)] }

    def AI(self, mapList, bullets, players, enemies, activeFrames):
        self.attackCount += 1
        if self.attackCount >= 30:
            self.attackCount = 0
            g = self.weapon
            for angle in g.shots:
                bullets.append(Bullet((self.x + (self.w / 2), self.y + (self.h / 2)), (self.worldX, self.worldY), g.bulletDmg,
                                      (randint(0, 360) * (180 / pi)) + ((angle + randint(-g.deviation, g.deviation)) * (pi / 180)),
                                      self.team, g.speed, g.range, g.maxBounces, g.r))
        grid = mapList.tileMap
        self.lastMove = [randint(-1, 2) if randint(0, 100) >= 95 else i for i in self.lastMove]
        self.moveCount += 0.2
        if self.lastMove[1] == 1:
            self.direction = "UP"
            if grid[int(self.x + (self.w / 2))][int((self.y + (self.h / 2)) - (self.h / 2))] == 0:
                self.y -= self.ms * self.slow

        elif self.lastMove[1] == -1:
            self.direction = "DOWN"
            if grid[int(self.x + (self.w / 2))][int((self.y + (self.h / 2)) + (self.h / 2))] == 0:
                self.y += self.ms * self.slow

        if self.lastMove[0] == -1:
            self.direction = "LEFT"
            if grid[int((self.x + (self.w / 2)) - (self.w / 2))][int(self.y + (self.h / 2))] == 0:
                self.x -= self.ms * self.slow

        elif self.lastMove[0] == 1:
            self.direction = "RIGHT"
            if grid[int((self.x + (self.w / 2)) + (self.w / 2))][int(self.y + (self.h / 2))] == 0:
                self.x += self.ms * self.slow

class Bullet:
    # Bullet class
    def __init__(self, pos, worldPos, dmg, a, t, speed, bulletRange, maxBounces, r):
        self.x, self.y      = pos
        self.worldX, self.worldY                            = worldPos
        self.dmg            = dmg;          self.speed      = speed
        self.angle          = a
        self.dx, self.dy    = cos(self.angle), sin(self.angle)
        self.team           = t
        self.r              = r
        self.age            = 0
        self.range          = bulletRange
        self.bounces        = 0;            self.maxBounces = maxBounces
        self.images         = bulletImages["leaf"]

    # Call upon bullet collision with a wall
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

# For when players and enemies shoot bullets
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
        self.rect       = (0.8,0.8)
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

# loads images for all of the tiles
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
        self.atkSpeed       = 1
        self.image          = None
        self.rect           = (0.8, 0.8)#[(15, 15),(15, 15),(15, 15),(15, 15),(15, 15),(15, 15),(15, 15)]

# For the minimap display
class Minimap:
    def __init__(self, tileMap):
        self.image = self.loadImage(tileMap)

    def loadImage(self, tileMap):
        image = pygame.Surface((len(tileMap) * TILE_WIDTH, len(tileMap[0]) * TILE_HEIGHT), pygame.SRCALPHA)
        for j, column in enumerate(tileMap):
            for k, row in enumerate(column):
                if row == 1:
                    pygame.draw.rect(image, BLACKA, (j * TILE_WIDTH, k * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT))
                elif row == 0:
                    pygame.draw.rect(image, BROWNA, (j * TILE_WIDTH, k * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT))
                else:
                    pygame.draw.rect(image, DIFFICULTY_COLOURS[row.difficulty], (j * TILE_WIDTH, k * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT))

        return image

# Shows melee attacks and checks for their collision with the player
class AttackRect:
    def __init__(self, x, y, wx, wy, w, h, team, d, af, l, c):
        self.rect           = pygame.Rect((x, y, w, h))
        self.team = team
        self.worldX, self.worldY = wx, wy
        self.damage         = d
        self.activeFrames   = af
        self.colour         = c
        self.frames         = 0
        self.length         = l
        self.delete         = False
        self.hit            = []

    def update(self, players):
        self.frames += 1
        collisionIndex = self.rect.collidelist([pygame.Rect((p.x * TILE_WIDTH, p.y * TILE_HEIGHT, p.w * TILE_HEIGHT, p.h * TILE_WIDTH)) for p in players])
        if self.frames in self.activeFrames:
            if collisionIndex != -1 and not collisionIndex in self.hit and self.team != players[collisionIndex].team:
                players[collisionIndex].health -= self.damage
                self.hit.append(collisionIndex)
        if self.frames >= self.length:
            self.delete = True

# Possible enemies for each difficulty level room
ENEMIES = { 1 : [Goblin(150, 0.1, 5, 25), WillOTheWisp(150, 0.08, 5, 25),
                 Saladmander(50, 0.03, 0, 0, gun=Gun([-5, 0, 5],    "Spread Fire", 0, 0.4, 100, 2, 10, 0, -15, 0.2, 1, "semi"))] ,
            2 : [Goblin(150, 0.1, 5, 25)] ,
            3 : [Goblin(150, 0.1, 5, 25)] ,
            4 : [Voidling(250, 0.08, 5, 25),
                 Saladmander(50, 0.03, 0, 0, gun=Gun([-5, 5],       "Spread Fire", 0, 0.4, 100, 2, 10, 0, -15, 0.2, 1, "semi"))] ,
            5 : [Voidling(250, 0.08, 5, 25)] }

# Room class
class Room:
    def __init__(self, difficulty, tileMaps, x, y):
        self.x, self.y                          = x, y
        self.tileMap, self.collisionMap         = tileMaps
        self.image, self.overlay, self.traps    = None, None, None
        self.difficulty                         = difficulty
        self.enemies                            = self.spawnEnemies()
        self.boss                               = []
        self.interactables                      = []
        self.simulated                          = False
        self.meleeRects                         = []

    # Loads the room to memory
    def loadRoom(self):
        room    =  pygame.Surface((len(self.tileMap) * TILE_WIDTH, len(self.tileMap[0]) * TILE_HEIGHT))
        
        overlay = [pygame.Surface((len(self.tileMap) * TILE_WIDTH, len(self.tileMap[0]) * TILE_HEIGHT), pygame.SRCALPHA),
                   pygame.Surface((len(self.tileMap) * TILE_WIDTH, len(self.tileMap[0]) * TILE_HEIGHT), pygame.SRCALPHA)]
        
        traps   = [pygame.Surface((len(self.tileMap) * TILE_WIDTH, len(self.tileMap[0]) * TILE_HEIGHT), pygame.SRCALPHA),
                   pygame.Surface((len(self.tileMap) * TILE_WIDTH, len(self.tileMap[0]) * TILE_HEIGHT), pygame.SRCALPHA),
                   pygame.Surface((len(self.tileMap) * TILE_WIDTH, len(self.tileMap[0]) * TILE_HEIGHT), pygame.SRCALPHA)]
        tiles = getTiles()
        for j, column in enumerate(self.tileMap):
            for k, row in enumerate(column):
                if row in [20, 21, 22, 23]:
                    #if row == 20:
                    room.blit(tiles[1][0], (j * TILE_WIDTH, k * TILE_HEIGHT))
                else:
                    tile = tiles[row][0]
                    if row in [5,6,7,8]:
                        overlay[0].blit(tiles[row][0], (j * TILE_WIDTH, k * TILE_HEIGHT))
                        if row == 5:    overlay[1].blit(tiles[6][0], (j * TILE_WIDTH, k * TILE_HEIGHT))
                        elif row == 6:  overlay[1].blit(tiles[5][0], (j * TILE_WIDTH, k * TILE_HEIGHT))
                        elif row == 7:  overlay[1].blit(tiles[8][0], (j * TILE_WIDTH, k * TILE_HEIGHT))
                        elif row == 8:  overlay[1].blit(tiles[7][0], (j * TILE_WIDTH, k * TILE_HEIGHT))

                    elif row in [2,3,4]:
                        traps[0].blit(tiles[row][0], (j * TILE_WIDTH, k * TILE_HEIGHT))
                        if row == 2:    traps[1].blit(tiles[3][0], (j * TILE_WIDTH, k * TILE_HEIGHT)); traps[2].blit(tiles[4][0], (j * TILE_WIDTH, k * TILE_HEIGHT))
                        elif row == 3:  traps[1].blit(tiles[4][0], (j * TILE_WIDTH, k * TILE_HEIGHT)); traps[2].blit(tiles[2][0], (j * TILE_WIDTH, k * TILE_HEIGHT))
                        elif row == 4:  traps[1].blit(tiles[2][0], (j * TILE_WIDTH, k * TILE_HEIGHT)); traps[2].blit(tiles[3][0], (j * TILE_WIDTH, k * TILE_HEIGHT))

                    else: room.blit(tiles[row][0], (j * TILE_WIDTH, k * TILE_HEIGHT))

        self.image, self.overlay, self.traps = room, overlay, traps

    # Unloads the room from memory
    def unloadRoom(self):
        self.image, self.overlay, self.traps = None, None, None

    # Spawns enemies at random, makes sure they don't spawn inside of a wall
    def spawnEnemies(self):
        enemies = [copy.copy(choice(ENEMIES[self.difficulty])) for e in range(ENEMY_NUMBERS[self.difficulty])]
        for e in enemies:
            remake = True
            e.worldX = self.x
            e.worldY = self.y
            while remake:
                remake = False
                e.x = randint(2,len(self.collisionMap) - 3)
                e.y = randint(2,len(self.collisionMap[0]) - 3)
                tiles = [(int(e.x), int(e.x + e.w)), (int(e.y), int(e.y + e.h))]
                for i in range(tiles[0][0], tiles[0][1] + 1):
                    for j in range(tiles[1][0], tiles[1][1] + 1):
                        if self.collisionMap[i][j] == 1:
                            remake = True
        return enemies
