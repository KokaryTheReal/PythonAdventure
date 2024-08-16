import pygame
import sys
import random
import time

from pygame import Surface, SurfaceType

pygame.init()

hintergrund = pygame.image.load("Grafiken/hintergrund.png")
screen: Surface | SurfaceType = pygame.display.set_mode([900, 450])
clock = pygame.time.Clock()
pygame.display.set_caption("2D Adventure")

pygame.mixer.music.load("Sounds/background-music.mp3")
pygame.mixer.music.play(-1)

schiessenSound = pygame.mixer.Sound("Sounds/laser-shoot.wav")
kollisionSound = pygame.mixer.Sound("Sounds/kollision.wav")
unverwundbarSound = pygame.mixer.Sound("Sounds/unverwundbar.wav")

angriffLinks = pygame.image.load("Grafiken/angriffLinks.png")
angriffRechts = pygame.image.load("Grafiken/angriffRechts.png")
sprung = pygame.image.load("Grafiken/sprung.png")
rechtsGehen = [pygame.image.load(f"Grafiken/rechts{i}.png") for i in range(1, 9)]
linksGehen = [pygame.image.load(f"Grafiken/links{i}.png") for i in range(1, 9)]
sprungSound = pygame.mixer.Sound("Sounds/cartoon-jump-6462.wav")
siegSound = pygame.mixer.Sound("Sounds/robosieg.wav")
verlorenSound = pygame.mixer.Sound("Sounds/robotod.wav")
siegBild = pygame.image.load("Grafiken/sieg.png")
verlorenBild = pygame.image.load("Grafiken/verloren.png")
leer = pygame.image.load("Grafiken/leer.png")
powerupBild: Surface | SurfaceType = pygame.image.load("Grafiken/powerup.png")

kugeln = []
powerups = []
spieler1 = None
zombie1 = None
zombie2 = None
gewonnen = False
verloren = False


def show_menu():
    menu_background = pygame.image.load("Grafiken/menu_background.png")
    screen.blit(menu_background, (0, 0))

    font_title = pygame.font.Font(None, 70)
    font_options = pygame.font.Font(None, 30)
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
        option_text = font_options.render(f"Drück {key}  {text}", True, option_color)
        if i < 7:
            option_rect = option_text.get_rect(topleft=(padding, 100 + i * 50))
        else:
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

        # Redraw menu
        screen.blit(menu_background, (0, 0))
        screen.blit(title_text, (150, 30))
        for i, (key, text) in enumerate(choices.items()):
            color = selected_color if i == selected_index else option_color
            option_text = font_options.render(f"Drück {key}  {text}", True, color)
            screen.blit(option_text, choice_rects[i].topleft)

        pygame.display.update()
        pygame.time.wait(100)

    return choices_made[0], choices_made[1], choices_made[2], choices_made[3]


