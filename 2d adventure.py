import pygame
import sys

pygame.init()
hintergrund = pygame.image.load("Grafiken/hintergrund.png")
screen = pygame.display.set_mode([900, 450])
clock = pygame.time.Clock()
pygame.display.set_caption("2d adventure")

# Musik und Soundeffekte laden
pygame.mixer.music.load("Sounds/background-music.mp3")
pygame.mixer.music.play(-1)  # -1 spielt die Musik in einer Endlosschleife

schiessenSound = pygame.mixer.Sound("Sounds/schiessen.wav")
einsammelnSound = pygame.mixer.Sound("Sounds/einsammeln.wav")
sprungSound = pygame.mixer.Sound("Sounds/sprung.wav")  # Definiere den Sprung-Soundeffekt

# Spieler Texturen
angriffLinks = pygame.image.load("Grafiken/angriffLinks.png")
angriffRechts = pygame.image.load("Grafiken/angriffRechts.png")
sprung = pygame.image.load("Grafiken/sprung.png")
rechtsGehen = [pygame.image.load("Grafiken/rechts1.png"), pygame.image.load("Grafiken/rechts2.png"),
               pygame.image.load("Grafiken/rechts3.png"), pygame.image.load("Grafiken/rechts4.png"),
               pygame.image.load("Grafiken/rechts5.png"), pygame.image.load("Grafiken/rechts6.png"),
               pygame.image.load("Grafiken/rechts7.png"), pygame.image.load("Grafiken/rechts8.png")]
linksGehen = [pygame.image.load("Grafiken/links1.png"), pygame.image.load("Grafiken/links2.png"),
              pygame.image.load("Grafiken/links3.png"), pygame.image.load("Grafiken/links4.png"),
              pygame.image.load("Grafiken/links5.png"), pygame.image.load("Grafiken/links6.png"),
              pygame.image.load("Grafiken/links7.png"), pygame.image.load("Grafiken/links8.png")]

# Zombie Texturen
zombieLinks = [pygame.image.load("Grafiken/l1.png"), pygame.image.load("Grafiken/l2.png"),
               pygame.image.load("Grafiken/l3.png"), pygame.image.load("Grafiken/l4.png")]
zombieRechts = [pygame.image.load("Grafiken/r1.png"), pygame.image.load("Grafiken/r2.png"),
                pygame.image.load("Grafiken/r3.png"), pygame.image.load("Grafiken/r4.png")]

