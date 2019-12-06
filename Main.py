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

mapList = generate(19, 19)

tileMapList  = []

mapDisplay   = [ pygame.Surface((HALF_RES[0], HALF_RES[1])) ,
                 pygame.Surface((HALF_RES[0], HALF_RES[1])) ,
                 pygame.Surface((HALF_RES[0], HALF_RES[1])) ,
                 pygame.Surface((HALF_RES[0], HALF_RES[1])) ]

#             Gun([Angles for each bullet], gun name, rarity level(0-4),
#                 speed, range, bounces, atk speed, deviation, damage, radius, slow, shot type)
spreadFire  = Weapon(Gun([-10, 0, 10], "Spread Fire", 0,
                  0.4,  45,    2,  10, 0,  15,     0.2,    1,      "semi"), "ranged")
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

def write(text, pos):
    screen.blit(pygame.font.SysFont('monospace', 20).render(str(text), False, BLACK),(pos[0], pos[1]))
            
def draw(grid, tileMapList, players, bullets, seeItems, guns, minimap, activeFrames):
    global mapDisplay
    screen.fill(BLACK)
    # Draws the screen for each player
    for i, player in enumerate(players):
        # Resets each screen
        mapDisplay[i].fill(BLACK)
        m = tileMapList[player.worldX][player.worldY]
        mapDisplay[i].blit(m.image, (0, 0))
        mapDisplay[i].blit(m.overlay[int(activeFrames) % 2], (0,0))
        mapDisplay[i].blit(m.traps[int(activeFrames / 2) % 3], (0,0))
              
        screen.blit(mapDisplay[i], DISPLAY_KEY[i])

        # Red bar behind the green bar
        pygame.draw.rect(screen, RED, (DISPLAY_KEY[i][0] + HALF_RES[0] - 25, DISPLAY_KEY[i][1], 25, 150))
        # Green bar goes over the red bar to show the player's current health compared to their max health
        pygame.draw.rect(screen, GREEN, (DISPLAY_KEY[i][0] + HALF_RES[0] - 25, DISPLAY_KEY[i][1] + 150, 25, -(player.health / player.maxHealth) * 150))

        # Draws melee attacks
        for a in m.meleeRects:
            if (a.worldX, a.worldY) == (player.worldX, player.worldY):
                pygame.draw.rect(screen, a.colour, (a.rect.x + DISPLAY_KEY[i][0], a.rect.y + DISPLAY_KEY[i][1], a.rect.w, a.rect.h), 3)

        # Draws bullets
        for bullet in bullets:
            if (bullet.worldX, bullet.worldY) == (player.worldX, player.worldY):
                screen.blit(bullet.images[bullet.age % len(bullet.images)], (bullet.x * TILE_WIDTH, bullet.y * TILE_HEIGHT))
