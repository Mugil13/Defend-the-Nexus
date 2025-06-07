import pygame
import random

# Initialize the game
pygame.init()

# Screen setup
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Define Enemy class
class Enemy:
    def __init__(self, health, speed, armor, path):
        self.health = health
        self.speed = speed
        self.armor = armor
        self.path = path
        self.x, self.y = self.path[0]  # Starting position

    def move(self):
        # Move along the path using the speed attribute
        if len(self.path) > 1:
            next_point = self.path[1]
            if self.x < next_point[0]:
                self.x += self.speed
            elif self.x > next_point[0]:
                self.x -= self.speed
            
            if self.y < next_point[1]:
                self.y += self.speed
            elif self.y > next_point[1]:
                self.y -= self.speed

            if (self.x, self.y) == next_point:
                self.path.pop(0)

    def draw(self, screen):
        # Draw the enemy on the screen
        pygame.draw.circle(screen, RED, (self.x, self.y), 10)

# Define Tower class
class Tower:
    def __init__(self, x, y, range, damage, attack_speed):
        self.x = x
        self.y = y
        self.range = range
        self.damage = damage
        self.attack_speed = attack_speed
        self.cooldown = 0

    def attack(self, enemies):
        # Attack the closest enemy within range
        for enemy in enemies:
            if self.is_in_range(enemy):
                enemy.health -= self.damage
                break

    def is_in_range(self, enemy):
        # Check if the enemy is within tower range
        return (self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2 <= self.range ** 2

    def draw(self, screen):
        # Draw the tower on the screen
        pygame.draw.circle(screen, GREEN, (self.x, self.y), 15)

# Main game loop
def game_loop():
    clock = pygame.time.Clock()
    running = True

    # Game elements
    towers = [Tower(400, 300, 100, 20, 1)]  # Example tower
    enemy_path = [(0, 100), (screen_width, 100)]  # Example enemy path from left to right
    enemies = [Enemy(100, 2, 0, enemy_path.copy())]  # Example enemy

    while running:
        screen.fill(WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Game logic
        for tower in towers:
            tower.attack(enemies)
            tower.draw(screen)

        for enemy in enemies:
            enemy.move()
            enemy.draw(screen)
            if enemy.health <= 0:
                enemies.remove(enemy)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    game_loop()
