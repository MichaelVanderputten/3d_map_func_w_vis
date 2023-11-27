import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set up the window
window_size = (800, 800)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Pygame 3D App")

# Set up colors
black = (0, 0, 0)
white = (255, 255, 255)

# Set up fonts
font = pygame.font.Font(None, 36)

# Initialize rotation variables
rotation_angle_x = 0
rotation_angle_y = 0
rotate_active = False
rotation_start_time = 0

# Initialize view variables
views = ["3D", "2D-XY", "2D-ZY", "2D-XZ"]
current_view_index = 0

# Draw view button
def draw_view_button():
    button_text = font.render("View: " + views[current_view_index], True, white)
    button_rect = button_text.get_rect(topleft=(window_size[0] - 150, 20))
    pygame.draw.rect(screen, black, button_rect)
    screen.blit(button_text, button_rect)

# Print view index
def draw_current_view_text():
    text = font.render("Current View: " + views[current_view_index], True, white)
    screen.blit(text, (10, window_size[1] - 50))

# Rotate points in 3D
def rotate_3d(x, y, z, center, angles):
    # Translate the points to the origin
    translated_x = x - center[0]
    translated_y = y - center[1]
    translated_z = z - center[2]

    # Rotate around the x-axis
    rotated_y = translated_y * math.cos(angles[0]) - translated_z * math.sin(angles[0])
    rotated_z = translated_y * math.sin(angles[0]) + translated_z * math.cos(angles[0])

    # Rotate around the y-axis
    rotated_x = translated_x * math.cos(angles[1]) + rotated_z * math.sin(angles[1])
    rotated_z = -translated_x * math.sin(angles[1]) + rotated_z * math.cos(angles[1])

    # Rotate around the z-axis (optional)
    rotated_x = rotated_x * math.cos(angles[2]) - rotated_y * math.sin(angles[2])
    rotated_y = rotated_x * math.sin(angles[2]) + rotated_y * math.cos(angles[2])

    # Translate the points back to the original position
    rotated_x += center[0]
    rotated_y += center[1]
    rotated_z += center[2]

    return rotated_x, rotated_y, rotated_z

# Initialize 3D points
points_3d = [
    (100, 100, 100),
    (200, 100, 100),
    (200, 200, 100),
    (100, 200, 100),
    (150, 150, 200),
    (100, 150, 250),
]  # test points

# Draw 3D scene
def draw_3d_scene():
    # Draw the X, Y, and Z axes in the 3D view
    for axis in [(1, 0, 0), (0, 1, 0), (0, 0, 1)]:
        axis_start = rotate_3d(0, 0, 0, center=(window_size[0] // 2, window_size[1] // 2, 0), angles=(rotation_angle_x, rotation_angle_y, 0))
        axis_end = rotate_3d(axis[0] * 150, axis[1] * 150, axis[2] * 150, center=(window_size[0] // 2, window_size[1] // 2, 0), angles=(rotation_angle_x, rotation_angle_y, 0))
        pygame.draw.line(screen, white, axis_start[:2], axis_end[:2], 2)

    # Draw 3D points
    for point in points_3d:
        rotated_point = rotate_3d(*point, center=(window_size[0] // 2, window_size[1] // 2, 0), angles=(rotation_angle_x, rotation_angle_y, 0))
        pygame.draw.circle(screen, white, (int(rotated_point[0]), int(rotated_point[1])), 5)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button clicked
                rotate_active = True
                rotation_start_time = pygame.time.get_ticks()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button released
                elapsed_time = pygame.time.get_ticks() - rotation_start_time
                if elapsed_time >= 1000:  # Check if the mouse was pressed for more than a second
                    rotate_active = False
                else:
                    rotate_active = False
                    current_view_index = (current_view_index + 1) % len(views)
                    print("Switched to", views[current_view_index])

    # Clear the screen
    screen.fill(black)

    # Draw the view button & text
    draw_view_button()
    draw_current_view_text()

    # Rotate the points based on mouse movement
    if rotate_active:
        dx, dy = pygame.mouse.get_rel()
        rotation_angle_x += dx * 0.01  # Horizontal rotation
        rotation_angle_y += dy * 0.01  # Vertical rotation

    # Draw the appropriate axes and points based on the current view
    if views[current_view_index] == "3D":
        # Draw 3D points
        draw_3d_scene()

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

    # Update the display
    pygame.display.flip()
