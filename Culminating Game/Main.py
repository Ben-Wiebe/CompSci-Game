import  pygame
from    math       import *
from    random     import *
from    settings   import *
from    classes    import *    
from    functions  import *
from    Maze       import generate
from    time       import sleep
pygame.init()

screen = pygame.display.set_mode(RESOLUTION, pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.FULLSCREEN)
clock = pygame.time.Clock()

mapList = [ [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] ,
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1] ,
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1] ,
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1] ,
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1] ,
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1] ,
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1] ,
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1] ,
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1] ,
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1] ,
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1] ,
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1] ,
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1] ,
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1] ,
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1] ,
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1] ,
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1] ,
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1] ,
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1] ,
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1] ,
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1] ,
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1] ,
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1] ,
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1] ,
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] ]

#mapList  = [[1 if x == 0 or y == 0 or x == 24 or y == 24 else 0 for x in range(25)] for y in range(25)]
mapList = generate(9,9)

minimap      = Room(mapList, mapList)

tileMapList  = []

mapDisplay   = [ pygame.Surface((HALF_RES[0], HALF_RES[1])) ,
                 pygame.Surface((HALF_RES[0], HALF_RES[1])) ,
                 pygame.Surface((HALF_RES[0], HALF_RES[1])) ,
                 pygame.Surface((HALF_RES[0], HALF_RES[1])) ]

#             Gun([Angles for each bullet], gun name, rarity level(0-4),
#                 speed, range, bounces, atk speed, deviation, damage, radius, slow, shot type)
spreadFire  = Weapon(Gun([-10, 0, 10], "Spread Fire", 0,
                  0.4,  100,    2,  10, 0,  15,     0.2,    1,      "semi"), "ranged")
superSpread = Weapon(Gun([i / 2 for i in range(-31, 30)], "Fan Shot", 0,
                  0.4,  80,     0,  12, 0,  2,      0.1,    1,      "semi"), "ranged")
burst       = Weapon(Gun([i / 10 for i in range(-26,25)], "Burst Fire", 0,
                  0.5,  80,     0,  15, 0,  1,      0.2,    1,      "semi"), "ranged")
tripleBurst = Weapon(Gun([i / 2 for i in range(-46, -35)] + [i / 2 for i in range(-9, 8)] + [i / 2 for i in range(34, 45)], "Triple Spread", 0,
                  0.3,  80,     0,  20, 0,  3,      0.1,    1,      "semi"), "ranged")
minigun     = Weapon(Gun([0], "Minigun", 0,
                  0.4,  80,     1,  2,  3,  8,      0.1,    0.4,    "auto"), "ranged")
bouncey     = Weapon(Gun([0], "Bounce Shot", 0,
                  0.3,  600,    12, 12, 2,  25,     0.4,    1,      "semi"), "ranged")
sniper      = Weapon(Gun([0], "Sniper", 0,
                  1.5,  800,    0,  40, 0,  75,     0.1,    1,      "semi"), "ranged")
shotgun     = Weapon(Gun([-3, -2, -1, -1, 0, 1, 1, 2, 3], "Shotgun", 0,
                  0.4,  20,     0,  60, 2,  15,     0.1,    1,      "semi"), "ranged")
lasergun    = Weapon(Gun([0], "Laser Gun", 0,
                  0.25, 25,     0,  1,  0,  3,      0.2,    0.3,    "auto"), "ranged")
plasma      = Weapon(Gun([i for i in range(-5, 5)], "Plasma Fire", 0,
                  0.25, 25,     0,  0,  0,  1,      0.3,    0,      "auto"), "ranged")

#players = [Player(1.2, 1.2, 0, 300), Player(2, 2, 1, 300), Player(3, 3, 1, 300), Player(4, 4, 1, 300)]
##roundTrig = [sin((i / 10)) for i in range(round(20*pi))]
##trigTable = {}

def write(text, pos):
    screen.blit(pygame.font.SysFont('monospace', 20).render(str(text), False, WHITE),(pos[0], pos[1]))
            
def draw(grid, tileMapList, players, enemies, bullets, seeItems, guns, updated, activeFrames):
    global mapDisplay
    screen.fill(BLACK)
