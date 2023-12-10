import math
import numpy as np

graphs = []
dims = 10

base_map = np.zeros((dims, dims, 3))
for i in range(dims):
    for j in range(dims):
        base_map[i, j, 0] = i  # x coordinate
        base_map[i, j, 1] = 0  # y coordinate
        base_map[i, j, 2] = j  # z coordinate

print(base_map)

def add_graph():
    graphs.append(np.copy(base_map))

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