##                pygame.draw.circle(screen,   WHITE, (round(bullet.x *  TILE_WIDTH) + DISPLAY_KEY[i][0],
##                                                     round(bullet.y * TILE_HEIGHT) + DISPLAY_KEY[i][1]),
##                                                     round(bullet.r * TILE_WIDTH))
        # Draws enemies
        if m.enemies:
            for e in m.enemies:
                if (e.worldX, e.worldY) == (player.worldX, player.worldY):
                    if not e.attacking:
                        if e.images:
                            screen.blit(e.images[e.direction][int(e.moveCount) % len(e.images[e.direction])],
                                        ((e.x * TILE_WIDTH) + DISPLAY_KEY[i][0], (e.y * TILE_HEIGHT) + DISPLAY_KEY[i][1]))
                    else:
                        screen.blit(e.attackingImages[e.direction][int(e.attackCount % len(e.attackingImages[e.direction]))],
                                    ((e.x * TILE_WIDTH) + DISPLAY_KEY[i][0], (e.y * TILE_HEIGHT) + DISPLAY_KEY[i][1]))
        # Draws bosses
        if m.boss:
            for b in m.boss:
                if (b.worldX, b.worldY) == (player.worldX, player.worldY):
                    if not b.attacking:
                        if b.images:
                            screen.blit(b.images[b.direction][int(b.moveCount) % len(b.images[b.direction])],
                                        ((b.x * TILE_WIDTH) + DISPLAY_KEY[i][0], (b.y * TILE_HEIGHT) + DISPLAY_KEY[i][1]))
                    else:
                        screen.blit(b.attackingImages[b.direction][int(b.attackCount % len(b.attackingImages[b.direction]))],
                                    ((b.x * TILE_WIDTH) + DISPLAY_KEY[i][0], (b.y * TILE_HEIGHT) + DISPLAY_KEY[i][1]))
        # Draws players
        for p in players:
            if (p.worldX, p.worldY) == (player.worldX, player.worldY):
                screen.blit(p.images[p.direction][int(p.moveCount) % len(p.images[p.direction])],
                            ((p.x * TILE_WIDTH) + DISPLAY_KEY[i][0], (p.y * TILE_HEIGHT) + DISPLAY_KEY[i][1]))
        # Draws the minimap if the player has it active
        if player.display == True:
            screen.blit(minimap.image, DISPLAY_KEY[i])
            pygame.draw.rect(screen, WHITE, (player.worldX * TILE_WIDTH + DISPLAY_KEY[i][0],
                                             player.worldY * TILE_HEIGHT + DISPLAY_KEY[i][1],
                                             TILE_WIDTH, TILE_HEIGHT))

    # Draws the lines separating each player's screen
    pygame.draw.line(screen, GREY, (0, HALF_RES[1]), (RESOLUTION[0], HALF_RES[1]), 5)
    pygame.draw.line(screen, GREY, (HALF_RES[0], 0), (HALF_RES[0], RESOLUTION[1]), 5)
            
    pygame.display.update()

# For drawing the home menu
def drawMenu(buttons, background):
    screen.fill(BLACK)
    screen.blit(background, (0, 0))
    for b in buttons:
        pygame.draw.rect(screen, WHITE, b[0])
        pygame.draw.rect(screen, BLACK, b[0], 1)
        write(b[1], (b[0].x, b[0].y))

    pygame.display.update()

# Initializes the maps
def startGame(mapList):
    return initializeRooms(mapList)

