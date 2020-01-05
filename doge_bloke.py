"""bug: can't unfreeze more than once after stage 1"""
import sys
import random
import pygame
from pygame import *

pygame.init()


WIDTH = 1280
HEIGHT = 720
BOX_WIDTH = BOX_HEIGHT = 50
ENEMY_WIDTH = ENEMY_HEIGHT = 50
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
CYAN = (100, 255, 255)
WHITE = (255, 255, 255)
BACKGROUND_COLOR = BLACK
PLAYER_COLOR = RED
ENEMY_COLOR = BLUE
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), FULLSCREEN)
FONT = pygame.font.SysFont('monospace', 30, bold=True, italic=False)

cheat = []
game_over = False
player_pos = [WIDTH/2, HEIGHT - 2 * BOX_HEIGHT]
enemy_pos = [0, 0]
enemy_list = [enemy_pos]
clock = pygame.time.Clock()
speed = 10
score = 0
god = False
freeze = False

def set_level(score, speed):
    """
    Difficulty increases as the game progresses
    """
    if score < 10:
        speed = 5
    elif score < 20:
        speed = 6
    elif score < 40:
        speed = 7
    elif score < 60:
        speed = 9
    elif score%50 == 0:
        speed += 1
    return speed

def enemy_generator(enemy_list, direction):
    """
    Generates enemies in the sky till there are a total of 10.
    Using probability, we generate enemies
    """
    delay = random.random()
    if len(enemy_list) < 10 and delay < 0.10:
        if direction == 'down':
            new_x_pos = random.randint(0, WIDTH-ENEMY_WIDTH)
            new_y_pos = 0
        elif direction == 'up':
            new_x_pos = random.randint(0, WIDTH-ENEMY_WIDTH)
            new_y_pos = HEIGHT
        elif direction == 'right':
            new_x_pos = 0
            new_y_pos = random.randint(0, HEIGHT-ENEMY_HEIGHT)
        elif direction == 'left':
            new_x_pos = WIDTH
            new_y_pos = random.randint(0, HEIGHT-ENEMY_HEIGHT)
        
        enemy_list.append([new_x_pos, new_y_pos])

def enemy_draw(enemy_list, ENEMY_COLOR):
    """
    Draw enemies on the screen
    """
    for enemy_pos in enemy_list:
        pygame.draw.rect(SCREEN, ENEMY_COLOR, (enemy_pos[0], enemy_pos[1], ENEMY_WIDTH, ENEMY_HEIGHT))

def enemy_position_update(enemy_list, score, direction, speed):
    """
    Update enemy positions according to speed and directions of 'falling'.
    The enemy is popped if it goes out of the screen
    """

    
    for index, enemy_pos in enumerate(enemy_list):
        
        if direction == 'up' or direction == 'down':
            if enemy_pos[1] >= 0 and enemy_pos[1] <= HEIGHT:
                if direction == 'down':
                    enemy_pos[1] += speed
                elif direction == 'up':
                    enemy_pos[1] -= speed
            else:
                score += 1
                enemy_list.pop(index)
        
        else:
            if enemy_pos[0] >= 0 and enemy_pos[0] <= WIDTH:
                if direction == 'right':
                    enemy_pos[0] += speed
                elif direction == 'left':
                    enemy_pos[0] -= speed
            else:
                score += 1
                enemy_list.pop(index)
        
    return score

def check_collision(player_pos, enemy_list):
    """
    We check all the possible collisions that can occur
    """
    for enemy_pos in enemy_list:
        if detect_collision(player_pos, enemy_pos):
            return True
    return False

def detect_collision(player_pos, enemy_pos):
    """
    We detect if the blocks have collided or not
    """
    p_x = player_pos[0]
    p_y = player_pos[1]
    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if (e_x >= p_x and e_x < p_x + BOX_WIDTH) or (p_x >= e_x and p_x < e_x + ENEMY_WIDTH):
        if (e_y >= p_y and e_y < p_y+ BOX_HEIGHT) or (p_y >= e_y and p_y < e_y + ENEMY_HEIGHT):
            return True
    else:
        return False

