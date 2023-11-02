import cv2
import os
import pygame
from game_constants import *
from game_functions import *
from computer_vision.color_segmentation import update_segmentation_red, update_segmentation_green


def main():

    last_yellow_shot = 0
    last_red_shot = 0
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 100
    yellow_health = 100

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
        position_yellow = update_segmentation_green(image_hsv)

        height, width, _ = frame.shape
        cv2.line(frame, (200, 0), (200, height), (0, 0, 255), 2)  # linha na posição x=200
        cv2.line(frame, (width - 200, 0), (width - 200, height), (0, 255, 0), 2)  # linha na posição x=width-200

        cv2.imshow("Image", frame)

        red_line_x = 200
        green_line_x = width - 200
        current_time = pygame.time.get_ticks()

        if position_red and position_red[0] < red_line_x and current_time - last_yellow_shot > BULLET_DELAY:
            bullet = pygame.Rect(yellow.x + SPACESHIP_WIDTH, yellow.y + SPACESHIP_HEIGHT//2 - 2, 10, 5)
            yellow_bullets.append(bullet)
            last_yellow_shot = current_time

        if position_yellow and position_yellow[0] > green_line_x and current_time - last_red_shot > BULLET_DELAY:
            bullet = pygame.Rect(red.x + SPACESHIP_WIDTH, red.y + SPACESHIP_HEIGHT//2 - 2, 10, 5)
            red_bullets.append(bullet)
            last_red_shot = current_time

        yellow_handle_movement(position_yellow, yellow)
        red_handle_movement(position_red, red)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == RED_HIT:
                red_health -= 1
                #BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                #BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    cv2.destroyAllWindows()
    cap.release()
    main()


if __name__ == "__main__":
    main()