# Starts the actual game loop
def game():
    tileMapList, minimap = startGame(mapList)
    players     = [Player(0, 0, 0, 150), Player(0, 0, 1, 150), Player(0, 0, 1, 150), Player(0, 0, 1, 150)]
    player      = players[0]
    m = tileMapList[player.worldX][player.worldY]
    for p in players:
        remake = True
        while remake:
            remake = False
            p.x = randint(1,len(m.tileMap) - 2)
            p.y = randint(1,len(m.tileMap[0]) - 2)
            tiles = [(int(p.x), int(p.x + p.w)), (int(p.y), int(p.y + p.h))]
            for i in range(tiles[0][0], tiles[0][1] + 1):
                for j in range(tiles[1][0], tiles[1][1] + 1):
                    if m.collisionMap[i][j] == 1:
                        remake = True
    seeItems    = False
    xChange = 0; yChange = 0
    bullets     = []
    guns        = [minigun, spreadFire]
    for p in players:
        p.weapon   = minigun
    player.computer = False
    firing = False
    activeFrames = 0
    # Draws the initial state of the game
    for p in players:
        tileMapList[p.worldX][p.worldY].loadRoom()
        tileMapList[p.worldX][p.worldY].simulated = False
    draw(mapList, tileMapList, players, bullets, seeItems, guns, minimap, activeFrames)
    # Loop for gameplay
    while True:
        m = tileMapList[player.worldX][player.worldY]
        draw(mapList, tileMapList, players, bullets, seeItems, guns, minimap, activeFrames)
        moved           = False
        activeFrames    += 0.1
        clock.tick(FPS_CAP)
        g = player.weapon.w
        pygame.display.set_caption("{} FPS".format(int(clock.get_fps())))
        for p in players:
            if p.shotCooldown < p.weapon.w.atkSpeed: p.shotCooldown += 1
            player.slow = 1
        # Checks if the players are standing on lava or spikes
        for p in players:
            p.checkFloor(tileMapList, players, activeFrames)
            tileMapList[p.worldX][p.worldY].simulated = False
        # Tracks keyboard/mouse events
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type    == pygame.QUIT: pygame.quit(); return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    if not player.display: player.display = True
                    else: player.display = False
                    
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
                            clickAngle = getAngle(((player.x + (player.w / 2)) * TILE_WIDTH),
                                                  ((player.y + (player.h / 2)) * TILE_HEIGHT),
                                                  pos[0],
                                                  pos[1])
                            shoot(bullets, player, clickAngle)
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                if player.weapon.wType == "ranged":
                    if event.button == 1:
                        firing = False
        # Moves all of the bullets for each room
        updateBullets(tileMapList, bullets, players)
        # Fires off bullets
        if firing and g.fireType == "auto":
            clickAngle = getAngle(((player.x + (player.w / 2)) * TILE_WIDTH), ((player.y + (player.h / 2)) * TILE_HEIGHT), pos[0], pos[1])
            shoot(bullets, player, clickAngle)
            clickAngle *= (180 / pi); clickAngle %= 360
            player.direction = closestKey(DIRECTIONS, clickAngle)

            player.slow = min(g.slow, player.slow)
            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.direction = "UP"
            if not m.collisionMap[int((player.x + (player.w / 2)))][int(player.y + (player.h / 2) - (player.h / 2))]:
                player.y -= player.ms * player.slow
                if not moved: player.moveCount += 0.25; moved = True

        if keys[pygame.K_s]:
            player.direction = "DOWN"
            if not m.collisionMap[int((player.x + (player.w / 2)))][int(player.y + (player.h / 2) + (player.h / 2))]:
                player.y += player.ms * player.slow
                if not moved: player.moveCount += 0.25; moved = True

        if keys[pygame.K_a]:
            player.direction = "LEFT"
            if not m.collisionMap[int(player.x + (player.w / 2) - (player.w / 2))][int((player.y + (player.h / 2)))]:
                player.x -= player.ms * player.slow
                if not moved: player.moveCount += 0.25; moved = True

        if keys[pygame.K_d]:
            player.direction = "RIGHT"
            if not m.collisionMap[int(player.x + (player.w / 2) + (player.w / 2))][int((player.y + (player.h / 2)))]:
                player.x += player.ms * player.slow
                if not moved: player.moveCount += 0.25; moved = True

        # If the player's health is less than 0 they die. Otherwise, checks for collision with melee attacks
        if players:
            for p in players:
                #if p.health <= 0: players.remove(p); break
                m = tileMapList[p.worldX][p.worldY]
                if not m.simulated:
                    if m.enemies:
                        for e in m.enemies:
                            if e.health <= 0: m.enemies.remove(e); break
                            e.AI(tileMapList[e.worldX][e.worldY], bullets, players, m.enemies, activeFrames)
                            
                    if m.boss:
                        for b in m.boss:
                            if b.health <= 0: m.boss.remove(b); break
                            b.AI(tileMapList[b.worldX][b.worldY], bullets, players, m.enemies, activeFrames)
                    
                    for a in m.meleeRects:
                        a.update(players)
                        if a.delete: m.meleeRects.remove(a); break
                    m.simulated = True
                    
# Main loop to start the game
def main():
    a = [pygame.transform.scale(pygame.image.load(r"resources\bosses\hastur\up1.png"), (int(TILE_WIDTH * 8), int(TILE_HEIGHT * 8))) for i in range(1,400)]
    # Buttons that you can press/display text
    startButton     = [pygame.Rect((HALF_RES[0] - 200, HALF_RES[1], 400, 20)), "Start Game"]
    loadingButton   = [pygame.Rect((HALF_RES[0] - 200, HALF_RES[1], 400, 20)), "Loading {} Tiles".format(19 * 19)]
    loadingButton2  = [pygame.Rect((HALF_RES[0] - 200, HALF_RES[1] + 20, 400, 20)), "This might take a while"]
    buttons = [startButton]
    bg = pygame.Surface((RESOLUTION[0], RESOLUTION[1]))
    pygame.draw.rect(bg, WHITE, (50, 50, RESOLUTION[0] - 50, RESOLUTION[1] - 50), 25)
    while True:
        drawMenu(buttons, bg)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if buttons[0][0].collidepoint(pos):
                    # Draws the loading screen while you wait for the game to load
                    drawMenu([loadingButton, loadingButton2], loadingBackground())
                    # Starts the game
                    game()

if __name__ == "__main__": main()
