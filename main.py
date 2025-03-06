import pygame, random, math
from pygame import mixer


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
for i in range(num_enemies):
    enemy_sprite.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(300, 545))
    enemyY.append(random.randint(0, 440))
    enemy_speed.append(1)  # Set monster speed to 1

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
restart_font = pygame.font.Font('freesansbold.ttf', 30)
score_font = pygame.font.Font('freesansbold.ttf', 30)

def player(x, y):
    window.blit(sprite, (x, y))

def enemy(x, y, i):
    window.blit(enemy_sprite[i], (x, y))

def shoot(x, y):
    global bullet_state
    bullet_state = "shoot"
    window.blit(bullet_sprite, (x + 35, y - 5))

def collision(enemyX, enemyY, bulletX, bulletY):
    dist = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow((enemyY + 20) - bulletY, 2)))
    return dist < 28

def reveal_score(x, y):
    label = font.render("Score: " + str(score), True, (244, 226, 198))
    window.blit(label, (x, y))

def reveal_game_over():
    label2 = game_over_font.render("GAME OVER", True, (255, 0, 0))
    score_label = score_font.render("Score: " + str(score), True, (255, 255, 0))  
    restart_label = restart_font.render("Press R to Restart", True, (255, 255, 255))
    window.fill(pygame.Color("black"))
    window.blit(label2, (160, 200))
    window.blit(score_label, (180, 270))
    window.blit(restart_label, (180, 330))
    pygame.mixer.music.stop()
    pygame.mixer.pause()

def reset_game():
    global playerX, playerY, bulletX, bullet_state, enemyX, enemyY, score, running
    playerX, playerY = 50, 100
    bulletX, bullet_state = 50, "loaded"
    score = 0
    for i in range(num_enemies):
        enemyX[i] = random.randint(300, 545)
        enemyY[i] = random.randint(0, 440)
    mixer.music.play(-1)

running = True
game_over = False

while running:
    window.fill((46, 139, 87))
    window.blit(background, (0, 0))
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  
        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            game_over = False
            reset_game()
    
    if game_over:
        # Display game over screen
        reveal_game_over()
    else:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and playerY > 0:
            playerY -= speed
        if keys[pygame.K_DOWN] and playerY < 440:
            playerY += speed
        if keys[pygame.K_SPACE] and bullet_state == "loaded":
            shot = mixer.Sound("shot.wav")
            shot.play()
            bulletY = playerY
            shoot(bulletX, bulletY)

        for i in range(num_enemies):
            if enemyX[i] <= 0:
                game_over = True
                reveal_game_over()
                break
            enemyX[i] -= enemy_speed[i]
            if collision(enemyX[i], enemyY[i], bulletX, bulletY) and bullet_state == "shoot":
                dead = mixer.Sound("zombie3.wav")
                dead.play()
                bulletX, bullet_state = 50, "loaded"
                score += 1
                enemyX[i] = random.randint(300, 545)
                enemyY[i] = random.randint(0, 440)
            enemy(enemyX[i], enemyY[i], i)

        if bulletX >= 500:
            bulletX, bullet_state = 50, "loaded"
        if bullet_state == "shoot":
            shoot(bulletX, bulletY)
            bulletX += bullet_speed
        player(playerX, playerY)
        reveal_score(textX, textY)
    
    pygame.display.update()

pygame.quit()
