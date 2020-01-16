from math import pi, sin, cos, atan2
from random import choice, randint
import copy
from settings import *
import pygame
pygame.init()

# Images for all of the types of bullets
bulletImages = {"leaf"  : [pygame.transform.scale(pygame.image.load(r"resources\bullets\leaf1.png"), (round(TILE_WIDTH / 1.5), round(TILE_HEIGHT / 1.5))),
                           pygame.transform.scale(pygame.image.load(r"resources\bullets\leaf2.png"), (round(TILE_WIDTH / 1.5), round(TILE_HEIGHT / 1.5))),
                           pygame.transform.scale(pygame.image.load(r"resources\bullets\leaf3.png"), (round(TILE_WIDTH / 1.5), round(TILE_HEIGHT / 1.5))),
                           pygame.transform.scale(pygame.image.load(r"resources\bullets\leaf4.png"), (round(TILE_WIDTH / 1.5), round(TILE_HEIGHT / 1.5)))] ,
                "rock"  : [pygame.transform.scale(pygame.image.load(r"resources\bullets\rock.png"),  (round(TILE_WIDTH / 1), round(TILE_HEIGHT / 1)))],
                "fire"  : [pygame.transform.scale(pygame.image.load(r"resources\bullets\fire.png"),  (round(TILE_WIDTH / 1), round(TILE_HEIGHT / 1)))],
                "air"   : [pygame.transform.scale(pygame.image.load(r"resources\bullets\air.png"),  (round(TILE_WIDTH / 1), round(TILE_HEIGHT / 1)))],
                "magic" : [pygame.transform.scale(pygame.image.load(r"resources\bullets\magic.png"),  (round(TILE_WIDTH / 1), round(TILE_HEIGHT / 1)))],
                "darkmagic" : [pygame.transform.scale(pygame.image.load(r"resources\bullets\darkmagic.png"),  (round(TILE_WIDTH / 1), round(TILE_HEIGHT / 1)))],
                "arrow1": [pygame.transform.scale(pygame.image.load(r"resources\bullets\arrow1.png"),  (round(TILE_WIDTH / 1), round(TILE_HEIGHT / 1)))],
                "arrow2": [pygame.transform.scale(pygame.image.load(r"resources\bullets\arrow2.png"),  (round(TILE_WIDTH / 1), round(TILE_HEIGHT / 1)))],
                "arrow3": [pygame.transform.scale(pygame.image.load(r"resources\bullets\arrow3.png"),  (round(TILE_WIDTH / 1), round(TILE_HEIGHT / 1)))],
                "arrow4": [pygame.transform.scale(pygame.image.load(r"resources\bullets\arrow4.png"),  (round(TILE_WIDTH / 1), round(TILE_HEIGHT / 1)))],
                "arrow5": [pygame.transform.scale(pygame.image.load(r"resources\bullets\arrow5.png"),  (round(TILE_WIDTH / 1), round(TILE_HEIGHT / 1)))],
                "arrow6": [pygame.transform.scale(pygame.image.load(r"resources\bullets\arrow6.png"),  (round(TILE_WIDTH / 1), round(TILE_HEIGHT / 1)))],
                "arrow7": [pygame.transform.scale(pygame.image.load(r"resources\bullets\arrow7.png"),  (round(TILE_WIDTH / 1), round(TILE_HEIGHT / 1)))],
                "bullet1": [pygame.transform.scale(pygame.image.load(r"resources\bullets\bullet1.png"),  (round(TILE_WIDTH / 1), round(TILE_HEIGHT / 1)))],
                "bullet2": [pygame.transform.scale(pygame.image.load(r"resources\bullets\bullet2.png"),  (round(TILE_WIDTH / 1), round(TILE_HEIGHT / 1)))],
                "bullet3": [pygame.transform.scale(pygame.image.load(r"resources\bullets\bullet3.png"),  (round(TILE_WIDTH / 1), round(TILE_HEIGHT / 1)))],
                "bullet4": [pygame.transform.scale(pygame.image.load(r"resources\bullets\bullet4.png"),  (round(TILE_WIDTH / 1), round(TILE_HEIGHT / 1)))],
                "bullet5": [pygame.transform.scale(pygame.image.load(r"resources\bullets\bullet5.png"),  (round(TILE_WIDTH / 1), round(TILE_HEIGHT / 1)))],
                "bullet6": [pygame.transform.scale(pygame.image.load(r"resources\bullets\bullet6.png"),  (round(TILE_WIDTH / 1), round(TILE_HEIGHT / 1)))],
                "bullet7": [pygame.transform.scale(pygame.image.load(r"resources\bullets\bullet7.png"),  (round(TILE_WIDTH / 1), round(TILE_HEIGHT / 1)))],
                "spear1": [pygame.transform.scale(pygame.image.load(r"resources\bullets\spear1.png"),  (round(TILE_WIDTH / 1), round(TILE_HEIGHT / 1)))],
                "spear2": [pygame.transform.scale(pygame.image.load(r"resources\bullets\spear2.png"),  (round(TILE_WIDTH / 1), round(TILE_HEIGHT / 1)))],
                "spear3": [pygame.transform.scale(pygame.image.load(r"resources\bullets\spear3.png"),  (round(TILE_WIDTH / 1), round(TILE_HEIGHT / 1)))],
                "spear4": [pygame.transform.scale(pygame.image.load(r"resources\bullets\spear4.png"),  (round(TILE_WIDTH / 1), round(TILE_HEIGHT / 1)))],
                "spear5": [pygame.transform.scale(pygame.image.load(r"resources\bullets\spear5.png"),  (round(TILE_WIDTH / 1), round(TILE_HEIGHT / 1)))],
                "spear6": [pygame.transform.scale(pygame.image.load(r"resources\bullets\spear6.png"),  (round(TILE_WIDTH / 1), round(TILE_HEIGHT / 1)))],
                "spear7": [pygame.transform.scale(pygame.image.load(r"resources\bullets\spear7.png"),  (round(TILE_WIDTH / 1), round(TILE_HEIGHT / 1)))]}

# Offsets for each weapon type
attackOffset = {"bow"       : {"UP"     : (0, 0),
                               "DOWN"   : (0, 0),
                               "LEFT"   : (-0.5, 0),
                               "RIGHT"  : (0, 0)},
                "gun"       : {"UP"     : (0, 0),
                               "DOWN"   : (0, 0),
                               "LEFT"   : (-0.5, 0),
                               "RIGHT"  : (0, 0)},
                "sword"     : {"UP"     : (0, 0),
                               "DOWN"   : (0, 0),
                               "LEFT"   : (-0.5, 0),
                               "RIGHT"  : (0, 0)},
                "gauntlet"   : {"UP"     : (0, 0),
                               "DOWN"   : (0, 0),
                               "LEFT"   : (-0.5, 0),
                               "RIGHT"  : (0, 0)},
                "spear"     : {"UP"     : (0, 0),
                               "DOWN"   : (0, 0),
                               "LEFT"   : (-0.5, 0),
                               "RIGHT"  : (0, 0)}}

# Returns the value at the closest key to a value in a dictionary
def closestKey(dictionary, val): return dictionary.get(val, dictionary[min(dictionary.keys(), key=lambda k: abs(k-val))])

