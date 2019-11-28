import pygame
pygame.init()
screen = pygame.display.set_mode((100, 100))

def convertS(e, d, v, h):
    image = pygame.transform.scale(pygame.image.load(r"resources\enemies\{}\{}.png".format(e, d)), (16, 32))
    images = [image.subsurface((0, 16 * y, 16, 16)) for y in range(v)]# + [image.subsurface((16, 16 * y, 16, 16)) for y in range(v)]
    pygame.display.update()
    for i in range(1, 3): pygame.image.save(images[i - 1], r"resources\enemies\{}\{}{}".format(e, d, i) + ".png")

convertS("goblin", "attackup", 2, 2)
convertS("goblin", "attackdown", 2, 2)
convertS("goblin", "attackleft", 2, 2)
convertS("goblin", "attackright", 2, 2)
