import pygame
import sys
import math

from datainfo import *
from data import *

# Initialize Pygame
pygame.init()

# Set up the window
window_size = (800, 800)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Pygame 3D App")

# Set up colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

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
swap_from_3d = 0

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
    translated_x = x
    translated_y = y
    translated_z = z

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

# Draw 3D scene
def draw_3d_scene():
    center = (0,0, 0)

    # Draw the X, Y, and Z axes in the 3D view
    fixed_axis_points_3d = {}
    for point in axis_points_3d:
        rotated_point = rotate_3d(*point, center, (rotation_angle_x, rotation_angle_y, 0))
        screen_coordinates = (int(rotated_point[0] + center[0])+400, int(rotated_point[1] + center[1]+400))
        fixed_axis_points_3d[point] = screen_coordinates
    #print(fixed_axis_points_3d)

    for axis_key in fixed_axis_points_3d.keys():
        axis_start = fixed_axis_points_3d[(0, 0, 0)]
        axis_end = fixed_axis_points_3d[axis_key]
        pygame.draw.line(screen, red, (axis_start[0] + center[0], axis_start[1] + center[1]), (axis_end[0] + center[0], axis_end[1] + center[1]), 2)
        pygame.draw.circle(screen, green, fixed_axis_points_3d[axis_key], 2)


    # Draw 3D points projected onto 2D plane based on the current view
    for point in points_3d:
        rotated_point = rotate_3d(*point, center, (rotation_angle_x, rotation_angle_y, 0))

        if views[current_view_index] == "2D-XY":
            screen_coordinates = (int(rotated_point[0]), int(rotated_point[1]))
        elif views[current_view_index] == "2D-ZY":
            screen_coordinates = (int(rotated_point[2]), int(rotated_point[1]))
        elif views[current_view_index] == "2D-XZ":
            screen_coordinates = (int(rotated_point[0]), int(rotated_point[2]))
        else:
            screen_coordinates = (int(rotated_point[0] + center[0])+400, int(rotated_point[1] + center[1]+400))

        c = create_heatmap(point, step_z, 0)
        pygame.draw.circle(screen, c, screen_coordinates, 5)



# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button clicked
                if(current_view_index != 0):
                    swap_from_3d = current_view_index
                    current_view_index = 0 # set 3d
                rotate_active = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button released
                    rotate_active = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                current_view_index = (current_view_index + 1) % len(views)
                print("Switched to", views[current_view_index])
            elif event.key == pygame.K_b:
                current_view_index = (current_view_index - 1) % len(views)
                print("Switched to", views[current_view_index])


    # Clear the screen
    screen.fill(black)

    # Draw the view button & text
    draw_view_button()
    draw_current_view_text()

    # Rotate the points based on mouse movement
    if rotate_active:
        dx, dy = pygame.mouse.get_rel()
        rotation_angle_y += dx * -0.01  # Horizontal rotation
        rotation_angle_x += dy * 0.01  # Vertical rotation

        if(swap_from_3d == 1):
            swap_from_3d = 0
            rotation_angle_x = 0
            rotation_angle_y = 0
        elif(swap_from_3d == 2):
            swap_from_3d = 0
            rotation_angle_x = 0
            rotation_angle_y = 1.575
        elif(swap_from_3d == 3):
            swap_from_3d = 0
            rotation_angle_x = -1.575
            rotation_angle_y = 0


    # Draw the appropriate axes and points based on the current view
    if views[current_view_index] == "3D":
        # Draw 3D points
        draw_3d_scene()

    elif views[current_view_index] == "2D-XY":
        # Draw x and Y axes
        pygame.draw.line(screen, white, (window_size[0]//2, window_size[1]//10), (window_size[0]//2, window_size[1]-(window_size[1]//10)), 2) # Y
        pygame.draw.line(screen, white, (window_size[0]//10, window_size[1]//2), (window_size[0]-(window_size[0]//10), window_size[1]//2), 2) # X
        # Label axes
        z_label = font.render("Y-axis", True, white)
        y_label = font.render("X-axis", True, white)
        screen.blit(z_label, (window_size[0]//2, window_size[1]//10))
        screen.blit(y_label, (window_size[0]//10, window_size[1]//2))

        #draw points using z and y
        for point in ori_points_3d:
            c = create_heatmap(point, step_z, 2)
            pygame.draw.circle(screen, c, (point[0]+400, point[1]+400), 5)

    elif views[current_view_index] == "2D-ZY":
        # Draw z and Y axes
        pygame.draw.line(screen, white, (window_size[0]//2, window_size[1]//10), (window_size[0]//2, window_size[1]-(window_size[1]//10)), 2) # Y
        pygame.draw.line(screen, white, (window_size[0]//10, window_size[1]//2), (window_size[0]-(window_size[0]//10), window_size[1]//2), 2) # Z
        # Label axes
        z_label = font.render("Y-axis", True, white)
        y_label = font.render("Z-axis", True, white)
        screen.blit(z_label, (window_size[0]//2, window_size[1]//10))
        screen.blit(y_label, (window_size[0]//10, window_size[1]//2))

        #draw points using z and y
        for point in ori_points_3d:
            c = create_heatmap(point, step_z, 0)
            pygame.draw.circle(screen, c, (point[2]+400, point[1]+400), 5)
    elif views[current_view_index] == "2D-XZ":
        # Draw x and z axes
        pygame.draw.line(screen, white, (window_size[0]//2, window_size[1]//10), (window_size[0]//2, window_size[1]-(window_size[1]//10)), 2) # z
        pygame.draw.line(screen, white, (window_size[0]//10, window_size[1]//2), (window_size[0]-(window_size[0]//10), window_size[1]//2), 2) # x
        # Label axes
        z_label = font.render("Z-axis", True, white)
        y_label = font.render("X-axis", True, white)
        screen.blit(z_label, (window_size[0]//2, window_size[1]//10))
        screen.blit(y_label, (window_size[0]//10, window_size[1]//2))

        #draw points using z and y
        for point in ori_points_3d:
            c = create_heatmap(point, step_z, 1)
            pygame.draw.circle(screen, c, (point[0]+400, point[2]+400), 5)

    # Update the display
    pygame.display.flip()
