import  pygame
from    pygame.math import Vector2
from    math        import *
from    random      import *
from    settings    import *
from    classes     import *    
from    functions   import *
from    Maze        import generate
from    copy        import copy
pygame.init()
pygame.joystick.init()

# Creates a canvas on which to draw the game
screen = pygame.display.set_mode(RESOLUTION, pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.FULLSCREEN)
clock = pygame.time.Clock()

# Uses the "Maze" file to generate a maze
mapList = generate(25,25)

tileMapList  = []

# Surfaces for each player's list
mapDisplay   = [ pygame.Surface((HALF_RES[0], HALF_RES[1])) ,
                 pygame.Surface((HALF_RES[0], HALF_RES[1])) ,
                 pygame.Surface((HALF_RES[0], HALF_RES[1])) ,
                 pygame.Surface((HALF_RES[0], HALF_RES[1])) ]

# A function to draw text at any given position on a surface
def write(text, pos, fontSize=20,surface=screen, colour=BLACK):
    surface.blit(pygame.font.SysFont('monospace', fontSize).render(str(text), False, colour),(pos[0], pos[1]))

menuScreen = [pygame.transform.scale(pygame.image.load(r"resources\buttons\title{}.png".format(i)), RESOLUTION) for i in range(1, 11)]

victory = pygame.Surface(RESOLUTION)
write("VICTORY", (0, 0), fontSize=320, surface = victory, colour = WHITE)
write("Press ESC to return to the main menu", (0, HALF_RES[1]), surface=victory, colour=WHITE)

# Function to draw the game onto a surface
def draw(grid, tileMapList, players, bullets, seeItems, minimap, controls, activeFrames):
    global mapDisplay
    screen.fill(BLACK) # Fills the screen so it's blank
    # Draws the screen for each player
    for i, player in enumerate(players):
        # Resets each screen
        mapDisplay[i].fill(BLACK)
        m = tileMapList[player.worldX][player.worldY]
        # Draws the background onto the display
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
##                screen.blit(bullet.images[(bullet.age // 3) % len(bullet.images)], (((bullet.x - bullet.r) * TILE_WIDTH) + DISPLAY_KEY[i][0],
##                                                                                    ((bullet.y - bullet.r) * TILE_HEIGHT) + DISPLAY_KEY[i][1]))

                rotatedImage = blitRotate(bullet.images[(bullet.age // 3) % len(bullet.images)], (((bullet.x - bullet.r) * TILE_WIDTH) + DISPLAY_KEY[i][0],
                                                                                    ((bullet.y - bullet.r) * TILE_HEIGHT) + DISPLAY_KEY[i][1]), -(bullet.angle+(pi/2)) * (180/pi))
                screen.blit(rotatedImage[0], rotatedImage[1])
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
                                    (((e.x + e.attackingOffset[e.direction][0]) * TILE_WIDTH) + DISPLAY_KEY[i][0],
                                     ((e.y + e.attackingOffset[e.direction][1]) * TILE_HEIGHT) + DISPLAY_KEY[i][1]))
        # Draws bosses
        if m.boss:
            for b in m.boss:
                if (b.worldX, b.worldY) == (player.worldX, player.worldY):
