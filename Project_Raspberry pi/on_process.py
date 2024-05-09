import pygame
import sys
from pygame.locals import *
import random
import time
import os
import bluetooth

# Initialize Pygame
pygame.init()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BORDER_MARGIN = 20

# Get screen dimensions
screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h

word_list = ["ม่วง", "ขาว", "แดง", "น้ำเงิน","เขียว"]
word_display = []

color_list = [(153,0,153),(255,255,255),(255,0,0),(0,0,255),(0, 255, 0)]
color_display = []

word_code = []
color_code = []

for i in range(0,15,1):
    word_display.append(random.choice(word_list))
    while True:
        color = random.randint(0, len(word_list)-1)
        if word_list[color] != word_display[i]:
            color_display.append(color_list[color])
            break

for i in range(0,len(word_display),1):
    for j in range(len(word_list)):
        if word_display[i] == word_list[j]:
            word_code.append(j)
            break

for i in range(0,len(color_display),1):
    for j in range(len(color_list)):
        if color_display[i] == color_list[j]:
            color_code.append(j)
            break

combined_data = [(word_code[x], color_code[x]) for x in range(len(word_code))]


# Constants
screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h
WHITE = (255, 255, 255)
BLACK = (0,0,0)
ARCADE_RED = (200, 0, 0)
FONT_SIZE = min(SCREEN_WIDTH, SCREEN_HEIGHT) // 10

font = pygame.font.Font("/home/strooptest/Desktop/Test_Bluetooth/BoonTook-Regular.ttf", FONT_SIZE)

# Placeholder functions for each option
def draw_menu(screen, title_text, title_rect, option_texts, option_rects, choice, device_connection_text, device_connection_rect):
    # Function to draw the menu on the screen
    screen.fill((0, 0, 0))
    screen.blit(title_text, title_rect)

    for i, (text, rect) in enumerate(zip(option_texts, option_rects)):
        if choice == i:  # Check if this option matches the current choice
            pygame.draw.rect(screen, (0, 255, 0), rect, 2)  # Draw green rectangle for the current choice
        else:
            pygame.draw.rect(screen, (255, 255, 255), rect, 2)  # Draw white rectangle for other options

        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

    # Draw the red rectangle for device connection text
    pygame.draw.rect(screen, (255, 0, 0), device_connection_rect)  # Red rectangle
    screen.blit(device_connection_text, device_connection_text_rect)  # Text

    pygame.display.flip()

