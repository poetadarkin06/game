import pygame
import sys

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BRICK_WIDTH = 80
BRICK_HEIGHT = 30
BRICK_GAP = 10

class GameObject(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x, y):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Paddle(GameObject):
    def __init__(self):
        super().__init__(BLUE, 100, 10, (SCREEN_WIDTH - 100) // 2, SCREEN_HEIGHT - 50)
        self.speed = 0

    def update(self):
        self.rect.x += self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

class Ball(GameObject):
    def __init__(self, paddle):
        super().__init__(RED, 10, 10, (SCREEN_WIDTH - 10) // 2, SCREEN_HEIGHT - 70)
        self.paddle = paddle
        self.speed_x = 3
        self.speed_y = -3

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x = -self.speed_x
        if self.rect.top <= 0:
            self.speed_y = -self.speed_y
        if pygame.sprite.collide_rect(self, self.paddle):
            self.speed_y = -self.speed_y

class Brick(GameObject):
    def __init__(self, x, y):
        super().__init__(GREEN, BRICK_WIDTH, BRICK_HEIGHT, x, y)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Brick Breaker")
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.bricks = pygame.sprite.Group()
        self.paddle = Paddle()
        self.ball = Ball(self.paddle)
        self.all_sprites.add(self.paddle, self.ball)
        self.lives = 3
        self.score = 0
        self.generate_bricks()

    def generate_bricks(self):
        for row in range(4):
            for column in range(10):
                brick = Brick(column * (BRICK_WIDTH + BRICK_GAP), row * (BRICK_HEIGHT + BRICK_GAP) + 50)
                self.bricks.add(brick)
                self.all_sprites.add(brick)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.paddle.speed = -5
                elif event.key == pygame.K_RIGHT:
                    self.paddle.speed = 5
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.paddle.speed = 0

    def update(self):
        self.all_sprites.update()
        brick_collisions = pygame.sprite.spritecollide(self.ball, self.bricks, True)
        if brick_collisions:
            self.ball.speed_y = -self.ball.speed_y
            self.score += 1
        if self.ball.rect.bottom >= SCREEN_HEIGHT:
            self.lives -= 1
            if self.lives > 0:
                self.ball.rect.x = self.paddle.rect.x + self.paddle.rect.width // 2 - self.ball.rect.width // 2
                self.ball.rect.y = self.paddle.rect.y - self.ball.rect.height
                self.ball.speed_y = -3
            else:
                self.game_over()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        font = pygame.font.Font(None, 36)
        lives_text = font.render(f"Lives: {self.lives}", True, WHITE)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(lives_text, (10, 10))
        self.screen.blit(score_text, (SCREEN_WIDTH - 150, 10))
        pygame.display.flip()

    def game_over(self):
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("Game Over", True, RED)
        restart_text = font.render("Press R to restart", True, WHITE)
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 + 50))
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        waiting = False
        self.reset()

    def reset(self):
        self.all_sprites.empty()
        self.bricks.empty()
        self.paddle = Paddle()
        self.ball = Ball(self.paddle)
        self.all_sprites.add(self.paddle, self.ball)
        self.lives = 3
        self.score = 0
        self.generate_bricks()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()