##    bulletOverlays  = {0 : pygame.Surface((HALF_RES[0], HALF_RES[1]), pygame.SRCALPHA), 1 : None, 2 : None, 3 : None}
##    for i,player in enumerate(players):
##        if (player.worldX, player.worldY) == (players[i].worldX, players[i].worldY):
##            bulletOverlays[i] = bulletOverlays[0]
##    
##    for bullet in bullets:
##        if (bullet.worldX, bullet.worldY) == (player.worldX, player.worldY):
##            pygame.draw.circle(bulletOverlay[i],    WHITE, (round(bullet.x *  TILE_WIDTH) + DISPLAY_KEY[i][0],
##                                                    round(bullet.y * TILE_HEIGHT) + DISPLAY_KEY[i][1]),
##                                                    round(bullet.r * TILE_WIDTH))
    for i, player in enumerate(players):
        mapDisplay[i].fill(BLACK)
        m = tileMapList[player.worldX][player.worldY]
        mapDisplay[i].blit(m.image, (0, 0))
        mapDisplay[i].blit(m.overlay[int(activeFrames) % 2], (0,0))
              
        screen.blit(mapDisplay[i], DISPLAY_KEY[i])

        write("{:^3}/{:^3} HP".format(player.health, player.maxHealth), (DISPLAY_KEY[i][0] + HALF_RES[0] - 175, DISPLAY_KEY[i][1] + 30, 150, 25))
##        pygame.draw.rect(screen, RED, (DISPLAY_KEY[i][0] + HALF_RES[0] - 175, DISPLAY_KEY[i][1] + 30, 150, 25))
##        pygame.draw.rect(screen, GREEN, (DISPLAY_KEY[i][0] + HALF_RES[0] - 175, DISPLAY_KEY[i][1] + 30,
##                                         max(1, player.health * ((175 * TILE_WIDTH + (175 * TILE_WIDTH)) / player.maxHealth)), 25))

        for bullet in bullets:
            if (bullet.worldX, bullet.worldY) == (player.worldX, player.worldY):
                pygame.draw.circle(screen,   WHITE, (round(bullet.x *  TILE_WIDTH) + DISPLAY_KEY[i][0],
                                                     round(bullet.y * TILE_HEIGHT) + DISPLAY_KEY[i][1]),
                                                     round(bullet.r * TILE_WIDTH))
        for e in enemies:
            if (e.worldX, e.worldY) == (player.worldX, player.worldY):
                if not e.attacking:
                    screen.blit(e.images[e.direction][int(e.moveCount) % len(e.images[e.direction])],
                                ((e.x * TILE_WIDTH) + DISPLAY_KEY[i][0], (e.y * TILE_HEIGHT) + DISPLAY_KEY[i][1]))
                else:
                    screen.blit(e.attackingImages[e.direction][int(e.attackCount)],
                                ((e.x * TILE_WIDTH) + DISPLAY_KEY[i][0], (e.y * TILE_HEIGHT) + DISPLAY_KEY[i][1]))
        for p in players:
            if (p.worldX, p.worldY) == (player.worldX, player.worldY):
                screen.blit(p.images[p.direction][int(p.moveCount) % len(p.images[p.direction])],
                            ((p.x * TILE_WIDTH) + DISPLAY_KEY[i][0], (p.y * TILE_HEIGHT) + DISPLAY_KEY[i][1]))

        if player.display == True:
            screen.blit(minimap.image, DISPLAY_KEY[i])
            pygame.draw.rect(screen, WHITE, (player.worldX * TILE_WIDTH, player.worldY * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT))

        pygame.draw.line(screen, GREY, (0, HALF_RES[1]), (RESOLUTION[0], HALF_RES[1]), 5)
        pygame.draw.line(screen, GREY, (HALF_RES[0], 0), (HALF_RES[0], RESOLUTION[1]), 5)
            
    pygame.display.update()

def startGame(mapList, tileMapList):
    return initializeRooms(mapList)

