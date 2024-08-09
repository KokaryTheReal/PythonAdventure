import pygame
import sys

pygame.init()
hintergrund = pygame.image.load("Grafiken/hintergrund.png")
screen = pygame.display.set_mode([900, 450])
clock = pygame.time.Clock()
pygame.display.set_caption("2d adventure")


def zeichnen():
    screen.blit(hintergrund, (0, 0))
    pygame.draw.rect(screen, (255, 0, 255), (x, y, breite, hoehe))
    pygame.display.update()


x = 300
y = 300
geschw = 3
breite = 40
hoehe = 80

linkeWand = pygame.draw.rect(screen, (0, 0, 0), (1, 0, 2, 450), 0)
rechteWand = pygame.draw.rect(screen, (0, 0, 0), (899, 0, 2, 450), 0)

go = True
while go:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    spielerRechteck = pygame.Rect(x, y, 40, 80)
    gedrueckt = pygame.key.get_pressed()
    if gedrueckt[pygame.K_UP]:
        y -= geschw
    if gedrueckt[pygame.K_RIGHT] and not spielerRechteck.colliderect(rechteWand):
        x += geschw
    if gedrueckt[pygame.K_LEFT] and not spielerRechteck.colliderect(linkeWand):
        x -= geschw

    zeichnen()
    clock.tick(60)
