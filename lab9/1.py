import pygame
import random

pygame.init()

WIDTH, HEIGHT = 840, 650
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

background = pygame.image.load("road.png").convert()
car_img = pygame.image.load("car.png").convert_alpha()
coin_img = pygame.image.load("coin.png").convert_alpha()
enemy_img = pygame.image.load("enemy1.png").convert_alpha()

car_img = pygame.transform.scale(car_img, (50, 80))
enemy_img = pygame.transform.scale(enemy_img, (50, 80))

player_x = 175
player_y = 500
player_speed = 5

coins = []
coin_timer = 0
coin_delay = 30
coin_speed = 3

enemies = []
enemy_timer = 0
enemy_delay = 70  
enemy_speed = 4

coins_collected = 0
font = pygame.font.SysFont(None, 36)


N = 3  
coins_since_last_speedup = 0

clock = pygame.time.Clock()
run = True
game_over = False

while run:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - 50:
            player_x += player_speed

        # Coin logic
        coin_timer += 1
        if coin_timer >= coin_delay:
            size = random.randint(20, 50)
            x = random.randint(150, WIDTH - 150 - size)
            coins.append({"rect": pygame.Rect(x, 0, size, size), "size": size})
            coin_timer = 0

        # Enemy logic
        enemy_timer += 1
        if enemy_timer >= enemy_delay:
            x = random.randint(150, WIDTH - 150 - 50)
            enemies.append(pygame.Rect(x, 0, 50, 80))
            enemy_timer = 0

        player_rect = pygame.Rect(player_x, player_y, 50, 80)

        for coin in coins[:]:
            coin["rect"].y += coin_speed
            if coin["rect"].y > HEIGHT:
                coins.remove(coin)
            elif coin["rect"].colliderect(player_rect):
                coins.remove(coin)
                coins_collected += 1
                coins_since_last_speedup += 1

               
                if coins_since_last_speedup >= N:
                    enemy_speed += 1
                    coins_since_last_speedup = 0

        for enemy in enemies[:]:
            enemy.y += enemy_speed
            if enemy.y > HEIGHT:
                enemies.remove(enemy)
            elif enemy.colliderect(player_rect):
                game_over = True

    win.blit(background, (0, 0))
    win.blit(car_img, (player_x, player_y))

    for coin in coins:
        scaled_coin = pygame.transform.scale(coin_img, (coin["size"], coin["size"]))
        win.blit(scaled_coin, (coin["rect"].x, coin["rect"].y))

    for enemy in enemies:
        win.blit(enemy_img, (enemy.x, enemy.y))

    score_text = font.render("Coins: " + str(coins_collected), True, (0, 0, 0))
    win.blit(score_text, (WIDTH - 150, 10))

    if game_over:
        over_text = font.render("Game Over!", True, (255, 0, 0))
        win.blit(over_text, (WIDTH // 2 - 80, HEIGHT // 2))

    pygame.display.update()

pygame.quit()