def main():
    players = [Player(1.2, 1.2, 0, 150), Player(1.2, 22.8, 1, 150), Player(22.8, 1.2, 1, 150), Player(22.8, 22.8, 1, 150)]

    player      = players[0]
    seeItems    = False
    xChange = 0; yChange = 0
    bullets     = []
    enemies     = [Voidling(12,12,1,1,150,0.12,10,10)]
    guns        = [minigun, spreadFire]
    #guns[1].pos = (10, 10)
    update      = False
    for p in players:
        p.weapon   = minigun
    player.computer = False
    firing = False
    activeFrames = 0
    draw(mapList, tileMapList, players, enemies, bullets, seeItems, guns, True, activeFrames)
    while True:
        m = tileMapList[player.worldX][player.worldY]
        draw(mapList, tileMapList, players, enemies, bullets, seeItems, guns, update, activeFrames)
        update = False
        moved = False
        activeFrames += 0.1
        pygame.display.update()
        clock.tick(FPS_CAP)
        g = player.weapon.w
        pygame.display.set_caption("{} FPS".format(int(clock.get_fps())))
        for p in players:
            if p.shotCooldown < p.weapon.w.atkSpeed: p.shotCooldown += 1
        for event in pygame.event.get():
            if event.type    == pygame.QUIT: pygame.quit(); return
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    if tileMapList[player.worldY - 1][player.worldX] != 1: player.worldY -= 1
                elif event.key == pygame.K_DOWN:
                    if tileMapList[player.worldY + 1][player.worldX] != 1: player.worldY += 1
                elif event.key == pygame.K_RIGHT:
                    if tileMapList[player.worldY][player.worldX + 1] != 1: player.worldX += 1
                elif event.key == pygame.K_LEFT:
                    if tileMapList[player.worldY][player.worldX - 1] != 1: player.worldX -= 1
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if player.weapon.wType == "melee":
                    player.attacking = True
                    if player.attackFrames == len(player.weapon.w.rect): player.attackFrames = 0
                    player.attackFrames += 1
                    hitbox = pygame.Rect(((player.x + DIRECTION_KEY[player.direction][0]) * TILE_WIDTH,
                                          (player.y + DIRECTION_KEY[player.direction][1]) * TILE_HEIGHT),
                                         player.weapon.w.rect)
                    for p in players:
                        if (p.worldX, p.worldY) == (player.worldX, player.worldY) and p.team != player.team:
                            playerBox = pygame.Rect((p.x * TILE_WIDTH, p.y * TILE_HEIGHT, p.w * TILE_WIDTH, p.h * TILE_HEIGHT))
                            if hitbox.colliderect(playerBox):
                                p.health -= 50
                    
                if player.weapon.wType == "ranged":
                    if event.button == 1:
                        if g.fireType == "auto":    firing = True
                        else:
                            firing = False
                            pos = pygame.mouse.get_pos()
                            clickAngle = getAngle(((player.x + (player.w / 2)) * TILE_WIDTH),
                                                  ((player.y + (player.h / 2)) * TILE_HEIGHT),
                                                  pos[0],
                                                  pos[1])
                            shoot(bullets, player, clickAngle)
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                if player.weapon.wType == "ranged":
                    if event.button == 1:
                        firing = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.direction = "UP"
            if not m.collisionMap[int((player.y + (player.h / 2)) - (player.h / 2))][int(player.x + (player.w / 2))]:
                player.y -= player.ms * player.slow
                if not moved: player.moveCount += 0.25; moved = True

        if keys[pygame.K_s]:
            player.direction = "DOWN"
            if not m.collisionMap[int((player.y + (player.h / 2)) + (player.h / 2))][int(player.x + (player.w / 2))]:
                player.y += player.ms * player.slow
                if not moved: player.moveCount += 0.25; moved = True

        if keys[pygame.K_a]:
            player.direction = "LEFT"
            if not m.collisionMap[int(player.y + (player.h / 2))][int((player.x + (player.w / 2)) - (player.w / 2))]:
                player.x -= player.ms * player.slow
                if not moved: player.moveCount += 0.25; moved = True
                
        if keys[pygame.K_d]:
            player.direction = "RIGHT"
            if not m.collisionMap[int(player.y + (player.h / 2))][int((player.x + (player.w / 2)) + (player.w / 2))]:
                player.x += player.ms * player.slow
                if not moved: player.moveCount += 0.25; moved = True

        #print(tileMapList)
        updateBullets(tileMapList, bullets, players, enemies)
        #updateMines(mines, players)
        if firing and g.fireType == "auto":
            pos = pygame.mouse.get_pos()
            clickAngle = getAngle(((player.x + (player.w / 2)) * TILE_WIDTH), ((player.y + (player.h / 2)) * TILE_HEIGHT), pos[0], pos[1])
            shoot(bullets, player, clickAngle)
            player.slow = g.slow
        else: player.slow = 1

        for e in enemies: e.AI(tileMapList[e.worldX][e.worldY], bullets, players)
        if players:
            if players[0].health <= 0:
                players.remove(players[0])
                sleep(1)
                main()

if __name__ == "__main__": tileMapList = startGame(mapList, tileMapList); main()
