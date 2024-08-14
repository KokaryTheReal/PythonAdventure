import pygame
import sys
import random
import time

pygame.init()

hintergrund = pygame.image.load("Grafiken/hintergrund.png")
screen = pygame.display.set_mode([900, 450])
clock = pygame.time.Clock()
pygame.display.set_caption("2d adventure")

pygame.mixer.music.load("Sounds/background-music.mp3")
pygame.mixer.music.play(-1)

schiessenSound = pygame.mixer.Sound("Sounds/laser-shoot.wav")
kollisionSound = pygame.mixer.Sound("Sounds/kollision.wav")
unverwundbarSound = pygame.mixer.Sound("Sounds/unverwundbar.wav")

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
sprungSound = pygame.mixer.Sound("Sounds/cartoon-jump-6462.wav")
siegSound = pygame.mixer.Sound("Sounds/robosieg.wav")
verlorenSound = pygame.mixer.Sound("Sounds/robotod.wav")
siegBild = pygame.image.load("Grafiken/sieg.png")
verlorenBild = pygame.image.load("Grafiken/verloren.png")
leer = pygame.image.load("Grafiken/leer.png")


def show_menu():
    menu_background = pygame.image.load("Grafiken/menu_background.png")
    screen.blit(menu_background, (0, 0))

    font_title = pygame.font.Font(None, 74)
    font_options = pygame.font.Font(None, 36)
    title_color = (255, 215, 0)
    option_color = (0, 0, 255)
    selected_color = (0, 255, 0)

    title_text = font_title.render("Wähle die Optionen", True, title_color)
    screen.blit(title_text, (150, 30))

    choices = {
        "1": "Spieler Speed: 5",
        "2": "Spieler Speed: 10",
        "3": "Spieler Speed: 15",
        "4": "Zombie Speed: 3",
        "5": "Zombie Speed: 6",
        "6": "Zombie Speed: 9",
        "7": "Punkte zum Gewinnen: 50",
        "8": "Punkte zum Gewinnen: 100",
        "9": "Punkte zum Gewinnen: 150",
        "Z": "Anzahl Zombies: 1",
        "X": "Anzahl Zombies: 2"
    }

    choice_rects = []
    padding = 50
    for i, (key, text) in enumerate(choices.items()):
        if i < 7:
            option_text = font_options.render(f"Drück {key}  {text}", True, option_color)
            option_rect = option_text.get_rect(topleft=(padding, 100 + i * 50))
        else:
            option_text = font_options.render(f"Drück {key}  {text}", True, option_color)
            option_rect = option_text.get_rect(topright=(900 - padding, 100 + (i - 7) * 50))

        choice_rects.append(option_rect)
        screen.blit(option_text, option_rect.topleft)

    pygame.display.update()

    choices_made = [None, None, None, None]
    selected_index = 0

    while None in choices_made:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(choices)
                if event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(choices)
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7,
                                 pygame.K_8, pygame.K_9, pygame.K_z, pygame.K_x]:
                    choice_key = chr(event.key).upper()
                    if choice_key in choices:
                        if choice_key in ['1', '2', '3']:
                            choices_made[0] = int(choices[choice_key].split(": ")[1])
                        elif choice_key in ['4', '5', '6']:
                            choices_made[1] = int(choices[choice_key].split(": ")[1])
                        elif choice_key in ['7', '8', '9']:
                            choices_made[2] = int(choices[choice_key].split(": ")[1])
                        elif choice_key in ['Z', 'X']:
                            choices_made[3] = int(choices[choice_key].split(": ")[1])

        screen.blit(menu_background, (0, 0))
        screen.blit(title_text, (150, 30))
        for i, (key, text) in enumerate(choices.items()):
            color = selected_color if i == selected_index else option_color
            if i < 7:
                option_text = font_options.render(f"Drück {key}  {text}", True, color)
                screen.blit(option_text, choice_rects[i].topleft)
            else:
                option_text = font_options.render(f"Drück {key}  {text}", True, color)
                screen.blit(option_text, choice_rects[i].topleft)

        pygame.display.update()
        pygame.time.wait(100)

    return choices_made[0], choices_made[1], choices_made[2], choices_made[3]


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
        self.ok = True
        self.unverwundbar = False
        self.unverwundbar_ende = 0
        self.unverwundbar_start = 0
        self.unverwundbarSound_playing = False
        self.leben = 4
        self.punkte = 0
        self.voll = pygame.image.load("Grafiken/voll.png")
        self.halb = pygame.image.load("Grafiken/halb.png")
        self.leer = pygame.image.load("Grafiken/leer.png")
        self.easterEggCount = 0

    def laufen(self, liste):
        if liste[0]:
            self.x -= self.geschw
            self.richtg = [1, 0, 0, 0]
            self.schritteLinks += 1
            self.easterEggCount += 1
        if liste[1]:
            self.x += self.geschw
            self.richtg = [0, 1, 0, 0]
            self.schritteRechts += 1
            self.easterEggCount += 1

    def easterEggAnzeigen(self):
        if self.easterEggCount >= 10:
            font = pygame.font.Font(None, 74)
            text = font.render("Wow du bist 10 Schritte gelaufen!", True, (255, 0, 0))
            screen.blit(text, (150, 200))

    def resetSchritte(self):
        self.schritteLinks = 0
        self.schritteRechts = 0

    def stehen(self):
        self.richtg = [0, 0, 1, 0]
        self.resetSchritte()

    def sprungSetzen(self):
        if self.sprungvar == -13:
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
                self.y -= (self.sprungvar ** 2) * 0.3 * n
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

    def herzen(self):
        if self.leben >= 2:
            screen.blit(self.voll, (207, 15))
        if self.leben >= 4:
            screen.blit(self.voll, (267, 15))

        if self.leben == 1:
            screen.blit(self.halb, (207, 15))
        elif self.leben >= 3:
            screen.blit(self.halb, (267, 15))

        if self.leben <= 0:
            screen.blit(self.leer, (207, 15))
        if self.leben >= 2:
            screen.blit(self.leer, (267, 15))

    def updateUnverwundbar(self):
        if self.unverwundbar and time.time() > self.unverwundbar_ende:
            self.unverwundbar = False
            if self.unverwundbarSound_playing:
                pygame.mixer.Sound.stop(unverwundbarSound)
                self.unverwundbarSound_playing = False

    def setUnverwundbar(self, dauer):
        if not self.unverwundbar:
            self.unverwundbar = True
            self.unverwundbar_ende = time.time() + dauer
            pygame.mixer.Sound.play(unverwundbarSound)
            self.unverwundbarSound_playing = True

    def punkteAnzeigen(self):
        font = pygame.font.Font(None, 36)
        text = font.render(f"Punkte: {self.punkte}", True, (255, 255, 255))
        screen.blit(text, (10, 10))


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
    def __init__(self, x, y, geschw, breite, hoehe, richtg, xMin, xMax):
        self.x = x
        self.y = y
        self.geschw = geschw
        self.breite = breite
        self.hoehe = hoehe
        self.richtg = richtg
        self.schritteRechts = 0
        self.schritteLinks = 0
        self.xMin = xMin
        self.xMax = xMax
        self.lebenzombie = 6
        self.linksListe = [pygame.image.load("Grafiken/l1.png"), pygame.image.load("Grafiken/l2.png"),
                           pygame.image.load("Grafiken/l3.png"), pygame.image.load("Grafiken/l4.png"),
                           pygame.image.load("Grafiken/l5.png"), pygame.image.load("Grafiken/l6.png"),
                           pygame.image.load("Grafiken/l7.png"), pygame.image.load("Grafiken/l8.png")]
        self.rechtsListe = [pygame.image.load("Grafiken/r1.png"), pygame.image.load("Grafiken/r2.png"),
                            pygame.image.load("Grafiken/r3.png"), pygame.image.load("Grafiken/r4.png"),
                            pygame.image.load("Grafiken/r5.png"), pygame.image.load("Grafiken/r6.png"),
                            pygame.image.load("Grafiken/r7.png"), pygame.image.load("Grafiken/r8.png")]
        self.ganzzombie = pygame.image.load("Grafiken/vollzombie.png")
        self.halbzombie = pygame.image.load("Grafiken/halbzombie.png")
        self.getroffen = False

    def herzenzombie(self):
        offset_x = 60

        start_x = self.x - (1 * offset_x)
        base_y = self.y - 40

        if self.lebenzombie >= 2:
            screen.blit(self.ganzzombie, (start_x, base_y))
        if self.lebenzombie >= 4:
            screen.blit(self.ganzzombie, (start_x + offset_x, base_y))
        if self.lebenzombie == 6:
            screen.blit(self.ganzzombie, (start_x + 2 * offset_x, base_y))

        if self.lebenzombie == 1:
            screen.blit(self.halbzombie, (start_x, base_y))
        elif self.lebenzombie == 3:
            screen.blit(self.halbzombie, (start_x + offset_x, base_y))
        elif self.lebenzombie == 5:
            screen.blit(self.halbzombie, (start_x + 2 * offset_x, base_y))

        if self.lebenzombie <= 0:
            screen.blit(leer, (start_x, base_y))
        if self.lebenzombie <= 2:
            screen.blit(leer, (start_x + offset_x, base_y))
        if self.lebenzombie <= 4:
            screen.blit(leer, (start_x + 2 * offset_x, base_y))

    def zZeichnen(self):
        if self.schritteRechts == 63:
            self.schritteRechts = 0
        if self.schritteLinks == 63:
            self.schritteLinks = 0

        if self.richtg[0]:
            screen.blit(self.linksListe[self.schritteLinks // 8], (self.x, self.y))
        if self.richtg[1]:
            screen.blit(self.rechtsListe[self.schritteRechts // 8], (self.x, self.y))

    def Laufen(self):
        self.x += self.geschw
        if self.geschw > 0:
            self.richtg = [0, 1]
            self.schritteRechts += 1
        if self.geschw < 0:
            self.richtg = [1, 0]
            self.schritteLinks += 1

    def hinHer(self):
        if self.x > self.xMax:
            self.geschw *= -1
        elif self.x < self.xMin:
            self.geschw *= -1
        self.Laufen()

    def resetGetroffen(self):
        self.getroffen = False


def zeichnen():
    screen.blit(hintergrund, (0, 0))
    for k in kugeln:
        k.zeichnen()
    spieler1.spZeichnen()
    zombie1.zZeichnen()
    if zombie2 is not None:
        zombie2.zZeichnen()
        zombie2.herzenzombie()
    zombie1.herzenzombie()
    spieler1.herzen()
    spieler1.punkteAnzeigen()
    if gewonnen:
        screen.blit(siegBild, (0, 0))
    elif verloren:
        screen.blit(verlorenBild, (0, 0))
    pygame.display.update()


def kugelHandler():
    global kugeln
    for k in kugeln:
        if 0 <= k.x <= 900:
            k.bewegen()
        else:
            kugeln.remove(k)


def Kollision():
    global kugeln, verloren, gewonnen, go, points_to_win

    zombie1Rechteck = pygame.Rect(zombie1.x + 18, zombie1.y + 24, zombie1.breite - 36, zombie1.hoehe - 24)

    if zombie2 is not None:
        zombie2Rechteck = pygame.Rect(zombie2.x + 18, zombie2.y + 24, zombie2.breite - 36, zombie2.hoehe - 24)
    else:
        zombie2Rechteck = None

    spielerRechteck = pygame.Rect(spieler1.x + 18, spieler1.y + 36, spieler1.breite - 36, spieler1.hoehe - 36)

    to_remove = []

    for k in kugeln:
        start_pos = (k.x, k.y)
        end_pos = (k.x + 5 * k.geschw, k.y)
        if zombie1Rechteck.clipline(start_pos, end_pos):
            to_remove.append(k)
            zombie1.lebenzombie -= 1
            if not zombie1.getroffen:
                pygame.mixer.Sound.play(kollisionSound)
                zombie1.getroffen = True
            if zombie1.lebenzombie <= 0 and not verloren:
                spieler1.punkte += 10
                spawnNeuerZombie()

        if zombie2 is not None and zombie2Rechteck is not None and zombie2Rechteck.clipline(start_pos, end_pos):
            to_remove.append(k)
            zombie2.lebenzombie -= 1
            if not zombie2.getroffen:
                pygame.mixer.Sound.play(kollisionSound)
                zombie2.getroffen = True
            if zombie2.lebenzombie <= 0 and not verloren:
                spieler1.punkte += 10
                spawnNeuerZombie()

    for k in to_remove:
        if k in kugeln:
            kugeln.remove(k)

    if zombie1Rechteck.colliderect(spielerRechteck) or (
            zombie2Rechteck is not None and zombie2Rechteck.colliderect(spielerRechteck)):
        if not spieler1.unverwundbar:
            spieler1.leben -= 1
            if spieler1.leben <= 0:
                verloren = True
                pygame.mixer.Sound.play(verlorenSound)
                go = False
            else:
                spieler1.setUnverwundbar(3)
                pygame.mixer.Sound.play(kollisionSound)

    zombie1.resetGetroffen()
    if zombie2 is not None:
        zombie2.resetGetroffen()

    if spieler1.punkte >= points_to_win:
        gewonnen = True
        pygame.mixer.Sound.play(siegSound)
        go = False


def spawnneuerzombie():
    global zombie1, zombie2

    if zombie1 is None or zombie1.lebenzombie <= 0:
        zombie1 = zombie(random.randint(40, 800), 273, zombie_speed, 96, 128, [0, 0], 40, 800)

    if zombie2 is None or zombie2.lebenzombie <= 0:
        zombie2 = zombie(random.randint(40, 800), 273, zombie_speed, 96, 128, [0, 0], 40, 800)


def setUnverwundbarSpieler():
    global unwidunzeit, unwidunstart
    unwidunzeit = random.uniform(5, 12)
    unwidunstart = time.time()
    spieler1.setUnverwundbar(3)


linkeWand = pygame.draw.rect(screen, (0, 0, 0), (1, 0, 2, 450), 0)
rechteWand = pygame.draw.rect(screen, (0, 0, 0), (899, 0, 2, 450), 0)
spieler1 = spieler(300, 273, 5, 96, 128, -13, [0, 0, 1, 0], 0, 0)
zombie1 = zombie(600, 273, 6, 96, 128, [0, 0], 40, 800)
zombie2 = zombie(200, 273, 6, 96, 128, [0, 0], 40, 800)
verloren = False
gewonnen = False
kugeln = []
go = True

setUnverwundbarSpieler()


def spawnNeuerZombie():
    global zombie1, zombie2

    if zombie1.lebenzombie <= 0 and (zombie2 is None or zombie2.lebenzombie > 0):
        zombie1 = zombie(random.randint(40, 800), 273, zombie_speed, 96, 128, [0, 0], 40, 800)

    if zombie2 is not None and zombie2.lebenzombie <= 0 < zombie1.lebenzombie:
        zombie2 = zombie(random.randint(40, 800), 273, zombie_speed, 96, 128, [0, 0], 40, 800)


def main():
    global go, verloren, gewonnen, spieler1, zombie1, zombie2, kugeln, unwidunstart, unwidunzeit, points_to_win, zombie_speed

    player_speed, zombie_speed, points_to_win, zombie_count = show_menu()

    spieler1 = spieler(300, 273, player_speed, 96, 128, -13, [0, 0, 1, 0], 0, 0)
    zombie1 = zombie(random.randint(40, 800), 273, zombie_speed, 96, 128, [0, 0], 40, 800)

    if zombie_count == 2:
        zombie2 = zombie(random.randint(40, 800), 273, zombie_speed, 96, 128, [0, 0], 40, 800)
    else:
        zombie2 = None

    if zombie_count > 1:
        zombie2 = zombie(random.randint(40, 800), 273, zombie_speed, 96, 128, [0, 0], 40, 800)
    else:
        zombie2 = None

    unwidunzeit = 0
    unwidunstart = time.time()

    while go:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        spielerRechteck = pygame.Rect(spieler1.x, spieler1.y, 96, 128)
        gedrueckt = pygame.key.get_pressed()

        if gedrueckt[pygame.K_RIGHT] and not spielerRechteck.colliderect(rechteWand):
            spieler1.laufen([0, 1])
        elif gedrueckt[pygame.K_LEFT] and not spielerRechteck.colliderect(linkeWand):
            spieler1.laufen([1, 0])
        else:
            spieler1.stehen()

        if gedrueckt[pygame.K_UP]:
            spieler1.sprungSetzen()
        spieler1.springen()

        if gedrueckt[pygame.K_SPACE]:
            if len(kugeln) <= 0 and spieler1.ok:
                kugeln.append(kugel(round(spieler1.x), round(spieler1.y), spieler1.last, 6))
                pygame.mixer.Sound.play(schiessenSound)
            spieler1.ok = False

        if not gedrueckt[pygame.K_SPACE]:
            spieler1.ok = True

        kugelHandler()
        zombie1.hinHer()
        if zombie2:
            zombie2.hinHer()

        spieler1.updateUnverwundbar()
        if time.time() - unwidunstart >= unwidunzeit:
            setUnverwundbarSpieler()

        Kollision()
        zeichnen()
        clock.tick(60)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        zeichnen()


main()
