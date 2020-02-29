import pygame
import sqlite3
from random import randint

font = "joystix_monospace.ttf"
score = 0
additonalbonus = 0


def text_format(message, textFont, textSize, textColor):
    newFont = pygame.font.Font(textFont, textSize)
    newText = newFont.render(message, 0, textColor)
    return newText


def car_and_player_select():
    pygame.init()
    pygame.mixer.music.load('menusound.wav')

    display_width = 800
    display_height = 600

    game_display = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("Race")

    clock = pygame.time.Clock()
    FPS = 120

    bg = pygame.image.load('bridge-cityscape-pixel-art.jpg')

    name = "player"
    player_name = "Name: {}".format(name)

    start_button = "Start"
    selected = player_name
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                pygame.mixer.music.play()
                if event.key == pygame.K_DOWN:
                    selected = start_button
                elif event.key == pygame.K_UP:
                    selected = player_name
                if selected == player_name:
                    if event.key == pygame.K_BACKSPACE:
                        name = name[:len(name) - 1]
                    else:
                        if len(name) < 6:
                            name += event.unicode.lower()
                    player_name = "Name: {}".format(name)
                    selected = player_name
                if selected == start_button:
                    if event.key == pygame.K_RETURN:
                        race(name)

        game_display.blit(bg, (0, 0))

        title = text_format("Race", font, 90, pygame.Color('white'))

        if selected == player_name:
            text_player = text_format("!" + player_name + "!", font, 60, (200, 0, 200))
        else:
            text_player = text_format(player_name, font, 60, (255, 255, 255))
        if selected == start_button:
            text_start = text_format("!" + start_button + "!", font, 60, (200, 0, 200))
        else:
            text_start = text_format(start_button, font, 60, (255, 255, 255))

        title_rect = title.get_rect()
        player_rect = text_player.get_rect()
        start_rect = text_start.get_rect()

        game_display.blit(title, (display_width / 2 - (title_rect[2] / 2), 80))
        game_display.blit(text_player, (display_width / 2 - (player_rect[2] / 2), 300))
        game_display.blit(text_start, (display_width / 2 - (start_rect[2] / 2), 360))

        pygame.display.update()
        clock.tick(FPS)


def main_menu():
    pygame.init()
    pygame.mixer.music.load('menusound.wav')

    display_width = 800
    display_height = 600

    game_display = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("Race")

    bg = pygame.image.load('bridge-cityscape-pixel-art.jpg')

    clock = pygame.time.Clock()
    FPS = 30

    button1 = 'Race Game'
    button2 = "Leaderboard"
    selected = button1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                pygame.mixer.music.play()
                if event.key == pygame.K_UP:
                    selected = button1
                elif event.key == pygame.K_DOWN:
                    selected = button2
                elif event.key == pygame.K_RETURN:
                    if selected == button1:
                        car_and_player_select()
                    elif selected == button2:
                        leaderboard()

        game_display.blit(bg, (0, 0))
        title = text_format("SomeRace", font, 90, pygame.Color('white'))
        if selected == button1:
            text_race = text_format("!" + button1 + "!", font, 60, (200, 0, 200))
        else:
            text_race = text_format(button1, font, 60, pygame.Color('white'))
        if selected == button2:
            text_run = text_format("!" + button2 + "!", font, 60, (200, 0, 200))
        else:
            text_run = text_format(button2, font, 60, pygame.Color('white'))

        title_rect = title.get_rect()
        race_rect = text_race.get_rect()
        run_rect = text_run.get_rect()

        game_display.blit(title, (display_width / 2 - (title_rect[2] / 2), 80))
        game_display.blit(text_race, (display_width / 2 - (race_rect[2] / 2), 300))
        game_display.blit(text_run, (display_width / 2 - (run_rect[2] / 2), 360))

        pygame.display.update()
        clock.tick(FPS)


