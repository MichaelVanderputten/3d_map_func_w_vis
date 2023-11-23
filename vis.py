import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the window
window_size = (800, 800)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Pygame App")

# Set up colors
white = (255, 255, 255)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear the screen
    screen.fill(white)

    # Update the display
    pygame.display.flip()

