import pygame
import random
import math
from pygame import mixer

# initialize pygame
pygame.init()

# create the screen
win = pygame.display.set_mode((800, 600))

# background image
bkgrnd = pygame.image.load('12.jpg')
# background music
mixer.music.load('bgsnippet.wav')
mixer.music.play(-1)

#Start
pygame.display.set_caption("Runtime Terrors")
icon = pygame.image.load('gameicon.png')
pygame.display.set_icon(icon)

# player
playerimg = pygame.image.load('computership.gif')
playerX = 370
playerY = 480
playerX_change = 0
playerY_chang = 0

# enemies - blackhat hacker (enemy) attributes are stored within array
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 7
for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load('blackhatenemy.gif'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 180))
    enemyX_change.append(1)
    enemyY_change.append(20)

# bullet info
# ready means you CANNOT see bullet on the window
# fire means you CAN see the bullet moving within the window
bulletimg1 = pygame.image.load('bullet1.gif')       #firewall image
bulletimg2 = pygame.image.load('bullet2.png')       #comodo antivirus
bulletX = 0
bulletY = playerY
bulletX_change = 0
bulletY_change = 3
bullet_state = 'ready'

# scoring
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game over
game_over_font = pygame.font.Font('freesansbold.ttf', 64)

#functions below define score/player/enemy onto window
def show_score(x, y):
    score = font.render('Score: ' + str(score_value), True, (139, 0, 0))
    win.blit(score, (x, y))

def game_over_text():
    over_text = font.render('GAME OVER', True, (139, 0, 0))
    win.blit(over_text, (300, 300))

def player(x, y):
    win.blit(playerimg, (x, y))

def enemy(x, y, i):
    win.blit(enemyimg[i], (x, y))

#toggle bullets between "1" and "0" when the user hits the spacebar
def toggle_bullet():
    if toggle_bullet.imgtoggle == 0:
        toggle_bullet.bulletimg = bulletimg1
        toggle_bullet.imgtoggle = 1
    else:
        toggle_bullet.bulletimg = bulletimg2
        toggle_bullet.imgtoggle = 0

#firing "1" and "0" when spacebar is pressed
def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    win.blit(toggle_bullet.bulletimg, (x + 16, y + 10))
     
#collision detection
def collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False

#Start of game (loop)
running = True
toggle_bullet.imgtoggle = 0
while running:
    #filling rgb
    win.fill((0, 0, 0))
    #rendering the background
    win.blit(bkgrnd, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #keystrokes - spacebar, right, left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_change = 2
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    toggle_bullet()               #calling to toggle images between 1 and 0
                    bullet_sound = mixer.Sound('bulletsound.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_LEFT:
                playerX_change = 0

    # checking to see user doesn't leave the frame/bounds of the game
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    #blackhat movement
    for i in range(num_of_enemies):
        # game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]

            # collision detection between enemy and bullet
        col = collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if col:
            col_sound = mixer.Sound('3xplosion.wav')
            col_sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 180)

        enemy(enemyX[i], enemyY[i], i)

    #tracking bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'
    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