def play_game():
    print("Executing playgame function")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    back_text = font.render("Back", True, (255, 255, 255))
    submit_text = font.render("Submit", True, (255, 255, 255))

    button_width = max(back_text.get_width(), submit_text.get_width()) + 40
    button_height = int(SCREEN_HEIGHT * 0.1)
    button_spacing = int(SCREEN_WIDTH * 0.05)

    back_rect = pygame.Rect(button_spacing, SCREEN_HEIGHT - button_height - button_spacing, button_width, button_height)
    submit_rect = pygame.Rect(SCREEN_WIDTH - button_spacing - button_width, SCREEN_HEIGHT - button_height - button_spacing, button_width, button_height)

    play_running = True
    while play_running:
        screen.fill(WHITE)

        pygame.draw.rect(screen, (255, 0, 0), back_rect)  # Red rectangle for "back" button
        screen.blit(back_text, (back_rect.centerx - back_text.get_width() // 2, back_rect.centery - back_text.get_height() // 2))  # Center the text

        pygame.draw.rect(screen, (0, 255, 0), submit_rect)  # Green rectangle for "next" button
        screen.blit(submit_text, (submit_rect.centerx - submit_text.get_width() // 2, submit_rect.centery - submit_text.get_height() // 2))  # Center the text

        pygame.display.flip()

        print("wait for command")
        command = arduino_sock.recv(1024).decode("utf-8")
        command = command.strip()  # Remove leading/trailing whitespace
        if command == '0':
            # Go to the next page
            play_running = False
            break
        elif command == '1':
            # Move to the next image
            print("pass")
            game_start()
            play_running = False  # Exit the inner loop to update the tutorial page


def game_start():
    start_time = time.time()
    print("Game_start")
    score = 0
    current_index_to_change = 0
    word_color_flags = [False] * 15
    font = pygame.font.Font("/home/strooptest/Desktop/Test_Bluetooth/BoonTook-Regular.ttf", FONT_SIZE)
    screen.fill(BLACK)
    pygame.display.flip()

    run = True
    while run:
        # วาด word list และกำหนดขนาดกรอบ
        for i in range(15):
            word = word_display[i]
            row = i // 5
            col = i % 5
            text_color = BLACK if word_color_flags[i] else color_display[i]
            text_surface = font.render(word, True, text_color)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 5 * col + SCREEN_WIDTH // 10, SCREEN_HEIGHT // 3 * row + SCREEN_HEIGHT // 6))
            screen.blit(text_surface, text_rect)

            # สร้างกรอบสีดำสำหรับ word list ที่ถูกส่งแล้ว
            if word_color_flags[i]:
                pygame.draw.rect(screen, BLACK, text_rect.inflate(BORDER_MARGIN, BORDER_MARGIN), 0)

            border_color = WHITE if current_index_to_change == i else BLACK  # เลือกสีของกรอบตามเงื่อนไข
            pygame.draw.rect(screen, border_color, text_rect.inflate(BORDER_MARGIN, BORDER_MARGIN), 2)

        pygame.display.flip()

        if current_index_to_change == 15:
            run = False
            break

        shuffled_data = list(combined_data[current_index_to_change])
        random.shuffle(shuffled_data)
            
        # Convert the shuffled tuple to a string representation
        data_str = str(shuffled_data)
        arduino_sock.send(data_str)  # Send the string
        print("Send choice")
        # Wait for the Arduino's acknowledgment
        Answer = arduino_sock.recv(1024).decode("utf-8")

        Answer = int(Answer)
        if Answer == combined_data[current_index_to_change][1]:
            score += 1
            word_color_flags[current_index_to_change] = True
        else:
            screen.fill(BLACK)
            word_color_flags[current_index_to_change] = True
            for i in range(15):
                word = word_display[i]
                row = i // 5
                col = i % 5
                text_color = BLACK if word_color_flags[i] else color_display[i]
                text_surface = font.render(word, True, text_color)
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 5 * col + SCREEN_WIDTH // 10, SCREEN_HEIGHT // 3 * row + SCREEN_HEIGHT // 6))
                screen.blit(text_surface, text_rect)

                # สร้างกรอบสีดำสำหรับ word list ที่ถูกส่งแล้ว
                if word_color_flags[i]:
                    pygame.draw.rect(screen, BLACK, text_rect.inflate(BORDER_MARGIN, BORDER_MARGIN), 0)

                border_color = WHITE if current_index_to_change == i else BLACK  # เลือกสีของกรอบตามเงื่อนไข
                pygame.draw.rect(screen, border_color, text_rect.inflate(BORDER_MARGIN, BORDER_MARGIN), 2)

        pygame.display.flip()  
        current_index_to_change += 1
            
    end_time = time.time()
    elapsed_time = end_time - start_time
    screen.fill(WHITE)

    # Render the elapsed_time in the middle of the screen
    font_big = pygame.font.Font("/home/strooptest/Desktop/Test_Bluetooth/BoonTook-Regular.ttf", FONT_SIZE + 10)  # ปรับขนาด font
    elapsed_time_text = font_big.render(f"Elapsed Time: {elapsed_time:.2f} seconds", True, BLACK)
    elapsed_time_rect = elapsed_time_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))  # ปรับตำแหน่ง

    score_text = font_big.render(f"Score: {score}/15", True, BLACK)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, elapsed_time_rect.bottom + 20))  # ปรับตำแหน่ง

    # Blit both the elapsed time and score texts on the screen
    screen.blit(elapsed_time_text, elapsed_time_rect)
    screen.blit(score_text, score_rect)

    pygame.display.flip()
    time.sleep(10)
    return