class spieler:
    def __init__(self, x, y, geschw, breite, hoehe, sprungvar, richtg, schritteRechts, schritteLinks):
        self.x = x
        self.y = y
        self.geschw = geschw
        self.breite = breite
        self.hoehe = hoehe
        self.sprungvar = sprungvar
        self.richtg = richtg
        self.schritteRechts = schritteRechts
        self.schritteLinks = schritteLinks
        self.sprung = False
        self.last = [1, 0]
        self.leben = 3  # Leben des Spielers

    def laufen(self, liste):
        if liste[0]:
            self.x -= self.geschw
            self.richtg = [1, 0, 0, 0]
            self.schritteLinks += 1
        if liste[1]:
            self.x += self.geschw
            self.richtg = [0, 1, 0, 0]
            self.schritteRechts += 1

    def resetSchritte(self):
        self.schritteLinks = 0
        self.schritteRechts = 0

    def stehen(self):
        self.richtg = [0, 0, 1, 0]
        self.resetSchritte()

    def sprungSetzen(self):
        if not self.sprung:  # Nur springen, wenn der Spieler nicht bereits in der Luft ist
            self.sprung = True
            self.sprungvar = 12
            pygame.mixer.Sound.play(sprungSound)

    def springen(self):
        if self.sprung:
            self.richtg = [0, 0, 0, 1]
            if self.sprungvar >= -12:
                n = 1
                if self.sprungvar < 0:
                    n = -1
                self.y -= (self.sprungvar ** 2) * 0.17 * n
                self.sprungvar -= 1
            else:
                self.sprung = False

    def spZeichnen(self):
        if self.schritteRechts == 63:
            self.schritteRechts = 0
        if self.schritteLinks == 63:
            self.schritteLinks = 0

        if self.richtg[0]:
            screen.blit(linksGehen[self.schritteLinks // 8], (self.x, self.y))
            self.last = [1, 0]

        if self.richtg[1]:
            screen.blit(rechtsGehen[self.schritteRechts // 8], (self.x, self.y))
            self.last = [0, 1]

        if self.richtg[2]:
            if self.last[0]:
                screen.blit(angriffLinks, (self.x, self.y))
            else:
                screen.blit(angriffRechts, (self.x, self.y))

        if self.richtg[3]:
            screen.blit(sprung, (self.x, self.y))

    def lebensanzeige(self):
        schrift = pygame.font.SysFont("comicsans", 30)
        text = schrift.render("Leben: " + str(self.leben), 1, (255, 255, 255))
        screen.blit(text, (10, 10))

    def kollidiertMitZombie(self, zombie):
        spielerRechteck = pygame.Rect(self.x, self.y, self.breite, self.hoehe)
        zombieRechteck = pygame.Rect(zombie.x, zombie.y, zombie.breite, zombie.hoehe)
        return spielerRechteck.colliderect(zombieRechteck)


class kugel:
    def __init__(self, spx, spy, richtung, geschw):
        self.x = spx
        self.y = spy
        if richtung[0]:
            self.x += 5
            self.geschw = -1 * geschw
        elif richtung[1]:
            self.x += 92
            self.geschw = geschw
        self.y += 84

    def bewegen(self):
        self.x += self.geschw

    def zeichnen(self):
        start_pos = (self.x, self.y)
        end_pos = (self.x + 5 * self.geschw, self.y)
        pygame.draw.line(screen, (255, 0, 0), start_pos, end_pos, 5)


class zombie:
    def __init__(self, x, y, geschw, breite, hoehe, xMin, xMax):
        self.x = x
        self.y = y
        self.geschw = geschw
        self.breite = breite
        self.hoehe = hoehe
        self.schritte = 0
        self.xMin = xMin
        self.xMax = xMax
        self.richtg = 1 if geschw > 0 else -1  # 1 für rechts, -1 für links

    def hinHer(self):
        self.x += self.geschw
        if self.x > self.xMax or self.x < self.xMin:
            self.geschw *= -1
            self.richtg *= -1  # Richtungswechsel
        self.schritte += 1
        if self.schritte >= len(zombieRechts) * 8:
            self.schritte = 0

    def zZeichnen(self):
        if self.richtg > 0:
            screen.blit(zombieRechts[self.schritte // 8], (self.x, self.y))
        else:
            screen.blit(zombieLinks[self.schritte // 8], (self.x, self.y))


class powerup:
    def __init__(self, x, y, typ):
        self.x = x
        self.y = y
        self.typ = typ
        self.bild = pygame.image.load("Grafiken/powerup.png")  # Beispielgrafik für das Power-Up
        self.breite = 32
        self.hoehe = 32

    def zeichnen(self):
        screen.blit(self.bild, (self.x, self.y))

    def einsammeln(self, spieler):
        spielerRechteck = pygame.Rect(spieler.x, spieler.y, spieler.breite, spieler.hoehe)
        powerupRechteck = pygame.Rect(self.x, self.y, self.breite, self.hoehe)
        if spielerRechteck.colliderect(powerupRechteck):
            if self.typ == "leben":
                spieler.leben += 1
            elif self.typ == "geschw":
                spieler.geschw += 1
            pygame.mixer.Sound.play(einsammelnSound)
            return True
        return False


def zeichnen():
    screen.blit(hintergrund, (0, 0))
    for k in kugeln:
        k.zeichnen()
    for z in zombies:
        z.zZeichnen()
    for p in powerups:
        p.zeichnen()
    spieler1.spZeichnen()
    spieler1.lebensanzeige()
    pygame.display.update()


spieler1 = spieler(300, 273, 5, 96, 128, -13, [0, 0, 1, 0], 0, 0)
zombie1 = zombie(600, 273, 4, 96, 128, 40, 800)
kugeln = []
zombies = [zombie1]
powerups = [powerup(200, 300, "leben"), powerup(400, 300, "geschw")]

while True:
    clock.tick(60)
    zeichnen()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        spieler1.laufen([True, False])
    elif keys[pygame.K_RIGHT]:
        spieler1.laufen([False, True])
    else:
        spieler1.stehen()

    if not spieler1.sprung:
        if keys[pygame.K_SPACE]:
            spieler1.sprungSetzen()

    if keys[pygame.K_x]:
        richtung = spieler1.richtg
        kugeln.append(kugel(spieler1.x, spieler1.y, richtung, 10))
        pygame.mixer.Sound.play(schiessenSound)  # Schießen Soundeffekt abspielen

    for kugel in kugeln[:]:
        kugel.bewegen()
        if kugel.x < 0 or kugel.x > screen.get_width():  # Kugel aus dem Bildschirm entfernen
            kugeln.remove(kugel)

    for zombie in zombies:
        zombie.hinHer()

    for powerup in powerups[:]:
        if powerup.einsammeln(spieler1):
            powerups.remove(powerup)

    spieler1.springen()
