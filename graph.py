import math
import numpy as np

from data import min_x, min_y, min_z, max_x, max_y, max_z
from datainfo import swap_axis

graphs = []

class GRAPH:
    def __init__(self):
        self.dims = 50
        self.min_val = -400 # change later
        self.max_val = abs(self.min_val)

        self.base_map_xy = np.zeros((self.dims, self.dims, 3))

        self.x_values = np.linspace(self.min_val, self.max_val, self.dims)
        self.y_values = np.linspace(self.min_val, self.max_val, self.dims)
        self.z_values = np.linspace(self.min_val, self.max_val, self.dims)

        self.init_grid()
        self.base_map_yx = swap_axis(self.base_map_xy, 1, 0)

    def init_grid(self):
        for i in range(self.dims):
            for j in range(self.dims):
                self.base_map_xy[i, j, 0] = self.x_values[i]  # x coordinate
                self.base_map_xy[i, j, 1] = 0  # y coordinate
                self.base_map_xy[i, j, 2] = self.z_values[j]  # z coordinate


    def update_graph(self, graph, primtype, sectype, axis, ap, bp, cp ,dp, asec, bs, cs ,ds):
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

            if primtype == "sinf":
                for row in range(len(graph)):
                    for col in range(len(graph[row])):
                        point = graph[row][col]
                        point[1] = sinf(ap*100, bp*100, point[0], cp*10, dp*10)

            if sectype == "sinf":
                for row in range(len(graph)):
                    for col in range(len(graph[row])):
                        point = graph[row][col]
                        point[1] += sinf(asec*100, bs*100, point[2], cs*10, ds*10)

            if primtype == "cosf":
                for row in range(len(graph)):
                    for col in range(len(graph[row])):
                        point = graph[row][col]
                        point[1] = cosf(ap*100, bp*100, point[0], cp*10, dp*10)

            if sectype == "cosf":
                for row in range(len(graph)):
                    for col in range(len(graph[row])):
                        point = graph[row][col]
                        point[1] += cosf(asec*100, bs*100, point[2], cs*10, ds*10)

            if primtype == "tanf":
                for row in range(len(graph)):
                    for col in range(len(graph[row])):
                        point = graph[row][col]
                        point[1] = tanf(ap*100, bp*100, point[0], cp*10, dp*10)

            if sectype == "tanf":
                for row in range(len(graph)):
                    for col in range(len(graph[row])):
                        point = graph[row][col]
                        point[1] += tanf(asec*100, bs*100, point[2], cs*10, ds*10)


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

            if primtype == "sinf":
                for row in range(len(graph)):
                    for col in range(len(graph[row])):
                        point = graph[row][col]
                        point[0] = sinf(ap*10, bp*10, point[1], cp*10, dp*10)

            if sectype == "sinf":
                for row in range(len(graph)):
                    for col in range(len(graph[row])):
                        point = graph[row][col]
                        point[0] += sinf(asec*10, bs*10, point[2], cs*10, ds*10)

    def graph_sec(self, point, sectype, asec, bs, cs ,ds):
        if sectype == "deg2":
            return(point[0] + deg2(asec, bs, cs, point[2]))
        if sectype == "deg3":
            return(point[0] + deg3(asec, bs, cs, ds, point[2]))
        if sectype == "lin":
            return(point[0] + lin(asec*10, bs*10, point[2]))
        if sectype == "sinf":
            return(point[0] + sinf(asec*10, bs*10, point[2], cs*10, ds*10))

    def add_graph(self, axis):
        if axis == "yx":
            graphs.append(np.copy(self.base_map_yx))
        else:
            graphs.append(np.copy(self.base_map_xy))

def deg2(a,b,c, x):
    return a*x**2 + b*x + c

def deg3(a,b,c,d,x):
    return a*x**3 + b*x**2 + c*x + d

def lin(m, b, x):
    return m*x + b

def sinf(a,b,x,c,d):
    return (a*math.sin(b*(x*math.pi-c)))*100 + d

def cosf(a,b,x,c,d):
    return (a*math.cos(b*(x*math.pi-c)))*100 + d

def tanf(a,b,x,c,d):
    return (a*math.tan(b*(x*math.pi-c)))*100 + d

def asinf(a,b,x,c,d):
    return (a*math.asin(b*(x*math.pi-c)))*100 + d

def acosf(a,b,x,c,d):
    return (a*math.acos(b*(x*math.pi-c)))*100 + d

def atanf(a,b,x,c,d):
    return (a*math.atan(b*(x*math.pi-c)))*100 + d