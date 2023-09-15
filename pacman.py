import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
PACMAN_RADIUS = 20
GHOST_RADIUS = 10
PACMAN_COLOR = (255, 255, 0)
GHOST_COLOR = (255, 0, 0)
WALL_COLOR = (0, 0, 255)
PACMAN_START_POSITION = [300, 300]
PACMAN_SPEED = 0.2
GHOST_SPEED = 0.05
NUM_GHOSTS = 1
MAX_SCORE = 4

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man")

# Define the walls (rectangles)
walls = [pygame.Rect(50, 50, 20, 500),
         pygame.Rect(50, 50, 500, 20),
         pygame.Rect(50, 530, 500, 20),
         pygame.Rect(530, 50, 20, 500)]

# Initialize Pac-Man's position and direction
pacman_position = list(PACMAN_START_POSITION)
pacman_direction = [0, 0]
score = 0

# Create ghost positions and directions within the rectangles
ghosts = []
for _ in range(NUM_GHOSTS):
    valid_position = False
    while not valid_position:
        ghost_position = [random.randint(50, 550), random.randint(50, 550)]
        ghost_rect = pygame.Rect(ghost_position[0] - GHOST_RADIUS,
                                 ghost_position[1] - GHOST_RADIUS,
                                 2 * GHOST_RADIUS,
                                 2 * GHOST_RADIUS)
        valid_position = all(not ghost_rect.colliderect(wall) for wall in walls)
    ghost_direction = [random.choice([-1, 1]) * GHOST_SPEED, random.choice([-1, 1]) * GHOST_SPEED]
    ghosts.append([ghost_position, ghost_direction])

# Main game loop
running = True
game_over = False
game_win = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # Check keyboard input for Pac-Man movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            pacman_direction = [-PACMAN_SPEED, 0]
        if keys[pygame.K_RIGHT]:
            pacman_direction = [PACMAN_SPEED, 0]
        if keys[pygame.K_UP]:
            pacman_direction = [0, -PACMAN_SPEED]
        if keys[pygame.K_DOWN]:
            pacman_direction = [0, PACMAN_SPEED]

        # Update Pac-Man's position
        pacman_position[0] += pacman_direction[0]
        pacman_position[1] += pacman_direction[1]

        # Collision detection with walls
        pacman_rect = pygame.Rect(pacman_position[0] - PACMAN_RADIUS,
                                  pacman_position[1] - PACMAN_RADIUS,
                                  2 * PACMAN_RADIUS,
                                  2 * PACMAN_RADIUS)
        for wall in walls:
            if pacman_rect.colliderect(wall):
                pacman_position[0] -= pacman_direction[0]
                pacman_position[1] -= pacman_direction[1]

        # Update ghost positions and handle collisions
        for i in range(NUM_GHOSTS):
            ghost_position, ghost_direction = ghosts[i]

            # Ghost AI: Simple chasing algorithm
            dx = pacman_position[0] - ghost_position[0]
            dy = pacman_position[1] - ghost_position[1]
            distance = math.sqrt(dx**2 + dy**2)

            if distance != 0:
                ghost_direction[0] = (dx / distance) * GHOST_SPEED
                ghost_direction[1] = (dy / distance) * GHOST_SPEED

            ghost_position[0] += ghost_direction[0]
            ghost_position[1] += ghost_direction[1]

            # Check collision with walls
            ghost_rect = pygame.Rect(ghost_position[0] - GHOST_RADIUS,
                                     ghost_position[1] - GHOST_RADIUS,
                                     2 * GHOST_RADIUS,
                                     2 * GHOST_RADIUS)
            for wall in walls:
                if ghost_rect.colliderect(wall):
                    ghost_position[0] -= ghost_direction[0]
                    ghost_position[1] -= ghost_direction[1]

            # Check collision with Pac-Man
            if pacman_rect.colliderect(ghost_rect):
                game_over = True  # Game over if Pac-Man collides with a ghost

        # Check if Pac-Man collects a point
        for wall in walls:
            if pacman_rect.colliderect(wall):
                score += 1
                walls.remove(wall)

        # Check for win condition
        if score >= MAX_SCORE:
            game_win = True

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw walls
    for wall in walls:
        pygame.draw.rect(screen, WALL_COLOR, wall)

    # Draw Pac-Man
    pygame.draw.circle(screen, PACMAN_COLOR, pacman_position, PACMAN_RADIUS)

    # Draw Ghosts
    for ghost_position, _ in ghosts:
        pygame.draw.circle(screen, GHOST_COLOR, ghost_position, GHOST_RADIUS)

    # Draw score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Display game over message
    if game_over:
        game_over_text = font.render("Game Over", True, (255, 255, 255))
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 - 20))

    if game_win:
        game_win_text = font.render("You Won", True, (255, 255, 255))
        screen.blit(game_win_text, (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 - 20))
        
    # Update the display
    pygame.display.flip()

# Game over
pygame.quit()
sys.exit()
