import math
import numpy as np

from data import min_x, min_y, min_z, max_x, max_y, max_z

graphs = []
dims = 25

min_val = -300
max_val = abs(min_val)

base_map_xy = np.zeros((dims, dims, 3))
base_map_yx = np.zeros((dims, dims, 3))
x_values = np.linspace(min_val, max_val, dims)
y_values = np.linspace(min_val, max_val, dims)
z_values = np.linspace(min_val, max_val, dims)

for i in range(dims):
    for j in range(dims):
        base_map_xy[i, j, 0] = x_values[i]  # x coordinate
        base_map_xy[i, j, 1] = 0  # y coordinate
        base_map_xy[i, j, 2] = z_values[j]  # z coordinate

for i in range(dims):
    for j in range(dims):
        base_map_yx[i, j, 0] = x_values[i]  # x coordinate
        base_map_yx[i, j, 1] = y_values[j]  # y coordinate
        base_map_yx[i, j, 2] = 0  # z coordinate


def update_graph(graph, primtype, sectype, axis, a, b, c ,d):
    if axis == "xy":
        if primtype == "deg2":
            for row in range(len(graph)):
                for col in range(len(graph[row])):
                    point = graph[row][col]
                    point[1] = deg2(a, b, c, point[0])

        if sectype == "deg2":
            for row in range(len(graph)):
                for col in range(len(graph[row])):
                    point = graph[row][col]
                    point[1] += deg2(a, b, c, point[2])
    elif axis == "yx":
        if primtype == "deg2":
            for row in range(len(graph)):
                for col in range(len(graph[row])):
                    point = graph[row][col]
                    point[0] = deg2(a, b, c, point[1])

        if sectype == "deg2":
            for row in range(len(graph)):
                for col in range(len(graph[row])):
                    point = graph[row][col]
                    point[0] += deg2(a, b, c, point[2])




def add_graph(axis):
    if axis == "yx":
        graphs.append(np.copy(base_map_yx))
    else:
        graphs.append(np.copy(base_map_xy))

def deg2(a,b,c, x):
    return a*x**2 + b*x + c

def deg3(a,b,c,d,x):
    return a*x**3 + b*x**2 + c*x + d

def lin(m,x,b):
    return m*x + b

def sinf(a,b,x,c,d):
    return a*math.sin(b*(x-c)) + d

def cosf(a,b,x,c,d):
    return a*math.cos(b*(x-c)) + d