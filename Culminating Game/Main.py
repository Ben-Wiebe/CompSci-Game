import  pygame
from    math       import *
from    random     import *
from    settings   import *
from    classes    import *    
from    functions  import *
from    Maze       import generate
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
mapList = generate(21,21)

minimap      = Room(mapList)

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

#players = [Player(1.2, 1.2, 0, 300), Player(9.5, 9.5, 1, 300), Player(11, 9.5, 2, 300), Player(12.5, 9.5, 3, 300), Player(14, 9.5, 4, 300), Player(15.5, 9.5, 5, 300)]
players = [Player(1.2, 1.2, 0, 300), Player(2, 2, 1, 300, worldX = 11), Player(3, 3, 1, 300), Player(4, 4, 1, 300)]
    
def draw(grid, tileMapList, players, bullets, seeItems, guns, updated):
    global mapDisplay
    screen.fill(BLACK)
    bulletOverlays  = {0 : None, 1 : None, 2 : None, 3 : None}
    for i, player in enumerate(players):
        bulletOverlays[i].append(pygame.Surface((HALF_RES[0], HALF_RES[1]), pygame.SRCALPHA))
        
        for bullet in bullets:
            if (bullet.worldX, bullet.worldY) == (player.worldX, player.worldY):
                pygame.draw.circle(bulletOverlay[i],    WHITE, (round(bullet.x *  TILE_WIDTH) + DISPLAY_KEY[i][0],
                                                        round(bullet.y * TILE_HEIGHT) + DISPLAY_KEY[i][1]),
                                                        round(bullet.r * TILE_WIDTH))
    for i, player in enumerate(players):
        #if updated:
        mapDisplay[i].fill(BLACK)
        #print(tileMapList)

        m = tileMapList[player.worldX][player.worldY]

        mapDisplay[i].blit(m.image, (0, 0))
              
        screen.blit(mapDisplay[i], DISPLAY_KEY[i])

        #screen.blit(bulletOverlay, DISPLAY_KEY[i])

        for bullet in bullets:
            if (bullet.worldX, bullet.worldY) == (player.worldX, player.worldY):
                pygame.draw.circle(screen,   WHITE, (round(bullet.x *  TILE_WIDTH) + DISPLAY_KEY[i][0],
                                                     round(bullet.y * TILE_HEIGHT) + DISPLAY_KEY[i][1]),
                                                     round(bullet.r * TILE_WIDTH) )
                
        for p in players:
            if (p.worldX, p.worldY) == (player.worldX, player.worldY):
                pygame.draw.rect(screen,        WHITE, ((p.x * TILE_WIDTH) + DISPLAY_KEY[i][0],
                                                           (p.y * TILE_HEIGHT) + DISPLAY_KEY[i][1],
                                                           p.w * TILE_WIDTH, p.h * TILE_HEIGHT) )
                pygame.draw.rect(screen,        RED,   ((p.x + (p.w / 2)) * TILE_WIDTH - (p.w * TILE_WIDTH) + DISPLAY_KEY[i][0],
                                                           p.y * TILE_HEIGHT + TILE_HEIGHT + DISPLAY_KEY[i][1],
                                                           (p.w * TILE_WIDTH) + (p.w * TILE_WIDTH), 5) )        
                pygame.draw.rect(screen,        GREEN, ((p.x + (p.w / 2)) * TILE_WIDTH - (p.w * TILE_WIDTH) + DISPLAY_KEY[i][0],
                                                           p.y * TILE_HEIGHT + TILE_HEIGHT + DISPLAY_KEY[i][1],
                                                           max(1, p.health * ((p.w * TILE_WIDTH + (p.w * TILE_WIDTH)) / p.maxHealth)), 5) )

            if p.weapon.wType == "melee":
                pygame.draw.rect(screen,        WHITE, ((p.x + DIRECTION_KEY[player.direction][0] * p.w) * TILE_WIDTH,
                                                        (p.y + DIRECTION_KEY[player.direction][1] * p.h) * TILE_HEIGHT,
                                                        p.weapon.w.rect[0] * TILE_WIDTH, p.weapon.w.rect[1] * TILE_HEIGHT), 0)

        if player.display == True:
            screen.blit(minimap.image, DISPLAY_KEY[i])
            pygame.draw.rect(screen, WHITE, (player.worldX * TILE_WIDTH, player.worldY * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT))

        pygame.draw.line(screen, GREY, (0, HALF_RES[1]), (RESOLUTION[0], HALF_RES[1]), 15)
        pygame.draw.line(screen, GREY, (HALF_RES[0], 0), (HALF_RES[0], RESOLUTION[1]), 15)
            
    pygame.display.update()

def startGame(mapList, tileMapList):
    return initializeRooms(mapList)
    
