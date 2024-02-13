import pygame
import random
from pygame import mixer

pygame.init()
mixer.init()
pygame.font.init()

width = 800
height = 600
WIN = pygame.display.set_mode((width, height))
pygame.display.set_caption('Blaster')

# load background image and music
BG = pygame.image.load('background.png')
mixer.music.load('background.wav')
mixer.music.play(-1)

# load player image
player_img = pygame.image.load('player.png')
player_bullet = pygame.image.load('bullet.png')

# enemy and enemy laser image
red_ship = pygame.image.load('pixel_ship_red_small.png')
blue_ship = pygame.image.load('pixel_ship_blue_small.png')
green_ship = pygame.image.load('pixel_ship_green_small.png')
monstar = pygame.image.load('enemy.png')

red_laser = pygame.image.load('pixel_laser_red.png')
blue_laser = pygame.image.load('pixel_laser_blue.png')
green_laser = pygame.image.load('pixel_laser_green.png')
monstar_laser = pygame.image.load('pixel_laser_yellow.png')


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not (self.y < height and self.y >= 0)

    def collision(self, obj):

        return collide(self, obj)



class Ship:
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(height):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 5
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = player_img
        self.laser_img = player_bullet
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.SCORE=0

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x + 15, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
            laser_music = mixer.Sound('laser.wav')
            laser_music.play()

    def update_score(self):
        self.SCORE+=1

    def get_score(self):
        return self.SCORE




    def move_lasers(self, vel, objs):
        self.cooldown()

        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(height):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        self.update_score()
                        collision_music = mixer.Sound('explosion.wav')
                        collision_music.play()

                        objs.remove(obj)

                        if laser in self.lasers:
                            self.lasers.remove(laser)


    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0),
                         (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10,
                                               self.ship_img.get_width() * (self.health / self.max_health), 10))

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)


class Enemy(Ship):
    COLOR_MAP = {"red": (red_ship, red_laser),
                 "blue": (blue_ship, blue_laser),
                 "green": (green_ship, green_laser),
                 "monstar": (monstar, monstar_laser)}

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 15, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
            laser_music = mixer.Sound('laser.wav')
            laser_music.play()


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y

    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def main():
    run = True
    fps = 60
    level = 0
    lives = 5
    vel = 10
    laser_vel = 5
    main_font = pygame.font.SysFont("comicsans", 40)
    lost_font = pygame.font.SysFont("comicsans", 70)
    score_font = pygame.font.SysFont("comicsans",30)

    enemies = []
    enemy_vel = 1
    wav_length = 5

    player = Player(300, 500)




    clock = pygame.time.Clock()
    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(BG, (0, 0))
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", True, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", True, (255, 255, 255))
        score_label = score_font.render(f"Score: {player.get_score()}",True,(255,255,255))
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (800 - level_label.get_width() - 10, 10))
        WIN.blit(score_label,(10,lives_label.get_height()+30))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        for enemy in enemies:
            enemy.draw(WIN)

        if lost:
            lost_label = lost_font.render('YOU LOST :(', True, (255, 255, 255))
            lost_label_rect = lost_label.get_rect(center=(width / 2, height / 2 - 50))
            score_label = lost_font.render(f'Your Score: {player.get_score()}', True, (255, 255, 255))
            score_label_rect = score_label.get_rect(center=(width / 2, height / 2 + 50))
            WIN.blit(lost_label, lost_label_rect)
            WIN.blit(score_label, score_label_rect)

        pygame.display.update()

    while run:
        clock.tick(fps)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > fps * 5:
                run = False
            else:
                continue

        if len(enemies) == 0:

            level += 1
            wav_length += 5

            for i in range(wav_length):
                enemy = Enemy(random.randrange(50, width - 100), random.randrange(-1000, -100),
                              random.choice(['red', 'blue', 'green', 'monstar']))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - vel > 0:
            player.x -= vel

        if keys[pygame.K_RIGHT] and player.x + vel + player.get_width() < width:
            player.x += vel

        if keys[pygame.K_UP] and player.y - vel > 0:
            player.y -= vel

        if keys[pygame.K_DOWN] and player.y + vel + player.get_height()+20 < height:
            player.y += vel

        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 3 * fps) == 1:
                enemy.shoot()





            if collide(enemy, player):
                player.health -= 10
                collision_music = mixer.Sound('explosion.wav')
                collision_music.play()
                enemies.remove(enemy)






            elif enemy.y + enemy.get_height() > height:
                lives -= 1
                enemies.remove(enemy)


        player.move_lasers(-laser_vel, enemies)


def main_menu():
    title_font=pygame.font.SysFont("comicsans",50)
    game_name=pygame.font.SysFont("comicsans",80)


    run=True
    while run:
        WIN.blit(BG,(0,0))
        game_label=game_name.render("WELCOME TO BLASTER",True,(255,255,255))
        title_label = title_font.render("Press Enter to begin... ", True, (255, 255, 255))
        WIN.blit(title_label, (width / 2 - title_label.get_width() / 2, height / 2))
        WIN.blit(game_label,(width/2-game_label.get_width()/2,height/2-title_label.get_height()-40))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    main()


    pygame.quit()

main_menu()
