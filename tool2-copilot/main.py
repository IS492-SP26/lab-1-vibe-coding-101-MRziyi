import sys
import random
import pygame


WIDTH = 900
HEIGHT = 500
FPS = 60

PADDLE_WIDTH = 12
PADDLE_HEIGHT = 80
PADDLE_SPEED = 6

BALL_SIZE = 12
BALL_SPEED_X = 5
BALL_SPEED_Y = 4

SCORE_FONT_SIZE = 36
MAX_SCORE = 11

BG_COLOR = (16, 16, 20)
LINE_COLOR = (60, 60, 70)
PADDLE_COLOR = (220, 220, 220)
BALL_COLOR = (220, 80, 80)
TEXT_COLOR = (230, 230, 230)


def reset_ball(ball_rect: pygame.Rect) -> tuple[int, int]:
    ball_rect.center = (WIDTH // 2, HEIGHT // 2)
    direction_x = random.choice([-1, 1])
    direction_y = random.choice([-1, 1])
    return BALL_SPEED_X * direction_x, BALL_SPEED_Y * direction_y


def clamp_paddle(paddle_rect: pygame.Rect) -> None:
    if paddle_rect.top < 0:
        paddle_rect.top = 0
    if paddle_rect.bottom > HEIGHT:
        paddle_rect.bottom = HEIGHT


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Ping-Pong")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", SCORE_FONT_SIZE)

    left_paddle = pygame.Rect(30, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = pygame.Rect(WIDTH - 30 - PADDLE_WIDTH, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(0, 0, BALL_SIZE, BALL_SIZE)

    ball_vel_x, ball_vel_y = reset_ball(ball)

    left_score = 0
    right_score = 0
    paused = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    paused = not paused
                if event.key == pygame.K_r:
                    left_score = 0
                    right_score = 0
                    ball_vel_x, ball_vel_y = reset_ball(ball)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            left_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_s]:
            left_paddle.y += PADDLE_SPEED
        if keys[pygame.K_UP]:
            right_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN]:
            right_paddle.y += PADDLE_SPEED

        clamp_paddle(left_paddle)
        clamp_paddle(right_paddle)

        if not paused and left_score < MAX_SCORE and right_score < MAX_SCORE:
            ball.x += ball_vel_x
            ball.y += ball_vel_y

            if ball.top <= 0 or ball.bottom >= HEIGHT:
                ball_vel_y *= -1

            if ball.colliderect(left_paddle) and ball_vel_x < 0:
                ball_vel_x *= -1
                offset = (ball.centery - left_paddle.centery) / (PADDLE_HEIGHT / 2)
                ball_vel_y = int(BALL_SPEED_Y * offset) or random.choice([-1, 1])

            if ball.colliderect(right_paddle) and ball_vel_x > 0:
                ball_vel_x *= -1
                offset = (ball.centery - right_paddle.centery) / (PADDLE_HEIGHT / 2)
                ball_vel_y = int(BALL_SPEED_Y * offset) or random.choice([-1, 1])

            if ball.right < 0:
                right_score += 1
                ball_vel_x, ball_vel_y = reset_ball(ball)

            if ball.left > WIDTH:
                left_score += 1
                ball_vel_x, ball_vel_y = reset_ball(ball)

        screen.fill(BG_COLOR)

        pygame.draw.line(screen, LINE_COLOR, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)
        pygame.draw.rect(screen, PADDLE_COLOR, left_paddle)
        pygame.draw.rect(screen, PADDLE_COLOR, right_paddle)
        pygame.draw.ellipse(screen, BALL_COLOR, ball)

        left_text = font.render(str(left_score), True, TEXT_COLOR)
        right_text = font.render(str(right_score), True, TEXT_COLOR)
        screen.blit(left_text, (WIDTH // 4 - left_text.get_width() // 2, 20))
        screen.blit(right_text, (WIDTH * 3 // 4 - right_text.get_width() // 2, 20))

        if left_score >= MAX_SCORE or right_score >= MAX_SCORE:
            winner = "Left" if left_score > right_score else "Right"
            win_text = font.render(f"{winner} wins!", True, TEXT_COLOR)
            prompt_text = font.render("Press R to restart", True, TEXT_COLOR)
            screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - 30))
            screen.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT // 2 + 10))

        if paused:
            pause_text = font.render("Paused", True, TEXT_COLOR)
            screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 30))

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
