## Author: Dang Duong-

from turtle import Vec2D
from typing import List
from defer import inline_callbacks
import matplotlib
from plyfile import PlyData, PlyElement
import math
from mpl_toolkits import mplot3d
import numpy as np 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


with open('testmesh.ply','rb') as f:
    plydata = PlyData.read(f)

data_length = plydata.elements[0].count

X_COORDINATE = 0
Y_COORDINATE = 1
Z_COORDINATE = 2
VERTICES_LIST = []

for i in range(data_length):
    VERTICES_LIST.append([plydata.elements[0].data[i][0],plydata.elements[0].data[i][1],plydata.elements[0].data[i][2],plydata.elements[0].data[i][3]])
X_coord = []
Y_coord = []
Z_coord = []

for j in range(data_length):
    X_coord.append(VERTICES_LIST[j][X_COORDINATE])
for k in range(data_length):
    Y_coord.append(VERTICES_LIST[k][Y_COORDINATE])
for g in range(data_length):
    Z_coord.append(VERTICES_LIST[g][Z_COORDINATE])
min_X = min(X_coord)
min_Y = min(Y_coord)
min_Z = min(Z_coord)
min_num = min(min_X, min_Y, min_Z)
for vertice in VERTICES_LIST:
    vertice[X_COORDINATE] += abs(min_num)
    vertice[Y_COORDINATE] += abs(min_num)
    vertice[Z_COORDINATE] += abs(min_num)

## Process to find the selected cubes
## Since the dimension of each cube is 2 x 2 x 2, therefore if a point have odd coordinate, 
## we can find the largest coordinate of the cube which that point stay inside by adding 1 
## to it. And if the point have even coordinate then we add 2. After having the maximum 
## x,y,z coordinates, we will be able to find all other coordinates. 
CUBE_SIZE = 1; 

## Format of a cube 
## POINT = (X, Y, Z)
## cube = [POINT_1, POINT_2, POINT_3, POINT_4, POINT_5, POINT_6, POINT_7, POINT_8] 
cube_list = []
for vertice in VERTICES_LIST:
    # if [math.floor(vertice[X_COORDINATE]) + 0.5, math.floor(vertice[Y_COORDINATE]) +0.5, math.floor(vertice[Z_COORDINATE])+0.5] not in cube_list:
    cube_list.append([math.floor(vertice[X_COORDINATE]) + 0.5, math.floor(vertice[Y_COORDINATE]) +0.5, math.floor(vertice[Z_COORDINATE])+0.5])


# cube_list.append([cube_list[0][0] +1, cube_list[0][1],cube_list[0][2]])

cube_list[1] = [cube_list[0][0], cube_list[0][1]+1,cube_list[0][2]]
cube_list[2] = [cube_list[0][0], cube_list[0][1],cube_list[0][2]+1]
cube_list[3] = [cube_list[0][0],cube_list[0][1]+1,cube_list[0][2]+1]

print(cube_list)

points_lookup_table = {
    0:[0,0,0],
    1:[0,1,0],
    2:[1,1,0],
    3:[1,0,0],
    4:[0,0,1],
    5:[0,1,1],
    6:[1,1,1],
    7:[1,0,1]
}

## return a set of points in a cube
def get_set_of_points_of_cube(point):
    set_of_points = []
    for i in range(8):
        set_of_points.append([point[0]+points_lookup_table[i][0],point[1]+points_lookup_table[i][1],point[2]+points_lookup_table[i][2]])
    return set_of_points

## return which point of a cube is inside the data set
def get_inside_point_cube_list(cube_list,point_in_offgrid):
    point_inside = []
    for point in point_in_offgrid:
        if point in cube_list:
            point_inside.append(point_in_offgrid.index(point))

    return point_inside