class Player: # Player class
    players = 0
    def __init__(self, x, y, team, maxHealth, worldX = 1, worldY = 1):
        self.alive          = True
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
        self.minimap        = False
        self.weaponDisplay  = True
        self.weapon         = None
        self.movedRooms     = False
        self.pickedUp       = False
        self.minimapToggle  = False
        self.weaponToggle   = False
        self.controlToggle  = False
        self.direction      = "RIGHT"
        self.moveCount      = 0
        self.joystick       = None
        self.cursor         = None
        self.controls       = False
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

    # Loads in all of the attacks for the weapon that you're using
    def loadAttacks(self, wtype, tier):
        if wtype == "bow":
            length = [2, 8, 10, 10]
            if tier == "s": length[2] = 6; length[3] = 6
            elif tier == "j": length = [2, 4, 5, 5]
            else: tier = str(tier + 1)
        elif wtype == "gun":
            length = [2, 3, 3, 3]
            if str(tier) in "sj": pass
            else: tier = str(tier + 1)
            if tier in [3, 4]:
                length[2] = 4; length[3] = 4
        elif wtype == "sword":
            length = [6, 6, 6, 6]
            if str(tier) in "sj": pass
            else: tier = str(tier + 1)
        elif wtype == "gauntlet":
            length = [3, 3, 3, 3]
            if str(tier) in "sj": pass
            else: tier = str(tier + 1)
        elif wtype == "spear":
            length = [2, 2, 2, 2]
            if str(tier) in "sj": pass
            else: tier = str(tier + 1)
        self.attackingImages= { "UP"    : [pygame.transform.scale(pygame.image.load(r"resources\player\red\{}\attackup{}{}".format(wtype, tier, i) + ".png"),
                                                                  (int(TILE_WIDTH * self.w), int(TILE_HEIGHT * self.h))) for i in range(1,max(length[0], 2))] ,
                                "DOWN"  : [pygame.transform.scale(pygame.image.load(r"resources\player\red\{}\attackdown{}{}".format(wtype, tier, i) + ".png"),
                                                                  (int(TILE_WIDTH * self.w), int(TILE_HEIGHT * self.h))) for i in range(1,length[1])] ,
                                "RIGHT" : [pygame.transform.scale(pygame.image.load(r"resources\player\red\{}\attackright{}{}".format(wtype, tier, i) + ".png"),
                                                                  (32, 24)) for i in range(1,length[2])] ,
                                "LEFT"  : [pygame.transform.scale(pygame.image.load(r"resources\player\red\{}\attackleft{}{}".format(wtype, tier, i) + ".png"),
                                                                  (32, 24)) for i in range(1,length[3])] }

##        # Lifesteal
##        self.health += bullet.dmg * (self.spec["lifesteal"] / 100)
##        if self.health > self.maxHealth: self.health = self.maxHealth
##        # More lifesteal the lower health you are at
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
        # Moves rooms when you're on a door tile
        for i in range(tiles[0][0], tiles[0][1] + 1):
            for j in range(tiles[1][0] + 1, tiles[1][1] + 1):
                if i >=0 and j >= 0 and i < len(wp.tileMap) and j < len(wp.tileMap[0]): pos = wp.tileMap[i][j]
                else: self.movedRooms = False; continue

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
        newPlayers = [i if i else None for i in players]
        sortedPlayers = sorted(newPlayers, key=lambda p: ((self.x - p.x) ** 2) + ((self.y - p.y) ** 2), reverse=False)
        for p in sortedPlayers:
            if (p.worldX, p.worldY) == (self.worldX, self.worldY): break
        if not self.attacking:
            if (p.worldX, p.worldY) == (self.worldX, self.worldY) and p:
                if round(activeFrames, 2) % 10 in [0, 1]:
                    # 8 directional shots around hastur
                    for angle in [pi / 4, pi / 2, (3 * pi) / 4, pi, (5 * pi) / 4, (3 * pi) / 2, (7 * pi) / 4, 2 * pi]:
                        bullets.append(Bullet((self.x + (self.w / 2), self.y + (self.h / 2)), (self.worldX, self.worldY), 25,
                                          (angle + atan2((p.y - self.y), (p.x - self.x)) * (pi / 180)),
                                          self.team, 0.12, 100, 3, 0.4, "rock"))
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
                                                         self.w * 0.8 * TILE_WIDTH, self.h * TILE_HEIGHT, self.team, 50, range(25, 27), 27, ORANGE))

        if self.attacking:
            self.attackCount += 0.15
            if self.attackCount >= 4:
                self.attacking = False

    def onDeath(self): pass
    
class Enemy:
    # General enemy class
    def __init__(self, maxHealth, ms, armour, damage, drops, gun=None):
        self.x = 0; self.worldX = 0
        self.y = 0; self.worldY = 0
        self.drops              = drops
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

    def onDeath(self, itemList):
        n = randint(0, 100)
        if randint(0, 15) >= 8:
            item = newObject(closestKey(self.drops, n))
            item.x, item.y = self.x, self.y
            item.worldX, item.worldY = self.worldX, self.worldY
            itemList.append(item)

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

    attackingOffset     = { "RIGHT" : (0, 0)    ,
                            "LEFT"  : (0, 0)    ,
                            "UP"    : (0, 0)    ,
                            "DOWN"  : (0, 0)    }
    
    def AI(self, mapList, bullets, players, enemies, activeFrames):
        def closestKey(dictionary, val): return dictionary.get(val, dictionary[min(dictionary.keys(), key=lambda k: abs(k-val))])
        grid = mapList.collisionMap
        newPlayers = [i if i else None for i in players]
        sortedPlayers = sorted(newPlayers, key=lambda p: ((self.x - p.x) ** 2) + ((self.y - p.y) ** 2), reverse=False)
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