##                    pygame.draw.rect(screen, RED, ((b.x * TILE_WIDTH) + (b.w / 2) + DISPLAY_KEY[i][0],
##                                                   (b.y * TILE_HEIGHT) + (b.h * TILE_HEIGHT) + DISPLAY_KEY[i][1],
##                                                   100, 15))
##                    pygame.draw.rect(screen, GREEN, ((b.x * TILE_WIDTH) + (b.w / 2) + DISPLAY_KEY[i][0],
##                                                     (b.y * TILE_HEIGHT) + (b.h * TILE_HEIGHT) + DISPLAY_KEY[i][1],
##                                                     (player.health / player.maxHealth) * 100, 15))
                    if not b.attacking:
                        if b.images:
                            screen.blit(b.images[b.direction][int(b.moveCount) % len(b.images[b.direction])],
                                        ((b.x * TILE_WIDTH) + DISPLAY_KEY[i][0], (b.y * TILE_HEIGHT) + DISPLAY_KEY[i][1]))
                    else:
                        screen.blit(b.attackingImages[b.direction][int(b.attackCount % len(b.attackingImages[b.direction]))],
                                    ((b.x * TILE_WIDTH) + DISPLAY_KEY[i][0], (b.y * TILE_HEIGHT) + DISPLAY_KEY[i][1]))
                        
        # Draws players
        for p in players:
            if (p.worldX, p.worldY) == (player.worldX, player.worldY) and p.alive:
                if p.attacking:
                    #print(int(p.attackFrames) % int(max(1,p.attackFrames)))
                    try:
                        screen.blit(p.attackingImages[p.direction][int(p.attackFrames) % len(p.attackingImages)],
                                    (((p.x + attackOffset[p.weapon.w.type][p.direction][0]) * TILE_WIDTH) + DISPLAY_KEY[i][0],
                                     ((p.y + attackOffset[p.weapon.w.type][p.direction][1]) * TILE_HEIGHT) + DISPLAY_KEY[i][1]))
                    except: pass
                else:
                    try:
                        screen.blit(p.images[p.direction][int(p.moveCount) % len(p.images[p.direction])],
                                    ((p.x * TILE_WIDTH) + DISPLAY_KEY[i][0],
                                     (p.y * TILE_HEIGHT) + DISPLAY_KEY[i][1]))
                    except: pass
                    
        if player.cursor and player.alive:
            write("{}".format(p.team), ((p.x * TILE_WIDTH) + DISPLAY_KEY[i][0], ((p.y - (p.h * TILE_HEIGHT * 1.2)) * TILE_HEIGHT) + DISPLAY_KEY[i][1]), fontSize = 30, colour = WHITE)
            pygame.draw.circle(screen, WHITE, (round(player.cursor[0] * TILE_WIDTH) + DISPLAY_KEY[i][0], round(player.cursor[1] * TILE_HEIGHT) + DISPLAY_KEY[i][1]), 2)

        for item in m.items:
            if player.weaponDisplay:
                if (item.worldX, item.worldY) == (player.worldX, player.worldY):
                    screen.blit(item.display, ((item.x * TILE_WIDTH) + DISPLAY_KEY[i][0], (item.y * TILE_HEIGHT) + DISPLAY_KEY[i][1]))

        # Draws the minimap if the player has it active
        if player.minimap == True:
            screen.blit(minimap.image, DISPLAY_KEY[i])
            pygame.draw.rect(screen, WHITE, (player.worldX * TILE_WIDTH + DISPLAY_KEY[i][0],
                                             player.worldY * TILE_HEIGHT + DISPLAY_KEY[i][1],
                                             TILE_WIDTH, TILE_HEIGHT))

        if player.controls and player.alive:
            screen.blit(controls, (DISPLAY_KEY[i][0], DISPLAY_KEY[i][1]))

    # Draws the lines separating each player's screen
    pygame.draw.line(screen, GREY, (0, HALF_RES[1]), (RESOLUTION[0], HALF_RES[1]), 5)
    pygame.draw.line(screen, GREY, (HALF_RES[0], 0), (HALF_RES[0], RESOLUTION[1]), 5)
            
    pygame.display.update()

