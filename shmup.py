# Background Music: Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3 <http://creativecommons.org/licenses/by/3.0/>
# Art from Kenny.nl
import pygame
import random

WIDTH = 480
HEIGHT = 600
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SHMUP!")
clock = pygame.time.Clock()

# draw text onto the screen
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, text_rect)

#spawn a new mob
def new_mob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

#draw a shield bar for the player
def draw_shield_bar(surf, x, y, shield_left):
    if shield_left <= 0:
        shield_left = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (shield_left / 500.0) * BAR_LENGTH
    outline_rect = pygame.Rect((x,y), (BAR_LENGTH, BAR_HEIGHT))
    fill_rect = pygame.Rect((x,y), (fill, BAR_HEIGHT))
    pygame.draw.rect(surf, WHITE, outline_rect,3)
    pygame.draw.rect(surf, GREEN, fill_rect)

# draw player lives used minified image of player
def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x - 30*i
        img_rect.y = y
        surf.blit(img, img_rect)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (60, 60))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 33
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 500
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hidden_timer = pygame.time.get_ticks()

    def update(self):
        if self.hidden and pygame.time.get_ticks() - self.hidden_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speedx = 5
        if keystate[pygame.K_SPACE] or keystate[pygame.K_UP]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()
    
    def hide(self):
        self.hidden = True
        self.hidden_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH /2, HEIGHT + 300)
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_img)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width) // 2
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150,-100)
        self.speedy = random.randrange(1,8)
        self.speedx = random.randrange(-3,3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()
    
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update  > 20:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = new_image.get_rect()
            self.rect.center = old_center
    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 25:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = -50
            self.speedy = 5
            self.speedx = random.randrange(-3,3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.height) // 2
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10
    
    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill() 
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75
    
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
#load graphics
background = pygame.image.load('assets/Backgrounds/stars.png').convert()
background_rect = background.get_rect()
player_img = pygame.image.load('assets/PNG/ufoGreen.png').convert()
player_live_img = pygame.transform.scale(player_img, (25, 25))
player_live_img.set_colorkey(BLACK)
meteor_list = ['meteorGrey_big1.png','meteorGrey_big2.png','meteorGrey_big3.png','meteorGrey_big4.png',
               'meteorGrey_med1.png','meteorGrey_med2.png',
               'meteorGrey_small1.png','meteorGrey_small2.png']
meteor_img = [pygame.image.load('assets/PNG/Meteors/' + name).convert() for name in meteor_list]
bullet_img = pygame.image.load('assets/PNG/Lasers/laserRed14.png').convert()
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'assets/PNG/Explosions/regularExplosion0{}.png'.format(i)
    img = pygame.image.load(filename).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75,75))
    img_sm = pygame.transform.scale(img, (32,32))
    explosion_anim['lg'].append(img_lg)
    explosion_anim['sm'].append(img_sm)
    filename = 'assets/PNG/Explosions/sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(filename).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)
#load Music
shoot_sound = pygame.mixer.Sound('assets/Music/hit.wav')
death_sound = pygame.mixer.Sound('assets/Music/explosion.wav')
death_sound.set_volume(0.5)
rumble_sound = pygame.mixer.Sound('assets/Music/rumble.ogg')
pygame.mixer.music.load('assets/Music/background.ogg')
pygame.mixer.music.set_volume(0.4)

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
    
for i in range(8):
    new_mob()
pygame.mixer.music.play(-1)
score = 0
# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    #check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(bullets,mobs, True, True)
    for hit in hits:
        score += 50 - hit.radius
        death_sound.play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        new_mob()
    #check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius*2
        death_sound.play()
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        new_mob()
        if player.shield <= 0:
            rumble_sound.play()
            expl = Explosion(hit.rect.center, 'player')
            all_sprites.add(expl)
            player.hide()
            player.lives -= 1
            player.shield = 500
    # if the player died and the explosion
    if player.lives == 0 and not expl.alive():
        running = False
    # Draw / render
    screen.fill(BLACK)
    screen.blit(background,background_rect)
    draw_text(screen, "Score: " + str(score),18, WIDTH / 2 , 10)
    draw_shield_bar(screen, 5,5, player.shield)
    draw_lives(screen, WIDTH - 35, 5, player.lives, player_live_img)
    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
