import pygame
import sys
import math

from datainfo import *
from data import *

from graph import *

class APP:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up the window
        self.window_size = (800, 800)
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Pygame 3D App")

        # Set up colors
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)

        # Set up fonts
        self.font = pygame.font.Font(None, 36)

        # Initialize rotation variables
        self.rotation_angle_x = 0
        self.rotation_angle_y = 0
        self.rotate_active = False
        self.rotation_start_time = 0

        self.viewer_position = (0, 0, -3*abs_z)
        
        self.graphprim = ["lin", "deg2", "deg3", "sinf", "cosf", "tanf"]
        self.graphprim_index = 0
        self.graphsec = ["lin", "deg2", "deg3", "sinf", "cosf", "tanf"]
        self.graphsec_index = 0

        self.xy_yx = "yx"
        self.prim_sec = "prim"
        self.primary = self.graphprim[self.graphprim_index]
        self.secondary = self.graphsec[self.graphsec_index]

        self.ap=0
        self.bp=0
        self.cp=0
        self.dp=0
        self.asec=0
        self.bs=0
        self.cs=0
        self.ds=0 # adjustment vars

        self.apmod = 0.1
        self.bpmod = 10
        self.cpmod = 10
        self.dpmod = 10

        self.asecmod = 0.1
        self.bsmod = 10
        self.csmod = 10
        self.dsmod = 10# scale adjustment vars

        self.addsub="add"

        # Initialize view variables
        self.views = ["3D", "2D-XY", "2D-ZY", "2D-XZ"]
        self.current_view_index = 0
        self.swap_from_3d = 0
        self.axis_color = False

    # Draw view button
    def draw_view_button(self):
        button_text = self.font.render("View: " + self.views[self.current_view_index], True, self.white)
        button_rect = button_text.get_rect(topleft=(self.window_size[0] - 150, 20))
        pygame.draw.rect(self.screen, self.black, button_rect)
        self.screen.blit(button_text, button_rect)

    # Print view index
    def draw_current_view_text(self):
        text = self.font.render("Current View: " + self.views[self.current_view_index], True, self.white)
        self.screen.blit(text, (10, self.window_size[1] - 50))

    def calculate_distance(self, point1, point2):
        return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2)

    # Rotate points in 3D
    def rotate_3d(self, x, y, z, info, center, angles):
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

    def draw_3d_graph(self):
        center = (0, 0, 0)
        #distance_to_center = self.calculate_distance(center, self.viewer_position)
        for graph in graphs:
            for row in range(len(graph) - 1):  # subtract 1 to avoid index out of range
                for col in range(len(graph[row]) - 1):  # subtract 1 to avoid index out of range
                    # Get points from current and next row
                    point1 = graph[row][col]
                    point2 = graph[row+1][col]
                    point3 = graph[row+1][col+1]
                    point4 = graph[row][col+1]

                    # Apply rotation to each 3D point
                    rotated_point1 = self.rotate_3d(point1[0], point1[1], point1[2], -1, center, (self.rotation_angle_x, self.rotation_angle_y, 0))
                    rotated_point2 = self.rotate_3d(point2[0], point2[1], point2[2], -1, center, (self.rotation_angle_x, self.rotation_angle_y, 0))
                    rotated_point3 = self.rotate_3d(point3[0], point3[1], point3[2], -1, center, (self.rotation_angle_x, self.rotation_angle_y, 0))
                    rotated_point4 = self.rotate_3d(point4[0], point4[1], point4[2], -1, center, (self.rotation_angle_x, self.rotation_angle_y, 0))

                    # Calculate screen coordinates
                    screen_coordinates1 = (int(rotated_point1[0] + center[0]) + 400, int(rotated_point1[1] + center[1] + 400))
                    screen_coordinates2 = (int(rotated_point2[0] + center[0]) + 400, int(rotated_point2[1] + center[1] + 400))
                    screen_coordinates3 = (int(rotated_point3[0] + center[0]) + 400, int(rotated_point3[1] + center[1] + 400))
                    screen_coordinates4 = (int(rotated_point4[0] + center[0]) + 400, int(rotated_point4[1] + center[1] + 400))

                    # Draw the rotated and scaled points
                    pygame.draw.polygon(self.screen, self.blue, (screen_coordinates1, screen_coordinates2, screen_coordinates3, screen_coordinates4), 2)

    # Draw 3D scene
    def draw_3d_scene(self):
        center = (0, 0, 0)

        # Calculate the distance from the viewer's perspective to the center of the scene
        distance_to_center = self.calculate_distance(center, self.viewer_position)

        # Draw the X, Y, and Z axes in the 3D view
        fixed_axis_points_3d = {}
        for point in axis_points_3d:
            rotated_point = self.rotate_3d(point[0], point[1], point[2], -1, center, (self.rotation_angle_x, self.rotation_angle_y, 0))
            screen_coordinates = (int(rotated_point[0] + center[0]) + 400, int(rotated_point[1] + center[1] + 400))

            # Calculate distance from the viewer to the current point
            distance_to_point = self.calculate_distance(self.viewer_position, rotated_point)

            # Scale factor based on distance (you can adjust this factor as needed)
            scale_factor = distance_to_center / distance_to_point

            # Apply the scale factor to the point size
            point_size = int(5 * scale_factor)

            fixed_axis_points_3d[point] = (screen_coordinates, point_size)

        for axis_key in fixed_axis_points_3d.keys():
            axis_start = fixed_axis_points_3d[(0, 0, 0)][0]
            axis_end = fixed_axis_points_3d[axis_key][0]
            point_size = fixed_axis_points_3d[axis_key][1]

            pygame.draw.line(self.screen, self.red, (axis_start[0] + center[0], axis_start[1] + center[1]),
                            (axis_end[0] + center[0], axis_end[1] + center[1]), 2)
            pygame.draw.circle(self.screen, self.green, axis_end, 2)

        # Draw 3D points projected onto 2D plane based on the current view
        for i, point in enumerate(points_3d):
            rotated_point = self.rotate_3d(*point, center, (self.rotation_angle_x, self.rotation_angle_y, 0))

            if self.views[self.current_view_index] == "2D-XY":
                screen_coordinates = (int(rotated_point[0]), int(rotated_point[1]))
            elif self.views[self.current_view_index] == "2D-ZY":
                screen_coordinates = (int(rotated_point[2]), int(rotated_point[1]))
            elif self.views[self.current_view_index] == "2D-XZ":
                screen_coordinates = (int(rotated_point[0]), int(rotated_point[2]))
            else:
                screen_coordinates = (
                int(rotated_point[0] + center[0]) + 400, int(rotated_point[1] + center[1] + 400))

            # Calculate distance from the viewer to the current point
            distance_to_point = self.calculate_distance(self.viewer_position, rotated_point)

            # Scale factor based on distance (you can adjust this factor as needed)
            scale_factor = distance_to_center / distance_to_point

            # Apply the scale factor to the point size
            point_size = int(5 * scale_factor)

            if self.axis_color:
                c = create_heatmap(point, step_i, 3)
            else:
                c = create_heatmap(point, point_relations_3d[i], 4)

            pygame.draw.circle(self.screen, c, screen_coordinates, point_size)

        self.draw_3d_graph() # draw graphs

    def adjust_mods(self):
        if self.primary == "lin":
            self.apmod = 1
            self.bpmod = 10

        elif self.primary == "deg2":
            self.apmod = 0.1
            self.bpmod = 1
            self.cpmod = 10
        
        elif self.primary == "deg3":
            self.apmod = 0.001
            self.bpmod = 0.1
            self.cpmod = 0.1
            self.dpmod = 10

        elif self.primary == "sinf":
            self.apmod = 0.1
            self.bpmod = 1
            self.cpmod = 1
            self.dpmod = 1
        
        elif self.primary == "cosf":
            self.apmod = 0.1
            self.bpmod = 1
            self.cpmod = 1
            self.dpmod = 1
        
        elif self.primary == "tanf":
            self.apmod = 0.1
            self.bpmod = 1
            self.cpmod = 1
            self.dpmod = 1

        if self.secondary == "lin":
            self.asecmod = 1
            self.bsmod = 50

        elif self.secondary == "deg2":
            self.asecmod = 0.1
            self.bsmod = 1
            self.csmod = 10

        elif self.secondary == "deg3":
            self.asecmod = 0.01
            self.bsmod = 0.1
            self.csmod = 1
            self.dpmod = 10

        elif self.secondary == "sinf":
            self.asecmod = 0.1
            self.bsmod = 1
            self.csmod = 1
            self.dsmod = 1

        elif self.secondary == "cosf":
            self.asecmod = 0.1
            self.bsmod = 1
            self.csmod = 1
            self.dsmod = 1

        elif self.secondary == "tanf":
            self.asecmod = 0.1
            self.bsmod = 1
            self.csmod = 1
            self.dsmod = 1

    def populate_x(self):
        for i, point in enumerate(points_3d):
            x_values_base_map[i] = np.array([[point[0], 0, 0, 0]])

    def higher_lower(self):
        #graph.update_graph(x_values_base_map, self.primary, self.secondary, self.xy_yx, self.ap/graph.max_val, self.bp/graph.max_val, -self.cp, self.dp, self.asec/graph.max_val, self.bs/graph.max_val, -self.cs, self.ds)
        if self.primary == "deg2" and self.xy_yx == "yx":
            for i, point in enumerate(points_3d):
                try:
                    initial_y = math.pi*(-(math.sqrt((self.ap/graph.max_val) * point[0] - (self.ap/graph.max_val) * (-self.cp) + 0.25 * ((self.bp/graph.max_val)**2)) + 0.5 * (self.bp/graph.max_val))) / (self.ap/graph.max_val)
                    point_top = (graph.graph_sec((point[0], point[1], point[2]), self.secondary, self.asec/graph.max_val, self.bs/graph.max_val, -self.cs, self.ds), initial_y, point[2], point[3])
                    offset = point[0] - point_top[0]
                    new_y = math.pi*(-(math.sqrt((self.ap/graph.max_val) * (point[0]+offset) - (self.ap/graph.max_val) * (-self.cp) + 0.25 * ((self.bp/graph.max_val)**2)) + 0.5 * (self.bp/graph.max_val))) / (self.ap/graph.max_val)
                    point_top = (point[0], new_y, point[2], point[3]) # offset x value to calulate y correctly

                    initial_y = math.pi*(math.sqrt((self.ap/graph.max_val) * point[0] - (self.ap/graph.max_val) * (-self.cp) + 0.25 * ((self.bp/graph.max_val)**2)) - 0.5 * (self.bp/graph.max_val)) / (self.ap/graph.max_val)
                    point_bottom = (graph.graph_sec((point[0], point[1], point[2]), self.secondary, self.asec/graph.max_val, self.bs/graph.max_val, -self.cs, self.ds), initial_y, point[2], point[3])
                    offset = point[0] - point_bottom[0]
                    new_y = math.pi*(math.sqrt((self.ap/graph.max_val) * (point[0] + offset) - (self.ap/graph.max_val) * (-self.cp) + 0.25 * ((self.bp/graph.max_val)**2)) - 0.5 * (self.bp/graph.max_val)) / (self.ap/graph.max_val)
                    point_bottom = (point[0], new_y, point[2], point[3])
                    
                    if (point[1] > point_bottom[1]):
                        # under bottom
                        point_relations_3d[i] = 1
                    elif (point[1] < point_top[1]):
                        # above top
                        point_relations_3d[i] = 3
                    elif (point[1] > point_top[1]):
                        #under top
                        point_relations_3d[i] = 2
                    else:
                        point_relations_3d[i] = -1

                    #point points along graph
                    rotated_pointa = self.rotate_3d(point_top[0], point_top[1], point_top[2], -1, (0,0,0), (self.rotation_angle_x, self.rotation_angle_y, 0))
                    screen_coordinatesa = (int(rotated_pointa[0]) + 400, int(rotated_pointa[1] + 400))
                    pygame.draw.circle(self.screen, (255,255,255), screen_coordinatesa, 5)
                    rotated_pointb = self.rotate_3d(point_bottom[0], point_bottom[1], point_bottom[2], -1, (0,0,0), (self.rotation_angle_x, self.rotation_angle_y, 0))
                    screen_coordinatesb = (int(rotated_pointb[0]) + 400, int(rotated_pointb[1] + 400))
                    pygame.draw.circle(self.screen, (255,255,255), screen_coordinatesb, 5)

                except Exception as e:
                    # point outside domain
                    #print(e)
                    point_relations_3d[i] = -1

            #print("pr3d: ", point_relations_3d)


    # Main game loop
    def run(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button clicked
                        if(self.current_view_index != 0):
                            self.swap_from_3d = self.current_view_index
                            self.current_view_index = 0 # set 3d
                        self.rotate_active = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:  # Left mouse button released
                            self.rotate_active = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.current_view_index = (self.current_view_index + 1) % len(self.views)
                        print("Switched to", self.views[self.current_view_index])
                    elif event.key == pygame.K_LEFT:
                        self.current_view_index = (self.current_view_index - 1) % len(self.views)
                        print("Switched to", self.views[self.current_view_index])
                    elif event.key == pygame.K_h:
                        if(self.axis_color):
                            self.axis_color = False
                            print("info color")
                        else:
                            self.axis_color = True # color based on axis or data
                            print("axis color")
                    elif event.key == pygame.K_n:
                        print("added new graph")
                        graph.add_graph(self.xy_yx)
                        #print("working update graph", graphs[0], self.primary, self.secondary, self.xy_yx, self.ap/graph.max_val, self.bp/graph.max_val, -self.cp, self.dp, self.asec/graph.max_val, self.bs/graph.max_val, -self.cs, self.ds)
                        graph.update_graph(graphs[0], self.primary, self.secondary, self.xy_yx, self.ap/graph.max_val, self.bp/graph.max_val, -self.cp, self.dp, self.asec/graph.max_val, self.bs/graph.max_val, -self.cs, self.ds)
                    elif event.key == pygame.K_MINUS:
                        print("sub mode")
                        self.addsub = "sub"
                    elif event.key == pygame.K_EQUALS:
                        print("add mode")
                        self.addsub = "add"
                    elif event.key == pygame.K_x:
                        if self.xy_yx == "xy":
                            self.xy_yx = "yx"
                        else:
                            self.xy_yx = "xy" # swap axis
                        swap_axis(graphs[0], 1, 0)

                    elif event.key == pygame.K_p:
                        self.prim_sec = "prim"
                    elif event.key == pygame.K_s:
                        self.prim_sec = "sec"

                    elif event.key == pygame.K_a and self.addsub == "add":
                        if self.prim_sec == "prim":
                            self.ap = self.ap+1
                        else:
                            self.asec = self.asec+1
                    elif event.key == pygame.K_a and self.addsub == "sub":
                        if self.prim_sec == "prim":
                            self.ap = self.ap-1
                        else:
                            self.asec = self.asec-1 # adjust a value based on mods

                    elif event.key == pygame.K_b and self.addsub == "add":
                        if self.prim_sec == "prim":
                            self.bp = self.bp+1
                        else:
                            self.bs = self.bs+1
                    elif event.key == pygame.K_b and self.addsub == "sub":
                        if self.prim_sec == "prim":
                            self.bp = self.bp-1
                        else:
                            self.bs = self.bs-1 # adjust b value based on mods

                    elif event.key == pygame.K_c and self.addsub == "add":
                        if self.prim_sec == "prim":
                            self.cp = self.cp+1
                        else:
                            self.cs = self.cs+1
                    elif event.key == pygame.K_c and self.addsub == "sub":
                        if self.prim_sec == "prim":
                            self.cp = self.cp-1
                        else:
                            self.cs = self.cs-1 # adjust c value based on mods

                    elif event.key == pygame.K_d and self.addsub == "add":
                        if self.prim_sec == "prim":
                            self.dp = self.dp+1
                        else:
                            self.ds = self.ds+1
                    elif event.key == pygame.K_d and self.addsub == "sub":
                        if self.prim_sec == "prim":
                            self.dp = self.dp-1
                        else:
                            self.ds = self.ds-1 # adjust d value based on mods
                    elif event.key == pygame.K_g and self.prim_sec == "prim":
                        self.graphprim_index = (self.graphprim_index + 1) % len(self.graphprim)
                        self.primary = self.graphprim[self.graphprim_index]
                        print("Switched to", self.graphprim[self.graphprim_index])
                    elif event.key == pygame.K_g and self.prim_sec == "sec":
                        self.graphsec_index = (self.graphsec_index + 1) % len(self.graphsec)
                        self.secondary = self.graphsec[self.graphsec_index]
                        print("Switched to", self.graphsec[self.graphsec_index])

                    elif event.key == pygame.K_r:
                        print("reset")
                        self.addsub = "none"
                        self.current_view_index = 0
                        self.graphsec_index = 0
                        self.graphprim_index = 0
                        self.ap=0
                        self.bp=0
                        self.cp=0
                        self.dp=0
                        self.asec=0
                        self.bs=0
                        self.cs=0
                        self.ds=0
                        graph.update_graph(
                            graphs[0], 
                            self.primary, 
                            self.secondary, 
                            self.xy_yx, 
                            self.ap/graph.max_val*self.apmod, 
                            self.bp/graph.max_val*self.bpmod, 
                            -self.cp*self.cpmod, 
                            self.dp*self.dpmod, 
                            self.asec/graph.max_val*self.asecmod,
                            self.bs/graph.max_val*self.bsmod, 
                            -self.cs*self.csmod, 
                            self.ds*self.dsmod
                        )
                
                elif event.type == pygame.KEYUP:
                    print("updating graph")
                    self.adjust_mods()
                    print(self.primary,",",self.secondary,",",self.prim_sec)
                    print(self.ap,",",self.bp,",",self.cp,",",self.dp)
                    print(self.apmod,",",self.bpmod,",",self.cpmod,",",self.dpmod)
                    print(self.asec,",",self.bs,",",self.cs,",",self.ds)
                    print(self.asecmod,",",self.bsmod,",",self.csmod,",",self.dsmod)
                    try:
                        graph.update_graph(
                            graphs[0], 
                            self.primary, 
                            self.secondary, 
                            self.xy_yx, 
                            self.ap/graph.max_val*self.apmod, 
                            self.bp/graph.max_val*self.bpmod, 
                            -self.cp*self.cpmod, 
                            self.dp*self.dpmod, 
                            self.asec/graph.max_val*self.asecmod, 
                            self.bs/graph.max_val*self.bsmod, 
                            -self.cs*self.csmod, 
                            self.ds*self.dsmod
                            )
                    except:
                        pass


            # Clear the screen
            self.screen.fill(self.black)

            # Draw the view button & text
            self.draw_view_button()
            self.draw_current_view_text()

            # Check if point is above graph
            if graphs:
                self.populate_x()
                self.higher_lower()

            # Rotate the points based on mouse movement
            if self.rotate_active:
                self.dx, self.dy = pygame.mouse.get_rel()
                self.rotation_angle_y += self.dx * -0.01  # Horizontal rotation
                self.rotation_angle_x += self.dy * -0.01  # Vertical rotation

                if(self.swap_from_3d == 1):
                    self.swap_from_3d = 0
                    self.rotation_angle_x = 0
                    self.rotation_angle_y = 0
                elif(self.swap_from_3d == 2):
                    self.swap_from_3d = 0
                    self.rotation_angle_x = 0
                    self.rotation_angle_y = 1.575
                elif(self.swap_from_3d == 3):
                    self.swap_from_3d = 0
                    self.rotation_angle_x = -1.575
                    self.rotation_angle_y = 0


            # Draw the appropriate axes and points based on the current view
            if self.views[self.current_view_index] == "3D":
                # Draw 3D points
                self.draw_3d_scene()

            elif self.views[self.current_view_index] == "2D-XY":
                # Draw x and Y axes
                pygame.draw.line(self.screen, self.white, (self.window_size[0]//2, self.window_size[1]//10), (self.window_size[0]//2, self.window_size[1]-(self.window_size[1]//10)), 2) # Y
                pygame.draw.line(self.screen, self.white, (self.window_size[0]//10, self.window_size[1]//2), (self.window_size[0]-(self.window_size[0]//10), self.window_size[1]//2), 2) # X
                # Label axes
                z_label = self.font.render("Y-axis", True, self.white)
                y_label = self.font.render("X-axis", True, self.white)
                self.screen.blit(z_label, (self.window_size[0]//2, self.window_size[1]//10))
                self.screen.blit(y_label, (self.window_size[0]//10, self.window_size[1]//2))

                #draw points using z and y
                if(self.axis_color):
                    for point in ori_points_3d:
                        c = create_heatmap(point, step_z, 2)
                        pygame.draw.circle(self.screen, c, (point[0]+400, point[1]+400), 5)
                else:
                    for point in ori_points_3d:
                        c = create_heatmap(point, step_i, 3)
                        pygame.draw.circle(self.screen, c, (point[0]+400, point[1]+400), 5)

            elif self.views[self.current_view_index] == "2D-ZY":
                # Draw z and Y axes
                pygame.draw.line(self.screen, self.white, (self.window_size[0]//2, self.window_size[1]//10), (self.window_size[0]//2, self.window_size[1]-(self.window_size[1]//10)), 2) # Y
                pygame.draw.line(self.screen, self.white, (self.window_size[0]//10, self.window_size[1]//2), (self.window_size[0]-(self.window_size[0]//10), self.window_size[1]//2), 2) # Z
                # Label axes
                z_label = self.font.render("Y-axis", True, self.white)
                y_label = self.font.render("Z-axis", True, self.white)
                self.screen.blit(z_label, (self.window_size[0]//2, self.window_size[1]//10))
                self.screen.blit(y_label, (self.window_size[0]//10, self.window_size[1]//2))

                #draw points using z and y
                if(self.axis_color):
                    for point in ori_points_3d:
                        c = create_heatmap(point, step_x, 0)
                        pygame.draw.circle(self.screen, c, (point[2]+400, point[1]+400), 5)
                else:
                    for point in ori_points_3d:
                        c = create_heatmap(point, step_i, 3)
                        pygame.draw.circle(self.screen, c, (point[2]+400, point[1]+400), 5)
            elif self.views[self.current_view_index] == "2D-XZ":
                # Draw x and z axes
                pygame.draw.line(self.screen, self.white, (self.window_size[0]//2, self.window_size[1]//10), (self.window_size[0]//2, self.window_size[1]-(self.window_size[1]//10)), 2) # z
                pygame.draw.line(self.screen, self.white, (self.window_size[0]//10, self.window_size[1]//2), (self.window_size[0]-(self.window_size[0]//10), self.window_size[1]//2), 2) # x
                # Label axes
                z_label = self.font.render("Z-axis", True, self.white)
                y_label = self.font.render("X-axis", True, self.white)
                self.screen.blit(z_label, (self.window_size[0]//2, self.window_size[1]//10))
                self.screen.blit(y_label, (self.window_size[0]//10, self.window_size[1]//2))

                #draw points using z and y
                if(self.axis_color):
                    for point in ori_points_3d:
                        c = create_heatmap(point, step_y, 1)
                        pygame.draw.circle(self.screen, c, (point[0]+400, point[2]+400), 5)
                else:
                    for point in ori_points_3d:
                        c = create_heatmap(point, step_i, 3)
                        pygame.draw.circle(self.screen, c, (point[0]+400, point[2]+400), 5)
            # Update the display
            pygame.display.flip()

if __name__ == "__main__":
    app = APP()
    graph = GRAPH()
    app.run()