# For drawing the home menu
def drawMenu(buttons, background, activeFrames):
    screen.fill(BLACK)
    screen.blit(background[activeFrames % len(background)], (0, 0))
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
    # Inititalizes all connected joysticks
    joysticks = []
    for i in range(pygame.joystick.get_count()):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        joysticks.append(joystick)
    tileMapList, minimap = startGame(mapList)
    # Player list
    players     = [Player(0, 0, 0, 500), Player(0, 0, 1, 500), Player(0, 0, 1, 500), Player(0, 0, 1, 500)]
    player      = players[0]
    m = tileMapList[player.worldX][player.worldY]
    for i, p in enumerate(players):
        if i <= len(joysticks) - 1:
            p.joystick = joysticks[i]
            p.joystick.init()
            p.cursor = (0, 0)
        else: p.joystick = None
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
    for p in players:
        # Gives each player a starting weapon and loads the sprites for the weapon
        p.weapon   = WEAPONS["sword"][1]
        p.loadAttacks(p.weapon.w.type, p.weapon.w.rarity)
    player.computer = False
    firing = False
    activeFrames = 0
    # Draws the initial state of the game
    for p in players:
        tileMapList[p.worldX][p.worldY].loadRoom()
        tileMapList[p.worldX][p.worldY].simulated = False
    controls = getControls()
    # Draws the initial state of the game
    draw(mapList, tileMapList, players, bullets, seeItems, minimap, controls, activeFrames)
    # Loop for gameplay
    while True:
        boss = False
        for x in tileMapList:
            for y in x:
                if not y in [0, 1]:
                    if y.boss:
                        continue
                    boss = True
        if len(players) == 1 and not boss:
            while True:
                screen.fill(0)
                screen.blit(victory, (0, 0))
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            main()
                pygame.display.update()
        pos = pygame.mouse.get_pos()
        m = tileMapList[player.worldX][player.worldY]
        draw(mapList, tileMapList, players, bullets, seeItems, minimap, controls, activeFrames)
        moved           = False
        activeFrames    += 0.1
        clock.tick(FPS_CAP)
        g = player.weapon.w
        pygame.display.set_caption("{} FPS".format(int(clock.get_fps())))
        # Resets the player slow, inches them closer to being able to attack
        for p in players:
            p.health = min(p.maxHealth, p.health + 0.05)
            if p.shotCooldown < p.weapon.w.atkSpeed: p.shotCooldown += 1
            p.slow = 1
        # Checks if the players are standing on lava or spikes and attacks if they are clicking
        for l, p in enumerate(players):
            g = p.weapon.w
            if p.weapon.wType == "ranged":
                if p.shotCooldown >= g.atkSpeed:
                    p.attackFrames = 0
                    if p.cursor: shot = [p.cursor[0] * TILE_WIDTH, p.cursor[1] * TILE_HEIGHT]
                    else: shot = pygame.mouse.get_pos()
                    if p.attacking:
                        for angle in g.shots:
                            adjusted = getAngle(((p.x + (p.w / 2)) * TILE_WIDTH),
                                                ((p.y + (p.h / 2)) * TILE_HEIGHT),
                                                shot[0],
                                                shot[1]) + ((angle + randint(-g.deviation, g.deviation)) * (pi / 180))
                            bullets.append(Bullet((p.x + (p.w / 2), p.y + (p.h / 2)), (p.worldX, p.worldY), g.bulletDmg,
                                                  adjusted,
                                                  p.team, g.speed, g.range, g.maxBounces, g.r, g.image))
                    p.attacking = False
                else: p.attacking = True; p.attackFrames += len(p.attackingImages[p.direction]) / g.atkSpeed; p.slow = g.slow

            elif p.weapon.wType == "melee":
                if p.shotCooldown >= g.atkSpeed:
                    if p.attacking: pass
                    p.attacking = False
                else: p.attacking = True; p.attackFrames += len(p.attackingImages[p.direction]) / g.atkSpeed; p.slow = 0.2
        
            p.checkFloor(tileMapList, players, activeFrames)
            tileMapList[p.worldX][p.worldY].simulated = False
        # Tracks keyboard/mouse events
        g = p.weapon.w
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: main()
                if event.key == pygame.K_f:
                    if not player.minimap: player.minimap = True
                    else: player.minimap = False

                elif event.key == pygame.K_g:
                    if not player.weaponDisplay: player.weaponDisplay = True
                    else: player.weaponDisplay = False

                elif event.key == pygame.K_e:
                    for i, item in enumerate(m.items):
                        if ((item.x - player.x) ** 2) + ((item.y - player.y) ** 2) < 6:
                            player.weapon.x = player.x; player.weapon.y = player.y
                            player.weapon.worldX = player.worldX; player.weapon.worldY = player.worldY
                            m.items.append(player.weapon)
                            player.weapon = item
                            player.loadAttacks(item.w.type, item.w.rarity)
                            m.items.remove(item)
                            break