def cube_analyzer(original_point, point_inside):
    meshes = []
    if len(point_inside) == 1:
        shape = []
        shape.append([original_point[0]+0.5,original_point[1] + points_lookup_table[point_inside[0]][1],original_point[2] + points_lookup_table[point_inside[0]][2]])
        shape.append([original_point[0] + points_lookup_table[point_inside[0]][0],original_point[1]+0.5,original_point[2]+ points_lookup_table[point_inside[0]][2]])
        shape.append([original_point[0]+ points_lookup_table[point_inside[0]][0],original_point[1]+ points_lookup_table[point_inside[0]][1],original_point[2]+0.5])
        meshes.append(shape)
    
    elif len(point_inside) == 2:
         
        ## on the same axis 
        if point_inside[1]-point_inside[0] == 1: ## same x or y 
            if points_lookup_table[point_inside[1]][0] - points_lookup_table[point_inside[0]][0] == 1: ##same y coordinate

                first_shape = []
                first_shape.append([original_point[0]+points_lookup_table[point_inside[0]][0],original_point[1] + 0.5,original_point[2] + points_lookup_table[point_inside[0]][2]])
                first_shape.append([original_point[0] + points_lookup_table[point_inside[0]][0],original_point[1] + points_lookup_table[point_inside[0]][1],original_point[2]+0.5])
                first_shape.append([original_point[0] + points_lookup_table[point_inside[1]][0],original_point[1] +points_lookup_table[point_inside[1]][1],original_point[2]+0.5])
                meshes.append(first_shape)
                second_shape = []
                second_shape.append([original_point[0] + points_lookup_table[point_inside[1]][0],original_point[1] + 0.5,original_point[2]+points_lookup_table[point_inside[1]][2]])
                second_shape.append([original_point[0] + points_lookup_table[point_inside[1]][0],original_point[1] + points_lookup_table[point_inside[1]][1],original_point[2]+0.5])
                second_shape.append([original_point[0]+points_lookup_table[point_inside[0]][0],original_point[1] + 0.5,original_point[2] + points_lookup_table[point_inside[0]][2]])
                meshes.append(second_shape)
            else: ## same x coordinate
                first_shape = []
                first_shape.append([original_point[0]+0.5,original_point[1] + points_lookup_table[point_inside[0]][1],original_point[2] + points_lookup_table[point_inside[0]][2]])
                first_shape.append([original_point[0] + points_lookup_table[point_inside[0]][0],original_point[1] + points_lookup_table[point_inside[0]][1],original_point[2]+0.5])
                first_shape.append([original_point[0] + points_lookup_table[point_inside[1]][0],original_point[1] +points_lookup_table[point_inside[1]][1],original_point[2]+0.5])
                meshes.append(first_shape)
                second_shape = []
                second_shape.append([original_point[0] + 0.5,original_point[1] + points_lookup_table[point_inside[1]][1],original_point[2]+points_lookup_table[point_inside[1]][2]])
                second_shape.append([original_point[0] + points_lookup_table[point_inside[1]][0],original_point[1] + points_lookup_table[point_inside[1]][1],original_point[2]+0.5])
                second_shape.append([original_point[0]+0.5,original_point[1]+ points_lookup_table[point_inside[1]][1],original_point[2] + points_lookup_table[point_inside[0]][2]])
                meshes.append(second_shape)

        elif point_inside[1] - point_inside[0] == 4: ##same z coordinate
            first_shape = []
            first_shape.append([original_point[0]+points_lookup_table[point_inside[0]][0],original_point[1] + 0.5,original_point[2] + points_lookup_table[point_inside[0]][2]])
            first_shape.append([original_point[0] + +0.5,original_point[1] + points_lookup_table[point_inside[0]][1],original_point[2]+points_lookup_table[point_inside[0]][2]])
            first_shape.append([original_point[0] + 0.5,original_point[1] + points_lookup_table[point_inside[1]][1],original_point[2]+points_lookup_table[point_inside[1]][2]])
            meshes.append(first_shape)
            second_shape = []
            second_shape.append([original_point[0] + points_lookup_table[point_inside[1]][0],original_point[1] + 0.5,original_point[2]+points_lookup_table[point_inside[1]][2]])
            second_shape.append([original_point[0] + 0.5,original_point[1] + points_lookup_table[point_inside[1]][1],original_point[2]+points_lookup_table[point_inside[1]][2]])
            second_shape.append([original_point[0]+points_lookup_table[point_inside[0]][0],original_point[1] + 0.5,original_point[2] + points_lookup_table[point_inside[0]][2]])
            meshes.append(second_shape)

        else: ##diagonal
            shape = []
            shape.append([original_point[0]+points_lookup_table[point_inside[0]][0],original_point[1]+0.5,original_point[2]+points_lookup_table[point_inside[0]][2]])
            shape.append([original_point[0]+0.5,original_point[1]+points_lookup_table[point_inside[0]][1],original_point[2]+points_lookup_table[point_inside[0]][2]])
            shape.append([original_point[0]+points_lookup_table[point_inside[0]][0],original_point[1]+points_lookup_table[point_inside[0]][1],original_point[2]+0.5])
            meshes.append(shape)
            second_shape =[]
            second_shape.append([original_point[0]+points_lookup_table[point_inside[1]][0],original_point[1]+0.5,original_point[2]+points_lookup_table[point_inside[1]][2]])
            second_shape.append([original_point[0]+0.5,original_point[1]+points_lookup_table[point_inside[1]][1],original_point[2]+points_lookup_table[point_inside[1]][2]])
            second_shape.append([original_point[0]+points_lookup_table[point_inside[1]][0],original_point[1]+points_lookup_table[point_inside[1]][1],original_point[2]+0.5])
            meshes.append(second_shape)

    elif(len(point_inside) == 3):
        if (original_point[2] + points_lookup_table[point_inside[0]][2]) == (original_point[2] + points_lookup_table[point_inside[1]][2]) == (original_point[2] + points_lookup_table[point_inside[2]][2]):
            first_shape = []
            first_shape.append([original_point[0]+points_lookup_table[point_inside[0]][0],original_point[1] + points_lookup_table[point_inside[0]][1],original_point[2]+0.5])
            first_shape.append([original_point[0]+points_lookup_table[point_inside[1]][0],original_point[1] + points_lookup_table[point_inside[1]][1],original_point[2]+0.5])
            first_shape.append([original_point[0]+points_lookup_table[point_inside[2]][0],original_point[1] + points_lookup_table[point_inside[2]][1],original_point[2]+0.5])
            meshes.append( first_shape)
            second_shape = []
            third_shape = []
            if original_point[0]+ points_lookup_table[point_inside[0]][0] != original_point[0]+points_lookup_table[point_inside[1]][0] and original_point[1]+ points_lookup_table[point_inside[0]][1] != original_point[1]+points_lookup_table[point_inside[1]][1]:
                print("first case")
                second_shape.append([original_point[0]+points_lookup_table[point_inside[0]][0],original_point[1] + points_lookup_table[point_inside[0]][1],original_point[2]+0.5])
                second_shape.append([original_point[0]+points_lookup_table[point_inside[1]][0],original_point[1] + points_lookup_table[point_inside[1]][1],original_point[2]+0.5])
                second_shape.append([original_point[0]+points_lookup_table[point_inside[0]][0],original_point[1]+0.5,original_point[2]+points_lookup_table[point_inside[0]][2]])
                meshes.append(second_shape)
                third_shape.append([original_point[0]+points_lookup_table[point_inside[1]][0],original_point[1] + points_lookup_table[point_inside[1]][1],original_point[2]+0.5])
                third_shape.append([original_point[0]+points_lookup_table[point_inside[0]][0],original_point[1]+0.5,original_point[2]+points_lookup_table[point_inside[0]][2]])
                third_shape.append([original_point[0]+0.5,original_point[1]+points_lookup_table[point_inside[0]][1],original_point[2]+points_lookup_table[point_inside[0]][2]])
                meshes.append(third_shape)
            elif original_point[0] + points_lookup_table[point_inside[0]][0] != original_point[0] + points_lookup_table[point_inside[2]][0] and original_point[1]+points_lookup_table[point_inside[0]][1] != original_point[1]+ points_lookup_table[point_inside[2]][1]:
                print("second case")
                second_shape.append([original_point[0]+points_lookup_table[point_inside[0]][0],original_point[1] + points_lookup_table[point_inside[0]][1],original_point[2]+0.5])
                second_shape.append([original_point[0]+points_lookup_table[point_inside[2]][0],original_point[1] + points_lookup_table[point_inside[2]][1],original_point[2]+0.5])
                second_shape.append([original_point[0]+points_lookup_table[point_inside[0]][0],original_point[1]+0.5,original_point[2]+points_lookup_table[point_inside[0]][2]])
                meshes.append(second_shape)
                third_shape.append([original_point[0]+points_lookup_table[point_inside[2]][0],original_point[1] + points_lookup_table[point_inside[2]][1],original_point[2]+0.5])
                third_shape.append([original_point[0]+points_lookup_table[point_inside[0]][0],original_point[1]+0.5,original_point[2]+points_lookup_table[point_inside[0]][2]])
                third_shape.append([original_point[0]+0.5,original_point[1]+points_lookup_table[point_inside[0]][1],original_point[2]+points_lookup_table[point_inside[0]][2]])
                meshes.append(third_shape)
            if original_point[0] + points_lookup_table[point_inside[1]][0] != original_point[0]+ points_lookup_table[point_inside[2]][0] and original_point[1] + points_lookup_table[point_inside[1]][1] != original_point[1]+ points_lookup_table[point_inside[2]][1]:
                print("third case")
                second_shape.append([original_point[0]+points_lookup_table[point_inside[1]][0],original_point[1] + points_lookup_table[point_inside[1]][1],original_point[2]+0.5])
                second_shape.append([original_point[0]+points_lookup_table[point_inside[2]][0],original_point[1] + points_lookup_table[point_inside[2]][1],original_point[2]+0.5])
                second_shape.append([original_point[0]+points_lookup_table[point_inside[2]][0],original_point[1]+0.5,original_point[2]+points_lookup_table[point_inside[1]][2]])
                meshes.append(second_shape)
                third_shape.append([original_point[0]+points_lookup_table[point_inside[1]][0],original_point[1] + points_lookup_table[point_inside[1]][1],original_point[2]+0.5])
                third_shape.append([original_point[0]+points_lookup_table[point_inside[2]][0],original_point[1]+0.5,original_point[2]+points_lookup_table[point_inside[1]][2]])
                third_shape.append([original_point[0]+0.5,original_point[1]+points_lookup_table[point_inside[1]][1],original_point[2]+points_lookup_table[point_inside[1]][2]])
                meshes.append(third_shape)

                
        elif (original_point[1] + points_lookup_table[point_inside[0]][1]) == (original_point[1] + points_lookup_table[point_inside[1]][1]) == (original_point[1] + points_lookup_table[point_inside[2]][1]):
            first_shape = []
            first_shape.append([original_point[0]+points_lookup_table[point_inside[0]][0],original_point[1] + 0.5,original_point[2]+points_lookup_table[point_inside[0]][2]])
            first_shape.append([original_point[0]+points_lookup_table[point_inside[1]][0],original_point[1] + 0.5,original_point[2]+points_lookup_table[point_inside[1]][2]])
            first_shape.append([original_point[0]+points_lookup_table[point_inside[2]][0],original_point[1] + 0.5,original_point[2]+points_lookup_table[point_inside[2]][2]])
            meshes.append(first_shape)
            second_shape = []
            third_shape = []
            if original_point[0]+ points_lookup_table[point_inside[0]][0] != original_point[0]+points_lookup_table[point_inside[1]][0] and original_point[2]+ points_lookup_table[point_inside[0]][2] != original_point[2]+points_lookup_table[point_inside[1]][2]:
                print("first case")
                second_shape.append([original_point[0]+points_lookup_table[point_inside[0]][0],original_point[1] + 0.5,original_point[2]+points_lookup_table[point_inside[0]][2]])
                second_shape.append([original_point[0]+points_lookup_table[point_inside[1]][0],original_point[1] + 0.5,original_point[2]+points_lookup_table[point_inside[1]][2]])
                second_shape.append([original_point[0]+0.5,original_point[1]+points_lookup_table[point_inside[0]][1],original_point[2]+points_lookup_table[point_inside[0]][2]])
                meshes.append(second_shape)
                third_shape.append([original_point[0]+points_lookup_table[point_inside[0]][0],original_point[1] + 0.5,original_point[2]+points_lookup_table[point_inside[0]][2]])
                third_shape.append([original_point[0]+0.5,original_point[1]+points_lookup_table[point_inside[1]][1],original_point[2]+points_lookup_table[point_inside[1]][2]])
                third_shape.append([original_point[0]+points_lookup_table[point_inside[0]][0],original_point[1]+points_lookup_table[point_inside[0]][1],original_point[2]+0.5])
                meshes.append(third_shape)
            elif original_point[0] + points_lookup_table[point_inside[0]][0] != original_point[0] + points_lookup_table[point_inside[2]][0] and original_point[2]+points_lookup_table[point_inside[0]][2] != original_point[2]+ points_lookup_table[point_inside[2]][2]:
                print("second case")
                second_shape.append([original_point[0]+points_lookup_table[point_inside[0]][0],original_point[1] + 0.5,original_point[2]+points_lookup_table[point_inside[0]][2]])
                second_shape.append([original_point[0]+points_lookup_table[point_inside[2]][0],original_point[1] + 0.5,original_point[2]+points_lookup_table[point_inside[2]][2]])
                second_shape.append([original_point[0]+0.5,original_point[1]+points_lookup_table[point_inside[2]][1],original_point[2]+points_lookup_table[point_inside[2]][2]])
                meshes.append(second_shape)
                third_shape.append([original_point[0]+points_lookup_table[point_inside[0]][0],original_point[1] + 0.5,original_point[2]+points_lookup_table[point_inside[0]][2]])
                third_shape.append([original_point[0]+0.5,original_point[1]+points_lookup_table[point_inside[2]][1],original_point[2]+points_lookup_table[point_inside[2]][2]])
                third_shape.append([original_point[0]+points_lookup_table[point_inside[0]][0],original_point[1]+points_lookup_table[point_inside[0]][1],original_point[2]+0.5])
                meshes.append(third_shape)
            elif original_point[0] + points_lookup_table[point_inside[1]][0] != original_point[0]+ points_lookup_table[point_inside[2]][0] and original_point[2] + points_lookup_table[point_inside[1]][2] != original_point[2]+ points_lookup_table[point_inside[2]][2]:
                print("third case")
                second_shape.append([original_point[0]+points_lookup_table[point_inside[1]][0],original_point[1] + 0.5,original_point[2]+points_lookup_table[point_inside[1]][2]])
                second_shape.append([original_point[0]+points_lookup_table[point_inside[2]][0],original_point[1] + 0.5,original_point[2]+points_lookup_table[point_inside[2]][2]])
                second_shape.append([original_point[0]+0.5,original_point[1]+points_lookup_table[point_inside[2]][1],original_point[2]+points_lookup_table[point_inside[2]][2]])
                meshes.append(second_shape)
                third_shape.append([original_point[0]+points_lookup_table[point_inside[1]][0],original_point[1]+0.5,original_point[2]+points_lookup_table[point_inside[1]][2]])
                third_shape.append([original_point[0]+0.5,original_point[1]+points_lookup_table[point_inside[2]][1],original_point[2]+points_lookup_table[point_inside[2]][2]])
                third_shape.append([original_point[0]+points_lookup_table[point_inside[1]][0],original_point[1]+points_lookup_table[point_inside[1]][1],original_point[2]+0.5])
                meshes.append(third_shape)
        elif (original_point[0] + points_lookup_table[point_inside[0]][0]) == (original_point[0] + points_lookup_table[point_inside[1]][0]) == (original_point[0] + points_lookup_table[point_inside[2]][0]):
            first_shape = []
            first_shape.append([original_point[0]+0.5,original_point[1]+ points_lookup_table[point_inside[0]][1],original_point[2]+points_lookup_table[point_inside[0]][2]])
            first_shape.append([original_point[0]+0.5,original_point[1] + points_lookup_table[point_inside[1]][1],original_point[2]+points_lookup_table[point_inside[1]][2]])
            first_shape.append([original_point[0]+0.5,original_point[1] + points_lookup_table[point_inside[2]][1],original_point[2]+points_lookup_table[point_inside[2]][2]])
            meshes.append(first_shape)
            second_shape = []
            third_shape = []
            if original_point[1]+ points_lookup_table[point_inside[0]][1] != original_point[1]+points_lookup_table[point_inside[1]][1] and original_point[2]+ points_lookup_table[point_inside[0]][2] != original_point[2]+points_lookup_table[point_inside[1]][2]:
                print("first case")
                second_shape.append([original_point[0]+0.5,original_point[1]+points_lookup_table[point_inside[0]][1],original_point[2]+points_lookup_table[point_inside[0]][2]])
                second_shape.append([original_point[0]+0.5,original_point[1]+points_lookup_table[point_inside[1]][1],original_point[2]+points_lookup_table[point_inside[1]][2]])
                second_shape.append([original_point[0]+points_lookup_table[point_inside[0]][1],original_point[1]+0.5,original_point[2]+points_lookup_table[point_inside[0]][2]])
                meshes.append(second_shape)
                third_shape.append([original_point[0]+0.5,original_point[1]+points_lookup_table[point_inside[0]][1],original_point[2]+points_lookup_table[point_inside[0]][2]])
                third_shape.append([original_point[0]+points_lookup_table[point_inside[1]][0],original_point[1]+0.5,original_point[2]+points_lookup_table[point_inside[1]][2]])
                third_shape.append([original_point[0]+points_lookup_table[point_inside[0]][0],original_point[1]+points_lookup_table[point_inside[1]][1],original_point[2]+0.5])
                meshes.append(third_shape)
            elif original_point[1] + points_lookup_table[point_inside[0]][1] != original_point[1] + points_lookup_table[point_inside[2]][1] and original_point[2]+points_lookup_table[point_inside[0]][2] != original_point[2]+ points_lookup_table[point_inside[2]][2]:
                print("second case")
                second_shape.append([original_point[0]+0.5,original_point[1] + points_lookup_table[point_inside[0]][1],original_point[2]+points_lookup_table[point_inside[0]][2]])
                second_shape.append([original_point[0]+0.5,original_point[1]+points_lookup_table[point_inside[2]][1],original_point[2]+points_lookup_table[point_inside[2]][2]])
                second_shape.append([original_point[0]+points_lookup_table[point_inside[0]][0],original_point[1]+0.5,original_point[2]+points_lookup_table[point_inside[2]][2]])
                meshes.append(second_shape)
                third_shape.append([original_point[0]+0.5,original_point[1] + points_lookup_table[point_inside[0]][1],original_point[2]+points_lookup_table[point_inside[0]][2]])
                third_shape.append([original_point[0]+points_lookup_table[point_inside[2]][0],original_point[1]+0.5,original_point[2]+points_lookup_table[point_inside[2]][2]])
                third_shape.append([original_point[0]+points_lookup_table[point_inside[0]][0],original_point[1]+points_lookup_table[point_inside[0]][1],original_point[2]+0.5])
                meshes.append(third_shape)
            elif original_point[1] + points_lookup_table[point_inside[1]][1] != original_point[1]+ points_lookup_table[point_inside[2]][1] and original_point[2] + points_lookup_table[point_inside[1]][2] != original_point[2]+ points_lookup_table[point_inside[2]][2]:
                print("third case")
                second_shape.append([original_point[0]+0.5,original_point[1] + points_lookup_table[point_inside[1]][1],original_point[2]+points_lookup_table[point_inside[1]][2]])
                second_shape.append([original_point[0]+0.5,original_point[1] + points_lookup_table[point_inside[2]][1],original_point[2]+points_lookup_table[point_inside[2]][2]])
                second_shape.append([original_point[0]+points_lookup_table[point_inside[1]][0],original_point[1]+points_lookup_table[point_inside[1]][1],original_point[2]+0.5])
                meshes.append(second_shape)
                third_shape.append([original_point[0]+0.5,original_point[1]+points_lookup_table[point_inside[2]][1],original_point[2]+points_lookup_table[point_inside[2]][2]])
                third_shape.append([original_point[0]+points_lookup_table[point_inside[2]][0],original_point[1]+0.5,original_point[2]+points_lookup_table[point_inside[2]][2]])
                third_shape.append([original_point[0]+points_lookup_table[point_inside[1]][0],original_point[1]+points_lookup_table[point_inside[1]][1],original_point[2]+0.5])
                meshes.append(third_shape)
        
        else:
            #missing just a line in the rectangle shape (case 12)
            if point_inside[1]-point_inside[0] == 1: ## same x or y 
                if points_lookup_table[point_inside[1]][0] - points_lookup_table[point_inside[0]][0] == 1: ##same y coordinate

                    first_shape = []
                    first_shape.append([original_point[0] + points_lookup_table[point_inside[0]][0],original_point[1] + 0.5,original_point[2] + points_lookup_table[point_inside[0]][2]])
                    first_shape.append([original_point[0] + points_lookup_table[point_inside[0]][0],original_point[1] + points_lookup_table[point_inside[0]][1],original_point[2]+0.5])
                    first_shape.append([original_point[0] + points_lookup_table[point_inside[1]][0],original_point[1] +points_lookup_table[point_inside[1]][1],original_point[2]+0.5])
                    meshes.append(first_shape)
                    second_shape = []
                    second_shape.append([original_point[0] + points_lookup_table[point_inside[1]][0],original_point[1] + 0.5,original_point[2]+points_lookup_table[point_inside[1]][2]])
                    second_shape.append([original_point[0] + points_lookup_table[point_inside[1]][0],original_point[1] + points_lookup_table[point_inside[1]][1],original_point[2]+0.5])
                    second_shape.append([original_point[0]+points_lookup_table[point_inside[0]][0],original_point[1] + 0.5,original_point[2] + points_lookup_table[point_inside[0]][2]])
                    meshes.append(second_shape)
                    third_shape = []
                    third_shape.append([original_point[0]+0.5, original_point[1]+points_lookup_table[point_inside[2]][1],original_point[2]+points_lookup_table[point_inside[2]][2]])
                    third_shape.append([original_point[0]+ points_lookup_table[point_inside[2]][0], original_point[1]+0.5,original_point[2]+points_lookup_table[point_inside[2]][2]])
                    third_shape.append([original_point[0]+points_lookup_table[point_inside[2]][0], original_point[1]+points_lookup_table[point_inside[2]][1],original_point[2]+0.5])
                    meshes.append(third_shape)
                else: ## same x coordinate
                    first_shape = []
                    first_shape.append([original_point[0]+0.5,original_point[1] + points_lookup_table[point_inside[0]][1],original_point[2] + points_lookup_table[point_inside[0]][2]])
                    first_shape.append([original_point[0] + points_lookup_table[point_inside[0]][0],original_point[1] + points_lookup_table[point_inside[0]][1],original_point[2]+0.5])
                    first_shape.append([original_point[0] + points_lookup_table[point_inside[1]][0],original_point[1] +points_lookup_table[point_inside[1]][1],original_point[2]+0.5])
                    meshes.append(first_shape)
                    second_shape = []
                    second_shape.append([original_point[0] + 0.5,original_point[1] + points_lookup_table[point_inside[1]][1],original_point[2]+points_lookup_table[point_inside[1]][2]])
                    second_shape.append([original_point[0] + points_lookup_table[point_inside[1]][0],original_point[1] + points_lookup_table[point_inside[1]][1],original_point[2]+0.5])
                    second_shape.append([original_point[0]+0.5,original_point[1]+ points_lookup_table[point_inside[1]][1],original_point[2] + points_lookup_table[point_inside[0]][2]])
                    meshes.append(second_shape)
                    third_shape = []
                    third_shape.append([original_point[0]+0.5, original_point[1]+points_lookup_table[point_inside[2]][1],original_point[2]+points_lookup_table[point_inside[2]][2]])
                    third_shape.append([original_point[0]+ points_lookup_table[point_inside[2]][0], original_point[1]+0.5,original_point[2]+points_lookup_table[point_inside[2]][2]])
                    third_shape.append([original_point[0]+points_lookup_table[point_inside[2]][0], original_point[1]+points_lookup_table[point_inside[2]][1],original_point[2]+0.5])
                    meshes.append(third_shape)


            elif point_inside[2] - point_inside[0] == 4: ##same z coordinate
                first_shape = []
                first_shape.append([original_point[0]+points_lookup_table[point_inside[0]][0],original_point[1] + 0.5,original_point[2] + points_lookup_table[point_inside[0]][2]])
                first_shape.append([original_point[0] + +0.5,original_point[1] + points_lookup_table[point_inside[0]][1],original_point[2]+points_lookup_table[point_inside[0]][2]])
                first_shape.append([original_point[0] + 0.5,original_point[1] + points_lookup_table[point_inside[2]][1],original_point[2]+points_lookup_table[point_inside[2]][2]])
                meshes.append(first_shape)
                second_shape = []
                second_shape.append([original_point[0] + points_lookup_table[point_inside[1]][0],original_point[1] + 0.5,original_point[2]+points_lookup_table[point_inside[2]][2]])
                second_shape.append([original_point[0] + 0.5,original_point[1] + points_lookup_table[point_inside[2]][1],original_point[2]+points_lookup_table[point_inside[2]][2]])
                second_shape.append([original_point[0]+points_lookup_table[point_inside[0]][0],original_point[1] + 0.5,original_point[2] + points_lookup_table[point_inside[0]][2]])
                meshes.append(second_shape)
                third_shape = []
                third_shape.append([original_point[0]+0.5, original_point[1]+points_lookup_table[point_inside[1]][1],original_point[2]+points_lookup_table[point_inside[1]][2]])
                third_shape.append([original_point[0]+ points_lookup_table[point_inside[1]][0], original_point[1]+0.5,original_point[2]+points_lookup_table[point_inside[1]][2]])
                third_shape.append([original_point[0]+points_lookup_table[point_inside[1]][0], original_point[1]+points_lookup_table[point_inside[1]][1],original_point[2]+0.5])
                meshes.append(third_shape)
            
            elif point_inside[2] - point_inside[1] == 4:
                first_shape = []
                first_shape.append([original_point[0]+points_lookup_table[point_inside[1]][0],original_point[1] + 0.5,original_point[2] + points_lookup_table[point_inside[1]][2]])
                first_shape.append([original_point[0] + +0.5,original_point[1] + points_lookup_table[point_inside[1]][1],original_point[2]+points_lookup_table[point_inside[1]][2]])
                first_shape.append([original_point[0] + 0.5,original_point[1] + points_lookup_table[point_inside[2]][1],original_point[2]+points_lookup_table[point_inside[2]][2]])
                meshes.append(first_shape)
                second_shape = []
                second_shape.append([original_point[0] + points_lookup_table[point_inside[2]][0],original_point[1] + 0.5,original_point[2]+points_lookup_table[point_inside[2]][2]])
                second_shape.append([original_point[0] + 0.5,original_point[1] + points_lookup_table[point_inside[2]][1],original_point[2]+points_lookup_table[point_inside[2]][2]])
                second_shape.append([original_point[0]+points_lookup_table[point_inside[1]][0],original_point[1] + 0.5,original_point[2] + points_lookup_table[point_inside[1]][2]])
                meshes.append(second_shape)
                third_shape = []
                third_shape.append([original_point[0]+0.5, original_point[1]+points_lookup_table[point_inside[0]][1],original_point[2]+points_lookup_table[point_inside[0]][2]])
                third_shape.append([original_point[0]+ points_lookup_table[point_inside[0]][0], original_point[1]+0.5,original_point[2]+points_lookup_table[point_inside[0]][2]])
                third_shape.append([original_point[0]+points_lookup_table[point_inside[0]][0], original_point[1]+points_lookup_table[point_inside[0]][1],original_point[2]+0.5])
                meshes.append(third_shape)
            

            else:
                first_shape = []
                first_shape.append([original_point[0]+0.5, original_point[1]+points_lookup_table[point_inside[0]][1],original_point[2]+points_lookup_table[point_inside[0]][2]])
                first_shape.append([original_point[0]+ points_lookup_table[point_inside[0]][0], original_point[1]+0.5,original_point[2]+points_lookup_table[point_inside[0]][2]])
                first_shape.append([original_point[0]+points_lookup_table[point_inside[0]][0], original_point[1]+points_lookup_table[point_inside[0]][1],original_point[2]+0.5])
                meshes.append(first_shape)
                second_shape = []
                second_shape.append([original_point[0]+0.5, original_point[1]+points_lookup_table[point_inside[1]][1],original_point[2]+points_lookup_table[point_inside[1]][2]])
                second_shape.append([original_point[0]+ points_lookup_table[point_inside[1]][0], original_point[1]+0.5,original_point[2]+points_lookup_table[point_inside[1]][2]])
                second_shape.append([original_point[0]+points_lookup_table[point_inside[1]][0], original_point[1]+points_lookup_table[point_inside[1]][1],original_point[2]+0.5])
                meshes.append(second_shape)
                third_shape = []
                third_shape.append([original_point[0]+0.5, original_point[1]+points_lookup_table[point_inside[2]][1],original_point[2]+points_lookup_table[point_inside[2]][2]])
                third_shape.append([original_point[0]+ points_lookup_table[point_inside[2]][0], original_point[1]+0.5,original_point[2]+points_lookup_table[point_inside[2]][2]])
                third_shape.append([original_point[0]+points_lookup_table[point_inside[2]][0], original_point[1]+points_lookup_table[point_inside[2]][1],original_point[2]+0.5])
                meshes.append(third_shape)
    
    elif len(point_inside) == 4:
        if points_lookup_table[point_inside[0]][2] == points_lookup_table[point_inside[1]][2] == points_lookup_table[point_inside[2]][2] == points_lookup_table[point_inside[3]][2]:
            first_shape = []
            first_shape.append([original_point[0] + points_lookup_table[point_inside[0]][0], original_point[1]+points_lookup_table[point_inside[0]][1],original_point[2]+0.5])
            first_shape.append([original_point[0] + points_lookup_table[point_inside[1]][0], original_point[1]+points_lookup_table[point_inside[1]][1],original_point[2]+0.5])
            first_shape.append([original_point[0] + points_lookup_table[point_inside[3]][0], original_point[1]+points_lookup_table[point_inside[3]][1],original_point[2]+0.5])
            meshes.append(first_shape)
            second_shape = []
            second_shape.append([original_point[0] + points_lookup_table[point_inside[1]][0], original_point[1]+points_lookup_table[point_inside[1]][1],original_point[2]+0.5])
            second_shape.append([original_point[0] + points_lookup_table[point_inside[3]][0], original_point[1]+points_lookup_table[point_inside[3]][1],original_point[2]+0.5])
            second_shape.append([original_point[0] + points_lookup_table[point_inside[2]][0], original_point[1]+points_lookup_table[point_inside[2]][1],original_point[2]+0.5])
            meshes.append(second_shape)
        elif points_lookup_table[point_inside[0]][1] == points_lookup_table[point_inside[1]][1] == points_lookup_table[point_inside[2]][1] == points_lookup_table[point_inside[3]][1]:
            first_shape = []
            first_shape.append([original_point[0] + points_lookup_table[point_inside[0]][0], original_point[1]+0.5,original_point[2]+points_lookup_table[point_inside[0]][2]])
            first_shape.append([original_point[0] + points_lookup_table[point_inside[1]][0], original_point[1]+0.5,original_point[2]+points_lookup_table[point_inside[1]][2]])
            first_shape.append([original_point[0] + points_lookup_table[point_inside[3]][0], original_point[1]+0.5,original_point[2]+points_lookup_table[point_inside[3]][2]])
            meshes.append(first_shape)
            second_shape = []
            second_shape.append([original_point[0] + points_lookup_table[point_inside[1]][0], original_point[1]+0.5,original_point[2]+points_lookup_table[point_inside[1]][2]])
            second_shape.append([original_point[0] + points_lookup_table[point_inside[3]][0], original_point[1]+0.5,original_point[2]+points_lookup_table[point_inside[3]][2]])
            second_shape.append([original_point[0] + points_lookup_table[point_inside[2]][0], original_point[1]+0.5,original_point[2]+points_lookup_table[point_inside[2]][2]])
            meshes.append(second_shape)
        elif points_lookup_table[point_inside[0]][0] == points_lookup_table[point_inside[1]][0] == points_lookup_table[point_inside[2]][0] == points_lookup_table[point_inside[3]][0]:
            first_shape = []
            first_shape.append([original_point[0] + 0.5, original_point[1]+points_lookup_table[point_inside[0]][1],original_point[2]+points_lookup_table[point_inside[0]][2]])
            first_shape.append([original_point[0] + 0.5, original_point[1]+points_lookup_table[point_inside[1]][1],original_point[2]+points_lookup_table[point_inside[1]][2]])
            first_shape.append([original_point[0] + 0.5, original_point[1]+points_lookup_table[point_inside[3]][1],original_point[2]+points_lookup_table[point_inside[3]][2]])
            meshes.append(first_shape)
            second_shape = []
            second_shape.append([original_point[0] + 0.5, original_point[1]+points_lookup_table[point_inside[1]][1],original_point[2]+points_lookup_table[point_inside[1]][2]])
            second_shape.append([original_point[0] + 0.5, original_point[1]+points_lookup_table[point_inside[2]][1],original_point[2]+points_lookup_table[point_inside[2]][2]])
            second_shape.append([original_point[0] + 0.5, original_point[1]+points_lookup_table[point_inside[0]][1],original_point[2]+points_lookup_table[point_inside[0]][2]])
            meshes.append(second_shape)

        elif point_inside[2] - point_inside[0] == 4 and point_inside[3] - point_inside[1] == 4:
            first_shape = []
            first_shape.append([original_point[0]+0.5,original_point[1]+points_lookup_table[point_inside[0]][1],original_point[2]+points_lookup_table[point_inside[0]][2]])
            first_shape.append([original_point[0]+points_lookup_table[point_inside[0]][0],original_point[1]+0.5,original_point[2]+points_lookup_table[point_inside[0]][2]])
            first_shape.append([original_point[0]+points_lookup_table[point_inside[2]][0],original_point[1]+0.5,original_point[2]+points_lookup_table[point_inside[2]][2]])
            meshes.append(first_shape)
            second_shape = []
            second_shape.append([original_point[0]+0.5,original_point[1]+points_lookup_table[point_inside[2]][1],original_point[2]+points_lookup_table[point_inside[2]][2]])
            second_shape.append([original_point[0]+points_lookup_table[point_inside[2]][0],original_point[1]+0.5,original_point[2]+points_lookup_table[point_inside[2]][2]])
            second_shape.append([original_point[0]+0.5,original_point[1]+points_lookup_table[point_inside[0]][1],original_point[2]+points_lookup_table[point_inside[0]][2]])
            meshes.append(second_shape)
            third_shape = []
            third_shape.append([original_point[0]+0.5,original_point[1]+points_lookup_table[point_inside[1]][1],original_point[2]+points_lookup_table[point_inside[1]][2]])
            third_shape.append([original_point[0]+points_lookup_table[point_inside[1]][0],original_point[1]+0.5,original_point[2]+points_lookup_table[point_inside[1]][2]])
            third_shape.append([original_point[0]+points_lookup_table[point_inside[3]][0],original_point[1]+0.5,original_point[2]+points_lookup_table[point_inside[3]][2]])
            meshes.append(third_shape)
            fourth_shape = []
            fourth_shape.append([original_point[0]+0.5,original_point[1]+points_lookup_table[point_inside[3]][1],original_point[2]+points_lookup_table[point_inside[3]][2]])
            fourth_shape.append([original_point[0]+points_lookup_table[point_inside[3]][0],original_point[1]+0.5,original_point[2]+points_lookup_table[point_inside[3]][2]])
            fourth_shape.append([original_point[0]+0.5,original_point[1]+points_lookup_table[point_inside[1]][1],original_point[2]+points_lookup_table[point_inside[1]][2]])
            meshes.append(fourth_shape)
        
        elif points_lookup_table[point_inside[0]][2] == points_lookup_table[point_inside[1]][2] == points_lookup_table[point_inside[2]][2] or points_lookup_table[point_inside[1]][2] == points_lookup_table[point_inside[2]][2] == points_lookup_table[point_inside[3]][2]:
            if original_point[0]+ points_lookup_table[point_inside[1]][0] != original_point[0]+points_lookup_table[point_inside[2]][0] and original_point[1]+ points_lookup_table[point_inside[1]][1] != original_point[1]+points_lookup_table[point_inside[2]][1]:
                if point_inside[0] + 4 == point_inside[3]:
                    first_shape = []
                    first_shape.append([original_point[0]+points_lookup_table[point_inside[1]][0],original_point[1]+points_lookup_table[point_inside[1]][1],original_point[2]+0.5])
                    first_shape.append([original_point[0]+points_lookup_table[point_inside[1]][0],original_point[1]+0.5,original_point[2]+points_lookup_table[point_inside[1]][2]])
                    first_shape.append([original_point[0]+0.5,original_point[1]+points_lookup_table[point_inside[2]][1],original_point[2]+points_lookup_table[point_inside[2]][2]])
                    meshes.append(first_shape)
                    second_shape = []
                    second_shape.append([original_point[0]+0.5,original_point[1]+points_lookup_table[point_inside[2]][1],original_point[2]+points_lookup_table[point_inside[2]][2]])
                    second_shape.append([original_point[0]+points_lookup_table[point_inside[1]][0],original_point[1]+points_lookup_table[point_inside[1]][1],original_point[2]+0.5])
                    second_shape.append([original_point[0]+0.5,original_point[1]+points_lookup_table[point_inside[3]][1],original_point[2]+points_lookup_table[point_inside[3]][2]])
                    meshes.append(second_shape)
                    third_shape = []
                    third_shape.append([original_point[0]+points_lookup_table[point_inside[1]][0],original_point[1]+points_lookup_table[point_inside[1]][1],original_point[2]+0.5])
                    third_shape.append([original_point[0]+0.5,original_point[1]+points_lookup_table[point_inside[3]][1],original_point[2]+points_lookup_table[point_inside[3]][2]])
                    third_shape.append([original_point[0]+points_lookup_table[point_inside[2]][0],original_point[1]+points_lookup_table[point_inside[2]][1],original_point[2]+0.5])
                    meshes.append(third_shape)
                    fourth_shape = []
                    fourth_shape.append([original_point[0]+0.5,original_point[1]+points_lookup_table[point_inside[3]][1],original_point[2]+points_lookup_table[point_inside[3]][2]])
                    fourth_shape.append([original_point[0]+points_lookup_table[point_inside[2]][0],original_point[1]+points_lookup_table[point_inside[2]][1],original_point[2]+0.5])
                    fourth_shape.append([original_point[0]+points_lookup_table[point_inside[3]][0],original_point[1]+0.5,original_point[2]+points_lookup_table[point_inside[3]][2]])
                    meshes.append(fourth_shape)
                elif point_inside[2] + 4 == point_inside[3]:
                    first_shape = []
                    first_shape.append([original_point[0]+points_lookup_table[point_inside[0]][0],original_point[1]+points_lookup_table[point_inside[0]][1],original_point[2] + 0.5])
                    first_shape.append([original_point[0]+points_lookup_table[point_inside[1]][0],original_point[1]+0.5,original_point[2] + points_lookup_table[point_inside[1]][2]])
                    first_shape.append([original_point[0]+points_lookup_table[point_inside[1]][0],original_point[1]+points_lookup_table[point_inside[1]][1],original_point[2] + 0.5])
                    meshes.append(first_shape)
                    second_shape = []
                    second_shape.append([original_point[0]+points_lookup_table[point_inside[0]][0],original_point[1]+points_lookup_table[point_inside[0]][1],original_point[2] + 0.5])
                    second_shape.append([original_point[0]+points_lookup_table[point_inside[1]][0],original_point[1]+0.5,original_point[2] + points_lookup_table[point_inside[1]][2]])
                    second_shape.append([original_point[0]+0.5,original_point[1]+points_lookup_table[point_inside[3]][1],original_point[2] + points_lookup_table[point_inside[3]][2]])
                    meshes.append(second_shape)
                    third_shape = []
                    third_shape.append([original_point[0]+points_lookup_table[point_inside[0]][0],original_point[1]+points_lookup_table[point_inside[0]][1],original_point[2] + 0.5])
                    third_shape.append([original_point[0]+0.5,original_point[1]+points_lookup_table[point_inside[3]][1],original_point[2] + points_lookup_table[point_inside[3]][2]])
                    third_shape.append([original_point[0]+points_lookup_table[point_inside[3]][0],original_point[1]+0.5,original_point[2] + points_lookup_table[point_inside[3]][2]])
                    meshes.append(third_shape)
                    fourth_shape = []
                    fourth_shape.append([original_point[0]+0.5,original_point[1]+points_lookup_table[point_inside[3]][1],original_point[2] + points_lookup_table[point_inside[3]][2]])
                    fourth_shape.append([original_point[0]+points_lookup_table[point_inside[1]][0],original_point[1]+0.5,original_point[2] + points_lookup_table[point_inside[1]][2]])
                    fourth_shape.append([original_point[0]+1,original_point[1]+1,original_point[2]+0.5])
                    meshes.append(fourth_shape)
                elif point_inside[1] + 4 == point_inside[3]:
                    first_shape = []
                    first_shape.append([original_point[0]+points_lookup_table[point_inside[0]][0],original_point[1]+0.5,original_point[2]+points_lookup_table[point_inside[2]][1]])
                    first_shape.append([original_point[0]+points_lookup_table[point_inside[2]][0],original_point[1]+points_lookup_table[point_inside[2]][1],original_point[2]+0.5])
                    first_shape.append([original_point[0]+points_lookup_table[point_inside[0]][0],original_point[1]+points_lookup_table[point_inside[0]][1],original_point[2]+0.5])
                    meshes.append(first_shape)
                    second_shape = []
                    second_shape.append([original_point[0]+points_lookup_table[point_inside[0]][0],original_point[1]+0.5,original_point[2]+points_lookup_table[point_inside[2]][1]])
                    second_shape.append([original_point[0]+points_lookup_table[point_inside[0]][0],original_point[1]+points_lookup_table[point_inside[0]][1],original_point[2]+0.5])
                    second_shape.append([original_point[0]+0.5,original_point[1]+points_lookup_table[point_inside[3]][1],original_point[2]+points_lookup_table[point_inside[3]][2]])
                    meshes.append(second_shape)
                    third_shape = []
                    third_shape.append([original_point[0]+0.5,original_point[1]+points_lookup_table[point_inside[3]][1],original_point[2]+points_lookup_table[point_inside[3]][2]])
                    third_shape.append([original_point[0]+points_lookup_table[point_inside[0]][0],original_point[1]+0.5,original_point[2]+points_lookup_table[point_inside[2]][1]])
                    third_shape.append([original_point[0]+0.5,original_point[1]+points_lookup_table[point_inside[1]][1],original_point[2]+points_lookup_table[point_inside[1]][2]])
                    meshes.append(third_shape)
                    fourth_shape = []
                    fourth_shape.append([original_point[0]+points_lookup_table[point_inside[0]][0],original_point[1]+points_lookup_table[point_inside[0]][1],original_point[2]+0.5])
                    fourth_shape.append([original_point[0]+0.5,original_point[1]+points_lookup_table[point_inside[3]][1],original_point[2]+points_lookup_table[point_inside[3]][2]])
                    fourth_shape.append([original_point[0]+points_lookup_table[point_inside[3]][0],original_point[1]+0.5,original_point[2]+points_lookup_table[point_inside[3]][2]])


                    


            # elif [points_in_off_grid_cube_1[0][0]+1,points_in_off_grid_cube_1[0][1],points_in_off_grid_cube_1[0][2]] in point_inside:
            #     if[points_in_off_grid_cube_1[0][0], points_in_off_grid_cube_1[0][1]+1,points_in_off_grid_cube_1[0][2]+1] and [points_in_off_grid_cube_1[0][0]+1,points_in_off_grid_cube_1[0][1]+1,points_in_off_grid_cube_1[0][2]+1]:
            #         first_shape = []
            #         first_shape.append([points_in_off_grid_cube_1[0][0],points_in_off_grid_cube_1[0][1]+0.5,points_in_off_grid_cube_1[0][2]])
            #         first_shape.append([points_in_off_grid_cube_1[0][0],points_in_off_grid_cube_1[0][1],points_in_off_grid_cube_1[0][2]+0.5])
            #         first_shape.append([points_in_off_grid_cube_1[0][0],points_in_off_grid_cube_1[0][1]+1.5,points_in_off_grid_cube_1[0][2]])
            #         first_shape.append([points_in_off_grid_cube_1[0][0],points_in_off_grid_cube_1[0][1],points_in_off_grid_cube_1[0][2]+1.5])
            #         triangle_mesh.append(first_shape)
            #         second_shape = []
            #         second_shape.append([points_in_off_grid_cube_1[0][0], points_in_off_grid_cube_1[0][1]+0.5,points_in_off_grid_cube_1[0][2]+1])
            #         second_shape.append([points_in_off_grid_cube_1[0][0], points_in_off_grid_cube_1[0][1]+1,points_in_off_grid_cube_1[0][2]+0.5])
            #         second_shape.append([points_in_off_grid_cube_1[0][0]+1, points_in_off_grid_cube_1[0][1]+0.5,points_in_off_grid_cube_1[0][2]+1])
            #         second_shape.append([points_in_off_grid_cube_1[0][0]+1, points_in_off_grid_cube_1[0][1]+1,points_in_off_grid_cube_1[0][2]+0.5])
            #         triangle_mesh.append(second_shape)

            # elif [points_in_off_grid_cube_1[0][0]+1,points_in_off_grid_cube_1[0][1]+1, points_in_off_grid_cube_1[0][2]] in point_inside and [points_in_off_grid_cube_1[0][0],points_in_off_grid_cube_1[0][1]+1, points_in_off_grid_cube_1[0][2]+1] in point_inside and [points_in_off_grid_cube_1[0][0]+1,points_in_off_grid_cube_1[0][1], points_in_off_grid_cube_1[0][2]+1] in point_inside:
            #     first_triangle = []
            #     first_triangle.append([points_in_off_grid_cube_1[0][0]+0.5,points_in_off_grid_cube_1[0][1],points_in_off_grid_cube_1[0][2]])
            #     first_triangle.append([points_in_off_grid_cube_1[0][0],points_in_off_grid_cube_1[0][1]+0.5,points_in_off_grid_cube_1[0][2]])
            #     first_triangle.append([points_in_off_grid_cube_1[0][0],points_in_off_grid_cube_1[0][1],points_in_off_grid_cube_1[0][2]+0.5])
            #     triangle_mesh.append(first_triangle)
            #     second_triangle = []
            #     second_triangle.append([points_in_off_grid_cube_1[0][0]+0.5,points_in_off_grid_cube_1[0][1]+1,points_in_off_grid_cube_1[0][2]])
            #     second_triangle.append([points_in_off_grid_cube_1[0][0]+1,points_in_off_grid_cube_1[0][1]+0.5,points_in_off_grid_cube_1[0][2]])
            #     second_triangle.append([points_in_off_grid_cube_1[0][0]+0.5,points_in_off_grid_cube_1[0][1]+1,points_in_off_grid_cube_1[0][2]])
            #     triangle_mesh.append(second_triangle)
            #     third_triangle = []
            #     third_triangle.append([points_in_off_grid_cube_1[0][0]+0.5,points_in_off_grid_cube_1[0][1],points_in_off_grid_cube_1[0][2]+1])
            #     third_triangle.append([points_in_off_grid_cube_1[0][0]+1,points_in_off_grid_cube_1[0][1]+0.5,points_in_off_grid_cube_1[0][2]+1])
            #     third_triangle.append([points_in_off_grid_cube_1[0][0]+1,points_in_off_grid_cube_1[0][1],points_in_off_grid_cube_1[0][2]+0.5])
            #     triangle_mesh.append(third_triangle)
            #     fourth_triangle = []
            #     fourth_triangle.append([points_in_off_grid_cube_1[0][0],points_in_off_grid_cube_1[0][1]+0.5,points_in_off_grid_cube_1[0][2]+1])
            #     fourth_triangle.append([points_in_off_grid_cube_1[0][0]+0.5,points_in_off_grid_cube_1[0][1]+1,points_in_off_grid_cube_1[0][2]+1])
            #     fourth_triangle.append([points_in_off_grid_cube_1[0][0],points_in_off_grid_cube_1[0][1]+1,points_in_off_grid_cube_1[0][2]+0.5])
            #     triangle_mesh.append(fourth_triangle)

            # elif [points_in_off_grid_cube_1[0][0] + 1, points_in_off_grid_cube_1[0][1],points_in_off_grid_cube_1[0][2]] in point_inside and [points_in_off_grid_cube_1[0][0], points_in_off_grid_cube_1[0][1]+1,points_in_off_grid_cube_1[0][2]] in point_inside:
            #     if [points_in_off_grid_cube_1[0][0], points_in_off_grid_cube_1[0][1], points_in_off_grid_cube_1[0][2]+1] in point_inside:
            #         first_shape = []
            #         first_shape.append([points_in_off_grid_cube_1[0][0]+1,points_in_off_grid_cube_1[0][1]+0.5,points_in_off_grid_cube_1])
            #         first_shape.append([points_in_off_grid_cube_1[0][0]+0.5,points_in_off_grid_cube_1[0][1]+1,points_in_off_grid_cube_1[0][2]])
            #         first_shape.append([points_in_off_grid_cube_1[0][0],points_in_off_grid_cube_1[0][1]+1,points_in_off_grid_cube_1[0][2]+0.5])
            #         triangle_mesh.append(first_shape)
            #         second_shape = []
            #         second_shape.append([points_in_off_grid_cube_1[0][0]+1,points_in_off_grid_cube_1[0][1]+0.5,points_in_off_grid_cube_1[0][2]])
            #         second_shape.append([points_in_off_grid_cube_1[0][0],points_in_off_grid_cube_1[0][1]+1,points_in_off_grid_cube_1[0][2]+0.5])
            #         second_shape.append([points_in_off_grid_cube_1[0][1],points_in_off_grid_cube_1[0][1]+0.5],points_in_off_grid_cube_1[0][2]+1)
            #         triangle_mesh.append(second_shape)
            #         third_shape = []
            #         third_shape.append([points_in_off_grid_cube_1[0][0]+1,points_in_off_grid_cube_1[0][1]+0.5,points_in_off_grid_cube_1[0][2]])
            #         third_shape.append([points_in_off_grid_cube_1[0][1],points_in_off_grid_cube_1[0][1]+0.5],points_in_off_grid_cube_1[0][2]+1)
            #         third_shape.append([points_in_off_grid_cube_1[0][0]+1,points_in_off_grid_cube_1[0][1],points_in_off_grid_cube_1[0][2]+0.5])
            #         triangle_mesh.append(third_shape)
            #         fourth_shape = []
            #         fourth_shape.append([points_in_off_grid_cube_1[0][1],points_in_off_grid_cube_1[0][1]+0.5],points_in_off_grid_cube_1[0][2]+1)
            #         fourth_shape.append([points_in_off_grid_cube_1[0][0]+1,points_in_off_grid_cube_1[0][1],points_in_off_grid_cube_1[0][2]+0.5])
            #         fourth_shape.append([points_in_off_grid_cube_1[0][0]+0.5,points_in_off_grid_cube_1[0][1],points_in_off_grid_cube_1[0][2]+1])
            #         triangle_mesh.append(fourth_shape)
                
            #     elif [points_in_off_grid_cube_1[0][0]+1,points_in_off_grid_cube_1[0][1]+1,points_in_off_grid_cube_1[0][2]+1] in point_inside:
            #         first_shape = []
            #         first_shape.append([points_in_off_grid_cube_1[0][0]+0.5,points_in_off_grid_cube_1[0][1]+1,points_in_off_grid_cube_1[0][2]+1])
            #         first_shape.append([points_in_off_grid_cube_1[0][0]+1,points_in_off_grid_cube_1[0][1]+0.5,points_in_off_grid_cube_1[0][2]+1])
            #         first_shape.append([points_in_off_grid_cube_1[0][0]+1,points_in_off_grid_cube_1[0][1]+1,points_in_off_grid_cube_1[0][2]+0.5])
            #         triangle_mesh.append(first_shape)
            #         second_shape = []
            #         second_shape.append([points_in_off_grid_cube_1[0][0],points_in_off_grid_cube_1[0][1],points_in_off_grid_cube_1[0][2]+0.5])
            #         second_shape.append([points_in_off_grid_cube_1[0][0]+1,points_in_off_grid_cube_1[0][1],points_in_off_grid_cube_1[0][2]+0.5])
            #         second_shape.append([points_in_off_grid_cube_1[0][0],points_in_off_grid_cube_1[0][1]+1,points_in_off_grid_cube_1[0][2]+0.5])
            #         triangle_mesh.append(second_shape)
            #         third_shape = []
            #         third_shape.append([points_in_off_grid_cube_1[0][0]+1,points_in_off_grid_cube_1[0][1],points_in_off_grid_cube_1[0][2]+0.5])
            #         third_shape.append([points_in_off_grid_cube_1[0][0],points_in_off_grid_cube_1[0][1]+1,points_in_off_grid_cube_1[0][2]+0.5])
            #         third_shape.append([points_in_off_grid_cube_1[0][0]+1,points_in_off_grid_cube_1[0][1]+0.5,points_in_off_grid_cube_1[0][2]])
            #         triangle_mesh.append(third_shape)
            #         fourth_shape = []
            #         fourth_shape.append([points_in_off_grid_cube_1[0][0]+1,points_in_off_grid_cube_1[0][1]+0.5,points_in_off_grid_cube_1[0][2]])
            #         fourth_shape.append([points_in_off_grid_cube_1[0][0]+0.5,points_in_off_grid_cube_1[0][1]+1,points_in_off_grid_cube_1[0][2]])
            #         fourth_shape.append([points_in_off_grid_cube_1[0][0],points_in_off_grid_cube_1[0][1]+1,points_in_off_grid_cube_1[0][2]+0.5])
            #         triangle_mesh.append(fourth_shape)
                
            #     elif [points_in_off_grid_cube_1[0][0],points_in_off_grid_cube_1[0][1]+1,points_in_off_grid_cube_1[0][2]+1] in point_inside:
            #         first_shape = []
            #         first_shape.append([points_in_off_grid_cube_1[0][0]+1,points_in_off_grid_cube_1[0][1]+0.5,points_in_off_grid_cube_1[0][2]])
            #         first_shape.append([points_in_off_grid_cube_1[0][0]+0.5,points_in_off_grid_cube_1[0][1]+1,points_in_off_grid_cube_1[0][2]])
            #         first_shape.append([points_in_off_grid_cube_1[0][0]+0.5,points_in_off_grid_cube_1[0][1]+1,points_in_off_grid_cube_1[0][2]+1])
            #         triangle_mesh.append(first_shape)
            #         second_shape = []
            #         second_shape.append([points_in_off_grid_cube_1[0][0]+1,points_in_off_grid_cube_1[0][1]+0.5,points_in_off_grid_cube_1[0][2]])
            #         second_shape.append([points_in_off_grid_cube_1[0][0]+0.5,points_in_off_grid_cube_1[0][1]+1,points_in_off_grid_cube_1[0][2]+1])
            #         second_shape.append([points_in_off_grid_cube_1[0][0],points_in_off_grid_cube_1[0][1],points_in_off_grid_cube_1[0][2]+0.5])
            #         triangle_mesh.append(second_shape)
            #         third_shape = []
            #         third_shape.append([points_in_off_grid_cube_1[0][0]+0.5,points_in_off_grid_cube_1[0][1]+1,points_in_off_grid_cube_1[0][2]+1])
            #         third_shape.append([points_in_off_grid_cube_1[0][0],points_in_off_grid_cube_1[0][1],points_in_off_grid_cube_1[0][2]+0.5])
            #         third_shape.append([points_in_off_grid_cube_1[0][0],points_in_off_grid_cube_1[0][1]+0.5,points_in_off_grid_cube_1[0][2]+1])
            #         triangle_mesh.append(third_shape)
            #         fourth_shape = []
            #         fourth_shape.append([points_in_off_grid_cube_1[0][0]+1,points_in_off_grid_cube_1[0][1]+0.5,points_in_off_grid_cube_1[0][2]])
            #         fourth_shape.append([points_in_off_grid_cube_1[0][0],points_in_off_grid_cube_1[0][1],points_in_off_grid_cube_1[0][2]+0.5])
            #         fourth_shape.append([points_in_off_grid_cube_1[0][0]+1,points_in_off_grid_cube_1[0][1],points_in_off_grid_cube_1[0][2]+0.5])
            #         triangle_mesh.append[fourth_shape]

            #     elif [points_in_off_grid_cube_1[0][0]+1,points_in_off_grid_cube_1[0][1],points_in_off_grid_cube_1[0][2]+1] in point_inside:
            #         first_shape = []
            #         first_shape.append([points_in_off_grid_cube_1[0][0]+1,points_in_off_grid_cube_1[0][1]+0.5,points_in_off_grid_cube_1[0][2]])
            #         first_shape.append([points_in_off_grid_cube_1[0][0]+0.5,points_in_off_grid_cube_1[0][1]+1,points_in_off_grid_cube_1[0][2]])
            #         first_shape.append([points_in_off_grid_cube_1[0][0]+1,points_in_off_grid_cube_1[0][1]+0.5,points_in_off_grid_cube_1[0][2]+1])
            #         triangle_mesh.append(first_shape)
            #         second_shape = []
            #         second_shape.append([points_in_off_grid_cube_1[0][0]+0.5,points_in_off_grid_cube_1[0][1]+1,points_in_off_grid_cube_1[0][2]])
            #         second_shape.append([points_in_off_grid_cube_1[0][0]+1,points_in_off_grid_cube_1[0][1]+0.5,points_in_off_grid_cube_1[0][2]+1])
            #         second_shape.append([points_in_off_grid_cube_1[0][0,points_in_off_grid_cube_1[0][1],points_in_off_grid_cube_1[0][2]+0.5]])
            #         triangle_mesh.append(second_shape)
            #         third_shape = []
            #         third_shape.append([points_in_off_grid_cube_1[0][0]+1,points_in_off_grid_cube_1[0][1]+0.5,points_in_off_grid_cube_1[0][2]+1])
            #         third_shape.append([points_in_off_grid_cube_1[0][0],points_in_off_grid_cube_1[0][1],points_in_off_grid_cube_1[0][2]+0.5])
            #         third_shape.append([points_in_off_grid_cube_1[0][0]+0.5, points_in_off_grid_cube_1[0][1],points_in_off_grid_cube_1[0][2]+1])
            #         triangle_mesh.append(third_shape)
            #         fourth_shape = []
            #         fourth_shape.append([points_in_off_grid_cube_1[0][0]+0.5,points_in_off_grid_cube_1[0][1]+1,points_in_off_grid_cube_1[0][2]])
            #         fourth_shape.append([points_in_off_grid_cube_1[0][0],points_in_off_grid_cube_1[0][1],points_in_off_grid_cube_1[0][2]+0.5])
            #         fourth_shape.append([points_in_off_grid_cube_1[0][0],points_in_off_grid_cube_1[0][1]+1,points_in_off_grid_cube_1[0][2]+0.5])
            #         triangle_mesh.append(fourth_shape)


    return meshes
