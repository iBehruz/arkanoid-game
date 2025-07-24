
import asyncio
import pygame
import random
import platform

# Start Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
BALL_SIZE = 10
BRICK_WIDTH, BRICK_HEIGHT = 80, 30
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Game states
TITLE_SCREEN = 0
PLAYING = 1
GAME_OVER = 2

# Sound (simple placeholder for Pyodide, works locally too)
try:
    sound_hit = pygame.mixer.Sound(pygame.sndarray.make_sound(
        pygame.sndarray.array(pygame.surfarray.make_surface([[255] * 44100] * 2))
    ))
except:
    sound_hit = None

# Game objects
class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 50, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = 7

    def move(self, dx):
        self.rect.x += dx
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_SIZE, BALL_SIZE)
        self.dx = 5
        self.dy = -5

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.dx = -self.dx
        if self.rect.top <= 0:
            self.dy = -self.dy

class Brick:
    def __init__(self, x, y, color=RED):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.color = color

class PowerUp:
    def __init__(self, x, y, type):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.type = type
        self.dy = 3

    def move(self):
        self.rect.y += self.dy

# Initialize game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FinEasy Arkanoid")
font = pygame.font.SysFont("arial", 36)
state = TITLE_SCREEN
paddle = Paddle()
balls = [Ball()]
bricks = []
power_ups = []
level = 1
muted = False
mute_button = pygame.Rect(WIDTH - 100, 10, 80, 30)

# Define levels
levels = [
    # Level 1: Basic grid
    [(x * (BRICK_WIDTH + 10) + 50, y * (BRICK_HEIGHT + 10) + 50, RED)
     for x in range(8) for y in range(3)],
    # Level 2: Alternating rows
    [(x * (BRICK_WIDTH + 10) + 50, y * (BRICK_HEIGHT + 10) + 50, BLUE)
     for x in range(8) for y in range(4) if y % 2 == 0],
    # Level 3: Full grid
    [(x * (BRICK_WIDTH + 10) + 50, y * (BRICK_HEIGHT + 10) + 50, YELLOW)
     for x in range(8) for y in range(5)]
]

def load_level(level_num):
    global bricks
    bricks = [Brick(x, y, color) for x, y, color in levels[min(level_num - 1, len(levels) - 1)]]

def reset_game():
    global state, level, balls, power_ups, paddle
    state = TITLE_SCREEN
    level = 1
    paddle = Paddle()
    balls = [Ball()]
    power_ups = []
    load_level(level)

async def game_loop():
    global state, level, muted, mute_button, balls, paddle, bricks, power_ups
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if state == TITLE_SCREEN and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                state = PLAYING
                load_level(level)
            if state == GAME_OVER and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset_game()
            if event.type == pygame.MOUSEBUTTONDOWN and mute_button.collidepoint(event.pos):
                muted = not muted

        if state == PLAYING:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                paddle.move(-paddle.speed)
            if keys[pygame.K_RIGHT]:
                paddle.move(paddle.speed)

            for ball in balls[:]:
                ball.move()
                if ball.rect.bottom >= HEIGHT:
                    balls.remove(ball)
                    if not balls:
                        state = GAME_OVER
                if ball.rect.colliderect(paddle.rect):
                    ball.dy = -ball.dy
                    if sound_hit and not muted:
                        sound_hit.play()
                for brick in bricks[:]:
                    if ball.rect.colliderect(brick.rect):
                        bricks.remove(brick)
                        ball.dy = -ball.dy
                        if sound_hit and not muted:
                            sound_hit.play()
                        if random.random() < 0.3:
                            power_type = random.choice(["coin_boost", "extra_ball"])
                            power_ups.append(PowerUp(brick.rect.centerx, brick.rect.centery, power_type))
                if not bricks:
                    level += 1
                    if level > len(levels):
                        state = GAME_OVER
                    else:
                        load_level(level)
                        balls = [Ball()]

            for power_up in power_ups[:]:
                power_up.move()
                if power_up.rect.colliderect(paddle.rect):
                    if power_up.type == "coin_boost":
                        paddle.rect.width = min(paddle.rect.width + 20, 200)
                    elif power_up.type == "extra_ball":
                        balls.append(Ball())
                    power_ups.remove(power_up)
                if power_up.rect.top > HEIGHT:
                    power_ups.remove(power_up)

        # Draw everything
        screen.fill(BLACK)
        if state == TITLE_SCREEN:
            text = font.render("FinEasy Arkanoid - Press SPACE", True, WHITE)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
        elif state == GAME_OVER:
            text = font.render("Game Over - Press R to Restart", True, WHITE)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
        else:
            pygame.draw.rect(screen, WHITE, paddle.rect)
            for ball in balls:
                pygame.draw.ellipse(screen, WHITE, ball.rect)
            for brick in bricks:
                pygame.draw.rect(screen, brick.color, brick.rect)
            for power_up in power_ups:
                color = YELLOW if power_up.type == "coin_boost" else BLUE
                pygame.draw.rect(screen, color, power_up.rect)

        # Draw mute button
        text = font.render("Mute" if not muted else "Unmute", True, WHITE)
        pygame.draw.rect(screen, BLUE, mute_button)
        screen.blit(text, (mute_button.x + 10, mute_button.y + 5))

        pygame.display.flip()
        await asyncio.sleep(1.0 / FPS)

if platform.system() == "Emscripten":
    asyncio.ensure_future(game_loop())
else:
    if __name__ == "__main__":
        asyncio.run(game_loop())