##            elif event.type == pygame.MOUSEBUTTONDOWN:
##                if player.weapon.wType == "melee":
##                    if player.attackFrames == len(player.weapon.w.rect): player.attackFrames = 0
##                    player.attackFrames += 1
##                    hitbox = pygame.Rect(((player.x + DIRECTION_KEY[player.direction][0]) * TILE_WIDTH,
##                                          (player.y + DIRECTION_KEY[player.direction][1]) * TILE_HEIGHT),
##                                         player.weapon.w.rect)
##                    for p in players:
##                        if (p.worldX, p.worldY) == (player.worldX, player.worldY) and p.team != player.team:
##                            playerBox = pygame.Rect((p.x * TILE_WIDTH, p.y * TILE_HEIGHT, p.w * TILE_WIDTH, p.h * TILE_HEIGHT))
##                            if hitbox.colliderect(playerBox):
##                                p.health -= 50
##                    
##                if player.weapon.wType == "ranged":
##                    if event.button == 1:
##                        if g.fireType == "auto":    firing = True
##                        else:
##                            firing = False
##                            g = p.weapon.w
##                            if p.shotCooldown >= g.atkSpeed:
##                                for angle in g.shots:
##                                    bullets.append(Bullet((p.x + (p.w / 2), p.y + (p.h / 2)), (p.worldX, p.worldY), g.bulletDmg,
##                                                          a + ((angle + randint(-g.deviation, g.deviation)) * (pi / 180)),
##                                                          p.team, g.speed, g.range, g.maxBounces, g.r, g.image))
##                                p.shotCooldown = 0
##                    
##            elif event.type == pygame.MOUSEBUTTONUP:
##                if player.weapon.wType == "ranged":
##                    if event.button == 1:
##                        firing = False
        # Moves all of the bullets for each room

        buttons = pygame.mouse.get_pressed()
        # Attacks for the player
        if buttons[0]:
            g = player.weapon.w
            if not player.attacking:
                
                player.shotCooldown = 0

                if player.weapon.wType == "melee":
                    if p.direction in "LEFT RIGHT":
                        m.meleeRects.append(AttackRect((player.x + (player.w * 0.6) * DIRECTION_KEY[player.direction][0]) * TILE_WIDTH,
                                                         (player.y + (player.h * 0.6) * DIRECTION_KEY[player.direction][1]) * TILE_HEIGHT,
                                                         player.worldX, player.worldY,
                                                         g.w * TILE_WIDTH, g.h * TILE_HEIGHT, player.team, g.dmg, range(g.atkSpeed-2, g.atkSpeed),
                                                         g.atkSpeed, g.colour))
                    elif p.direction in "UP DOWN":
                        m.meleeRects.append(AttackRect(p.x * TILE_WIDTH,
                                                         (p.y + ((p.h * 0.8) * DIRECTION_KEY[p.direction][1])) * TILE_HEIGHT,
                                                         p.worldX, p.worldY,
                                                         g.h * TILE_WIDTH, g.w * TILE_HEIGHT, p.team, g.dmg, range(g.atkSpeed-2, g.atkSpeed),
                                                         g.atkSpeed, g.colour))

        updateBullets(tileMapList, bullets, players)
        
        keys = pygame.key.get_pressed()
        # Moves the player
        try:
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
        except: pass

        # Fires off bullets
        if firing and g.fireType == "auto":
            clickAngle = getAngle(((player.x + (player.w / 2)) * TILE_WIDTH), ((player.y + (player.h / 2)) * TILE_HEIGHT), pos[0], pos[1])
            shoot(bullets, player, clickAngle)
            clickAngle *= (180 / pi); clickAngle %= 360
            player.direction = closestKey(DIRECTIONS, clickAngle)

            player.slow = min(g.slow, player.slow)

        # Movement and attacking if the player is using a joystick
        for i, p in enumerate(players):
            g = p.weapon.w
            m = tileMapList[p.worldX][p.worldY]
            if p.joystick:
                j = p.joystick
                if j.get_button(1):
                    for i, item in enumerate(m.items):
                        if ((item.x - p.x) ** 2) + ((item.y - p.y) ** 2) < 6 and not p.pickedUp:
                            p.weapon.x = p.x; p.weapon.y = p.y
                            p.weapon.worldX = p.worldX; p.weapon.worldY = p.worldY
                            m.items.append(p.weapon)
                            p.weapon = item
                            p.loadAttacks(item.w.type, item.w.rarity)
                            m.items.remove(item)
                            p.pickedUp = True
                            break
                        
                else: p.pickedUp = False

                if j.get_button(0):
                    if not p.minimapToggle:
                        if not p.minimap: p.minimap = True
                        else: p.minimap = False
                    p.minimapToggle = True
                else: p.minimapToggle = False

                if j.get_button(2):
                    if not p.controlToggle:
                        if not p.controls: p.controls = True
                        else: p.controls = False
                    p.controlToggle = True
                else: p.controlToggle = False
                
                if j.get_button(3):
                    if not p.weaponToggle:
                        if not p.weaponDisplay: p.weaponDisplay = True
                        else: p.weaponDisplay = False
                    p.weaponToggle = True
                else: p.weaponToggle = False

                if j.get_button(7):
                    if not p.attacking:
                        p.shotCooldown = 0
                        p.slow = 0
                        if p.weapon.wType == "melee":
                            if p.direction in "LEFT RIGHT":
                                m.meleeRects.append(AttackRect((p.x + (p.w * 0.6) * DIRECTION_KEY[p.direction][0]) * TILE_WIDTH,
                                                                 (p.y + (p.h * 0.6) * DIRECTION_KEY[p.direction][1]) * TILE_HEIGHT,
                                                                 p.worldX, p.worldY,
                                                                 g.w * TILE_WIDTH, g.h * TILE_HEIGHT, p.team, g.dmg, range(g.atkSpeed-2, g.atkSpeed),
                                                                 g.atkSpeed, g.colour))
                            elif p.direction in "UP DOWN":
                                m.meleeRects.append(AttackRect(p.x * TILE_WIDTH,
                                                                 (p.y + ((p.h * 0.8) * DIRECTION_KEY[p.direction][1])) * TILE_HEIGHT,
                                                                 p.worldX, p.worldY,
                                                                 g.h * TILE_WIDTH, g.w * TILE_HEIGHT, p.team, g.dmg, range(g.atkSpeed-2, g.atkSpeed),
                                                                 g.atkSpeed, g.colour))


