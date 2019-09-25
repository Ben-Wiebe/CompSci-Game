from math import *
from random import *
from settings import *
from classes import *
import pygame

def getAngle(x1,y1,x2,y2):
    return atan2((y2 - y1), (x2 - x1))

def distance(x1, y1, x2, y2):
    return ((x2 - x1) ** 2) + ((y2 - y1) ** 2) ** 0.5

def updateBullets(grid, b, players):
    def playerCollision(bullet, x, y):
        for player in players:
            hitbox = pygame.Rect((player.x * TILE_WIDTH, player.y * TILE_HEIGHT, player.w * TILE_WIDTH, player.h * TILE_HEIGHT))
            #if hitbox.collidepoint((x * TILE_WIDTH, y * TILE_HEIGHT)) and bullet.team != player.team:
            if hitbox.colliderect(((x - bullet.r) * TILE_WIDTH, (y - bullet.r) * TILE_HEIGHT, bullet.r * 2 * TILE_WIDTH, bullet.r * 2 * TILE_HEIGHT)) \
                and (bullet.team != player.team) and ((bullet.worldX, bullet.worldY) == (player.worldX, player.worldY)):
                b.remove(bullet)
                player.health -= bullet.dmg
                players[bullet.team].onHit(player, bullet)
                if player.health <= 0:
                    if not player.onDeath(): players.remove(player)
                return True
        
    for bullet in b:
        checks  = round(bullet.speed * 10)
        moveX   = cos(bullet.angle) * (bullet.speed / checks)
        moveY   = sin(bullet.angle) * (bullet.speed / checks)
        for i in range(checks):
            movedX = bullet.x + moveX
            movedY = bullet.y + moveY
            if playerCollision(bullet, movedX, movedY): break
            if bullet.age > bullet.range: b.remove(bullet); break
            if bullet.bounces > bullet.maxBounces: b.remove(bullet); break
            if grid[bullet.worldX][bullet.worldY].tileMap[int(bullet.y)][int(movedX)] != 1: bullet.x = movedX
            else:                                                                           bullet.collide('y'); break
            if grid[bullet.worldX][bullet.worldY].tileMap[int(movedY)][int(bullet.x)] != 1: bullet.y = movedY
            else:                                                                           bullet.collide('x'); break
        bullet.age += 1

def shoot(bullets, p, a):
    g = p.weapon.w
    if p.shotCooldown >= g.atkSpeed:
        for angle in g.shots:
            bullets.append(Bullet((p.x + (p.w / 2), p.y + (p.h / 2)), (p.worldX, p.worldY), g.bulletDmg,
                                  a + ((angle + randint(-g.deviation, g.deviation)) * (pi / 180)),
                                  p.team, g.speed, g.range, g.maxBounces, g.r))
        p.shotCooldown = 0

def AI(players, grid, bullets):
    for p in players:
        if p.computer:
            p.d = [randint(0,1) if randint(0,15) == 1 else p.d[i] for i in range(4)]
            if p.d[0]:
                if not grid[int((p.y + (p.h / 2)) - (p.h / 2))][int(p.x + (p.w / 2))]: p.y -= p.ms * p.slow
                else: p.d[0] = 0; p.d[1] = 1

            if p.d[1]:
                if not grid[int((p.y + (p.h / 2)) + (p.h / 2))][int(p.x + (p.w / 2))]: p.y += p.ms * p.slow
                else: p.d[1] = 0; p.d[0] = 1

            if p.d[2]:
                if not grid[int(p.y + (p.h / 2))][int((p.x + (p.w / 2)) - (p.w / 2))]: p.x -= p.ms * p.slow
                else: p.d[2] = 0; p.d[3] = 1

            if p.d[3]:
                if not grid[int(p.y + (p.h / 2))][int((p.x + (p.w / 2)) + (p.w / 2))]: p.x += p.ms * p.slow
                else: p.d[3] = 0; p.d[2] = 1

            expected = [0, 0]
            if (players[0].worldX, players[0].worldY) == (p.worldX, p.worldY):
                playerAngle = getAngle(p.x, p.y, players[0].x + expected[0], players[0].y + expected[1])
                shoot(bullets, p, playerAngle)     
                p.slow = p.weapon.w.slow
            
def initializeRooms(grid):
    w = grid
    for i, y in enumerate(grid):
        for j, x in enumerate(y):
            #if x == 0:
            w[i][j] = Room(choice(ROOMS))

    for i, y in enumerate(grid):
        for j, room in enumerate(y):
            pass
    
    return w
