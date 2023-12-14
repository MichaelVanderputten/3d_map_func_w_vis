import pygame
import sys
import math

from datainfo import *
from data import *

from graph import *

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

viewer_position = (0, 0, -3*abs_z)

# Initialize view variables
views = ["3D", "2D-XY", "2D-ZY", "2D-XZ"]
current_view_index = 0
swap_from_3d = 0
axis_color = False

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

def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2)

# Rotate points in 3D
def rotate_3d(x, y, z, info, center, angles):
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

def draw_3d_graph():
    center = (0, 0, 0)
    distance_to_center = calculate_distance(center, viewer_position)
    for graph in graphs:
        for row in range(len(graph) - 1):  # subtract 1 to avoid index out of range
            for col in range(len(graph[row]) - 1):  # subtract 1 to avoid index out of range
                # Get points from current and next row
                point1 = graph[row][col]
                point2 = graph[row+1][col]
                point3 = graph[row+1][col+1]
                point4 = graph[row][col+1]

                # Apply rotation to each 3D point
                rotated_point1 = rotate_3d(point1[0], point1[1], point1[2], -1, center, (rotation_angle_x, rotation_angle_y, 0))
                rotated_point2 = rotate_3d(point2[0], point2[1], point2[2], -1, center, (rotation_angle_x, rotation_angle_y, 0))
                rotated_point3 = rotate_3d(point3[0], point3[1], point3[2], -1, center, (rotation_angle_x, rotation_angle_y, 0))
                rotated_point4 = rotate_3d(point4[0], point4[1], point4[2], -1, center, (rotation_angle_x, rotation_angle_y, 0))

                # Calculate screen coordinates
                screen_coordinates1 = (int(rotated_point1[0] + center[0]) + 400, int(rotated_point1[1] + center[1] + 400))
                screen_coordinates2 = (int(rotated_point2[0] + center[0]) + 400, int(rotated_point2[1] + center[1] + 400))
                screen_coordinates3 = (int(rotated_point3[0] + center[0]) + 400, int(rotated_point3[1] + center[1] + 400))
                screen_coordinates4 = (int(rotated_point4[0] + center[0]) + 400, int(rotated_point4[1] + center[1] + 400))

                # Draw the rotated and scaled points
                pygame.draw.polygon(screen, blue, (screen_coordinates1, screen_coordinates2, screen_coordinates3, screen_coordinates4), 2)




# Draw 3D scene
def draw_3d_scene():
    center = (0, 0, 0)

    # Calculate the distance from the viewer's perspective to the center of the scene
    distance_to_center = calculate_distance(center, viewer_position)

    # Draw the X, Y, and Z axes in the 3D view
    fixed_axis_points_3d = {}
    for point in axis_points_3d:
        rotated_point = rotate_3d(point[0], point[1], point[2], -1, center, (rotation_angle_x, rotation_angle_y, 0))
        screen_coordinates = (int(rotated_point[0] + center[0]) + 400, int(rotated_point[1] + center[1] + 400))

        # Calculate distance from the viewer to the current point
        distance_to_point = calculate_distance(viewer_position, rotated_point)

        # Scale factor based on distance (you can adjust this factor as needed)
        scale_factor = distance_to_center / distance_to_point

        # Apply the scale factor to the point size
        point_size = int(5 * scale_factor)

        fixed_axis_points_3d[point] = (screen_coordinates, point_size)

    for axis_key in fixed_axis_points_3d.keys():
        axis_start = fixed_axis_points_3d[(0, 0, 0)][0]
        axis_end = fixed_axis_points_3d[axis_key][0]
        point_size = fixed_axis_points_3d[axis_key][1]

        pygame.draw.line(screen, red, (axis_start[0] + center[0], axis_start[1] + center[1]),
                         (axis_end[0] + center[0], axis_end[1] + center[1]), 2)
        pygame.draw.circle(screen, green, axis_end, 2)

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
            screen_coordinates = (
            int(rotated_point[0] + center[0]) + 400, int(rotated_point[1] + center[1] + 400))

        # Calculate distance from the viewer to the current point
        distance_to_point = calculate_distance(viewer_position, rotated_point)

        # Scale factor based on distance (you can adjust this factor as needed)
        scale_factor = distance_to_center / distance_to_point

        # Apply the scale factor to the point size
        point_size = int(5 * scale_factor)

        c = create_heatmap(point, step_i, 3)
        pygame.draw.circle(screen, c, screen_coordinates, point_size)

    draw_3d_graph() # draw graphs