class EarthElemental(Enemy):
    images              = { "RIGHT" : [pygame.transform.scale(pygame.image.load(r"resources\enemies\earthelemental\right{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,3)] ,
                            "LEFT"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\earthelemental\left{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,3)] ,
                            "UP"    : [pygame.transform.scale(pygame.image.load(r"resources\enemies\earthelemental\up{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,3)] ,
                            "DOWN"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\earthelemental\down{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,3)] }

    attackingImages     = { "RIGHT" : [pygame.transform.scale(pygame.image.load(r"resources\enemies\earthelemental\attackright{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 4), int(TILE_HEIGHT * 4))) for i in range(1,4)] ,
                            "LEFT"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\earthelemental\attackleft{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 3.5), int(TILE_HEIGHT * 4))) for i in range(1,4)] ,
                            "UP"    : [pygame.transform.scale(pygame.image.load(r"resources\enemies\earthelemental\attackup{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 3))) for i in range(1,4)] ,
                            "DOWN"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\earthelemental\attackdown{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 3))) for i in range(1,4)] }
    attackingOffset     = { "RIGHT" : (-0.8, -1)    ,
                            "LEFT"  : (-1, -1)   ,
                            "UP"    : (0, -0.8) ,
                            "DOWN"  : (0, 0)    }
    
    def AI(self, mapList, bullets, players, enemies, activeFrames):
        def closestKey(dictionary, val): return dictionary.get(val, dictionary[min(dictionary.keys(), key=lambda k: abs(k-val))])
        grid = mapList.collisionMap
        newPlayers = [i if i else None for i in players]
        sortedPlayers = sorted(newPlayers, key=lambda p: ((self.x - p.x) ** 2) + ((self.y - p.y) ** 2), reverse=False)
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

                if ((self.x - p.x) ** 2) + ((self.y - p.y) ** 2) < 48:
                    self.attacking = True
                    self.attackCount = 0
##                    if lineCasting(grid, (self.x, self.y), (p.x, p.y), angle) == True:
##                        self.attacking = True
##                        self.attackCount = 0
##                    if self.direction in "LEFT RIGHT":
##                        mapList.meleeRects.append(AttackRect((self.x + (self.w // 2) * DIRECTION_KEY[self.direction][0]) * TILE_WIDTH,
##                                                             (self.y + (self.h // 2) * DIRECTION_KEY[self.direction][1]) * TILE_HEIGHT,
##                                                             self.worldX, self.worldY,
##                                                             self.w * 0.8 * TILE_WIDTH, self.h * 0.8 * TILE_HEIGHT, self.team, 40, range(15, 25), 25, PURPLE))
##                    elif self.direction in "UP DOWN":
##                        mapList.meleeRects.append(AttackRect(self.x * TILE_WIDTH,
##                                                             (self.y + ((self.h // 2) * DIRECTION_KEY[self.direction][1])) * TILE_HEIGHT,
##                                                             self.worldX, self.worldY,
##                                                             self.w * 0.8 * TILE_WIDTH, self.h * TILE_HEIGHT, self.team, 40, range(15, 25), 25, PURPLE))

        if self.attacking:
            self.attackCount += 0.1
            if self.attackCount >= 3:
                self.attacking = False
            if round(self.attackCount, 3) == 2.7:
                g = self.weapon
                angle = atan2((p.y - self.y), (p.x - self.x))
                angle %= 2 * pi
                for a in g.shots:
                    bullets.append(Bullet((self.x + (self.w / 2), self.y + (self.h / 2)), (self.worldX, self.worldY), g.bulletDmg,
                                          (angle) + ((a + randint(-g.deviation, g.deviation)) * (pi / 180)),
                                          self.team, g.speed, g.range, g.maxBounces, g.r, "rock"))

class Wizard(Enemy):
    images              = { "RIGHT" : [pygame.transform.scale(pygame.image.load(r"resources\enemies\wizard\right{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,3)] ,
                            "LEFT"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\wizard\left{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,3)] ,
                            "UP"    : [pygame.transform.scale(pygame.image.load(r"resources\enemies\wizard\up{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,2)] ,
                            "DOWN"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\wizard\down{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,3)] }

    attackingImages     = { "RIGHT" : [pygame.transform.scale(pygame.image.load(r"resources\enemies\wizard\attackright{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 4), int(TILE_HEIGHT * 4))) for i in range(1,7)] ,
                            "LEFT"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\wizard\attackleft{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 3.5), int(TILE_HEIGHT * 4))) for i in range(1,7)] ,
                            "UP"    : [pygame.transform.scale(pygame.image.load(r"resources\enemies\wizard\attackup{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 3))) for i in range(1,7)] ,
                            "DOWN"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\wizard\attackdown{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 3))) for i in range(1,7)] }
    attackingOffset     = { "RIGHT" : (0, 0)    ,
                            "LEFT"  : (0, 0)    ,
                            "UP"    : (0, 0)    ,
                            "DOWN"  : (0, 0)    }
    
    def AI(self, mapList, bullets, players, enemies, activeFrames):
        def closestKey(dictionary, val): return dictionary.get(val, dictionary[min(dictionary.keys(), key=lambda k: abs(k-val))])
        grid = mapList.collisionMap
        newPlayers = [i if i else None for i in players]
        sortedPlayers = sorted(newPlayers, key=lambda p: ((self.x - p.x) ** 2) + ((self.y - p.y) ** 2), reverse=False)
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

                if ((self.x - p.x) ** 2) + ((self.y - p.y) ** 2) < 48:
                    self.attacking = True
                    self.attackCount = 0
##                    if lineCasting(grid, (self.x, self.y), (p.x, p.y), angle) == True:
##                        self.attacking = True
##                        self.attackCount = 0
##                    if self.direction in "LEFT RIGHT":
##                        mapList.meleeRects.append(AttackRect((self.x + (self.w // 2) * DIRECTION_KEY[self.direction][0]) * TILE_WIDTH,
##                                                             (self.y + (self.h // 2) * DIRECTION_KEY[self.direction][1]) * TILE_HEIGHT,
##                                                             self.worldX, self.worldY,
##                                                             self.w * 0.8 * TILE_WIDTH, self.h * 0.8 * TILE_HEIGHT, self.team, 40, range(15, 25), 25, PURPLE))
##                    elif self.direction in "UP DOWN":
##                        mapList.meleeRects.append(AttackRect(self.x * TILE_WIDTH,
##                                                             (self.y + ((self.h // 2) * DIRECTION_KEY[self.direction][1])) * TILE_HEIGHT,
##                                                             self.worldX, self.worldY,
##                                                             self.w * 0.8 * TILE_WIDTH, self.h * TILE_HEIGHT, self.team, 40, range(15, 25), 25, PURPLE))

        if self.attacking:
            self.attackCount += 0.1
            if self.attackCount >= 3:
                self.attacking = False
            if round(self.attackCount, 3) == 2.7:
                g = self.weapon
                angle = atan2((p.y - self.y), (p.x - self.x))
                angle %= 2 * pi
                for a in g.shots:
                    bullets.append(Bullet((self.x + (self.w / 2), self.y + (self.h / 2)), (self.worldX, self.worldY), g.bulletDmg,
                                          (angle) + ((a + randint(-g.deviation, g.deviation)) * (pi / 180)),
                                          self.team, g.speed, g.range, g.maxBounces, g.r, "magic"))

class Cultist(Enemy):
    images              = { "RIGHT" : [pygame.transform.scale(pygame.image.load(r"resources\enemies\cultist\right{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,3)] ,
                            "LEFT"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\cultist\left{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,3)] ,
                            "UP"    : [pygame.transform.scale(pygame.image.load(r"resources\enemies\cultist\up{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,3)] ,
                            "DOWN"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\cultist\down{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,3)] }

    attackingImages     = { "RIGHT" : [pygame.transform.scale(pygame.image.load(r"resources\enemies\cultist\attackright{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 4), int(TILE_HEIGHT * 4))) for i in range(1,6)] ,
                            "LEFT"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\cultist\attackleft{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 3.5), int(TILE_HEIGHT * 4))) for i in range(1,6)] ,
                            "UP"    : [pygame.transform.scale(pygame.image.load(r"resources\enemies\cultist\attackup{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 3))) for i in range(1,4)] ,
                            "DOWN"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\cultist\attackdown{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 3))) for i in range(1,4)] }
    attackingOffset     = { "RIGHT" : (0, 0)    ,
                            "LEFT"  : (-0.8, 0)    ,
                            "UP"    : (0, 0)    ,
                            "DOWN"  : (0, 0)    }
    
    def AI(self, mapList, bullets, players, enemies, activeFrames):
        def closestKey(dictionary, val): return dictionary.get(val, dictionary[min(dictionary.keys(), key=lambda k: abs(k-val))])
        grid = mapList.collisionMap
        newPlayers = [i if i else None for i in players]
        sortedPlayers = sorted(newPlayers, key=lambda p: ((self.x - p.x) ** 2) + ((self.y - p.y) ** 2), reverse=False)
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

                if ((self.x - p.x) ** 2) + ((self.y - p.y) ** 2) < 48:
                    self.attacking = True
                    self.attackCount = 0
##                    if lineCasting(grid, (self.x, self.y), (p.x, p.y), angle) == True:
##                        self.attacking = True
##                        self.attackCount = 0
##                    if self.direction in "LEFT RIGHT":
##                        mapList.meleeRects.append(AttackRect((self.x + (self.w // 2) * DIRECTION_KEY[self.direction][0]) * TILE_WIDTH,
##                                                             (self.y + (self.h // 2) * DIRECTION_KEY[self.direction][1]) * TILE_HEIGHT,
##                                                             self.worldX, self.worldY,
##                                                             self.w * 0.8 * TILE_WIDTH, self.h * 0.8 * TILE_HEIGHT, self.team, 40, range(15, 25), 25, PURPLE))
##                    elif self.direction in "UP DOWN":
##                        mapList.meleeRects.append(AttackRect(self.x * TILE_WIDTH,
##                                                             (self.y + ((self.h // 2) * DIRECTION_KEY[self.direction][1])) * TILE_HEIGHT,
##                                                             self.worldX, self.worldY,
##                                                             self.w * 0.8 * TILE_WIDTH, self.h * TILE_HEIGHT, self.team, 40, range(15, 25), 25, PURPLE))

        if self.attacking:
            self.attackCount += 0.1
            if self.attackCount >= 3:
                self.attacking = False
            if round(self.attackCount, 3) == 2.7:
                g = self.weapon
                angle = atan2((p.y - self.y), (p.x - self.x))
                angle %= 2 * pi
                for a in g.shots:
                    bullets.append(Bullet((self.x + (self.w / 2), self.y + (self.h / 2)), (self.worldX, self.worldY), g.bulletDmg,
                                          (angle) + ((a + randint(-g.deviation, g.deviation)) * (pi / 180)),
                                          self.team, g.speed, g.range, g.maxBounces, g.r, "darkmagic"))

class Skeleton(Enemy):
    images              = { "RIGHT" : [pygame.transform.scale(pygame.image.load(r"resources\enemies\skeleton\right{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,3)] ,
                            "LEFT"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\skeleton\left{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,3)] ,
                            "UP"    : [pygame.transform.scale(pygame.image.load(r"resources\enemies\skeleton\up{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,3)] ,
                            "DOWN"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\skeleton\down{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,3)] }

    attackingImages     = { "RIGHT" : [pygame.transform.scale(pygame.image.load(r"resources\enemies\skeleton\attackright{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,3)] ,
                            "LEFT"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\skeleton\attackleft{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,3)] ,
                            "UP"    : [pygame.transform.scale(pygame.image.load(r"resources\enemies\skeleton\attackup{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,7)] ,
                            "DOWN"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\skeleton\attackdown{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,7)] }
    attackingOffset     = { "RIGHT" : (0, 0)    ,
                            "LEFT"  : (0, 0)    ,
                            "UP"    : (0, 0)    ,
                            "DOWN"  : (0, 0)    }
    
    def AI(self, mapList, bullets, players, enemies, activeFrames):
        def closestKey(dictionary, val): return dictionary.get(val, dictionary[min(dictionary.keys(), key=lambda k: abs(k-val))])
        grid = mapList.collisionMap
        newPlayers = [i if i else None for i in players]
        sortedPlayers = sorted(newPlayers, key=lambda p: ((self.x - p.x) ** 2) + ((self.y - p.y) ** 2), reverse=False)
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

                if ((self.x - p.x) ** 2) + ((self.y - p.y) ** 2) < 48:
                    self.attacking = True
                    self.attackCount = 0
##                    if lineCasting(grid, (self.x, self.y), (p.x, p.y), angle) == True:
##                        self.attacking = True
##                        self.attackCount = 0
##                    if self.direction in "LEFT RIGHT":
##                        mapList.meleeRects.append(AttackRect((self.x + (self.w // 2) * DIRECTION_KEY[self.direction][0]) * TILE_WIDTH,
##                                                             (self.y + (self.h // 2) * DIRECTION_KEY[self.direction][1]) * TILE_HEIGHT,
##                                                             self.worldX, self.worldY,
##                                                             self.w * 0.8 * TILE_WIDTH, self.h * 0.8 * TILE_HEIGHT, self.team, 40, range(15, 25), 25, PURPLE))
##                    elif self.direction in "UP DOWN":
##                        mapList.meleeRects.append(AttackRect(self.x * TILE_WIDTH,
##                                                             (self.y + ((self.h // 2) * DIRECTION_KEY[self.direction][1])) * TILE_HEIGHT,
##                                                             self.worldX, self.worldY,
##                                                             self.w * 0.8 * TILE_WIDTH, self.h * TILE_HEIGHT, self.team, 40, range(15, 25), 25, PURPLE))

        if self.attacking:
            self.attackCount += 0.1
            if self.attackCount >= 3:
                self.attacking = False
            if round(self.attackCount, 3) == 2.7:
                g = self.weapon
                angle = atan2((p.y - self.y), (p.x - self.x))
                angle %= 2 * pi
                for a in g.shots:
                    bullets.append(Bullet((self.x + (self.w / 2), self.y + (self.h / 2)), (self.worldX, self.worldY), g.bulletDmg,
                                          (angle) + ((a + randint(-g.deviation, g.deviation)) * (pi / 180)),
                                          self.team, g.speed, g.range, g.maxBounces, g.r, "arrow1"))

class AirElemental(Enemy):
    images              = { "RIGHT" : [pygame.transform.scale(pygame.image.load(r"resources\enemies\airelemental\right{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,6)] ,
                            "LEFT"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\airelemental\left{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,6)] ,
                            "UP"    : [pygame.transform.scale(pygame.image.load(r"resources\enemies\airelemental\up{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,7)] ,
                            "DOWN"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\airelemental\down{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,7)] }

    attackingImages     = { "RIGHT" : [pygame.transform.scale(pygame.image.load(r"resources\enemies\airelemental\attackright{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 4), int(TILE_HEIGHT * 4))) for i in range(1,6)] ,
                            "LEFT"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\airelemental\attackleft{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 3.5), int(TILE_HEIGHT * 4))) for i in range(1,6)] ,
                            "UP"    : [pygame.transform.scale(pygame.image.load(r"resources\enemies\airelemental\attackup{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 3))) for i in range(1,6)] ,
                            "DOWN"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\airelemental\attackdown{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 3))) for i in range(1,6)] }
    attackingOffset     = { "RIGHT" : (-0.8, -1)    ,
                            "LEFT"  : (-1, -1)   ,
                            "UP"    : (0, -0.8) ,
                            "DOWN"  : (0, 0)    }
    
    def AI(self, mapList, bullets, players, enemies, activeFrames):
        def closestKey(dictionary, val): return dictionary.get(val, dictionary[min(dictionary.keys(), key=lambda k: abs(k-val))])
        grid = mapList.collisionMap
        newPlayers = [i if i else None for i in players]
        sortedPlayers = sorted(newPlayers, key=lambda p: ((self.x - p.x) ** 2) + ((self.y - p.y) ** 2), reverse=False)
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

                if ((self.x - p.x) ** 2) + ((self.y - p.y) ** 2) < 48:
                    self.attacking = True
                    self.attackCount = 0
##                    if lineCasting(grid, (self.x, self.y), (p.x, p.y), angle) == True:
##                        self.attacking = True
##                        self.attackCount = 0
##                    if self.direction in "LEFT RIGHT":
##                        mapList.meleeRects.append(AttackRect((self.x + (self.w // 2) * DIRECTION_KEY[self.direction][0]) * TILE_WIDTH,
##                                                             (self.y + (self.h // 2) * DIRECTION_KEY[self.direction][1]) * TILE_HEIGHT,
##                                                             self.worldX, self.worldY,
##                                                             self.w * 0.8 * TILE_WIDTH, self.h * 0.8 * TILE_HEIGHT, self.team, 40, range(15, 25), 25, PURPLE))
##                    elif self.direction in "UP DOWN":
##                        mapList.meleeRects.append(AttackRect(self.x * TILE_WIDTH,
##                                                             (self.y + ((self.h // 2) * DIRECTION_KEY[self.direction][1])) * TILE_HEIGHT,
##                                                             self.worldX, self.worldY,
##                                                             self.w * 0.8 * TILE_WIDTH, self.h * TILE_HEIGHT, self.team, 40, range(15, 25), 25, PURPLE))

        if self.attacking:
            self.attackCount += 0.1
            if self.attackCount >= 3:
                self.attacking = False
            if round(self.attackCount, 3) == 2.7:
                g = self.weapon
                angle = atan2((p.y - self.y), (p.x - self.x))
                angle %= 2 * pi
                for a in g.shots:
                    bullets.append(Bullet((self.x + (self.w / 2), self.y + (self.h / 2)), (self.worldX, self.worldY), g.bulletDmg,
                                          (angle) + ((a + randint(-g.deviation, g.deviation)) * (pi / 180)),
                                          self.team, g.speed, g.range, g.maxBounces, g.r, "air"))
                    
class FireElemental(Enemy):
    images              = { "RIGHT" : [pygame.transform.scale(pygame.image.load(r"resources\enemies\fireelemental\right{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,7)] ,
                            "LEFT"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\fireelemental\left{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,7)] ,
                            "UP"    : [pygame.transform.scale(pygame.image.load(r"resources\enemies\fireelemental\up{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,7)] ,
                            "DOWN"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\fireelemental\down{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,7)] }

    attackingImages     = { "RIGHT" : [pygame.transform.scale(pygame.image.load(r"resources\enemies\fireelemental\attackright{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 4), int(TILE_HEIGHT * 4))) for i in range(1,7)] ,
                            "LEFT"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\fireelemental\attackleft{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 3.5), int(TILE_HEIGHT * 4))) for i in range(1,7)] ,
                            "UP"    : [pygame.transform.scale(pygame.image.load(r"resources\enemies\fireelemental\attackup{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 3))) for i in range(1,7)] ,
                            "DOWN"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\fireelemental\attackdown{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 3))) for i in range(1,7)] }
    attackingOffset     = { "RIGHT" : (-0.8, -1)    ,
                            "LEFT"  : (-1, -1)   ,
                            "UP"    : (0, -0.8) ,
                            "DOWN"  : (0, 0)    }
    
    def AI(self, mapList, bullets, players, enemies, activeFrames):
        def closestKey(dictionary, val): return dictionary.get(val, dictionary[min(dictionary.keys(), key=lambda k: abs(k-val))])
        grid = mapList.collisionMap
        newPlayers = [i if i else None for i in players]
        sortedPlayers = sorted(newPlayers, key=lambda p: ((self.x - p.x) ** 2) + ((self.y - p.y) ** 2), reverse=False)
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

                if ((self.x - p.x) ** 2) + ((self.y - p.y) ** 2) < 48:
                    self.attacking = True
                    self.attackCount = 0
##                    if lineCasting(grid, (self.x, self.y), (p.x, p.y), angle) == True:
##                        self.attacking = True
##                        self.attackCount = 0
##                    if self.direction in "LEFT RIGHT":
##                        mapList.meleeRects.append(AttackRect((self.x + (self.w // 2) * DIRECTION_KEY[self.direction][0]) * TILE_WIDTH,
##                                                             (self.y + (self.h // 2) * DIRECTION_KEY[self.direction][1]) * TILE_HEIGHT,
##                                                             self.worldX, self.worldY,
##                                                             self.w * 0.8 * TILE_WIDTH, self.h * 0.8 * TILE_HEIGHT, self.team, 40, range(15, 25), 25, PURPLE))
##                    elif self.direction in "UP DOWN":
##                        mapList.meleeRects.append(AttackRect(self.x * TILE_WIDTH,
##                                                             (self.y + ((self.h // 2) * DIRECTION_KEY[self.direction][1])) * TILE_HEIGHT,
##                                                             self.worldX, self.worldY,
##                                                             self.w * 0.8 * TILE_WIDTH, self.h * TILE_HEIGHT, self.team, 40, range(15, 25), 25, PURPLE))

        if self.attacking:
            self.attackCount += 0.25
            if self.attackCount >= 3:
                self.attacking = False
            if self.attackCount == 2.75:
                g = self.weapon
                angle = atan2((p.y - self.y), (p.x - self.x))
                angle %= 2 * pi
                for a in g.shots:
                    bullets.append(Bullet((self.x + (self.w / 2), self.y + (self.h / 2)), (self.worldX, self.worldY), g.bulletDmg,
                                          (angle) + ((a + randint(-g.deviation, g.deviation)) * (pi / 180)),
                                          self.team, g.speed, g.range, g.maxBounces, g.r, "fire"))

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

    attackingOffset     = { "RIGHT" : (0, 0)    ,
                            "LEFT"  : (0, 0)    ,
                            "UP"    : (0, 0)    ,
                            "DOWN"  : (0, 0)    }
    
    def AI(self, mapList, bullets, players, enemies, activeFrames):
        def closestKey(dictionary, val): return dictionary.get(val, dictionary[min(dictionary.keys(), key=lambda k: abs(k-val))])
        grid = mapList.collisionMap
        newPlayers = [i if i else None for i in players]
        sortedPlayers = sorted(newPlayers, key=lambda p: ((self.x - p.x) ** 2) + ((self.y - p.y) ** 2), reverse=False)
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

##                angle = atan2((p.y - self.y), (p.x - self.x)) * (180 / pi)
##                nextX, nextY = pathfind(grid, (int(self.x + self.w), int(self.y + self.h)), (int(p.x + p.w), int(p.y + p.h)))[0]
##                angle = atan2((nextY - self.y), (nextX - self.x)) * (180 / pi)
##                angle %= 360
##                self.direction = closestKey(DIRECTIONS, angle)
##                angle *= (pi / 180)
##                moveX = cos(angle) * self.ms * self.slow
##                moveY = sin(angle) * self.ms * self.slow
##                if grid[int((self.x + (self.w / 2) + ((self.w / 2) * DIRECTION_KEY[self.direction][0])) + moveX)] \
##                   [int(self.y + (self.h / 2))] != 1: self.x += moveX
##                if grid[int(self.x + (self.w / 2))] \
##                   [int((self.y + (self.h / 2) + ((self.h / 2) * DIRECTION_KEY[self.direction][1])) + moveY)] != 1: self.y += moveY

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

class Zombie(Enemy):
    images              = { "RIGHT" : [pygame.transform.scale(pygame.image.load(r"resources\enemies\zombie\right{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,5)] ,
                            "LEFT"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\zombie\left{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,5)] ,
                            "UP"    : [pygame.transform.scale(pygame.image.load(r"resources\enemies\zombie\up{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,3)] ,
                            "DOWN"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\zombie\down{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,3)] }

    attackingImages     = { "RIGHT" : [pygame.transform.scale(pygame.image.load(r"resources\enemies\zombie\attackright{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,3)] ,
                            "LEFT"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\zombie\attackleft{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,3)] ,
                            "UP"    : [pygame.transform.scale(pygame.image.load(r"resources\enemies\zombie\attackup{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,3)] ,
                            "DOWN"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\zombie\attackdown{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,3)] }

    attackingOffset     = { "RIGHT" : (0, 0)    ,
                            "LEFT"  : (0, 0)    ,
                            "UP"    : (0, 0)    ,
                            "DOWN"  : (0, 0)    }
    
    def AI(self, mapList, bullets, players, enemies, activeFrames):
        def closestKey(dictionary, val): return dictionary.get(val, dictionary[min(dictionary.keys(), key=lambda k: abs(k-val))])
        grid = mapList.collisionMap
        newPlayers = [i if i else None for i in players]
        sortedPlayers = sorted(newPlayers, key=lambda p: ((self.x - p.x) ** 2) + ((self.y - p.y) ** 2), reverse=False)
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

##                angle = atan2((p.y - self.y), (p.x - self.x)) * (180 / pi)
##                nextX, nextY = pathfind(grid, (int(self.x + self.w), int(self.y + self.h)), (int(p.x + p.w), int(p.y + p.h)))[0]
##                angle = atan2((nextY - self.y), (nextX - self.x)) * (180 / pi)
##                angle %= 360
##                self.direction = closestKey(DIRECTIONS, angle)
##                angle *= (pi / 180)
##                moveX = cos(angle) * self.ms * self.slow
##                moveY = sin(angle) * self.ms * self.slow
##                if grid[int((self.x + (self.w / 2) + ((self.w / 2) * DIRECTION_KEY[self.direction][0])) + moveX)] \
##                   [int(self.y + (self.h / 2))] != 1: self.x += moveX
##                if grid[int(self.x + (self.w / 2))] \
##                   [int((self.y + (self.h / 2) + ((self.h / 2) * DIRECTION_KEY[self.direction][1])) + moveY)] != 1: self.y += moveY

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

class Ogre(Enemy):
    images              = { "RIGHT" : [pygame.transform.scale(pygame.image.load(r"resources\enemies\ogre\right{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,3)] ,
                            "LEFT"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\ogre\left{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,3)] ,
                            "UP"    : [pygame.transform.scale(pygame.image.load(r"resources\enemies\ogre\up{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,3)] ,
                            "DOWN"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\ogre\down{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,3)] }

    attackingImages     = { "RIGHT" : [pygame.transform.scale(pygame.image.load(r"resources\enemies\ogre\attackright{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,3)] ,
                            "LEFT"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\ogre\attackleft{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,3)] ,
                            "UP"    : [pygame.transform.scale(pygame.image.load(r"resources\enemies\ogre\attackup{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,2)] ,
                            "DOWN"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\ogre\attackdown{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,3)] }

    attackingOffset     = { "RIGHT" : (0, 0)    ,
                            "LEFT"  : (0, 0)    ,
                            "UP"    : (0, 0)    ,
                            "DOWN"  : (0, 0)    }
    
    def AI(self, mapList, bullets, players, enemies, activeFrames):
        def closestKey(dictionary, val): return dictionary.get(val, dictionary[min(dictionary.keys(), key=lambda k: abs(k-val))])
        grid = mapList.collisionMap
        newPlayers = [i if i else None for i in players]
        sortedPlayers = sorted(newPlayers, key=lambda p: ((self.x - p.x) ** 2) + ((self.y - p.y) ** 2), reverse=False)
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

##                angle = atan2((p.y - self.y), (p.x - self.x)) * (180 / pi)
##                nextX, nextY = pathfind(grid, (int(self.x + self.w), int(self.y + self.h)), (int(p.x + p.w), int(p.y + p.h)))[0]
##                angle = atan2((nextY - self.y), (nextX - self.x)) * (180 / pi)
##                angle %= 360
##                self.direction = closestKey(DIRECTIONS, angle)
##                angle *= (pi / 180)
##                moveX = cos(angle) * self.ms * self.slow
##                moveY = sin(angle) * self.ms * self.slow
##                if grid[int((self.x + (self.w / 2) + ((self.w / 2) * DIRECTION_KEY[self.direction][0])) + moveX)] \
##                   [int(self.y + (self.h / 2))] != 1: self.x += moveX
##                if grid[int(self.x + (self.w / 2))] \
##                   [int((self.y + (self.h / 2) + ((self.h / 2) * DIRECTION_KEY[self.direction][1])) + moveY)] != 1: self.y += moveY

                if ((self.x - p.x) ** 2) + ((self.y - p.y) ** 2) < 4.5:
                    self.attacking = True
                    self.attackCount = 0
                    self.damage += 5
                    if self.direction in "LEFT RIGHT":
                        mapList.meleeRects.append(AttackRect((self.x + (self.w // 2) * DIRECTION_KEY[self.direction][0]) * TILE_WIDTH,
                                                             (self.y + (self.h // 2) * DIRECTION_KEY[self.direction][1]) * TILE_HEIGHT,
                                                             self.worldX, self.worldY,
                                                             self.w * 0.8 * TILE_WIDTH, self.h * 0.8 * TILE_HEIGHT, self.team, self.damage, range(15, 20), 20, GREEN))
                    elif self.direction in "UP DOWN":
                        mapList.meleeRects.append(AttackRect(self.x * TILE_WIDTH,
                                                             (self.y + ((self.h // 2) * DIRECTION_KEY[self.direction][1])) * TILE_HEIGHT,
                                                             self.worldX, self.worldY,
                                                             self.w * 0.8 * TILE_WIDTH, self.h * TILE_HEIGHT, self.team, self.damage, range(15, 20), 20, GREEN))

        if self.attacking:
            self.attackCount += 0.1
            if self.attackCount >= 3:
                self.attacking = False

class Tentacle(Enemy):
    images              = { "RIGHT" : [pygame.transform.scale(pygame.image.load(r"resources\enemies\tentacle\attackright{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,2)] ,
                            "LEFT"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\tentacle\attackleft{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,2)] ,
                            "UP"    : [pygame.transform.scale(pygame.image.load(r"resources\enemies\tentacle\attackright{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,2)] ,
                            "DOWN"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\tentacle\attackleft{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,2)] }

    attackingImages     = { "RIGHT" : [pygame.transform.scale(pygame.image.load(r"resources\enemies\tentacle\attackright{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,4)] ,
                            "LEFT"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\tentacle\attackleft{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,4)] ,
                            "UP"    : [pygame.transform.scale(pygame.image.load(r"resources\enemies\tentacle\attackup{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,5)] ,
                            "DOWN"  : [pygame.transform.scale(pygame.image.load(r"resources\enemies\tentacle\attackdown{}".format(i) + ".png"),
                                                              (int(TILE_WIDTH * 2), int(TILE_HEIGHT * 2))) for i in range(1,5)] }

    attackingOffset     = { "RIGHT" : (0, 0)    ,
                            "LEFT"  : (0, 0)    ,
                            "UP"    : (-1, 0)   ,
                            "DOWN"  : (0, 0)    }
    
    def AI(self, mapList, bullets, players, enemies, activeFrames):
        def closestKey(dictionary, val): return dictionary.get(val, dictionary[min(dictionary.keys(), key=lambda k: abs(k-val))])
        grid = mapList.collisionMap
        newPlayers = [i if i else None for i in players]
        sortedPlayers = sorted(newPlayers, key=lambda p: ((self.x - p.x) ** 2) + ((self.y - p.y) ** 2), reverse=False)
        for p in sortedPlayers:
            if (p.worldX, p.worldY) == (self.worldX, self.worldY): break
        if not self.attacking:
            if (p.worldX, p.worldY) == (self.worldX, self.worldY):
                if ((self.x - p.x) ** 2) + ((self.y - p.y) ** 2) < 7:
                    angle = atan2((p.y - self.y), (p.x - self.x)) * (180 / pi)
                    angle %= 360
                    self.attacking = True
                    self.attackCount = 0
                    self.direction = closestKey(DIRECTIONS, angle)
                    if self.direction in "LEFT RIGHT":
                        mapList.meleeRects.append(AttackRect((self.x + (self.w // 2) * DIRECTION_KEY[self.direction][0]) * TILE_WIDTH,
                                                             (self.y + (self.h // 2) * DIRECTION_KEY[self.direction][1]) * TILE_HEIGHT,
                                                             self.worldX, self.worldY,
                                                             self.w * 0.8 * TILE_WIDTH, self.h * 1.3 * TILE_HEIGHT, self.team, self.damage, range(15, 20), 20, PURPLE))
                    elif self.direction in "UP DOWN":
                        mapList.meleeRects.append(AttackRect(self.x * TILE_WIDTH,
                                                             (self.y + ((self.h // 2) * DIRECTION_KEY[self.direction][1])) * TILE_HEIGHT,
                                                             self.worldX, self.worldY,
                                                             self.w * 1.3 * TILE_WIDTH, self.h * TILE_HEIGHT, self.team, self.damage, range(15, 20), 20, PURPLE))
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

    attackingOffset     = { "RIGHT" : (0, 0)    ,
                            "LEFT"  : (0, 0)    ,
                            "UP"    : (0, 0)    ,
                            "DOWN"  : (0, 0)    }
    
    def AI(self, mapList, bullets, players, enemies, activeFrames):
        self.w = 1
        self.h = 2
        def closestKey(dictionary, val): return dictionary.get(val, dictionary[min(dictionary.keys(), key=lambda k: abs(k-val))])
        grid = mapList.collisionMap
        newPlayers = [i if i else Player(1000, 1000, team, maxHealth) for i in players]
        sortedPlayers = sorted(newPlayers, key=lambda p: ((self.x - p.x) ** 2) + ((self.y - p.y) ** 2), reverse=False)
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

    attackingOffset     = { "RIGHT" : (0, 0)    ,
                            "LEFT"  : (0, 0)    ,
                            "UP"    : (0, 0)    ,
                            "DOWN"  : (0, 0)    }
    
    def AI(self, mapList, bullets, players, enemies, activeFrames):
        self.attackCount += 1
        if self.attackCount >= 30:
            self.attackCount = 0
            g = self.weapon
            for angle in g.shots:
                bullets.append(Bullet((self.x + (self.w / 2), self.y + (self.h / 2)), (self.worldX, self.worldY), g.bulletDmg,
                                      (randint(0, 360) * (180 / pi)) + ((angle + randint(-g.deviation, g.deviation)) * (pi / 180)),
                                      self.team, g.speed, g.range, g.maxBounces, g.r, "leaf"))
        grid = mapList.tileMap
        self.lastMove = [randint(-1, 2) if randint(0, 100) >= 98 else i for i in self.lastMove]
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
    def __init__(self, pos, worldPos, dmg, a, t, speed, bulletRange, maxBounces, r, image):
        self.x, self.y      = pos
        self.worldX, self.worldY                            = worldPos
        self.dmg            = dmg;          self.speed      = speed
        self.angle          = a
        self.dx, self.dy    = cos(self.angle), sin(self.angle)
        self.team           = t
        self.r              = r
        self.age            = 0
        self.range          = bulletRange
        self.bounces        = 0
        self.maxBounces     = maxBounces
        self.images         = bulletImages[image]

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
    def __init__(self, x, y, worldX, worldY, weapon, wType):
        self.x          = x
        self.y          = y
        self.worldX     = worldX
        self.worldY     = worldY
        self.w          = weapon
        self.name       = weapon.name
        self.wType      = wType
        self.display    = self.initWindow()

    def initWindow(self):
        def write(text, pos):
            w.blit(pygame.font.SysFont("monospace", 11).render(str(text), False, WHITEA),(pos[0], pos[1]))
            
        if self.wType == "ranged":
            w = pygame.Surface((201, 120), pygame.SRCALPHA)
            w.fill(BLACKA)
            pygame.draw.rect(w, BLACK, (0, 0, 201, 120), 1)
            
            write(self.name, (10, 10))
            write("Damage: {}".format(self.w.bulletDmg), (10, 25))
            write("Attacks per Second: {}".format(round(FPS_CAP / max(0.1, self.w.atkSpeed), 3)), (10, 40))
            write("Deviation: + or - {} Degrees".format(self.w.deviation), (10, 55))
            write("Weapon Type: {}".format(self.w.fireType), (10, 70))
            write("Bullet Size: {}".format(self.w.r), (10, 85))

        elif self.wType == "melee":
            w = pygame.Surface((201, 120), pygame.SRCALPHA)
            w.fill(BLACKA)
            pygame.draw.rect(w, BLACK, (0, 0, 201, 120), 1)
            
            write(self.name, (10, 10))
            write("Damage: {}".format(self.w.dmg), (10, 25))
            write("Attacks per Second: {}".format(round(FPS_CAP / max(0.1, self.w.atkSpeed), 3)), (10, 40))

        return w

# For when players and enemies shoot bullets
class Gun:
    def __init__(self, shots, name, rarity, speed, bulletRange, maxBounces, atkSpeed, deviation, dmg, r, slow, fireType, image, pos=(1, 1), state=1, weaponType="bow"):
        self.shots      = shots
        self.name       = name
        self.rarity     = rarity
        self.type       = weaponType
        self.speed      = speed
        self.range      = bulletRange
        self.maxBounces = maxBounces
        self.atkSpeed   = atkSpeed
        self.deviation  = deviation
        self.bulletDmg  = dmg
        self.fireType   = fireType
        self.image      = image
        self.r          = r
        self.slow       = slow
        self.pos        = pos
        self.state      = state
        self.rect       = (0.8, 0.8)

class Melee:
    def __init__(self, name, rarity, atkSpeed, dmg, w, h, colour, pos=(1, 1), weaponType="bow"):
        self.w = w
        self.h = h
        self.name = name
        self.rarity = rarity
        self.atkSpeed = atkSpeed
        self.dmg = dmg
        self.colour = colour
        self.type = weaponType
        self.pos = pos
        
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

# For the minimap display
class Minimap:
    def __init__(self, tileMap):
        self.image = self.loadImage(tileMap)

    def loadImage(self, tileMap):
        image = pygame.Surface((len(tileMap) * TILE_WIDTH, len(tileMap[0]) * TILE_HEIGHT), pygame.SRCALPHA)
        def write(text, pos):
            image.blit(pygame.font.SysFont("monospace", 11).render(str(text), False, BLACK),(pos[0], pos[1]))
        for j, column in enumerate(tileMap):
            for k, row in enumerate(column):
                if row == 1:
                    pygame.draw.rect(image, BLACKA, (j * TILE_WIDTH, k * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT))
                elif row == 0:
                    pygame.draw.rect(image, BROWNA, (j * TILE_WIDTH, k * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT))
                else:
                    pygame.draw.rect(image, DIFFICULTY_COLOURS[row.difficulty], (j * TILE_WIDTH, k * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT))
                    write(row.difficulty, (j * TILE_WIDTH, k * TILE_HEIGHT))

        return image

# Shows melee attacks and checks for their collision with the player
class AttackRect:
    def __init__(self, x, y, wx, wy, w, h, team, d, af, l, c):
        self.rect           = pygame.Rect((x, y, w, h))
        self.team           = team
        self.worldX, self.worldY = wx, wy
        self.damage         = d
        self.activeFrames   = af
        self.colour         = c
        self.frames         = 0
        self.length         = l
        self.delete         = False
        self.hit            = []

    def update(self, players, tileMapList):
        self.frames += 1
        for p in players:
            mapList = tileMapList[p.worldX][p.worldY]
            entities = players + mapList.enemies + mapList.boss
            for i,e in enumerate(entities):
                if self.rect.colliderect(pygame.Rect((e.x * TILE_WIDTH, e.y * TILE_HEIGHT, e.w * TILE_HEIGHT, e.h * TILE_WIDTH))):
                    if self.frames in self.activeFrames:
                        if not i in self.hit and self.team != e.team:
                            e.health -= self.damage
                            self.hit.append(i)
        if self.frames >= self.length:
            self.delete = True

WEAPONS = { "sword"     : { 1   : Weapon(8, 8, 1, 1, Melee("Basic Sword", 1, 15, 30, 1.5, 1.8, GREY, weaponType="sword"), "melee"),
                            2   : Weapon(8, 8, 1, 1, Melee("Bronze Longsword", 2, 15, 45, 1.5, 1.8, ORANGE, weaponType="sword"), "melee"),
                            3   : Weapon(8, 8, 1, 1, Melee("Skeletal Blade", 3, 15, 75, 1.5, 1.8, GREY, weaponType="sword"), "melee"),
                            4   : Weapon(8, 8, 1, 1, Melee("Venomshank", 4, 15, 100, 1.5, 1.8, GREEN, weaponType="sword"), "melee"),
                            5   : Weapon(8, 8, 1, 1, Melee("Corpsemaker", 5, 15, 150, 1.5, 1.8, BLACK, weaponType="sword"), "melee"),
                            "j" : Weapon(8, 8, 1, 1, Melee("Crowbar", "j", 15, 150, 1.5, 1.8, RED, weaponType="sword"), "melee"),
                            "s" : Weapon(8, 8, 1, 1, Melee("Allbiter", "s", 15, 180, 1.5, 1.8, BROWN, weaponType="sword"), "melee")} ,

            "gauntlet"  : { 1   : Weapon(8, 8, 1, 1, Melee("Basic Gauntlets", 1, 20, 30, 1, 1.3, RED, weaponType="gauntlet"), "melee"),
                            2   : Weapon(8, 8, 1, 1, Melee("Bronze Gauntlets", 2, 20, 40, 1, 1.4, RED, weaponType="gauntlet"), "melee"),
                            3   : Weapon(8, 8, 1, 1, Melee("Silver Gauntlets", 3, 20, 55, 1.1, 1.5, RED, weaponType="gauntlet"), "melee"),
                            4   : Weapon(8, 8, 1, 1, Melee("Golden Gauntlets", 4, 20, 75, 1.1, 1.6, RED, weaponType="gauntlet"), "melee"),
                            5   : Weapon(8, 8, 1, 1, Melee("Onyx Gauntlets", 5, 20, 100, 1.2, 1.6, RED, weaponType="gauntlet"), "melee"),
                            "j" : Weapon(8, 8, 1, 1, Melee("Oven Mitts", "j", 20, 100, 1.2, 1.6, RED, weaponType="gauntlet"), "melee"),
                            "s" : Weapon(8, 8, 1, 1, Melee("Cataclysmic Gauntlets", "s", 15, 120, 1.3, 1.7, RED, weaponType="gauntlet"), "melee")} ,

            "spear"     : { 1   : Weapon(8, 8, 1, 1, Gun([0],  "Wooden Spear", 1, 0.5, 80, 0, 45, 5, 30, 0.1, 0.9, "auto", "spear1",weaponType="spear"), "ranged"),
                            2   : Weapon(8, 8, 1, 1, Gun([0],  "Halberd", 2, 0.5, 90, 0, 40, 0, 45, 0.1, 0.9, "auto", "spear2",weaponType="spear"), "ranged"),
                            3   : Weapon(8, 8, 1, 1, Gun([0],  "Gungnir", 3, 0.5, 100, 0, 35, 0, 70, 0.1, 0.9, "auto", "spear3",weaponType="spear"), "ranged"),
                            4   : Weapon(8, 8, 1, 1, Gun([0],  "Ascalon", 4, 0.5, 110, 0, 30, 0, 85, 0.1, 0.9, "auto", "spear4",weaponType="spear"), "ranged"),
                            5   : Weapon(8, 8, 1, 1, Gun([0],  "Trident", 5, 0.5, 120, 0, 25, 0, 100, 0.1, 0.9, "auto", "spear5",weaponType="spear"), "ranged"),
                            "j" : Weapon(8, 8, 1, 1, Gun([0],  "Toothpick", "j", 0.5, 130, 0, 20, 0, 115, 0.1, 0.9, "auto", "spear6",weaponType="spear"), "ranged"),
                            "s" : Weapon(8, 8, 1, 1, Gun([0],  "Bloodforged Warspear", "s", 0.5, 150, 0, 15, 0, 135, 0.1, 0.9, "auto", "spear7",weaponType="spear"), "ranged")} ,

            "bow"       : { 1   : Weapon(8, 8, 1, 1, Gun([0],  "Basic Bow", 1, 0.5, 80, 0, 25, 5, 25, 0.1, 0.9, "auto", "arrow1",weaponType="bow"), "ranged") ,
                            2   : Weapon(8, 8, 1, 1, Gun([0],  "Yew Bow", 2, 0.5, 80, 0, 24, 4, 30, 0.1, 0.9, "auto", "arrow2",weaponType="bow"), "ranged") ,
                            3   : Weapon(8, 8, 1, 1, Gun([0],  "Short Bow", 3, 0.7, 70, 0, 20, 4, 30, 0.1, 0.9, "auto", "arrow3",weaponType="bow"), "ranged") ,
                            4   : Weapon(8, 8, 1, 1, Gun([0],  "Long Bow", 4, 0.7, 120, 0, 30, 3, 60, 0.1, 0.9, "auto", "arrow4",weaponType="bow"), "ranged") ,
                            5   : Weapon(8, 8, 1, 1, Gun([0],  "Crossbow", 5, 0.9, 140, 0, 45, 0, 80, 0.1, 0.6, "auto", "arrow5",weaponType="bow"), "ranged") ,
                            "j" : Weapon(8, 8, 1, 1, Gun([0],  "Slingshot", "j", 0.4, 69, 0, 40, 8, 50, 0.1, 1, "auto", "arrow6",weaponType="bow"), "ranged") ,
                            "s" : Weapon(8, 8, 1, 1, Gun([-15,0,15], "Bow of Unsung Heroes", "s", 0.8, 100, 1, 15, 0, 75, 0.1, 1, "auto", "arrow7",weaponType="bow"), "ranged")} ,

            "gun"       : { 1   : Weapon(8, 8, 1, 1, Gun([0],  "Basic Gun", 1, 0.8, 65, 0, 20, 8, 50, 0.1, 1, "auto", "bullet1",weaponType="gun"), "ranged") ,
                            2   : Weapon(8, 8, 1, 1, Gun([0],  "Storm-Forged Blaster", 2, 0.4, 80, 0, 18, 8, 50, 0.1, 1, "auto", "bullet2",weaponType="gun"), "ranged") ,
                            3   : Weapon(8, 8, 1, 1, Gun([0],  "Autocannon", 3, 0.8, 90, 0, 16, 8, 50, 0.1, 1, "auto", "bullet3",weaponType="gun"), "ranged") ,
                            4   : Weapon(8, 8, 1, 1, Gun([0],  "Phase Blaster", 4, 0.8, 100, 0, 15, 8, 50, 0.1, 1, "auto", "bullet4",weaponType="gun"), "ranged") ,
                            5   : Weapon(8, 8, 1, 1, Gun([0],  "Photon Pulse Rifle", 5, 0.9, 160, 0, 35, 8, 50, 0.1, 1, "auto", "bullet5",weaponType="gun"), "ranged") ,
                            "j" : Weapon(8, 8, 1, 1, Gun([0],  "NORF Gun", "j", 0.8, 90, 0, 40, 8, 50, 0.1, 1, "auto", "bullet6",weaponType="gun"), "ranged") ,
                            "s" : Weapon(8, 8, 1, 1, Gun([0],  "Bernadetta", "s", 0.9, 140, 0, 20, 8, 50, 0.1, 1, "auto", "bullet7",weaponType="gun"), "ranged") } }

def newObject(weapon):
    return Weapon(weapon.x, weapon.y, weapon.worldX, weapon.worldY, weapon.w, weapon.wType)

# Possible enemies for each difficulty level room
ENEMIES = { 3 : [EarthElemental(400, 0.1, 5, 25, {0 : WEAPONS["bow"][4], 25 : WEAPONS["gauntlet"][3], 50 : WEAPONS["gauntlet"][2], 90 : WEAPONS["sword"][3], 100 : WEAPONS["gun"]["s"]},
                                gun = Gun([0], "Rock", 0, 0.2, 100, 2, 25, 0, 10, 0.2, 1, "semi", "rock")),
                 FireElemental(200, 0.08, 5, 25, {0 : WEAPONS["gun"]["s"], 10 : WEAPONS["gun"][4], 50 : WEAPONS["spear"][5], 75 : WEAPONS["spear"][4], 100 : WEAPONS["sword"][3]},
                                gun = Gun([0], "Fire", 0, 0.5, 100, 2, 25, 0, 25, 0.2, 0, "semi", "fire")),
                 AirElemental(320, 0.08, 5, 25, {0 : WEAPONS["gun"]["j"], 15 : WEAPONS["bow"][4], 50 : WEAPONS["bow"][3], 75 : WEAPONS["spear"][4], 100 : WEAPONS["spear"][3]},
                                gun = Gun([0], "Fire", 0, 0.2, 100, 2, 25, 0, 25, 0.2, 1, "semi", "air"))] ,
            1 : [Goblin(150, 0.1, 5, 25, {0 : WEAPONS["bow"][1], 15 : WEAPONS["sword"][2], 50 : WEAPONS["gauntlet"][1], 75 : WEAPONS["spear"][1], 100 : WEAPONS["spear"][2]}),
                 Ogre(250, 0.14, 5, 15, {0 : WEAPONS["sword"][1], 40 : WEAPONS["sword"][2], 60 : WEAPONS["gauntlet"][1], 85 : WEAPONS["gauntlet"][2], 100 : WEAPONS["sword"][3]}),
                 Saladmander(50, 0.03, 0, 0, {0 : WEAPONS["bow"][1], 15 : WEAPONS["gauntlet"][1], 50 : WEAPONS["gauntlet"][2], 75 : WEAPONS["sword"][1], 100 : WEAPONS["gun"][1]},
                             gun=Gun([-5, 0, 5],    "Spread Fire", 0, 0.4, 100, 2, 10, 0, -5, 0.2, 1, "semi", "leaf"))] ,
            2 : [WillOTheWisp(180, 0.08, 5, 45, {0 : WEAPONS["gun"][1], 15 : WEAPONS["gun"][2], 50 : WEAPONS["sword"][1], 75 : WEAPONS["sword"][2], 100 : WEAPONS["gun"]["j"]}),
                 Zombie(250, 0.06, 5, 75, {0 : WEAPONS["gun"][2], 15 : WEAPONS["spear"][2], 50 : WEAPONS["spear"][1], 75 : WEAPONS["sword"][3], 100 : WEAPONS["sword"][2]}),
                 Skeleton(150, 0.1, 5, 25, {0 : WEAPONS["bow"][3], 25 : WEAPONS["bow"][2], 50 : WEAPONS["bow"][1], 90 : WEAPONS["spear"][2], 100 : WEAPONS["sword"][2]},
                                gun = Gun([0], "Rock", 0, 0.2, 100, 2, 30, 0, 50, 0.2, 1, "semi", "arrow1"))] ,
            4 : [Tentacle(250, 0, 5, 100, {0 : WEAPONS["bow"]["s"], 15 : WEAPONS["sword"]["s"], 50 : WEAPONS["bow"][5], 75 : WEAPONS["sword"][5], 100 : WEAPONS["gun"][5]}),
                 Wizard(200, 0.08, 5, 25, {0 : WEAPONS["gun"]["s"], 15 : WEAPONS["bow"][5], 50 : WEAPONS["gun"][5], 75 : WEAPONS["gun"]["j"], 100 : WEAPONS["spear"][5]},
                                gun = Gun([0], "Fire", 0, 0.2, 100, 2, 25, 0, 100, 0.2, 1, "semi", "magic"))] ,
            5 : [Voidling(250, 0.08, 5, 25, {0 : WEAPONS["gun"][5], 15 : WEAPONS["gauntlet"][5], 50 : WEAPONS["gauntlet"]["j"], 75 : WEAPONS["bow"]["s"], 100 : WEAPONS["sword"]["s"]}),
                 Cultist(200, 0.06, 5, 25, {0 : WEAPONS["gun"]["s"], 15 : WEAPONS["bow"]["s"], 50 : WEAPONS["gun"][5], 75 : WEAPONS["spear"]["s"], 100 : WEAPONS["gauntlet"]["s"]},
                                gun = Gun([0], "Fire", 0, 0.2, 100, 2, 25, 0, 120, 0.2, 1, "semi", "darkmagic"))] }

##screen = pygame.display.set_mode((200, 200))
##screen.fill(WHITE)
##testItem = Weapon(1, 1, 1, 1, Gun([i / 2 for i in range(-31, 30)], "Fan Shot", 0, 0.4, 80, 0, 12, 0, 2, 0.1, 1, "semi", "rock"), "ranged")
##screen.blit(testItem.display, (0, 0))
##pygame.display.update()

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
        self.items                              = []
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
