from datainfo import *

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
    (-101,100,178, 1),
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

ori_points_3d = [
    (-101,100,178, 1),
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

max_z = find_max_value(ori_points_3d[:3], 2)
min_z = find_min_value(ori_points_3d[:3], 2)
max_y = find_max_value(ori_points_3d[:3], 1)
min_y = find_min_value(ori_points_3d[:3], 1)
max_x = find_max_value(ori_points_3d[:3], 0)
min_x = find_min_value(ori_points_3d[:3], 0)

max_i = find_max_value(ori_points_3d[:3], 3)
min_i = find_min_value(ori_points_3d[:3], 3)
step_i = 255/(max_i + abs(min_i))
print(max_i, min_i)
print(step_i)

step_x = 255/(max_x + abs(min_x))
step_y = 255/(max_y + abs(min_y))
step_z = 255/(max_z + abs(min_z)) # global data info. change later