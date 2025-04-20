import pygame
import time
import random

pygame.init()

# Screen setup
width, height = 600, 400
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("🐍 Snake Game")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
dark_green = (0, 155, 0)
blue = (0, 0, 255)
gray = (40, 40, 40)
food_colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (255, 105, 180)]

# Game settings
block_size = 20
initial_speed = 15

# Fonts
font_main = pygame.font.SysFont("comicsansms", 35)
font_small = pygame.font.SysFont("comicsansms", 25)

clock = pygame.time.Clock()

def draw_grid():
    for x in range(0, width, block_size):
        pygame.draw.line(win, gray, (x, 0), (x, height))
    for y in range(0, height, block_size):
        pygame.draw.line(win, gray, (0, y), (width, y))

def draw_snake(snake_list):
    for i, pos in enumerate(snake_list):
        color = green if i == len(snake_list) - 1 else dark_green
        pygame.draw.rect(win, color, [pos[0], pos[1], block_size, block_size])

def draw_food(x, y, color):
    pygame.draw.rect(win, color, [x, y, block_size, block_size])

def display_message(text, color, y_offset=0):
    message = font_main.render(text, True, color)
    rect = message.get_rect(center=(width // 2, height // 2 + y_offset))
    win.blit(message, rect)

def display_score(score, high_score):
    value = font_small.render(f"Score: {score}  |  High Score: {high_score}", True, white)
    win.blit(value, [10, 10])

def pause_game():
    paused = True
    while paused:
        win.fill(black)
        display_message("Paused", white, -30)
        display_message("Press P to Resume", gray, 30)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                paused = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                paused = False

def gameLoop():
    game_over = False
    game_close = False

    x = width // 2
    y = height // 2

    dx = 0
    dy = 0

    snake = []
    length = 1
    score = 0
    high_score = 0
    snake_speed = initial_speed

    foodx = round(random.randrange(0, width - block_size) / block_size) * block_size
    foody = round(random.randrange(0, height - block_size) / block_size) * block_size
    food_color = random.choice(food_colors)

    while not game_over:
        while game_close:
            win.fill(black)
            display_message("Game Over!", red, -30)
            display_message("Press C to Play Again or Q to Quit", white, 30)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_close = False
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_close = False
                        game_over = True
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx == 0:
                    dx = -block_size
                    dy = 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx = block_size
                    dy = 0
                elif event.key == pygame.K_UP and dy == 0:
                    dy = -block_size
                    dx = 0
                elif event.key == pygame.K_DOWN and dy == 0:
                    dy = block_size
                    dx = 0
                elif event.key == pygame.K_p:
                    pause_game()

        x += dx
        y += dy

        if x >= width or x < 0 or y >= height or y < 0:
            game_close = True

        win.fill(black)
        draw_grid()
        draw_food(foodx, foody, food_color)

        snake.append([x, y])
        if len(snake) > length:
            del snake[0]

        for segment in snake[:-1]:
            if segment == [x, y]:
                game_close = True

        draw_snake(snake)
        high_score = max(high_score, score)
        display_score(score, high_score)

        pygame.display.update()

        # Food collision
        if x == foodx and y == foody:
            foodx = round(random.randrange(0, width - block_size) / block_size) * block_size
            foody = round(random.randrange(0, height - block_size) / block_size) * block_size
            food_color = random.choice(food_colors)
            length += 1
            score += 1
            if score % 5 == 0:
                snake_speed += 1  # Increase speed every 5 points

        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Run the game
gameLoop()
