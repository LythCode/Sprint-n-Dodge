import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the game window
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Eat the red dots")

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 10  # Player radius for collision detection
        self.speed = 1  # Regular movement speed
        self.sprint_speed = 4  # Sprint movement speed
        self.sprint_duration = 5  # Duration of sprint in seconds
        self.sprint_cooldown = 5  # Cooldown period for sprint in seconds
        self.is_sprinting = False  # Flag to indicate if sprint is active
        self.sprint_start_time = 0  # Time when sprint started

    def move(self, dx, dy):
        if self.is_sprinting:
            speed = self.sprint_speed
        else:
            speed = self.speed

        # Check if the new position is within the screen boundaries
        if 0 <= self.x + dx * speed <= width:
            self.x += dx * speed
        if 0 <= self.y + dy * speed <= height:
            self.y += dy * speed

    def update(self):
        # Handle sprint activation
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not self.is_sprinting and pygame.time.get_ticks() - self.sprint_start_time >= self.sprint_cooldown * 1000:
            self.is_sprinting = True
            self.sprint_start_time = pygame.time.get_ticks()

        # Check sprint duration and deactivate sprint if time is up
        if self.is_sprinting and pygame.time.get_ticks() - self.sprint_start_time >= self.sprint_duration * 1000:
            self.is_sprinting = False
            self.sprint_start_time = pygame.time.get_ticks()
    def draw(self):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.radius)

class Enemy:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.velocity = random.uniform(1, 0.6)  # Random initial velocity
        self.direction = random.uniform(0, 2 * math.pi)  # Random initial direction

    def move(self):
        # Calculate the new position based on direction and velocity
        self.x += math.cos(self.direction) * self.velocity
        self.y += math.sin(self.direction) * self.velocity

        # Check if the enemy hits the borders of the screen
        if self.x - self.radius <= 0 or self.x + self.radius >= width:
            self.direction = math.pi - self.direction  # Reverse the x-axis direction
        if self.y - self.radius <= 0 or self.y + self.radius >= height:
            self.direction = -self.direction  # Reverse the y-axis direction

        # Limit the enemy's position within the screen boundaries
        self.x = max(self.radius, min(self.x, width - self.radius))
        self.y = max(self.radius, min(self.y, height - self.radius))

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

player = Player(width // 2, height // 2)  # Place the player at the center of the screen

enemies = []  # List to store enemy instances

enemy_count = 5  # Initial number of enemies
max_enemies = 50  # Maximum number of enemies
level = 1  # Current level

def spawn_enemies():
    for _ in range(enemy_count):
        x = random.randint(0, width)
        y = random.randint(0, height)
        radius = 10  # Adjust enemy radius as desired
        color = (255, 0, 0)  # Adjust enemy color as desired
        enemy = Enemy(x, y, radius, color)
        enemies.append(enemy)

def next_level():
    global enemy_count, level
    level += 1
    enemy_count = min(enemy_count + 1, max_enemies)
    spawn_enemies()

def reset_game():
    global enemy_count, level, score
    enemy_count = 5
    level = 1
    score = 0
    spawn_enemies()

spawn_enemies()

score = 0  # Player's score

running = True

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle key presses
    keys = pygame.key.get_pressed()
    move_speed = 0.5  # Adjust the movement speed as needed

    if keys[pygame.K_LEFT]:
        player.move(-move_speed, 0)
    if keys[pygame.K_RIGHT]:
        player.move(move_speed, 0)
    if keys[pygame.K_UP]:
        player.move(0, -move_speed)
    if keys[pygame.K_DOWN]:
        player.move(0, move_speed)

    # Update game logic
    player.update()

    # Check for collision between player and enemy
    for enemy in enemies:
        enemy.move()
        distance = math.hypot(player.x - enemy.x, player.y - enemy.y)
        if distance < player.radius + enemy.radius:
            enemies.remove(enemy)
            score += 1

    # Check if there are no remaining enemies
    if len(enemies) == 0:
        next_level()

    # Check if the player is outside the screen boundaries, and adjust its position if needed
    if player.x < player.radius:
        player.x = player.radius
    elif player.x > width - player.radius:
        player.x = width - player.radius
    if player.y < player.radius:
        player.y = player.radius
    elif player.y > height - player.radius:
        player.y = height - player.radius

    # Render graphics
    screen.fill((0, 0, 0))

    for enemy in enemies:
        enemy.draw()

    player.draw()

    # Render the player's score, level, and speed
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    level_text = font.render(f"Level: {level}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 50))

    if player.is_sprinting:
        sprint_time_remaining = max(0, (player.sprint_start_time + player.sprint_duration * 1000 - pygame.time.get_ticks()) // 1000)
        sprint_text = font.render(f"Sprint: {sprint_time_remaining}s", True, (255, 255, 255))
        screen.blit(sprint_text, (10, 90))

    pygame.display.flip()

# Quit the game
pygame.quit()