completed_points = []
point_set = []
triangle_mesh = []

point = [cube_list[0][0],cube_list[0][1],cube_list[0][2]]
points_in_off_grid_cube_1 = get_set_of_points_of_cube(point)
point_set.append(points_in_off_grid_cube_1)
list_point_inside_cubelist = get_inside_point_cube_list(cube_list, points_in_off_grid_cube_1)
print(len(list_point_inside_cubelist))

cube = cube_analyzer(point,list_point_inside_cubelist)
for p in cube: 

    triangle_mesh.append(p)

print(triangle_mesh)

# for i in range(3):

#     cube1 = cube_list[i]
    
#     off_grid_cubes = []
#     off_grid_cubes.append([cube1[0]-1,cube1[1]-1,cube1[2]-1]) #shifted
#     off_grid_cubes.append([cube1[0]-1,cube1[1],cube1[2]-1])
#     off_grid_cubes.append([cube1[0],cube1[1],cube1[2]-1])
#     off_grid_cubes.append([cube1[0],cube1[1]-1,cube1[2]-1])
#     off_grid_cubes.append([cube1[0]-1,cube1[1]-1,cube1[2]]) #wrong
#     off_grid_cubes.append([cube1[0]-1,cube1[1],cube1[2]])
#     off_grid_cubes.append([cube1[0],cube1[1],cube1[2]])
#     off_grid_cubes.append([cube1[0],cube1[1]-1,cube1[2]])
#     for point in off_grid_cubes:
#         if point in completed_points:
#             continue
#         else:
#             completed_points.append(point)
#         points_in_off_grid_cube_1 = get_set_of_points_of_cube(point)
#         point_set.append(points_in_off_grid_cube_1)
#         list_point_inside_cubelist = get_inside_point_cube_list(cube_list, points_in_off_grid_cube_1)
#         cube = cube_analyzer(point,list_point_inside_cubelist)
#         for p in cube: 

