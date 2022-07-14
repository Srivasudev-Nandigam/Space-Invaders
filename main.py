import pygame
import math
import random
from pygame import mixer

# Initialize the pygame
pygame.init()

# Background
background = pygame.image.load('SIBackground.png')

# Game Start Text
start_font = pygame.font.Font('Game Of Squids.ttf', 64)
allowed = True
start_game = False
start_screen = True


def start_game_text():
    start_text = start_font.render("START GAME BY:", True, (0, 255, 100))
    screen.blit(start_text, (100, 200))
    start_text = start_font.render("CLICKING ENTER", True, (100, 255, 255))
    screen.blit(start_text, (100, 300))


# Gave Over Text
over_font = pygame.font.Font('Game Of Squids.ttf', 64)


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (0, 255, 100))
    screen.blit(over_text, (200, 250))
    allowed = True


# Background Sound
mixer.music.load("background.mp3")
mixer.music.play(-1)
allow_laser = True

# creates the screen
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Score

score_value = 0
font = pygame.font.Font('Game Of Squids.ttf', 32)

textX = 10
textY = 10


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (0, 100, 255))
    screen.blit(score, (x, y))


# Player
playerImg = pygame.image.load('rocket.png')
playerX = 370
playerY = 480
playerX_change = 0


def player(x, y):
    screen.blit(playerImg, (x, y))


# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 370
bulletY = 470
bullet_call = False
bullet_allow = True
bullet_hit = True
bullet_hitter = False


def bullet(x, y):
    screen.blit(bulletImg, (x, y))


# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.5)
    enemyY_change.append(0)


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game loop
running = True
while running:
    # RGB
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.6
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.6
            if event.key == pygame.K_UP and bullet_allow == True:
                bullet_call = True
                bullet_allow = False
                bulletX = playerX

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_RETURN and allowed:
                print(start_game)
                start_game = True
                allowed = False

    if start_screen:
        start_game_text()

    if start_game:
        start_screen = False
        playerX += playerX_change

        if playerX <= 0:
            playerX = 736
        elif playerX >= 736:
            playerX = 0

        player(playerX, playerY)

        # Enemy controls
        for i in range(num_of_enemies):

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 0.5

                enemyY[i] = enemyY[i] + 40
            elif enemyX[i] >= 736:
                enemyX_change[i] = -0.5
                enemyY[i] = enemyY[i] + 40

            # Collision
            collison = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collison:
                collision_sound = mixer.Sound('explosion.wav')
                collision_sound.play()
                bulletY = 480
                bullet_hit = True
                bullet_hitter = True
                score_value += 1
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)

            if bullet_hit:
                enemy(enemyX[i], enemyY[i], i)

            # Game Over
            if enemyY[i] > 400:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                break

        if bullet_call == True:
            bullet_sound = mixer.Sound('laser.wav')
            if allow_laser:
                bullet_sound.play()
                allow_laser = False
            bullet(bulletX + 13, bulletY)
            bulletY = bulletY - 2
            if bulletY == 0 or bullet_hitter:
                bullet_allow = True
                bullet_call = False
                bullet_hitter = False
                allow_laser = True
                bulletY = 480

    show_score(textX, textY)
    pygame.display.update()