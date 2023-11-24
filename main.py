import cv2
import pygame
from ultralytics import YOLO
from game_constants import *
from game_functions import *
# from computer_vision.color_segmentation import update_segmentation_red, update_segmentation_green
from computer_vision.object_detection import update_detection_yolo

def main():
    last_green_shot = 0
    last_red_shot = 0
    green = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    model = YOLO("yolov8n.pt")

    red_bullets = []
    green_bullets = []

    red_health = 10
    green_health = 10


    clock = pygame.time.Clock()
    run = True

    # Initialize video capture
    cap = cv2.VideoCapture()
    if not cap.isOpened():
        cap.open(0)

    while run:
        clock.tick(FPS)
        if not cap.isOpened():
            cap.open(0)
        ret, frame = cap.read()
        frame = frame[:, ::-1, :].copy()
        yolo_objects = update_detection_yolo(frame, model)

        # Convert frame to HSV color space for color segmentation
        # image_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # position_red = update_segmentation_red(image_hsv)
        # position_green = update_segmentation_green(image_hsv)

        height, width, _ = frame.shape

        # Draw boundary lines for shooting activation
        cv2.line(frame, (200, 0), (200, height), (0, 255, 0), 2)
        cv2.line(frame, (width - 200, 0), (width - 200, height), (0, 0, 255), 2)

        green_line_x = 200
        red_line_x = width - 200
        current_time = pygame.time.get_ticks()

        # Shooting logic for green and red spaceships
        '''
        if position_green and position_green[0] > green_line_x and current_time - last_green_shot > BULLET_DELAY:
            bullet = pygame.Rect(green.x + SPACESHIP_WIDTH, green.y + SPACESHIP_HEIGHT // 2 - 2, 10, 5)
            green_bullets.append(bullet)
            last_green_shot = current_time

        if position_red and position_red[0] < red_line_x and current_time - last_red_shot > BULLET_DELAY:
            bullet = pygame.Rect(red.x - 10, red.y + SPACESHIP_HEIGHT // 2 - 2, 10, 5)
            red_bullets.append(bullet)
            last_red_shot = current_time
        '''

        # Handle spaceship movement
        # green_handle_movement(position_green, green)
        # red_handle_movement(position_red, red)

        for object in yolo_objects:
            box = object.boxes.data[0]
            pt1 = (int(box[0]), int(box[1]))
            pt2 = (int(box[2]), int(box[3]))
            confidence = box[4]
            class_id = int(box[5])

            # Calcular o centro da caixa delimitadora
            x_center = (pt1[0] + pt2[0]) // 2
            y_center = (pt1[1] + pt2[1]) // 2
            position = (x_center, y_center)

            if class_id == 67:  # ID da classe para a nave vermelha
                cv2.rectangle(img=frame, pt1=pt1, pt2=pt2, color=(0, 0, 255), thickness=2)
                green_handle_movement(position, red)

                # Lógica de disparo para a nave vermelha
                if x_center < red_line_x and current_time - last_red_shot > BULLET_DELAY:
                    bullet = pygame.Rect(red.x - 10, red.y + SPACESHIP_HEIGHT // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    last_red_shot = current_time

            elif class_id == 47:  # ID da classe para a nave verde
                cv2.rectangle(img=frame, pt1=pt1, pt2=pt2, color=(0, 255, 0), thickness=2)
                red_handle_movement(position, green)

                # Lógica de disparo para a nave verde
                if x_center > green_line_x and current_time - last_green_shot > BULLET_DELAY:
                    bullet = pygame.Rect(green.x + SPACESHIP_WIDTH, green.y + SPACESHIP_HEIGHT // 2 - 2, 10, 5)
                    green_bullets.append(bullet)
                    last_green_shot = current_time

        # Event handling for quitting and hits
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == RED_HIT:
                red_health -= 1
            if event.type == GREEN_HIT:
                green_health -= 1

        # Check for a winner
        winner_text = ""
        if red_health <= 0:
            winner_text = "Green Wins!"
        if green_health <= 0:
            winner_text = "Red Wins!"
        if winner_text != "":
            draw_winner(winner_text)
            break

        # Display the processed frame
        cv2.imshow("Image", frame)

        # Handle bullet movement and collisions
        handle_bullets(green_bullets, red_bullets, green, red)

        # Draw game window and update display
        draw_window(red, green, red_bullets, green_bullets, red_health, green_health)

    # Cleanup on exit
    cv2.destroyAllWindows()
    cap.release()

if __name__ == "__main__":
    main()