#             triangle_mesh.append(p)

fig = plt.figure(figsize=(8, 6))
ax = plt.axes(projection='3d')
ax.scatter(cube_list[0][0],cube_list[0][1],cube_list[0][2], c = "red")
ax.scatter(cube_list[1][0],cube_list[1][1],cube_list[1][2], c = "orange")
ax.scatter(cube_list[2][0],cube_list[2][1],cube_list[2][2], c = "purple")
ax.scatter(cube_list[3][0],cube_list[3][1],cube_list[3][2], c = "black")
plt.xlabel('x')
plt.ylabel('y')
ax.set_xlim(0, 3)
ax.set_ylim(25, 28)
ax.set_zlim(80,83)


for i in range(len(triangle_mesh)):
    plt.plot([triangle_mesh[i][0][0],triangle_mesh[i][1][0],triangle_mesh[i][2][0],triangle_mesh[i][0][0]],[triangle_mesh[i][0][1],triangle_mesh[i][1][1],triangle_mesh[i][2][1],triangle_mesh[i][0][1]],[triangle_mesh[i][0][2],triangle_mesh[i][1][2],triangle_mesh[i][2][2],triangle_mesh[i][0][2]],'bo',linestyle="-",c = "green")
    plt.fill()

# plt.plot([points_in_off_grid_cube_1[0][0],points_in_off_grid_cube_1[1][0]],[points_in_off_grid_cube_1[0][1],points_in_off_grid_cube_1[1][1]],[points_in_off_grid_cube_1[0][2],points_in_off_grid_cube_1[1][2]],'bo',linestyle="--")
# plt.plot([points_in_off_grid_cube_1[1][0],points_in_off_grid_cube_1[2][0]],[points_in_off_grid_cube_1[1][1],points_in_off_grid_cube_1[2][1]],[points_in_off_grid_cube_1[1][2],points_in_off_grid_cube_1[2][2]],'bo',linestyle="--")
# plt.plot([points_in_off_grid_cube_1[2][0],points_in_off_grid_cube_1[3][0]],[points_in_off_grid_cube_1[2][1],points_in_off_grid_cube_1[3][1]],[points_in_off_grid_cube_1[2][2],points_in_off_grid_cube_1[3][2]],'bo',linestyle="--")
# plt.plot([points_in_off_grid_cube_1[3][0],points_in_off_grid_cube_1[0][0]],[points_in_off_grid_cube_1[3][1],points_in_off_grid_cube_1[0][1]],[points_in_off_grid_cube_1[3][2],points_in_off_grid_cube_1[0][2]],'bo',linestyle="--")
# plt.plot([points_in_off_grid_cube_1[0][0],points_in_off_grid_cube_1[4][0]],[points_in_off_grid_cube_1[0][1],points_in_off_grid_cube_1[4][1]],[points_in_off_grid_cube_1[0][2],points_in_off_grid_cube_1[4][2]],'bo',linestyle="--")
# plt.plot([points_in_off_grid_cube_1[1][0],points_in_off_grid_cube_1[5][0]],[points_in_off_grid_cube_1[1][1],points_in_off_grid_cube_1[5][1]],[points_in_off_grid_cube_1[1][2],points_in_off_grid_cube_1[5][2]],'bo',linestyle="--")
# plt.plot([points_in_off_grid_cube_1[2][0],points_in_off_grid_cube_1[6][0]],[points_in_off_grid_cube_1[2][1],points_in_off_grid_cube_1[6][1]],[points_in_off_grid_cube_1[2][2],points_in_off_grid_cube_1[6][2]],'bo',linestyle="--")
# plt.plot([points_in_off_grid_cube_1[3][0],points_in_off_grid_cube_1[7][0]],[points_in_off_grid_cube_1[3][1],points_in_off_grid_cube_1[7][1]],[points_in_off_grid_cube_1[3][2],points_in_off_grid_cube_1[7][2]],'bo',linestyle="--")
# plt.plot([points_in_off_grid_cube_1[4][0],points_in_off_grid_cube_1[5][0]],[points_in_off_grid_cube_1[4][1],points_in_off_grid_cube_1[5][1]],[points_in_off_grid_cube_1[4][2],points_in_off_grid_cube_1[5][2]],'bo',linestyle="--")
# plt.plot([points_in_off_grid_cube_1[5][0],points_in_off_grid_cube_1[6][0]],[points_in_off_grid_cube_1[5][1],points_in_off_grid_cube_1[6][1]],[points_in_off_grid_cube_1[5][2],points_in_off_grid_cube_1[6][2]],'bo',linestyle="--")
# plt.plot([points_in_off_grid_cube_1[6][0],points_in_off_grid_cube_1[7][0]],[points_in_off_grid_cube_1[6][1],points_in_off_grid_cube_1[7][1]],[points_in_off_grid_cube_1[6][2],points_in_off_grid_cube_1[7][2]],'bo',linestyle="--")
# plt.plot([points_in_off_grid_cube_1[7][0],points_in_off_grid_cube_1[4][0]],[points_in_off_grid_cube_1[7][1],points_in_off_grid_cube_1[4][1]],[points_in_off_grid_cube_1[7][2],points_in_off_grid_cube_1[4][2]],'bo',linestyle="--")