##                    cursorAngle = getAngle(((p.x + (p.w / 2)) * TILE_WIDTH),
##                                                  ((p.y + (p.h / 2)) * TILE_HEIGHT),
##                                                  p.cursor[0] * TILE_WIDTH,
##                                                  p.cursor[1] * TILE_HEIGHT)
##                    shoot(bullets, player, cursorAngle)

                # Converts a 2D vector containing the direction values of the joystick's axis into polar coordinates
                if not (round(j.get_axis(0), 2), round(j.get_axis(1), 2)) == (0, 0):
                    vec = Vector2(round(j.get_axis(0), 4), round(j.get_axis(1), 4))
                    radius, angle = vec.as_polar()
                    if radius > 0.5:
                        # Uses the polar coordinate system to determine the angle at which the joystick is angled
                        angle %= 360
                        moveX = cos(angle * (pi / 180)) * p.ms * p.slow
                        moveY = sin(angle * (pi / 180)) * p.ms * p.slow
                        p.direction = closestKey(DIRECTIONS, angle)
                        try:
                            if m.collisionMap[int((p.x + (p.w / 2) + ((p.w / 2) * DIRECTION_KEY[p.direction][0])) + moveX)] \
                               [int(p.y + (p.h / 2))] != 1: p.x += moveX
                            if m.collisionMap[int(p.x + (p.w / 2))] \
                               [int((p.y + (p.h / 2) + ((p.h / 2) * DIRECTION_KEY[p.direction][1])) + moveY)] != 1: p.y += moveY
                        except: pass
                if not (round(j.get_axis(2), 3), round(j.get_axis(3), 3)) == (0, 0):
                    vec = Vector2(round(j.get_axis(2), 4), round(j.get_axis(3), 4))
                    radius, angle = vec.as_polar()
                    # Uses the polar coordinate system to determine the angle at which the joystick is angled
                    angle %= 360
                    p.cursor = (p.x + (p.w / 2) + (cos(angle * (pi / 180)) * 3), p.y + (p.h / 2) + (sin(angle * (pi / 180)) * 3))
                    p.direction = closestKey(DIRECTIONS, angle)

        # If the player's health is less than 0 they die. Otherwise, checks for collision with melee attacks
        if players:
            for i,p in enumerate(players):
                if p.health <= 0: players.remove(p); continue
                m = tileMapList[p.worldX][p.worldY]
                if not m.simulated:
                    if m.enemies:
                        for e in m.enemies:
                            if e.health <= 0: e.onDeath(m.items); m.enemies.remove(e); break
                            e.AI(tileMapList[e.worldX][e.worldY], bullets, players, m.enemies, activeFrames)

                    if m.boss:
                        for b in m.boss:
                            if b.health <= 0: b.onDeath(); m.boss.remove(b); break
                            b.AI(tileMapList[b.worldX][b.worldY], bullets, players, m.enemies, activeFrames)
                    retry = True
                    
                    for a in m.meleeRects: a.update(players, tileMapList)
                    allRects = m.meleeRects.copy()
                    for a in m.meleeRects:
                        if a.delete: allRects.remove(a)
                    m.meleeRects = allRects        
                    m.simulated = True
        else: pygame.quit(); break
                    
# Main loop to start the game
def main():
    activeFrames = 0
    # Buttons that you can press/display text
    startButton     = [pygame.Rect((HALF_RES[0] - 200, HALF_RES[1], 400, 20)), "Start Game"]
    loadingButton   = [pygame.Rect((HALF_RES[0] - 200, HALF_RES[1], 400, 20)), "Loading {} Tiles".format(19 * 19)]
    loadingButton2  = [pygame.Rect((HALF_RES[0] - 200, HALF_RES[1] + 20, 400, 20)), "This might take a while"]
    buttons = [startButton]
    bg = pygame.Surface((RESOLUTION[0], RESOLUTION[1]))
    pygame.draw.rect(bg, WHITE, (50, 50, RESOLUTION[0] - 100, RESOLUTION[1] - 100), 25)
    while True:
        activeFrames += 1
        drawMenu(buttons, menuScreen, activeFrames)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: pygame.quit(); return
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if buttons[0][0].collidepoint(pos):
                    # Draws the loading screen while you wait for the game to load
                    drawMenu([loadingButton, loadingButton2], [loadingBackground()], activeFrames)
                    # Starts the game
                    game()

if __name__ == "__main__": main()
