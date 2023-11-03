import pygame
import cv2
from game_constants import *

def draw_window(red, green, red_bullets, green_bullets, red_health, green_health):

    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    green_health_text = HEALTH_FONT.render("Health: " + str(green_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(green_health_text, (10, 10))

    WIN.blit(GREEN_SPACESHIP, (green.x, green.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in green_bullets:
        pygame.draw.rect(WIN, GREEN, bullet)

    pygame.display.update()

def green_handle_movement(position, green):
    if position:
        x_center, y_center, w, h = position

        # Mova a nave apenas verticalmente para a posição detectada
        green.y = y_center - SPACESHIP_HEIGHT // 2

        # Garanta que a nave não ultrapasse as bordas superior e inferior da tela
        if green.y < 0:
            green.y = 0
        if green.y + SPACESHIP_HEIGHT > HEIGHT:
            green.y = HEIGHT - SPACESHIP_HEIGHT

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

def handle_bullets(green_bullets, red_bullets, green, red):

    for bullet in green_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            green_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            green_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if green.colliderect(bullet):
            pygame.event.post(pygame.event.Event(GREEN_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()/2,
        HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)

