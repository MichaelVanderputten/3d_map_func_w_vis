import math
import numpy as np

from data import min_x, min_y, min_z, max_x, max_y, max_z
from datainfo import swap_axis

graphs = []
dims = 25

min_val = -300
max_val = abs(min_val)

base_map_xy = np.zeros((dims, dims, 3))

x_values = np.linspace(min_val, max_val, dims)
y_values = np.linspace(min_val, max_val, dims)
z_values = np.linspace(min_val, max_val, dims)

for i in range(dims):
    for j in range(dims):
        base_map_xy[i, j, 0] = x_values[i]  # x coordinate
        base_map_xy[i, j, 1] = 0  # y coordinate
        base_map_xy[i, j, 2] = z_values[j]  # z coordinate

base_map_yx = swap_axis(base_map_xy, 1, 0)


def update_graph(graph, primtype, sectype, axis, ap, bp, cp ,dp, asec, bs, cs ,ds):
    if axis == "xy":
        if primtype == "deg2":
            for row in range(len(graph)):
                for col in range(len(graph[row])):
                    point = graph[row][col]
                    point[1] = deg2(ap, bp, cp, point[0])

        if sectype == "deg2":
            for row in range(len(graph)):
                for col in range(len(graph[row])):
                    point = graph[row][col]
                    point[1] += deg2(asec, bs, cs, point[2])
        
        if primtype == "deg3":
            for row in range(len(graph)):
                for col in range(len(graph[row])):
                    point = graph[row][col]
                    point[1] = deg3(ap, bp, cp, dp, point[0])

        if sectype == "deg3":
            for row in range(len(graph)):
                for col in range(len(graph[row])):
                    point = graph[row][col]
                    point[1] += deg3(asec, bs, cs, ds, point[2])

        if primtype == "lin":
            for row in range(len(graph)):
                for col in range(len(graph[row])):
                    point = graph[row][col]
                    point[1] = lin(ap*10, bp*10, point[0])

        if sectype == "lin":
            for row in range(len(graph)):
                for col in range(len(graph[row])):
                    point = graph[row][col]
                    point[1] += lin(asec*10, bs*10, point[2])


    elif axis == "yx":
        if primtype == "deg2":
            for row in range(len(graph)):
                for col in range(len(graph[row])):
                    point = graph[row][col]
                    point[0] = deg2(ap, bp, cp, point[1])

        if sectype == "deg2":
            for row in range(len(graph)):
                for col in range(len(graph[row])):
                    point = graph[row][col]
                    point[0] += deg2(asec, bs, cs, point[2])

        if primtype == "deg3":
            for row in range(len(graph)):
                for col in range(len(graph[row])):
                    point = graph[row][col]
                    point[0] = deg3(ap, bp, cp, dp, point[1])

        if sectype == "deg3":
            for row in range(len(graph)):
                for col in range(len(graph[row])):
                    point = graph[row][col]
                    point[0] += deg3(asec, bs, cs, ds, point[2])

        if primtype == "lin":
            for row in range(len(graph)):
                for col in range(len(graph[row])):
                    point = graph[row][col]
                    point[0] = lin(ap*10, bp*10, point[1])

        if sectype == "lin":
            for row in range(len(graph)):
                for col in range(len(graph[row])):
                    point = graph[row][col]
                    point[0] += lin(asec*10, bs*10, point[2])




def add_graph(axis):
    if axis == "yx":
        graphs.append(np.copy(base_map_yx))
    else:
        graphs.append(np.copy(base_map_xy))

def deg2(a,b,c, x):
    return a*x**2 + b*x + c

def deg3(a,b,c,d,x):
    return a*x**3 + b*x**2 + c*x + d

def lin(m, b, x):
    return m*x + b

def sinf(a,b,x,c,d):
    return a*math.sin(b*(x-c)) + d

def cosf(a,b,x,c,d):
    return a*math.cos(b*(x-c)) + d