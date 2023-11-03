import cv2
import os
import pygame
from game_constants import *
from game_functions import *
from computer_vision.color_segmentation import update_segmentation_red, update_segmentation_green

def main():

    last_green_shot = 0  # Renomeado de last_yellow_shot para last_green_shot
    last_red_shot = 0
    green = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)  # Renomeado de yellow para green
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    green_bullets = []  # Renomeado de yellow_bullets para green_bullets

    red_health = 10
    green_health = 10  # Renomeado de yellow_health para green_health

    clock = pygame.time.Clock()
    run = True

    cap = cv2.VideoCapture()
    if not cap.isOpened():
        cap.open(0)

    while run:
        clock.tick(FPS)

        if not cap.isOpened():
            cap.open(0)
        ret, frame = cap.read()
        frame = frame[:, ::-1, :].copy()

        image_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        position_red = update_segmentation_red(image_hsv)
        position_green = update_segmentation_green(image_hsv)  # Renomeado de position_yellow para position_green

        height, width, _ = frame.shape

        cv2.line(frame, (200, 0), (200, height), (0, 255, 0), 2)  # Linha verde na posição x=200
        cv2.line(frame, (width - 200, 0), (width - 200, height), (0, 0, 255),
                 2)  # Linha vermelha na posição x=width-200

        cv2.imshow("Image", frame)

        green_line_x = 200
        red_line_x = width - 200
        current_time = pygame.time.get_ticks()

        # Ajuste na lógica de disparo
        # A nave verde dispara quando um objeto verde passa a linha verde do lado esquerdo para o lado direito
        if position_green and position_green[0] > green_line_x and current_time - last_green_shot > BULLET_DELAY:
            bullet = pygame.Rect(green.x + SPACESHIP_WIDTH, green.y + SPACESHIP_HEIGHT // 2 - 2, 10, 5)
            green_bullets.append(bullet)
            last_green_shot = current_time

        # A nave vermelha dispara quando um objeto vermelho passa a linha vermelha do lado direito para o lado esquerdo
        if position_red and position_red[0] < red_line_x and current_time - last_red_shot > BULLET_DELAY:
            bullet = pygame.Rect(red.x - 10, red.y + SPACESHIP_HEIGHT // 2 - 2, 10, 5)
            red_bullets.append(bullet)
            last_red_shot = current_time

        green_handle_movement(position_green, green)  # Renomeado de yellow_handle_movement para green_handle_movement
        red_handle_movement(position_red, red)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == RED_HIT:
                red_health -= 1

            if event.type == GREEN_HIT:  # Renomeado de YELLOW_HIT para GREEN_HIT
                green_health -= 1

        winner_text = ""
        if red_health <= 0:
            winner_text = "Green Wins!"  # Renomeado de Yellow Wins para Green Wins

        if green_health <= 0:  # Renomeado de yellow_health para green_health
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        handle_bullets(green_bullets, red_bullets, green, red)  # Renomeado de yellow_bullets para green_bullets

        draw_window(red, green, red_bullets, green_bullets, red_health, green_health)  # Renomeado de yellow para green

    cv2.destroyAllWindows()
    cap.release()
    main()

if __name__ == "__main__":
    main()