a=0
b=0
c=0
d=0

addsub="add"

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
            if event.key == pygame.K_RIGHT:
                current_view_index = (current_view_index + 1) % len(views)
                print("Switched to", views[current_view_index])
            elif event.key == pygame.K_LEFT:
                current_view_index = (current_view_index - 1) % len(views)
                print("Switched to", views[current_view_index])
            elif event.key == pygame.K_h:
                if(axis_color):
                    axis_color = False
                    print("info color")
                else:
                    axis_color = True # color based on axis or data
                    print("axis color")
            elif event.key == pygame.K_n:
                print("added new graph")
                add_graph("xy")
                print(graphs)
                update_graph(graphs[0], "deg2", "deg2", "xy", a/max_val, b/max_val, c, d)
            elif event.key == pygame.K_MINUS:
                print("sub mode")
                addsub = "sub"
            elif event.key == pygame.K_EQUALS:
                print("add mode")
                addsub = "add"
            elif event.key == pygame.K_a and addsub == "add":
                print("add 1")
                a=a+0.1
            elif event.key == pygame.K_a and addsub == "sub":
                print("sub 1")
                a=a-0.1

            elif event.key == pygame.K_b and addsub == "add":
                print("add 1")
                b=b+10
            elif event.key == pygame.K_b and addsub == "sub":
                print("sub 1")
                b=b-10

            elif event.key == pygame.K_c and addsub == "add":
                print("add 1")
                c=c+10
            elif event.key == pygame.K_c and addsub == "sub":
                print("sub 1")
                c=c-10

            elif event.key == pygame.K_d and addsub == "add":
                print("add 1")
                d=d+10
            elif event.key == pygame.K_d and addsub == "sub":
                print("sub 1")
                d=d-10

            elif event.key == pygame.K_r:
                print("reset")
                addsub = "none"
                current_view_index = 0
                a=0
                b=0
                c=0
                d=0
                update_graph(graphs[0], "deg2", "deg2", "xy", a/max_val, b/max_val, c, d)

        
        elif event.type == pygame.KEYUP:
            print("updating graph")
            update_graph(graphs[0], "deg2", "deg2", "xy", a/max_val, b/max_val, c, d)


    # Clear the screen
    screen.fill(black)

    # Draw the view button & text
    draw_view_button()
    draw_current_view_text()

    # Rotate the points based on mouse movement
    if rotate_active:
        dx, dy = pygame.mouse.get_rel()
        rotation_angle_y += dx * -0.01  # Horizontal rotation
        rotation_angle_x += dy * -0.01  # Vertical rotation

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
        if(axis_color):
            for point in ori_points_3d:
                c = create_heatmap(point, step_z, 2)
                pygame.draw.circle(screen, c, (point[0]+400, point[1]+400), 5)
        else:
            for point in ori_points_3d:
                c = create_heatmap(point, step_i, 3)
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
        if(axis_color):
            for point in ori_points_3d:
                c = create_heatmap(point, step_x, 0)
                pygame.draw.circle(screen, c, (point[2]+400, point[1]+400), 5)
        else:
            for point in ori_points_3d:
                c = create_heatmap(point, step_i, 3)
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
        if(axis_color):
            for point in ori_points_3d:
                c = create_heatmap(point, step_y, 1)
                pygame.draw.circle(screen, c, (point[0]+400, point[2]+400), 5)
        else:
            for point in ori_points_3d:
                c = create_heatmap(point, step_i, 3)
                pygame.draw.circle(screen, c, (point[0]+400, point[2]+400), 5)
    # Update the display
    pygame.display.flip()