# GAME LOOP
while not game_over:
    for event in pygame.event.get():

        # We close the window if 'x' is pressed
        if event.type == pygame.QUIT:
            sys.exit()

        # We now detect keyboard cheats
        if event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_g:
                god = not god
            if event.key == pygame.K_f:
                freeze = not freeze

            #elif event.key == pygame.K_x:
            #    if str(cheat.append(event.key)) == 'matrix':
            #        # ACTIVATE MATRIX FUNCTION
            #    else:
            #       cheat.append(event.key)
                
        # We now detect keyboard changes
        if event.type == pygame.KEYDOWN:
            x = player_pos[0]
            y = player_pos[1]
            if event.key == pygame.K_LEFT:
                x -= BOX_WIDTH/2
            elif event.key == pygame.K_RIGHT:
                x += BOX_WIDTH/2
            elif event.key == pygame.K_UP:
                y -= BOX_HEIGHT/2
            elif event.key == pygame.K_DOWN:
                y += BOX_HEIGHT/2
            player_pos = [x, y]
        
        # Detect if player goes out of the screen
        #print('x: ' + str(player_pos[0]))
        #print('y: ' + str(player_pos[1]))

        if player_pos[0] < 0:
            player_pos[0] = 0
        elif player_pos[1] < 0:
            player_pos[1] = 0
        elif player_pos[0] > WIDTH - BOX_WIDTH:
            player_pos[0] = WIDTH - BOX_WIDTH
        elif player_pos[1] > HEIGHT - BOX_HEIGHT:
            player_pos[1] = HEIGHT - BOX_HEIGHT

    # Determine direction
    compare = score % 200
    if compare <= 50:
        direction = 'down'
    elif compare <= 100:
        direction = 'up'
    elif compare <= 150:
        direction = 'right'
    elif compare < 200:
        direction = 'left'

    # Determine colors
    if direction == 'down' or direction == 'left':
        BACKGROUND_COLOR = BLACK
        PLAYER_COLOR = RED
        ENEMY_COLOR = BLUE
        TEXT_COLOR = YELLOW
    elif direction == 'up' or direction == 'right':
        BACKGROUND_COLOR = WHITE
        PLAYER_COLOR = RED
        ENEMY_COLOR = GREEN
        TEXT_COLOR = BLACK

    if god:
        BACKGROUND_COLOR = CYAN
        TEXT_COLOR = BLACK
    
    # Filling black in rest of the screen but the block
    SCREEN.fill(BACKGROUND_COLOR)

    # FREEZE CHEAT
    if freeze:
        speed = 0
    else:
        speed = set_level(score, speed)
    

    # Drawing and updating enemy blocks, collision detection, score display
    enemy_generator(enemy_list, direction)
    
    score = enemy_position_update(enemy_list, score, direction, speed)
    text = "Score: " + str(score)
    label = FONT.render(text, 1, TEXT_COLOR)


    SCREEN.blit(label, (WIDTH-200, HEIGHT-45))
    # CHEATS
    if god:
        SCREEN.blit(FONT.render("101010", 1, TEXT_COLOR), (0, 0))
    if freeze:
        SCREEN.blit(FONT.render("FREEZE", 1, TEXT_COLOR), (0, HEIGHT-45))
    
    if check_collision(player_pos, enemy_list):
            game_over = True
            PLAYER_COLOR = YELLOW
    enemy_draw(enemy_list, ENEMY_COLOR)

    # Drawing our player box

    pygame.draw.rect(SCREEN, PLAYER_COLOR, (player_pos[0], player_pos[1], BOX_WIDTH, BOX_HEIGHT))

    # 30 fps
    clock.tick(30)

    # Updating the screen
    pygame.display.update()


    # CHEAT CODE: 'g', if pressed twice, nullifies the effect
    if god:
        game_over = False

print()
print("Your Final Score is: " + str(score))
