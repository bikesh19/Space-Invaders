import pygame
import random
from pygame import mixer

clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((800, 600))

#sounds
mixer.music.load('background.wav')
mixer.music.play(-1)
shootSound = mixer.Sound("shoot.wav")
explosionSound = mixer.Sound("explosion.wav")
gameOverSound = mixer.Sound("gameover.wav")


#title & logo
pygame.display.set_caption('Space Invaders')
icon= pygame.image.load('startup.png')
pygame.display.set_icon(icon)

#background
background =pygame.image.load('space.jpg')

#player
playerImg = pygame.image.load('rocket.png')
playerX = 375
playerY = 500

#enemy
enemyImg = pygame.image.load('space.png')
enemyX = random.randint(0,750)
enemyY =5

#bullet
bullets= []
bulletImg = pygame.image.load('bullets.png')
bulletX = 0
bulletY =500
bullet_state = "ready"

# Initialize the last bullet time and firing delay
last_bullet_time = 0
bullet_delay = 1000  # Delay in milliseconds (e.g., 300 ms)

# Speeds
# Speeds
player_speed = 200  # Pixels per second
enemy_speed_x = 100  # Pixels per second
enemy_speed_y = 10  # Pixels per second
bullet_speed = 10  # Pixels per second

def collision(bullet_surface, bullet_x, bullet_y, enemy_surface, enemy_x, enemy_y):
    # Create masks from surfaces
    bullet_mask = pygame.mask.from_surface(bullet_surface)
    enemy_mask = pygame.mask.from_surface(enemy_surface)

    # Calculate the offset between the two objects
    offset_x = enemy_x - bullet_x
    offset_y = enemy_y - bullet_y

    # Check for collision using masks
    collision_point = bullet_mask.overlap(enemy_mask, (offset_x, offset_y))
    if collision_point:
        explosionSound.play()
        return True
    else:
        return False


def fire_bullet(x, y):
    global last_bullet_time
    current_time = pygame.time.get_ticks()  # Get the current time in milliseconds
    if current_time - last_bullet_time > bullet_delay:
        shootSound.play()
        bullets.append({"x": x + 12, "y": y - 22, "state": "fire"})
        last_bullet_time = current_time  # Update the last bullet time

def player(x,y):
    screen.blit(playerImg,(x, y))

def enemy(x,y):
    screen.blit(enemyImg,(x, y))

# Draw and update bullets
def update_bullets():
    global score_value, enemyX, enemyY, enemy_speed_x, enemy_speed_y
    for bullet in bullets[:]:  # Iterate over a copy of the list to allow safe removal
        if bullet["state"] == "fire":
            # Move the bullet
            bullet["y"] -= bullet_speed
            # Draw the bullet
            screen.blit(bulletImg, (bullet["x"], bullet["y"]))

            # Check collision
            if collision(bulletImg, bullet["x"], bullet["y"], enemyImg, enemyX, enemyY):
                score_value += 1
                bullets.remove(bullet)  # Remove the bullet upon collision
                enemyX = random.randint(0, 750)
                enemyY = 5
                enemy_speed_x += 10  # Increase enemy speed on hit
                enemy_speed_y += 1.5
            # Remove bullet if it goes off-screen
            elif bullet["y"] <= 0:
                bullets.remove(bullet)

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 30)
textX=10
textY=10
def show_score(x,y):
    score = font.render("Score : " + str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))



active_keys = set()
latest_dir= None
notgameover=True
while notgameover :
    dt = clock.tick(60) / 1000  # Time in seconds since last frame (delta time)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            notgameover = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                active_keys.add("left")
                latest_dir = "left"
            elif event.key == pygame.K_RIGHT:
                active_keys.add("right")
                latest_dir = "right"
            elif event.key == pygame.K_SPACE:  # Fire bullets with delay
                fire_bullet(playerX, bulletY)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                active_keys.discard("left")
            elif event.key == pygame.K_RIGHT:
                active_keys.discard("right")

    # Movement logic
    if "left" in active_keys and "right" in active_keys:
        if latest_dir == "left":
            playerX -= player_speed * dt
        elif latest_dir == "right":
            playerX += player_speed * dt
    elif "left" in active_keys:
        playerX -= player_speed * dt
    elif "right" in active_keys:
        playerX += player_speed * dt

    # Keep player in bounds
    if playerX < 0:
        playerX = 750
    elif playerX > 750:
        playerX = 0

    # Update enemy position
    enemyY += enemy_speed_y * dt
    enemyX += enemy_speed_x * dt
    if enemyX >= 750 or enemyX <= 0:
        enemy_speed_x *= -1

    # Update bullets
    for bullet in bullets[:]:
        bullet["y"] -= bullet_speed * dt
        if collision(bulletImg, bullet["x"], bullet["y"], enemyImg, enemyX, enemyY):
            score_value += 1
            bullets.remove(bullet)
            enemyX = random.randint(0, 750)
            enemyY = 5
            enemy_speed_x += enemy_speed_x / 2

        elif bullet["y"] <= 0:
            bullets.remove(bullet)

    if enemyY >= 450:
        notgameover = False
    # Draw everything
    screen.fill((255, 165, 0))
    screen.blit(background, (0, 0))
    player(playerX, playerY)
    enemy(enemyX, enemyY)
    update_bullets()
    show_score(textX, textY)
    if not notgameover:
        text_over = font.render("GAME OVER ", True, (255, 255, 255))
        screen.blit(text_over, (340, 280))
        gameOverSound.play()
        pygame.display.update()
        pygame.time.delay(3000)  # Pause for 3 seconds
    pygame.display.update()