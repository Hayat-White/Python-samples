import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Setup the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Clock for controlling the speed
clock = pygame.time.Clock()

def game_loop():
    # Initialize variables
    game_over = False
    x, y = WIDTH // 2, HEIGHT // 2
    dx, dy = 0, 0
    snake = [(x, y)]
    food = (random.randrange(0, WIDTH, BLOCK_SIZE), random.randrange(0, HEIGHT, BLOCK_SIZE))
    score = 0

    # Font for score display
    font = pygame.font.SysFont(None, 35)

    def draw_score():
        text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(text, [10, 10])

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            # Control the snake
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -BLOCK_SIZE
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, BLOCK_SIZE
                elif event.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -BLOCK_SIZE, 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = BLOCK_SIZE, 0

        # Move the snake
        x = (x + dx) % WIDTH
        y = (y + dy) % HEIGHT
        snake.append((x, y))

        # Check for collision with food
        if (x, y) == food:
            score += 1
            food = (random.randrange(0, WIDTH, BLOCK_SIZE), random.randrange(0, HEIGHT, BLOCK_SIZE))
        else:
            snake.pop(0)

        # Check for self-collision
        if len(snake) != len(set(snake)):
            game_over = True

        # Draw the game
        screen.fill(BLACK)
        pygame.draw.rect(screen, RED, (*food, BLOCK_SIZE, BLOCK_SIZE))
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (*segment, BLOCK_SIZE, BLOCK_SIZE))
        draw_score()

        pygame.display.update()
        clock.tick(10)

    # Game Over screen
    screen.fill(BLACK)
    text = font.render("Game Over!", True, RED)
    screen.blit(text, [WIDTH // 2 - 50, HEIGHT // 2])
    pygame.display.update()
    time.sleep(2)
    pygame.quit()

# Run the game
game_loop()
