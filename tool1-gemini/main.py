
import pygame
import sys

# --- Game Setup ---
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping-Pong")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game objects
player1 = pygame.Rect(50, HEIGHT // 2 - 35, 15, 70)
player2 = pygame.Rect(WIDTH - 65, HEIGHT // 2 - 35, 15, 70)
ball = pygame.Rect(WIDTH // 2 - 10, HEIGHT // 2 - 10, 20, 20)

# Paddle speeds
player1_speed = 7
player2_speed = 7
ball_speed_x = 6
ball_speed_y = 6
player1_score = 0
player2_score = 0
score_font = pygame.font.Font(None, 50)

# Clock
clock = pygame.time.Clock()

def ball_restart():
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH/2, HEIGHT/2)
    ball_speed_y *= -1
    ball_speed_x *= -1

# --- Main Game Loop ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # --- Player Input ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player1.y -= player1_speed
    if keys[pygame.K_s]:
        player1.y += player1_speed
    if keys[pygame.K_UP]:
        player2.y -= player2_speed
    if keys[pygame.K_DOWN]:
        player2.y += player2_speed

    # --- Ball Movement ---
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # --- Boundaries ---
    if player1.top <= 0:
        player1.top = 0
    if player1.bottom >= HEIGHT:
        player1.bottom = HEIGHT
    if player2.top <= 0:
        player2.top = 0
    if player2.bottom >= HEIGHT:
        player2.bottom = HEIGHT

    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    if ball.left <= 0:
        player2_score += 1
        ball_restart()

    if ball.right >= WIDTH:
        player1_score += 1
        ball_restart()

    # --- Collisions ---
    if ball.colliderect(player1) or ball.colliderect(player2):
        ball_speed_x *= -1

    # --- Drawing ---
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player1)
    pygame.draw.rect(screen, WHITE, player2)
    pygame.draw.rect(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    player1_text = score_font.render(f"{player1_score}", True, WHITE)
    screen.blit(player1_text, (WIDTH/2 - 50, 20))

    player2_text = score_font.render(f"{player2_score}", True, WHITE)
    screen.blit(player2_text, (WIDTH/2 + 30, 20))

    pygame.display.flip()
    clock.tick(60)
