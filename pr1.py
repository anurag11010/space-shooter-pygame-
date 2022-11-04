import pygame
import random
import math
from pygame import mixer

global diff
diff = 0.3

# Initialise Pygame
pygame.init()

# Create Screen
screen = pygame.display.set_mode((800, 600))

# Background
bg = pygame.image.load('bg1.jpg')

# bg music
mixer.music.load('bg.wav')
mixer.music.play(-1)

#Title and Icon
pygame.display.set_caption("SPACE WARS")
icon = pygame.image.load('ufo2.png')
pygame.display.set_icon(icon)

# Player
Player = pygame.image.load('player.png')
Px = 370
Py = 480
Px_change = 0

# Enemy
Enemy = []
Ex = []
Ey = []
Ex_change = []
Ey_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    Enemy.append(pygame.image.load('enemy1.png'))
    Ex.append(random.randint(5, 730))
    Ey.append(random.randint(50, 150))
    Ex_change.append(diff)
    Ey_change.append(45)

# Bullet
# ready - can't see
# fire - visible
bullet = pygame.image.load('bullet.png')
Bx = 0
By = 480
Bx_change = 0
By_change = 2
B_state = "ready"

# score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game over
Over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    s = font.render("SCORE : " + str(score), True, (255, 255, 255))
    screen.blit(s, (x, y))

def player(x, y):
    screen.blit(Player, (x, y))

def enemy(x, y, i):
    screen.blit(Enemy[i], (x, y))

def game_over():
    over_text = Over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def fire(x, y):
    global B_state
    B_state = "fire"
    screen.blit(bullet, (x, y))

def add_enemies(i):
    for x in range(i):
        Enemy.append(pygame.image.load('enemy1.png'))
        Ex.append(random.randint(5, 730))
        Ey.append(random.randint(50, 150))
        Ex_change.append(diff)
        Ey_change.append(45)

def diff_inc():
    for i in range(num_of_enemies):
        Ex_change[i]=diff
        Ex[i]=(random.randint(5, 730))
        Ey[i]=(random.randint(50, 150))


def level_changed():
    x = Px
    y = Py
    flag = True
    while flag:
        screen.fill((255, 109, 0))
        screen.blit(bg, (0, 0))
        check = False

        if x > 370:
            x -= 0.6
        if x < 370:
            x += 0.6
        if x < 371 and x > 369:
            x = 370

        if x == 370:
            y -= 0.8
            check = True

        if y - 481 > 0 and y - 481 < 1:
            y = 480

        if y - 5 < 1:
            y = 600

        if y == 480 and check:
            flag = False


        player(x, y)
        show_score(textX, textY)
        pygame.display.update()


def isCollision(ex, ey, bx, by):
    dis = math.sqrt(math.pow(ex-bx, 2)+math.pow(ey-by, 2))
    if dis < 27:
        return True
    else:
        return False

# Px1 = 370+64
# def player2():
#     screen.blit(Player,(Px1,Py))


# Game LOOP
running = True
while running:

    # Red Green Blue
    screen.fill((255, 109, 0))
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # print("Left Key")
                Px_change -= 0.4
            if event.key == pygame.K_RIGHT:
                # print("Right Key")
                Px_change += 0.4
            if event.key == pygame.K_SPACE and B_state == "ready":
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
                Bx = Px
                fire(Bx, By)

        if event.type == pygame.KEYUP:
            Px_change = 0

    Px += Px_change
    if Px < 6:
        Px = 6
    elif Px > 730:
        Px = 730

    for i in range(num_of_enemies):

        # Game Over
        if Ey[i] > 440:
            for j in range(num_of_enemies):
                Ey[j] = 2000
            over_sound = mixer.Sound('gameover.wav')
            over_sound.play()
            game_over()
            break

        Ex[i] += Ex_change[i]
        if Ex[i] < 6:
            Ex_change[i] = diff
            Ey[i] += Ey_change[i]
        elif Ex[i] > 730:
            Ex_change[i] = -diff
            Ey[i] += Ey_change[i]

        # collison
        col = isCollision(Ex[i], Ey[i], Bx, By)
        if col:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            By = 480
            B_state = "ready"
            score += 1
            Ex[i] = random.randint(5, 730)
            Ey[i] = random.randint(50, 150)

            # level 2
            if score == 5:
                level_changed()
                bg = pygame.image.load('bg2.jpg')
                num_of_enemies+=2
                diff += 0.1
                add_enemies(2)
                diff_inc()
                mixer.music.load('bg1.wav')
                mixer.music.play(-1)


            # level 3
            if score == 10:
                level_changed()
                bg = pygame.image.load('bg3.jpg')
                num_of_enemies+=2
                diff += 0.1
                mixer.music.load('bg2.wav')
                add_enemies(2)
                diff_inc()
                By_change+=0.5
                mixer.music.play(-1)

            # level 4
            if score == 15:
                level_changed()
                bg = pygame.image.load('bg4.jpg')
                num_of_enemies+=2
                diff += 0.1
                add_enemies(2)
                diff_inc()
                mixer.music.play(-1)

            # level 5
            if score == 20:
                level_changed()
                bg = pygame.image.load('bg5.jpg')
                num_of_enemies+=2
                diff += 0.2
                add_enemies(2)
                diff_inc()
                mixer.music.play(-1)

        enemy(Ex[i], Ey[i], i)

    # bullet movement
    if B_state == "fire":
        fire(Bx, By)
        By -= By_change

    if By <= 0:
        B_state = "ready"
        By = 480

    player(Px, Py)
    show_score(textX, textY)
    pygame.display.update()

print("Your Score is :",score)