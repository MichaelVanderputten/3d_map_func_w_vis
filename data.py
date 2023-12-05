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
    (-101,100,178),
    (125,-234,156),
    (203,200,-267),
    (-10,-395,98),
    (163,178,-13),
    (115,-64,362),
    (109,291,-168),
    (-285,-32,232),
    (87,278,-187),
    (-38,108,-90),
    (308,-150,120),
] # test points

ori_points_3d = [
    (-101,100,178),
    (125,-234,156),
    (203,200,-267),
    (-10,-395,98),
    (163,178,-13),
    (115,-64,362),
    (109,291,-168),
    (-285,-32,232),
    (87,278,-187),
    (-38,108,-90),
    (308,-150,120),
] # test points

max_z = find_max_value(ori_points_3d, 2)
min_z = find_min_value(ori_points_3d, 2)
max_y = find_max_value(ori_points_3d, 1)
min_y = find_min_value(ori_points_3d, 1)
max_x = find_max_value(ori_points_3d, 0)
min_x = find_min_value(ori_points_3d, 0)

step_x = (max_x + abs(min_x))/255
step_y = (max_y + abs(min_y))/255
step_z = (max_z + abs(min_z))/255 # global data info. change later