class Car(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__()

        self.oldimage = pygame.image.load('yellowcar.png')
        self.image = pygame.transform.scale(self.oldimage, (60, 140))
        self.rect = self.image.get_rect()
        self.add(group)
        self.rect.x = 430
        self.rect.y = 460

    def update(self, game_paused, movingright, movingleft, movingforward, movingback):
        if not game_paused:
            if movingleft:
                if self.rect.x > 0:
                    self.rect.x -= 6
            if movingright:
                if self.rect.x < 800 - 60:
                    self.rect.x += 6
            if movingback:
                if self.rect.y < 600 - 140:
                    self.rect.y += 6
            if movingforward:
                if self.rect.y > 0:
                    self.rect.y -= 6


class Block(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__()
        self.oldimage = pygame.image.load('QQcPh2g.png')
        self.image = pygame.transform.scale(self.oldimage, (randint(60, 120), 20))

        self.add(group)

        self.x = randint(0, 720)
        self.rect = self.image.get_rect(center=(self.x, 0))
        self.speed = 6

    def update(self):
        global score
        if self.rect.y < 600:
            self.rect.y += self.speed + score / 10
        else:
            score += 1
            self.kill()


class Bonus(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__()

        self.oldimage = pygame.image.load('star.png')
        self.image = pygame.transform.scale(self.oldimage, (40, 40))

        self.add(group)

        self.x = randint(0, 720)
        self.rect = self.image.get_rect(center=(self.x, 0))
        self.speed = 6

    def update(self):
        global score
        if self.rect.y < 600:
            self.rect.y += self.speed + score / 10
        else:
            self.kill()


def dodged():
    text_score = text_format("Score: {}".format(score + additonalbonus), font, 30, (0, 0, 0))
    return text_score


def race(name):
    global score
    global additonalbonus
    pygame.time.set_timer(pygame.USEREVENT, 750)
    all_sprites = pygame.sprite.Group()
    blocks = pygame.sprite.Group()
    bonuspoints = pygame.sprite.Group()
    sound1 = pygame.mixer.Sound('crashsound.wav')
    sound2 = pygame.mixer.Sound('bonus.wav')
    movingleft = False
    movingright = False
    movingforward = False
    movingback = False
    game_paused = False
    crashed = False
    crash_sound_played = False
    score_added = False
    player_name = name
    pygame.init()
    display_width = 800
    display_height = 600

    bg = pygame.image.load('backgroundroad.png')

    display = pygame.display.set_mode((display_width, display_height))

    clock = pygame.time.Clock()

    player = Car(all_sprites)
    bgy = -600

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if not crashed:
                if not game_paused:
                    if event.type == pygame.USEREVENT:
                        Block(blocks)
                        Bonus(bonuspoints)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        movingleft = True
                    if event.key == pygame.K_RIGHT:
                        movingright = True
                    if event.key == pygame.K_UP:
                        movingforward = True
                    if event.key == pygame.K_DOWN:
                        movingback = True
                    if event.key == pygame.K_ESCAPE:
                        if not game_paused:
                            game_paused = True
                        else:
                            game_paused = False
                    if game_paused:
                        if event.key == pygame.K_q:
                            main_menu()

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        movingleft = False
                    if event.key == pygame.K_RIGHT:
                        movingright = False
                    if event.key == pygame.K_UP:
                        movingforward = False
                    if event.key == pygame.K_DOWN:
                        movingback = False
            else:
                if not crash_sound_played:
                    sound1.play()
                    crash_sound_played = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        main_menu()
                    if event.key == pygame.K_a:
                        race(player_name)

        if not crashed:
            if not game_paused:
                if bgy <= 0:
                    bgy += 6 + score / 10
                else:
                    bgy -= 600
            display.blit(bg, (0, bgy))

            all_sprites.draw(display)
            blocks.draw(display)
            bonuspoints.draw(display)

            display.blit(dodged(), (0, 0))

            blocks_hit_list = pygame.sprite.spritecollide(player, blocks, False)
            bonus_hit_list = pygame.sprite.spritecollide(player, bonuspoints, True)

            if len(blocks_hit_list) > 0:
                crashed = True
            if len(bonus_hit_list) > 0:
                additonalbonus += 10
                sound2.play()
            if game_paused:
                text_paused = text_format("press 'q' to quit", font, 30, (0, 0, 0))
                display.blit(text_paused, (0, 45))
            if not game_paused:
                blocks.update()
                bonuspoints.update()
                player.update(game_paused, movingright, movingleft, movingforward, movingback)
        else:
            if not score_added:
                add_score(player_name, score, additonalbonus)
                score_added = True
            score = 0
            additonalbonus = 0

            text_quit = text_format("press 'q' to quit", font, 30, (0, 0, 0))
            display.blit(text_quit, (0, 45))

            text_paused = text_format("press 'a' to play again", font, 30, (0, 0, 0))
            display.blit(text_paused, (0, 90))

            text_crashed = text_format("Crashed", font, 90, (0, 0, 0))
            display.blit(text_crashed, (140, 200))

        pygame.display.update()
        clock.tick(60)


def add_score(name, score, bonus):

    added = False
    totalscore = score + bonus

    con = sqlite3.connect('LeaderboardDataBase.db')
    cur = con.cursor()
    result = cur.execute('''SELECT * FROM Leaderboard''').fetchall()

    for element in result:
        if name == element[0]:
            if totalscore > int(element[1]):
                cur.execute('UPDATE Leaderboard SET Score = "%s" WHERE Player_Name == "%s"' % (totalscore, name))
            added = True
            break

    if not added:
        cur.execute("INSERT INTO Leaderboard(Player_Name, Score) VALUES('%s', '%s')" % (name, totalscore))

    con.commit()
    con.close()


def leaderboard():
    pygame.init()
    pygame.mixer.music.load('menusound.wav')

    display_width = 800
    display_height = 600

    display = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("Race")

    bg = pygame.image.load('bridge-cityscape-pixel-art.jpg')

    clock = pygame.time.Clock()
    FPS = 30

    con = sqlite3.connect("LeaderboardDataBase.db")
    cur = con.cursor()
    result = cur.execute('''SELECT * FROM Leaderboard ORDER BY Score desc''').fetchall()
    cur.close()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()

        text_quit = text_format("press 'esc' to main menu", font, 30, (0, 0, 0))

        display.blit(bg, (0, 0))
        display.blit(text_quit, (0, 0))
        if len(result) >= 5:
	        for i in range(5):
	            display.blit(text_format("{}.".format(i + 1) + result[i][0] + " - " + str(result[i][1]),
	                                         font, 50, (0, 0, 0)), (100, 120 + 65 * i))
	else:
		for i in range(len(result)):
			display.blit(text_format("{}.".format(i + 1) + result[i][0] + " - " + str(result[i][1]),
	                                         font, 50, (0, 0, 0)), (100, 120 + 65 * i))
        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main_menu()