# for set in point_set:
#     plt.plot([set[0][0],set[1][0]],[set[0][1],set[1][1]],[set[0][2],set[1][2]],'bo',linestyle="--")
#     plt.plot([set[1][0],set[2][0]],[set[1][1],set[2][1]],[set[1][2],set[2][2]],'bo',linestyle="--")
#     plt.plot([set[2][0],set[3][0]],[set[2][1],set[3][1]],[set[2][2],set[3][2]],'bo',linestyle="--")
#     plt.plot([set[3][0],set[0][0]],[set[3][1],set[0][1]],[set[3][2],set[0][2]],'bo',linestyle="--")
#     plt.plot([set[0][0],set[4][0]],[set[0][1],set[4][1]],[set[0][2],set[4][2]],'bo',linestyle="--")
#     plt.plot([set[1][0],set[5][0]],[set[1][1],set[5][1]],[set[1][2],set[5][2]],'bo',linestyle="--")
#     plt.plot([set[2][0],set[6][0]],[set[2][1],set[6][1]],[set[2][2],set[6][2]],'bo',linestyle="--")
#     plt.plot([set[3][0],set[7][0]],[set[3][1],set[7][1]],[set[3][2],set[7][2]],'bo',linestyle="--")
#     plt.plot([set[4][0],set[5][0]],[set[4][1],set[5][1]],[set[4][2],set[5][2]],'bo',linestyle="--")
#     plt.plot([set[5][0],set[6][0]],[set[5][1],set[6][1]],[set[5][2],set[6][2]],'bo',linestyle="--")
#     plt.plot([set[6][0],set[7][0]],[set[6][1],set[7][1]],[set[6][2],set[7][2]],'bo',linestyle="--")
#     plt.plot([set[7][0],set[4][0]],[set[7][1],set[4][1]],[set[7][2],set[4][2]],'bo',linestyle="--")
plt.show()