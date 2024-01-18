from datainfo import *
import numpy as np

# Initialize 3D points
axis_points_3d = [
    (0, 100, 0),
    (0, -100, 0),
    (100, 0, 0),
    (-100, 0, 0),
    (0, 0, 100),
    (0, 0, -100),
    (0, 0, 0),
] # axis points

points_3d = [
    (125,-234,156, 2),
    (203,200,-267, 3),
    (-10,-395,98, 1),
    (163,178,-13, 2),
    (115,-64,362, 2),
    (109,291,-168, 2),
    (-285,-32,232, 1),
    (87,278,-187, 2),
    (-38,108,-90, 1),
    (308,-150,120, 3),
] # test points

point_relations_3d = [0] * len(points_3d)

x_values_base_map = np.zeros((len(points_3d), 1, 4))

higher = points_3d
lower = points_3d # higher and lower points

ori_points_3d = points_3d # save unrotated

max_z = find_max_value(ori_points_3d[:3], 2)
min_z = find_min_value(ori_points_3d[:3], 2)
max_y = find_max_value(ori_points_3d[:3], 1)
min_y = find_min_value(ori_points_3d[:3], 1)
max_x = find_max_value(ori_points_3d[:3], 0)
min_x = find_min_value(ori_points_3d[:3], 0)

max_i = find_max_value(ori_points_3d[:3], 3)
min_i = find_min_value(ori_points_3d[:3], 3)
try:
    step_i = 255/(max_i + abs(min_i))
except:
    step_i = 255

try:
    step_x = 255/(max_x + abs(min_x))
except:
    stpe_x = 255

try:
    step_y = 255/(max_y + abs(min_y))
except:
    step_y = 255

try:
    step_z = 255/(max_z + abs(min_z))
except:
    step_z = 255 # global data info. change later

abs_z = min_z
if(max_z > min_z):
    abs_z = max_z