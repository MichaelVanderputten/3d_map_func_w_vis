import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the window
window_size = (800, 800)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Pygame App")

# Set up colors
black = (0, 0, 0)
white = (255,255,255)

# set up fonts
font = pygame.font.Font(None, 36)

# initialize view variables
views = ["3D", "2D-XY", "2D-ZY", "2D-XZ"]
current_view_index = 0

# draw view button
def draw_view_button():
    button_text = font.render("View: " + views[current_view_index], True, (white))
    button_rect = button_text.get_rect(topleft=(window_size[0] - 150, 20))
    pygame.draw.rect(screen, black, button_rect)
    screen.blit(button_text, button_rect)

# print view index
def draw_current_view_text():
    text = font.render("Current View: " + views[current_view_index], True, (white))
    screen.blit(text, (10, window_size[1] - 50))

# initialzie graph
def initialize_graph():
    # Clear the screen
    screen.fill(black)

    # Draw the appropriate axes based on the current view
    if views[current_view_index] == "3D":
        # Draw X, Y, and Z axes
        cpx = window_size[1]/10
        cpy = window_size[1]-(window_size[1]/10) # common point

        xx = window_size[1]-(window_size[1]/10)
        xy = window_size[1]-(window_size[1]/10)

        yx = (window_size[1]/10)
        yy = (window_size[1]/10)
        
        zx = window_size[0] // 2
        zy = window_size[1] // 2 # end points

        pygame.draw.line(screen, white, (cpx, cpy), (xx, xy), 2) # x
        pygame.draw.line(screen, white, (cpx, cpy), (yx, yy), 2) # y 
        pygame.draw.line(screen, white, (cpx, cpy), (zx, zy), 2) # z
        # Label axes
        x_label = font.render("X-axis", True, white)
        y_label = font.render("Y-axis", True, white)
        z_label = font.render("Z-axis", True, white)
        screen.blit(x_label, (xx, xy))
        screen.blit(y_label, (yx, yy))
        screen.blit(z_label, (cpx, cpy))


    elif views[current_view_index] == "2D-XY":
        cpx = window_size[1]/10
        cpy = window_size[1]-(window_size[1]/10) # common point

        xx = window_size[1]-(window_size[1]/10)
        xy = window_size[1]-(window_size[1]/10)

        yx = (window_size[1]/10)
        yy = (window_size[1]/10) # end points
        # Draw X and Y axes
        pygame.draw.line(screen, white, (cpx, cpy), (xx, xy), 2) # x
        pygame.draw.line(screen, white, (cpx, cpy), (yx, yy), 2) # y 
        # Label axes
        x_label = font.render("X-axis", True, white)
        y_label = font.render("Y-axis", True, white)
        screen.blit(x_label, (xx, xy))
        screen.blit(y_label, (yx, yy))
    elif views[current_view_index] == "2D-ZY":
        cpx = window_size[1]/10
        cpy = window_size[1]-(window_size[1]/10) # common point

        zx = window_size[1]-(window_size[1]/10)
        zy = window_size[1]-(window_size[1]/10)

        yx = (window_size[1]/10)
        yy = (window_size[1]/10) # end points
        # Draw z and Y axes
        pygame.draw.line(screen, white, (cpx, cpy), (zx, zy), 2) # z
        pygame.draw.line(screen, white, (cpx, cpy), (yx, yy), 2) # y 
        # Label axes
        z_label = font.render("Z-axis", True, white)
        y_label = font.render("Y-axis", True, white)
        screen.blit(z_label, (zx, zy))
        screen.blit(y_label, (yx, yy))
    elif views[current_view_index] == "2D-XZ":
        cpx = window_size[1]/10
        cpy = window_size[1]-(window_size[1]/10) # common point

        xx = window_size[1]-(window_size[1]/10)
        xy = window_size[1]-(window_size[1]/10)

        zx = (window_size[1]/10)
        zy = (window_size[1]/10) # end points
        # Draw x and z axes
        pygame.draw.line(screen, white, (cpx, cpy), (xx, xy), 2) # x
        pygame.draw.line(screen, white, (cpx, cpy), (zx, zy), 2) # z
        # Label axes
        x_label = font.render("X-axis", True, white)
        z_label = font.render("Z-axis", True, white)
        screen.blit(x_label, (xx, xy))
        screen.blit(z_label, (zx, zy))


# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button clicked
                # Cycle through views
                current_view_index = (current_view_index + 1) % len(views)
                print("Switched to", views[current_view_index])

    # Clear the screen
    screen.fill(black)

    # Draw the view button & text
    draw_view_button()
    draw_current_view_text()

    # init graph
    initialize_graph()

    # Update the display
    pygame.display.flip()

