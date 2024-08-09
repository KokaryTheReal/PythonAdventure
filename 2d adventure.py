import pygame
import sys

pygame.init()
hintergrund = pygame.image.load("Grafiken/hintergrund.png")
screen = pygame.display.set_mode([900, 450])
clock = pygame.time.Clock()
pygame.display.set_caption("2d adventure")

stehen = pygame.image.load("Grafiken/stand.png")
sprung = pygame.image.load("Grafiken/sprung.png")
rechtsGehen = [pygame.image.load("Grafiken/rechts1.png"), pygame.image.load("Grafiken/rechts2.png"),
               pygame.image.load("Grafiken/rechts3.png"), pygame.image.load("Grafiken/rechts4.png"),
               pygame.image.load("Grafiken/rechts5.png"), pygame.image.load("Grafiken/rechts6.png"),
               pygame.image.load("Grafiken/rechts7.png"), pygame.image.load("Grafiken/rechts8.png")]
linksGehen = [pygame.image.load("Grafiken/links1.png"), pygame.image.load("Grafiken/links2.png"),
              pygame.image.load("Grafiken/links3.png"), pygame.image.load("Grafiken/links4.png"),
              pygame.image.load("Grafiken/links5.png"), pygame.image.load("Grafiken/links6.png"),
              pygame.image.load("Grafiken/links7.png"), pygame.image.load("Grafiken/links8.png")]
sprungSound = pygame.mixer.Sound("Sounds/cartoon-jump-6462.wav")


def zeichnen(liste):
    global schritteRechts, schritteLinks
    screen.blit(hintergrund, (0, 0))

    if schritteRechts == 63:
        schritteRechts = 0
    if schritteLinks == 63:
        schritteLinks = 0

    if liste[0]:
        screen.blit(linksGehen[schritteLinks // 8], (x, y))

    if liste[1]:
        screen.blit(rechtsGehen[schritteRechts // 8], (x, y))

    if liste[2]:
        screen.blit(stehen, (x, y))

    if liste[3]:
        screen.blit(sprung, (x, y))

    pygame.display.update()


x = 300
y = 273
geschw = 5
breite = 40
hoehe = 80

linkeWand = pygame.draw.rect(screen, (0, 0, 0), (1, 0, 2, 450), 0)
rechteWand = pygame.draw.rect(screen, (0, 0, 0), (899, 0, 2, 450), 0)

go = True
sprungvar = -13
#[links,rechts,stand,sprung]
richtg = [0, 0, 0, 0]
schritteRechts = 0
schritteLinks = 0
while go:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    spielerRechteck = pygame.Rect(x, y, 96, 128)
    gedrueckt = pygame.key.get_pressed()
    richtg = [0, 0, 1, 0]
    if gedrueckt[pygame.K_UP] and sprungvar == -13:
        sprungvar = 12
    if gedrueckt[pygame.K_RIGHT] and not spielerRechteck.colliderect(rechteWand):
        x += geschw
        richtg = [0, 1, 0, 0]
        schritteRechts += 1
    if gedrueckt[pygame.K_LEFT] and not spielerRechteck.colliderect(linkeWand):
        x -= geschw
        richtg = [1, 0, 0, 0]
        schritteLinks += 1

    if sprungvar == 12:
        pygame.mixer.Sound.play(sprungSound)

    if sprungvar >= -12:
        richtg = [0, 0, 0, 1]
        n = 1
        if sprungvar < 0:
            n = -1
        y -= (sprungvar ** 2) * 0.17 * n
        sprungvar -= 1

    if richtg[2] or richtg[3]:
        schritteRechts = 0
        schritteLinks = 0

    zeichnen(richtg)
    clock.tick(60)
