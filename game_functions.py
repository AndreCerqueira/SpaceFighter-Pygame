import pygame
import cv2
from game_constants import *

def draw_window(red, green, red_bullets, green_bullets, red_health, green_health):
    # Draw the game window and health indicators
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    # Display health for both spaceships
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    green_health_text = HEALTH_FONT.render("Health: " + str(green_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(green_health_text, (10, 10))

    # Draw spaceships
    WIN.blit(GREEN_SPACESHIP, (green.x, green.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    # Draw bullets
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in green_bullets:
        pygame.draw.rect(WIN, GREEN, bullet)

    # Update the display
    pygame.display.update()

def green_handle_movement(position, green):
    # Handle the green spaceship's vertical movement
    if position:
        x_center, y_center = position
        green.y = y_center - SPACESHIP_HEIGHT // 2
        green.y = max(0, min(green.y, HEIGHT - SPACESHIP_HEIGHT))

def red_handle_movement(position, red):
    # Handle the red spaceship's vertical movement
    if position:
        x_center, y_center = position
        red.y = y_center - SPACESHIP_HEIGHT // 2
        red.y = max(0, min(red.y, HEIGHT - SPACESHIP_HEIGHT))

def handle_bullets(green_bullets, red_bullets, green, red):
    # Move bullets and check for hits or out-of-bounds
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
    # Display the winner text
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)
