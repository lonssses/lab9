import pygame
import math

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("paint with shapes")
clock = pygame.time.Clock()

drawing = False
last_pos = None
radius = 5
color = 'black'
tool = 'pen'
start_pos = None
mode = 'circle'  

screen.fill(pygame.Color('white'))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Клавиши
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                screen.fill(pygame.Color('white'))
            if event.key == pygame.K_e:
                tool = 'eraser'
            if event.key == pygame.K_p:
                tool = 'pen'
            if event.key == pygame.K_f:
                tool = 'figure'
            if event.key == pygame.K_1:
                color = 'black'
            if event.key == pygame.K_2:
                color = 'red'
            if event.key == pygame.K_3:
                color = 'blue'
            if event.key == pygame.K_c:
                mode = 'circle'
            if event.key == pygame.K_a:
                mode = 'square'
            if event.key == pygame.K_t:
                mode = 'triangle_eq'
            if event.key == pygame.K_r:
                mode = 'triangle_rt'
            if event.key == pygame.K_h:
                mode = 'rhombus'

        # Нажатие мыши
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos
            last_pos = event.pos

        # Отпускание кнопки мыши
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            if tool != 'figure':
                continue

            x1, y1 = start_pos
            x2, y2 = end_pos

            if mode == 'circle':
                center = ((x1 + x2) // 2, (y1 + y2) // 2)
                radius_shape = int(min(abs(x2 - x1), abs(y2 - y1)) // 2)
                pygame.draw.circle(screen, pygame.Color(color), center, radius_shape)

            elif mode == 'square':
                side = min(abs(x2 - x1), abs(y2 - y1))
                top_left_x = x1 if x1 < x2 else x1 - side
                top_left_y = y1 if y1 < y2 else y1 - side
                pygame.draw.rect(screen, pygame.Color(color), (top_left_x, top_left_y, side, side))

            elif mode == 'triangle_eq':
                base = abs(x2 - x1)
                height = base * math.sqrt(3) / 2
                top = ((x1 + x2) // 2, y1)
                left = (x1, y1 + int(height))
                right = (x2, y1 + int(height))
                pygame.draw.polygon(screen, pygame.Color(color), [top, left, right])

            elif mode == 'triangle_rt':
                pygame.draw.polygon(screen, pygame.Color(color), [(x1, y1), (x1, y2), (x2, y2)])

            elif mode == 'rhombus':
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2
                dx = abs(x2 - x1) // 2
                dy = abs(y2 - y1) // 2
                points = [
                    (center_x, center_y - dy),  
                    (center_x + dx, center_y),  
                    (center_x, center_y + dy),  
                    (center_x - dx, center_y)   
                ]
                pygame.draw.polygon(screen, pygame.Color(color), points)

        # Рисование pen/eraser
        if event.type == pygame.MOUSEMOTION and drawing:
            if tool == 'pen':
                pygame.draw.line(screen, pygame.Color(color), last_pos, event.pos, radius)
                last_pos = event.pos
            elif tool == 'eraser':
                pygame.draw.circle(screen, pygame.Color('white'), event.pos, radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()