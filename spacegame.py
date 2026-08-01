"""
Space Collector - a simple falling-object collector game built with Pygame.

You control a basket at the bottom of the screen and move it left/right
to catch stars falling from the top. Catching a star scores a point;
missing one (letting it fall off the bottom) costs a life. The game
speeds up gradually and ends when you run out of lives.
"""

import random
import sys

import pygame

# --- Constants -------------------------------------------------------------
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
FPS = 60

WHITE = (255, 255, 255)
BLACK = (20, 20, 30)
YELLOW = (255, 215, 0)
BLUE = (70, 130, 220)
RED = (220, 60, 60)

PLAYER_WIDTH = 90
PLAYER_HEIGHT = 20
PLAYER_SPEED = 8

STAR_SIZE = 24
STAR_SPAWN_MS = 700  # lower this over time to speed up the game
STARTING_LIVES = 3


class Player(pygame.sprite.Sprite):
    """The basket the user moves left and right to catch falling stars."""

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 20

    def update(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += PLAYER_SPEED
        # Keep the player fully on screen.
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, SCREEN_WIDTH)


class Star(pygame.sprite.Sprite):
    """A falling object the player tries to catch."""

    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((STAR_SIZE, STAR_SIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - STAR_SIZE)
        self.rect.y = -STAR_SIZE
        self.speed = speed

    def update(self, keys):
        # keys is unused here but kept so both sprite types share one
        # update() signature, letting a single group.update(keys) call
        # drive everything.
        self.rect.y += self.speed


def draw_text(surface, text, size, color, center):
    font = pygame.font.SysFont(None, size)
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=center)
    surface.blit(rendered, rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Collector")
    clock = pygame.time.Clock()

    player = Player()
    all_sprites = pygame.sprite.Group(player)
    stars = pygame.sprite.Group()

    # Custom event used to spawn a new star at a regular interval.
    SPAWN_STAR = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_STAR, STAR_SPAWN_MS)

    score = 0
    lives = STARTING_LIVES
    star_speed = 4
    game_over = False

    while True:
        # --- Event handling --------------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                # Let the player restart with R after a game over.
                if event.key == pygame.K_r and game_over:
                    return main()

            if event.type == SPAWN_STAR and not game_over:
                star = Star(star_speed)
                stars.add(star)
                all_sprites.add(star)

        if not game_over:
            # --- Update ---------------------------------------------------
            keys = pygame.key.get_pressed()
            player.update(keys)
            stars.update(keys)

            # Check which stars the player caught vs. which fell off screen.
            caught = pygame.sprite.spritecollide(player, stars, dokill=True)
            score += len(caught)

            for star in list(stars):
                if star.rect.top > SCREEN_HEIGHT:
                    star.kill()
                    lives -= 1

            # Every 5 points, speed up the stars a little.
            star_speed = 4 + score // 5

            if lives <= 0:
                game_over = True

        # --- Draw -----------------------------------------------------
        screen.fill(BLACK)
        all_sprites.draw(screen)
        draw_text(screen, f"Score: {score}", 28, WHITE, (80, 25))
        draw_text(screen, f"Lives: {lives}", 28, RED, (SCREEN_WIDTH - 80, 25))

        if game_over:
            draw_text(screen, "GAME OVER", 48, WHITE,
                      (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
            draw_text(screen, "Press R to restart or Esc to quit", 24, WHITE,
                      (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
