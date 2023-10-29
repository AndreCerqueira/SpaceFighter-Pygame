import pygame
import cv2
from game_constants import *

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):

    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

def yellow_handle_movement(position, yellow):
    if position:
        x_center, y_center, w, h = position

        # Mova a nave apenas verticalmente para a posição detectada
        yellow.y = y_center - SPACESHIP_HEIGHT // 2

        # Garanta que a nave não ultrapasse as bordas superior e inferior da tela
        if yellow.y < 0:
            yellow.y = 0
        if yellow.y + SPACESHIP_HEIGHT > HEIGHT:
            yellow.y = HEIGHT - SPACESHIP_HEIGHT

def red_handle_movement(position, red):
    if position:
        x_center, y_center, w, h = position

        # Mova a nave apenas verticalmente para a posição detectada
        red.y = y_center - SPACESHIP_HEIGHT // 2

        # Garanta que a nave não ultrapasse as bordas superior e inferior da tela
        if red.y < 0:
            red.y = 0
        if red.y + SPACESHIP_HEIGHT > HEIGHT:
            red.y = HEIGHT - SPACESHIP_HEIGHT

def handle_bullets(yellow_bullets, red_bullets, yellow, red):

    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()/2,
        HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)