class Spieler:
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
        self.shoot_speed = 6
        self.powerup_active = False
        self.powerup_end_time = 0
        self.double_jump = False
        self.double_jump_end_time = 0
        self.next_double_jump_time = random.randint(5, 10) + time.time()
        self.kugel = []

    def laufen(self, liste):
        if liste is None:
            raise ValueError("Liste darf nicht None seine.")

        if liste[0]:
            self.x -= self.geschw
            self.richtg = [1, 0, 0, 0]
            self.schritteLinks += 1
            if self.schritteLinks % 8 == 0:
                self.easterEggCount += 1
        if liste[1]:
            self.x += self.geschw
            self.richtg = [0, 1, 0, 0]
            self.schritteRechts += 1
            if self.schritteRechts % 8 == 0:
                self.easterEggCount += 1

    def easterEggAnzeigen(self):
        if self.easterEggCount >= 100:
            font = pygame.font.Font(None, 74)
            text = font.render("Du bist 100 Schritte gelaufen!", True, (255, 0, 0))
            screen.blit(text, (150, 200))

    def resetSchritte(self):
        self.schritteLinks = 0
        self.schritteRechts = 0

    def stehen(self):
        self.richtg = [0, 0, 1, 0]
        self.resetSchritte()

    def powerup_spawning(self):
        if not self.powerup_active:
            if random.randint(1, 100) == 1:
                self.powerup_x = random.randint(0, 900 - 20)
                self.powerup_y = random.randint(0, 450 - 20)
                self.powerup_start_time = pygame.time.get_ticks()
                self.powerup_active = True

        if self.powerup_active:
            screen.blit(powerupBild, (self.powerup_x, self.powerup_y))

            if (self.x < self.powerup_x + 20 and self.x + self.breite > self.powerup_x and
                    self.y < self.powerup_y + 20 and self.y + self.hoehe > self.powerup_y):
                self.powerup_active = False
                self.powerup_end_time = pygame.time.get_ticks() + 10000
                self.powerup_x = -1
                self.powerup_y = -1
                self.shoot_speed = 12
                unverwundbarSound.play()

        if pygame.time.get_ticks() > self.powerup_end_time and self.shoot_speed == 12:
            self.shoot_speed = 6

    def sprungSetzen(self):
        if self.sprungvar == -13:
            self.sprung = True
            if time.time() >= self.next_double_jump_time:
                self.double_jump = True
                self.double_jump_end_time = time.time() + 3
                self.next_double_jump_time = random.randint(5, 10) + time.time()
            if self.double_jump:
                self.sprungvar = 24
            else:
                self.sprungvar = 12
            pygame.mixer.Sound.play(sprungSound)

    def verwundbarkeit(self):
        if self.unverwundbar:
            if not self.unverwundbarSound_playing:
                unverwundbarSound.play()
                self.unverwundbarSound_playing = True
            if pygame.time.get_ticks() > self.unverwundbar_ende:
                self.unverwundbar = False
                self.unverwundbarSound_playing = False

    def bildAendern(self):
        if self.sprung:
            screen.blit(sprung, (self.x, self.y))
        else:
            if self.richtg[1]:
                screen.blit(rechtsGehen[self.schritteRechts // 8 % len(rechtsGehen)], (self.x, self.y))
            elif self.richtg[0]:
                screen.blit(linksGehen[self.schritteLinks // 8 % len(linksGehen)], (self.x, self.y))
            else:
                if self.last[1] == 1:
                    screen.blit(angriffRechts, (self.x, self.y))
                else:
                    screen.blit(angriffLinks, (self.x, self.y))

    def aufRaenderPruefen(self, liste):
        if liste[0]:
            if self.x - self.geschw < 0:
                self.x = 0
        if liste[1]:
            if self.x + self.geschw > 900 - self.breite:
                self.x = 900 - self.breite
        if liste[2]:
            if self.y - self.geschw < 0:
                self.y = 0
        if liste[3]:
            if self.y + self.geschw > 450 - self.hoehe:
                self.y = 450 - self.hoehe

    def anzeigen(self):
        self.bildAendern()
        self.verwundbarkeit()
        self.powerup_spawning()
        self.easterEggAnzeigen()
        if self.leben == 4:
            screen.blit(self.voll, (10, 10))
        elif self.leben == 3:
            screen.blit(self.halb, (10, 10))
        elif self.leben == 2:
            screen.blit(self.leer, (10, 10))
        elif self.leben == 1:
            screen.blit(self.leer, (10, 40))
        elif self.leben == 0:
            screen.blit(self.leer, (10, 70))
        pygame.display.update()

    def springen(self):
        if self.sprung:
            self.richtg = [0, 0, 0, 1]
            if self.sprungvar >= -13:
                n = 1
                if self.sprungvar < 0:
                    n = -1
                self.y -= (self.sprungvar ** 2) * 0.3 * n
                self.sprungvar -= 1
            else:
                self.sprung = False
                if time.time() > self.double_jump_end_time:
                    self.double_jump = False

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

    def updatePowerUp(self):
        if self.powerup_active and time.time() > self.powerup_end_time:
            self.powerup_active = False
            self.shoot_speed = 6

    def activatePowerUp(self):
        if not self.powerup_active:
            self.powerup_active = True
            self.powerup_end_time = time.time() + 3
            self.shoot_speed = 2

    def update(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.sprung = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                self.sprung = False

        if self.sprung:
            if self.double_jump:
                self.y -= 15
            else:
                self.y -= 10

        if self.y < 0:
            self.y = 0

    def kollision(self, andere):
        if (self.x < andere.x + andere.breite and
                self.x + self.breite > andere.x and
                self.y < andere.y + andere.hoehe and
                self.y + self.hoehe > andere.y):
            return True
        return False

    def punkteErhalten(self, punkte):
        self.punkte += punkte

    def punkteAbziehen(self, punkte):
        self.punkte -= punkte

    def schießen(self):
        neue_kugel = kugel(self.x, self.y)
        self.kugel.append(neue_kugel)


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
        pygame.draw.line(screen, (255, 0, 0), (self.x, self.y), (self.x + 5 * self.geschw, self.y), 5)


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
        self.angriffsmodus = False
        self.angriffEntfernung = 200
        self.zombieBlitzZeit = 0
        self.zombieUnverwundbarDauer = 1
        self.verstaerkungSchwelle = 3

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
        if not self.angriffsmodus:
            self.x += self.geschw
            if self.geschw > 0:
                self.richtg = [0, 1]
                self.schritteRechts += 1
            if self.geschw < 0:
                self.richtg = [1, 0]
                self.schritteLinks += 1

    def hinHer(self):
        if not self.angriffsmodus:
            if self.x > self.xMax:
                self.geschw *= -1
            elif self.x < self.xMin:
                self.geschw *= -1
            self.Laufen()

    def angreifen(self, spieler_position):
        entfernung = abs(self.x - spieler_position)
        if entfernung < self.angriffEntfernung:
            self.angriffsmodus = True
            if self.x < spieler_position:
                self.geschw = abs(self.geschw)
            else:
                self.geschw = -abs(self.geschw)
            self.Laufen()
        else:
            self.angriffsmodus = False

    def resetGetroffen(self):
        self.getroffen = False

    def schadenErleiden(self, schaden):
        if time.time() > self.zombieBlitzZeit + self.zombieUnverwundbarDauer:
            self.lebenzombie -= schaden
            self.zombieBlitzZeit = time.time()

            if self.lebenzombie > 0 and self.lebenzombie % self.verstaerkungSchwelle == 0:
                self.geschw *= 1.5

    def blitz(self):
        if time.time() - self.zombieBlitzZeit < self.zombieUnverwundbarDauer:
            if int(time.time() * 10) % 2 == 0:
                return True
        return False

    def anzeigen(self):
        if not self.blitz():
            self.zZeichnen()
        self.herzenzombie()

    def update(self, spieler_position):
        self.hinHer()
        self.angreifen(spieler_position)
        self.anzeigen()


def zeichnen():
    screen.blit(hintergrund, (0, 0))
    for k in kugeln:
        k.zeichnen()
    for powerup in powerups:
        powerup.zeichnen()
    spieler1.spZeichnen()
    zombie1.zZeichnen()
    if zombie2 is not None:
        zombie2.zZeichnen()
        zombie2.herzenzombie()
    zombie1.herzenzombie()
    spieler1.herzen()
    spieler1.punkteAnzeigen()
    spieler1.easterEggAnzeigen()
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


class PowerUp:
    def __init__(self, x, y, breite, hoehe, image):
        self.height = 20
        self.width = 20
        self.x = x
        self.y = y
        self.breite = breite
        self.hoehe = hoehe
        self.image = powerupBild
        self.rect = pygame.Rect(self.x, self.y, self.breite, self.hoehe)

    def zeichnen(self):
        screen.blit(self.image, (self.x, self.y))

    def update_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.breite, self.hoehe)

    def check_collision(self, player):
        powerup_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        player_rect = pygame.Rect(player.x, player.y, player.breite, player.hoehe)
        return powerup_rect.colliderect(player_rect)


def spawn_powerup():
    x = random.randint(0, 800)
    y = random.randint(0, 400)

    breite = 20
    hoehe = 20
    image = "Grafiken/powerup.png"

    powerups.append(PowerUp(x, y, breite, hoehe, image))


def Kollision():
    global kugeln, verloren, gewonnen, go, points_to_win, powerups

    zombie1Rechteck = pygame.Rect(zombie1.x + 18, zombie1.y + 24, zombie1.breite - 36, zombie1.hoehe - 24)

    if zombie2 is not None:
        zombie2Rechteck = pygame.Rect(zombie2.x + 18, zombie2.y + 24, zombie2.breite - 36, zombie2.hoehe - 24)
    else:
        zombie2Rechteck = None

    if zombie1 is not None:
        zombie1.resetGetroffen()
    else:
        print("zombie1 ist None.")

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

    for powerup in powerups[:]:
        if powerup.check_collision(spieler1):
            spieler1.activatePowerUp()
            powerups.remove(powerup)


def spielLoop(spieler_geschw=7, zombie_geschw=5):
    global gewonnen, verloren
    spieler1 = Spieler(x=100, y=300, geschw=spieler_geschw, breite=60, hoehe=71, sprungvar=12, richtg=[0, 0, 1, 0],
                       schritteRechts=0, schritteLinks=0)
    zombie1 = zombie(x=300, y=300, geschw=zombie_geschw, breite=64, hoehe=64, richtg=[1, 0], xMin=200, xMax=500)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(hintergrund, (0, 0))

        spieler1.herzen()
        zombie1.herzenzombie()

        spieler1.spZeichnen()
        zombie1.zZeichnen()

        pygame.display.update()
        clock.tick(30)


def spawnNeuerZombie():
    global zombie1, zombie2

    if zombie1.lebenzombie <= 0 and (zombie2 is None or zombie2.lebenzombie > 0):
        zombie1 = zombie(random.randint(40, 800), 273, zombie_speed, 96, 128, [0, 0], 40, 800)

    if zombie2 is not None and zombie2.lebenzombie <= 0 < zombie1.lebenzombie:
        zombie2 = zombie(random.randint(40, 800), 273, zombie_speed, 96, 128, [0, 0], 40, 800)


def setUnverwundbarSpieler():
    global unwidunzeit, unwidunstart
    unwidunzeit = random.uniform(5, 12)
    unwidunstart = time.time()
    spieler1.setUnverwundbar(3)


linkeWand = pygame.draw.rect(screen, (0, 0, 0), (1, 0, 2, 450), 0)
rechteWand = pygame.draw.rect(screen, (0, 0, 0), (899, 0, 2, 450), 0)

spieler1 = Spieler(300, 273, 5, 96, 128, -13, [0, 0, 1, 0], 0, 0)
powerup = PowerUp(100, 200, 20, 20, powerupBild)
zombie1 = zombie(600, 273, 6, 96, 128, [0, 0], 40, 800)
zombie2 = zombie(200, 273, 6, 96, 128, [0, 0], 40, 800)
verloren = False
gewonnen = False
kugel = []
laufrichtung = [False, False, False, False]
go = True
next_powerup_time: int = 0
spawn_powerup()
setUnverwundbarSpieler()


def main(laufrichtung=[False, False, False, False]):
    global go, verloren, gewonnen, spieler1, zombie1, zombie2, kugeln, points_to_win, zombie_speed, next_powerup_time

    player_speed, zombie_speed, points_to_win, zombie_count = show_menu()

    spieler1 = Spieler(300, 273, player_speed, 96, 128, -13, [0, 0, 1, 0], 0, 0)
    zombie1 = zombie(random.randint(40, 800), 273, zombie_speed, 96, 128, [0, 0], 40, 800)
    powerup = PowerUp(random.randint(0, 880), random.randint(0, 430), 20, 20, powerupBild)

    if zombie_count == 2:
        zombie2 = zombie(random.randint(40, 800), 273, zombie_speed, 96, 128, [0, 0], 40, 800)
    else:
        zombie2 = None

    unwidunzeit = 0
    unwidunstart = time.time()
    next_powerup_time = time.time() + 5

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(hintergrund, (0, 0))

        spieler1.laufen(laufrichtung)
        spieler1.sprungSetzen()
        spieler1.springen()
        spieler1.aufRaenderPruefen(laufrichtung)
        spieler1.spZeichnen()
        spielerRechteck = pygame.Rect(spieler1.x, spieler1.y, 96, 128)
        gedrueckt = pygame.key.get_pressed()

        if time.time() > next_powerup_time:
            spawn_powerup()
            next_powerup_time = time.time() + 10  # Nächstes PowerUp in 10 Sekunden

        if gedrueckt[pygame.K_RIGHT] and not spielerRechteck.colliderect(rechteWand):
            spieler1.laufen([0, 1])
        elif gedrueckt[pygame.K_LEFT] and not spielerRechteck.colliderect(linkeWand):
            spieler1.laufen([1, 0])
        else:
            spieler1.stehen()

        if gedrueckt[pygame.K_UP] and not spielerRechteck.colliderect(linkeWand or rechteWand):
            spieler1.springen()

        if gedrueckt[pygame.K_SPACE]:
            spieler1.schießen()

        if not verloren and not gewonnen:
            zombie1.hinHer()
            if zombie2:
                zombie2.hinHer()
            Kollision()

        if zombie1 is not None:
            zombie1.resetGetroffen()
        else:
            print("zombie1 ist None und kann nicht verwendet werden.")

        screen.blit(hintergrund, (0, 0))

        for powerup in powerups[:]:
            powerup.zeichnen()

            if spielerRechteck.colliderect(powerup.rect):
                spieler1.apply_powerup(powerup.typ)
                powerups.remove(powerup)
                pass

        if not verloren and not gewonnen:
            spieler1.updatePowerUp()

        spieler_geschw, zombie_geschw, punkte_zum_gewinn, anzahl_zombies = show_menu()
        spielLoop()

        if verloren:
            screen.blit(verlorenBild, (0, 0))
        elif gewonnen:
            screen.blit(siegBild, (0, 0))
        else:
            spieler1.spZeichnen()
            for KUGEL in spieler1.kugel[:]:
                KUGEL.bewegen()
                KUGEL.zeichnen()

            zombie1.zZeichnen()
            if zombie2:
                zombie2.zZeichnen()

        powerup.zeichnen()
        pygame.display.flip()
        clock.tick(60)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        zeichnen()


main()