def show_tutorial():
    print("Executing show_tutorial function")
    # Load tutorial images
    tutorial_images = ["pic/tutorial_image1.png", "pic/tutorial_image2.png", "pic/tutorial_image3.png"]
    current_image_index = 0

    # Check if tutorial images exist
    for image_path in tutorial_images:
        if not os.path.exists(image_path):
            print(f"Error: Tutorial image '{image_path}' not found.")
            sys.exit()

    # Load font and create a surface for the "back" and "next" buttons
    font = pygame.font.Font(None, int(SCREEN_HEIGHT * 0.09))
    back_text = font.render("Back", True, (255, 255, 255))
    next_text = font.render("Next", True, (255, 255, 255))

    # Determine the size of the "back" and "next" buttons
    button_width = max(back_text.get_width(), next_text.get_width()) + 40
    button_height = int(SCREEN_HEIGHT * 0.1)
    button_spacing = int(SCREEN_WIDTH * 0.05)

    back_rect = pygame.Rect(button_spacing, SCREEN_HEIGHT - button_height - button_spacing, button_width, button_height)
    next_rect = pygame.Rect(SCREEN_WIDTH - button_spacing - button_width, SCREEN_HEIGHT - button_height - button_spacing, button_width, button_height)

    # Set up the Pygame screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Game loop for the tutorial page
    tutorial_running = True
    while tutorial_running:
        print("loop_ok")
        screen.fill((0, 0, 0))  # Fill the screen with black
        title_font = pygame.font.Font(None, int(SCREEN_HEIGHT * 0.2))
        tutorial_title = title_font.render("Tutorial", True, (255, 255, 255))
        title_rect = tutorial_title.get_rect(center=(SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.13)))
        screen.blit(tutorial_title, title_rect)

        # Display current tutorial image at a smaller size
        original_image = pygame.image.load(tutorial_images[current_image_index])
        scaled_width = int(original_image.get_width() * 0.5)  # Adjust the scale factor as needed
        scaled_height = int(original_image.get_height() * 0.5)  # Adjust the scale factor as needed
        scaled_image = pygame.transform.scale(original_image, (scaled_width, scaled_height))
        image_rect = scaled_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(scaled_image, image_rect)

        # Display "back" and "next" buttons
        pygame.draw.rect(screen, (255, 0, 0), back_rect)  # Red rectangle for "back" button
        screen.blit(back_text, (back_rect.centerx - back_text.get_width() // 2, back_rect.centery - back_text.get_height() // 2))  # Center the text

        pygame.draw.rect(screen, (0, 255, 0), next_rect)  # Green rectangle for "next" button
        screen.blit(next_text, (next_rect.centerx - next_text.get_width() // 2, next_rect.centery - next_text.get_height() // 2))  # Center the text

        pygame.display.flip()

        command = arduino_sock.recv(1024).decode("utf-8")
        command = command.strip()  # Remove leading/trailing whitespace
        if command == '0':
            print("command_0")
            # Go to the next page
            tutorial_running = False
            return
        if command == '1':
            print("command_1")
            # Move to the next image
            current_image_index = (current_image_index + 1) % len(tutorial_images) 
        # Do not quit Pygame, just return from the function

def exit_game():
    print("Exiting the game")
    pygame.quit()
    sys.exit()

def connect_to_arduino(pi_address, port):
    try:
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect((pi_address, port))
        print("Connected to Arduino")
        return sock
    except bluetooth.BluetoothError as e:
        print("Bluetooth connection error:", e)
        return None

def moveToPage(choice):
    if choice == 0:
        print("choice Play\n")
        play_game()
    elif choice == 1:
        print("choice Tutorial\n")
        show_tutorial() 
        draw_menu(screen, title_text, title_rect, option_texts, option_rects, choice, device_connection_text, device_connection_rect)
    elif choice == 2:   
        print("choice exit\n")
        exit_game() 
        
# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Stroop Test Menu")

# Define fonts and text for the main menu
title_font_size = int(SCREEN_WIDTH * 0.125)
font_size = int(SCREEN_WIDTH * 0.0525)

title_font = pygame.font.Font(None, title_font_size)
font = pygame.font.Font(None, font_size)

title_text = title_font.render("Stroop Test", True, (255, 255, 255))
title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6))

# Define menu options
options = ["Play", "Tutorial", "Exit"]
option_texts = [font.render(option, True, (255, 255, 255)) for option in options]

# Determine the position and size of the red rectangle
device_connection_rect = pygame.Rect(SCREEN_WIDTH - 230, SCREEN_HEIGHT - 50, 200, 30)  # Adjust position and size as needed

# Render the "Device_connection" text
device_connection_font = pygame.font.Font(None, 24)  # Adjust font size as needed
device_connection_text = device_connection_font.render("Device Connection", True, (255, 255, 255))
# Calculate the position of the text to center it within the rectangle
device_connection_text_rect = device_connection_text.get_rect(center=device_connection_rect.center)


# Calculate layout parameters for the main menu
total_height = title_rect.height + sum(text.get_height() for text in option_texts) + len(option_texts) * int(SCREEN_HEIGHT * 0.025)
start_y = (SCREEN_HEIGHT - total_height) // 2
title_rect.top = start_y - int(SCREEN_HEIGHT * 0.0333)
start_y += title_rect.height + int(SCREEN_HEIGHT * 0.025)
spacing = int(SCREEN_HEIGHT * 0.0167)

# Set a fixed width and height for all option rectangles in the main menu
rect_width = int(SCREEN_WIDTH * 0.5)  # Adjust the width
rect_height = int(SCREEN_HEIGHT * 0.1)  # Adjust the height

# Position the options and rectangles in the main menu
rects = [pygame.Rect((SCREEN_WIDTH - rect_width) // 2, start_y + i * (rect_height + int(SCREEN_HEIGHT * 0.025)), rect_width, rect_height) for i in range(len(option_texts))]
option_rects = rects  # Assign the same rectangles to option_rects

# Game loop for the main menu
running = True
selected_option = 0  # Start with the first option selected
state = 0 #check is first run or not
choice = 0

print("Waiting for connection ....")

pi_address = "00:21:09:00:27:B7"  # Replace with your Pi's Bluetooth address
port = 1  # Bluetooth port

while running:
    if state == 1:
        while True:
            command = arduino_sock.recv(1024).decode("utf-8")
            command = command.strip()  # Remove leading/trailing whitespace
            if command == '0':
                choice += 1
                if choice >= 3:
                    choice = 0
                print("choice = :" + str(choice))
            elif command == '1':
                moveToPage(choice)
            draw_menu(screen, title_text, title_rect, option_texts, option_rects, choice, device_connection_text, device_connection_rect)

    draw_menu(screen, title_text, title_rect, option_texts, option_rects, choice, device_connection_text, device_connection_rect)
    if state == 0:
        arduino_sock = connect_to_arduino(pi_address, port)
        arduino_sock.send(b"Start\n")  # Make sure to include the newline character
        print("Data sent to Arduino")
        received_data = arduino_sock.recv(1024).decode("utf-8")
        print("Received data from Arduino:", received_data)
        state = 1   

if received_data:
        for i in range(5,0,-1):
            screen.fill(WHITE)
            pygame.display.flip()
            Ready_text = font.render(f"Ready ...{i:d}", True, (0, 0, 0))
            Ready_rect = Ready_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(Ready_text, Ready_rect)
            pygame.display.flip()
            time.sleep(1)

        start_time = time.time()
        screen.fill(BLACK)
        pygame.display.flip()

        for i in range(15):
            word = word_display[i]
            row = i // 5
            col = i % 5
            text_surface = font.render(word, True, color_display[i])
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 5 * col + SCREEN_WIDTH // 10, SCREEN_HEIGHT // 3 * row + SCREEN_HEIGHT // 6))
            screen.blit(text_surface, text_rect)
        pygame.display.flip()

        
# Quit Pygame and close the window for the main menu
pygame.quit()
sys.exit()
