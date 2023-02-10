import pygame, random, math
from pygame import mixer

#initialize all imported pygame modules
pygame.init()

# Creates game window and background 
window = pygame.display.set_mode((600, 500))
background = pygame.image.load("background.png")

# Background music 
mixer.music.load('theme.wav')
mixer.music.play(-1)

# Title and icon for game 
pygame.display.set_caption("Apocalypse")
icon = pygame.image.load('zombie.png')
pygame.display.set_icon(icon)

# Player sprite
sprite = pygame.image.load('character.png')
playerX = 50
playerY = 100
speed = 3

# Zombie/enemy sprite 
enemy_sprite = []
enemyX = []
enemyY = []
enemy_speed = []
num_enemies = 3

# Loading multiple enemies into game 
for i in range(num_enemies) :
    enemy_sprite.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(300, 545))
    enemyY.append(random.randint(0, 440))
    enemy_speed.append(1.5)

# Bullet sprite
bullet_sprite = pygame.image.load('bullet.png')
bulletX = 50
bulletY = 0
bullet_speed = 7.5
bullet_state = "loaded"

# Tracking score 
score = 0
font = pygame.font.Font('freesansbold.ttf', 25)
textX = 10
textY = 10

game_over_font = pygame.font.Font('freesansbold.ttf', 50)

# 'Drawing' player 
def player(x, y) :
    window.blit(sprite, (x, y))

# 'Drawing' enemies 
def enemy(x, y, i) :
    window.blit(enemy_sprite[i], (x, y))

# 'Drawing' bullets 
def shoot(x, y) :
    global bullet_state 
    bullet_state = "shoot"
    window.blit(bullet_sprite, (x + 35, y-5))

# Determines whether bullet has hit enemy
def collision(enemyX, enemyY, bulletX, bulletY) :
    dist = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow((enemyY + 20) - bulletY, 2)))
    if dist < 28 :
        return True
    else :
        return False

# Reveals score 
def reveal_score(x, y) :
    label = font.render("Score : " + str(score), True, (244, 226, 198))
    window.blit(label, (x, y))

# Game over 
def reveal_game_over() :
    label2 = game_over_font.render("GAME OVER ", True, (255, 0, 0))
    window.fill(pygame.Color("black"))
    window.blit(label2, (160, 200))
    pygame.mixer.music.stop()
    pygame.mixer.pause()

running = True

# main loop
while running :

    window.fill((46, 139, 87))
    
    window.blit(background, (0, 0))

    pygame.time.delay(10)

    # Quitting game 
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            running = False    

    keys = pygame.key.get_pressed()

    # player movement 
    if keys[pygame.K_UP] and playerY > 0 :
        playerY -= speed
    if keys[pygame.K_DOWN] and playerY < 440 :
        playerY += speed
    
    # Shooting 
    if keys[pygame.K_SPACE] :
        if bullet_state is "loaded" :
            shot = mixer.Sound("shot.wav")
            shot.play()
            bulletY = playerY
            shoot(bulletX, bulletY )

    for i in range(num_enemies) :

        # If enemy has reached 'end zone', player loses 
        if enemyX[i] <= 0 :
            for j in range(num_enemies) :
                enemyX[j] = -100
            playerX = - 100
            bulletX = -100
            bullet_state == "done"
            reveal_game_over()
            break

        enemyX[i] -= enemy_speed[i]
        
        # When enemy is shot/killed by bullet 
        killed = collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if killed and bullet_state == "shoot":
            dead = mixer.Sound("zombie3.wav")
            dead.play()
            bulletX = 50
            bullet_state = "loaded"
            # increases score 
            score += 1
            # draws enemy in a new random position 
            enemyX[i] = random.randint(300, 545)
            enemyY[i] = random.randint(0, 440)
        
        enemy(enemyX[i], enemyY[i], i)

    # When bullet goes out of screen
    if bulletX >= 500 :
        bulletX = 50
        bullet_state = "loaded"

    if bullet_state is "shoot" :
        shoot(bulletX, bulletY)
        bulletX += bullet_speed

    player(playerX, playerY)
    reveal_score(textX, textY)

    pygame.display.update()

pygame.quit()    