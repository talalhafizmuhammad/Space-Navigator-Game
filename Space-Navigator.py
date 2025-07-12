import pygame
import random
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Navigator")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 100)

font_small = pygame.font.SysFont("Arial", 24)
font_large = pygame.font.SysFont("Arial", 48)

player_size = 30
player_pos = [WIDTH // 2, HEIGHT - 60]
player_speed = 7

score = 0
high_score = 0
game_state = "menu"
stars = [[random.randint(0, WIDTH), random.randint(0, HEIGHT)] for _ in range(400)]

class Asteroid:
    def __init__(self):
        self.size = random.randint(15 , 40)
        self.x = random.randint(self.size, WIDTH - self.size)
        self.y = -self.size
        self.speed = random.randint(3, 6)
        self.color = (150, 150, 150)

    def update(self):
        self.y += self.speed

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)

    def check_collision(self, player_pos, player_size):
        dx = self.x - player_pos[0]
        dy = self.y - player_pos[1]
        distance_squared = dx * dx + dy * dy
        radius_sum = self.size + player_size // 2
        return distance_squared < radius_sum * radius_sum

asteroids = []
asteroid_timer = 0
asteroid_delay = 30

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.life = 30

    def update(self):
        self.y += 2
        self.life -= 1
        return self.life > 0

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 2)

particles = []

clock = pygame.time.Clock()

running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                if game_state == "menu" or game_state == "gameover":
                    game_state = "playing"
                    player_pos = [WIDTH // 2, HEIGHT - 60]
                    asteroids = []
                    particles = []
                    score = 0
                    asteroid_timer = 0

    for star in stars:
        star[1] += 1
        if star[1] > HEIGHT:
            star[1] = 0
            star[0] = random.randint(0, WIDTH)
        pygame.draw.circle(screen, WHITE, star, 1)

    keys = pygame.key.get_pressed()

    if game_state == "playing":
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_pos[0] = max(player_size // 2, player_pos[0] - player_speed)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_pos[0] = min(WIDTH - player_size // 2, player_pos[0] + player_speed)

        particles.append(Particle(player_pos[0], player_pos[1] + player_size // 2, BLUE))
        for particle in particles[:]:
            if not particle.update():
                particles.remove(particle)
            else:
                particle.draw(screen)
        asteroid_timer += 1
        if asteroid_timer >= asteroid_delay:
            asteroid_timer = 0
            asteroids.append(Asteroid())
            asteroid_delay = max(15, 30 - score // 500)

        for asteroid in asteroids[:]:
            asteroid.update()
            asteroid.draw(screen)
            if asteroid.y > HEIGHT + asteroid.size:
                asteroids.remove(asteroid)
                score += 10
            elif asteroid.check_collision(player_pos, player_size):
                game_state = "gameover"
                if score > high_score:
                    high_score = score

        pygame.draw.polygon(screen, WHITE, [
            (player_pos[0], player_pos[1] - player_size // 2),
            (player_pos[0] - player_size // 2, player_pos[1] + player_size // 2),
            (player_pos[0] + player_size // 2, player_pos[1] + player_size // 2)
        ])
        screen.blit(font_small.render(f"Score: {score}", True, WHITE), (10, 10))
        screen.blit(font_small.render(f"High Score: {high_score}", True, WHITE), (10, 40))

    elif game_state == "menu":
        title = font_large.render("SPACE NAVIGATOR", True, YELLOW)
        prompt = font_small.render("Press SPACE to start", True, WHITE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//3))
        screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//2))

    elif game_state == "gameover":
        over = font_large.render("GAME OVER", True, RED)
        retry = font_small.render("Press SPACE to try again", True, WHITE)
        screen.blit(over, (WIDTH//2 - over.get_width()//2, HEIGHT//2 - 40))
        screen.blit(retry, (WIDTH//2 - retry.get_width()//2, HEIGHT//2 + 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
