import pygame
import random

pygame.init()

# Settings
WIDTH, HEIGHT = 400, 400
CELL = 20
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake - Simple Timed Food")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)

font = pygame.font.SysFont(None, 24)
score = 0
speed = 10

snake = [(5, 5)]
direction = (1, 0)

clock = pygame.time.Clock()
run = True


def generate_food():
    size = random.randint(1, 3)
    while True:
        x = random.randint(0, WIDTH // CELL - size)
        y = random.randint(0, HEIGHT // CELL - size)
        blocks = [(x + dx, y + dy) for dx in range(size) for dy in range(size)]
        if not any(part in snake for part in blocks):
            return {
                "blocks": blocks,
                "points": len(blocks),
                "timer": pygame.time.get_ticks()
            }

food = generate_food()


while run:
    clock.tick(speed)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and direction != (0, 1):
        direction = (0, -1)
    if keys[pygame.K_DOWN] and direction != (0, -1):
        direction = (0, 1)
    if keys[pygame.K_LEFT] and direction != (1, 0):
        direction = (-1, 0)
    if keys[pygame.K_RIGHT] and direction != (-1, 0):
        direction = (1, 0)

    
    head = snake[0]
    new_x = (head[0] + direction[0]) % (WIDTH // CELL)
    new_y = (head[1] + direction[1]) % (HEIGHT // CELL)
    new_head = (new_x, new_y)

    
    if new_head in snake:
        text = font.render("Game Over!", True, (255, 0, 0))
        win.blit(text, (WIDTH // 2 - 50, HEIGHT // 2))
        pygame.display.update()
        pygame.time.delay(2000)
        run = False
        break

    snake.insert(0, new_head)

   
    if pygame.time.get_ticks() - food["timer"] > 3000:
        food = generate_food()

 
    elif new_head in food["blocks"]:
        score += food["points"]
        if score % 3 == 0:
            speed += 1
        food = generate_food()
    else:
        snake.pop()

   
    win.fill(WHITE)

   
    for part in snake:
        pygame.draw.rect(win, GREEN, (part[0]*CELL, part[1]*CELL, CELL, CELL))

    
    for block in food["blocks"]:
        pygame.draw.rect(win, RED, (block[0]*CELL, block[1]*CELL, CELL, CELL))

    
    text = font.render("Score: " + str(score), True, BLACK)
    win.blit(text, (10, 10))

    pygame.display.update()

pygame.quit()