def main():
    global TILE_WIDTH, TILE_HEIGHT
    player      = players[0]
    seeItems    = False
    xChange = 0; yChange = 0
    bullets     = []
    guns        = [minigun, spreadFire]
    #guns[1].pos = (10, 10)
    update      = False
    for p in players:
        p.weapon   = minigun
    player.weapon  = Weapon(Melee(), "melee")
    player.computer = False
    firing = False
    draw(mapList, tileMapList, players, bullets, seeItems, guns, True)
    while True:
        m = tileMapList[player.worldX][player.worldY]
        draw(mapList, tileMapList, players, bullets, seeItems, guns, update)
        update = False
        pygame.display.update()
        clock.tick(FPS_CAP)
        g = player.weapon.w
        pygame.display.set_caption("{} FPS".format(int(clock.get_fps())))
        for p in players:
            if p.shotCooldown < p.weapon.w.atkSpeed: p.shotCooldown += 1
        for event in pygame.event.get():
            if event.type    == pygame.QUIT: pygame.quit(); return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    for g in guns:
                        if g.state == 1:
                            if (int(player.x),int(player.y)) == (int(g.pos[0]),int(g.pos[1])):
                                playerGun = player.weapon.w
                                player.weapon.w.state = 0
                                playerGun.state = 1
                                playerGun.pos = (player.x, player.y)
                                guns.remove(player.weapon.w)
                                guns.append(playerGun)
                                break

                elif event.key == pygame.K_z:
                    if seeItems == True: seeItems = False
                    else: seeItems = True

                elif event.key == pygame.K_UP:
                    if tileMapList[player.worldY - 1][player.worldX] != 1: player.worldY -= 1
                elif event.key == pygame.K_DOWN:
                    if tileMapList[player.worldY + 1][player.worldX] != 1: player.worldY += 1
                elif event.key == pygame.K_RIGHT:
                    if tileMapList[player.worldY][player.worldX + 1] != 1: player.worldX += 1
                elif event.key == pygame.K_LEFT:
                    if tileMapList[player.worldY][player.worldX - 1] != 1: player.worldX -= 1

                elif event.key == pygame.K_f:
                    player.toggleDisplay()
                    
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

                elif event.button == 4:
                    TILE_WIDTH  += 1
                    TILE_HEIGHT += 1
                    update = True
                
                elif event.button == 5 and TILE_WIDTH > 2 and TILE_HEIGHT > 2:
                    TILE_WIDTH  -= 1
                    TILE_HEIGHT -= 1
                    update = True
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                if player.weapon.wType == "ranged":
                    if event.button == 1:
                        firing = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.direction = 0
            if not m.tileMap[int((player.y + (player.h / 2)) - (player.h / 2))][int(player.x + (player.w / 2))]: player.y -= player.ms * player.slow

        if keys[pygame.K_s]:
            player.direction = 1
            if not m.tileMap[int((player.y + (player.h / 2)) + (player.h / 2))][int(player.x + (player.w / 2))]: player.y += player.ms * player.slow

        if keys[pygame.K_a]:
            player.direction = 2
            if not m.tileMap[int(player.y + (player.h / 2))][int((player.x + (player.w / 2)) - (player.w / 2))]: player.x -= player.ms * player.slow

        if keys[pygame.K_d]:
            player.direction = 3
            if not m.tileMap[int(player.y + (player.h / 2))][int((player.x + (player.w / 2)) + (player.w / 2))]: player.x += player.ms * player.slow


        if keys[pygame.K_1]:            player.weapon = spreadFire
        if keys[pygame.K_2]:            player.weapon = minigun
        if keys[pygame.K_3]:            player.weapon = sniper
        if keys[pygame.K_4]:            player.weapon = bouncey
        if keys[pygame.K_5]:            player.weapon = shotgun
        if keys[pygame.K_6]:            player.weapon = lasergun
        if keys[pygame.K_7]:            player.weapon = superSpread
        if keys[pygame.K_8]:            player.weapon = burst
        if keys[pygame.K_9]:            player.weapon = tripleBurst
        if keys[pygame.K_0]:            player.weapon = plasma

        if keys[pygame.K_t]:
            for p in players:           p.health    = p.maxHealth
        if keys[pygame.K_y]:
            for p in players:           p.health        = 1
        if keys[pygame.K_k]:            player.health   = 1

        #print(tileMapList)
        updateBullets(tileMapList, bullets, players)
        #updateMines(mines, players)
        if firing and g.fireType == "auto":
            pos = pygame.mouse.get_pos()
            clickAngle = getAngle(((player.x + (player.w / 2)) * TILE_WIDTH), ((player.y + (player.h / 2)) * TILE_HEIGHT), pos[0], pos[1])
            shoot(bullets, player, clickAngle)
            player.slow = g.slow
        else: player.slow = 1
        AI(players, mapList, bullets)

if __name__ == "__main__": tileMapList = startGame(mapList, tileMapList); main()
