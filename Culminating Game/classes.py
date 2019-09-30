from math import pi, sin, cos
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
        self.w              = 0.8
        self.h              = 0.8
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
        self.spec           = {"lifesteal" : 0, "missingHpHeal" : 0, "revive" : True, "currentHealthDmg" : 0, "missingHpDmg" : 0, "playerHpBonus" : 0}

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
            #self.spec["revive"] = False
            return True

    def toggleDisplay(self):
        if self.display == True:    self.display = False
        else:                       self.display = True

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

class Melee:
    def __init__(self):
        #self.w, self.h      = d
        self.atkSpeed       = 1
        self.image          = None
        self.rect           = (0.8, 0.8)#[(15, 15),(15, 15),(15, 15),(15, 15),(15, 15),(15, 15),(15, 15)]

class Room:
    def __init__(self, tileMap):
        self.tileMap    = tileMap
        self.image      = self.initRoom()
        self.difficulty = None

    def initRoom(self):
        w = pygame.Surface((len(self.tileMap[0]) * TILE_WIDTH, len(self.tileMap) * TILE_HEIGHT))

        for j, column in enumerate(self.tileMap):
            for k, row in enumerate(column):
                if row == 1:
                    colour = GREY
                elif row == 0:
                    colour = BROWN
                else:
                    colour = BLACK
           
                pygame.draw.rect(w,  colour, (TILE_HEIGHT * k, TILE_WIDTH * j, TILE_WIDTH, TILE_HEIGHT))

        return w
