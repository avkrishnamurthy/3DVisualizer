from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import numpy as np
from math import *

#Object Class to represent the object obtained from the input object text file
class Object3D:
    def __init__(self, points, faces, edge_vertex_color):
        #List of vertices
        self.points = points
        #List of faces
        self.faces = faces
        #x, y angle of object
        self.xangle = 0
        self.yangle = 0
        #List for x,y projection coordinates accounting for rotation
        self.xyprojection = [None]*len(points)
        #Simple projection matrix to project 3d into 2d
        self.proj_matrix = np.matrix([[1, 0, 0],
                                      [0, 1, 0]])
        #Color of object vertices and edges
        self.edge_vertex_color = edge_vertex_color

    #Function to determine x,y coordinates after projection and rotation
    def project(self, window_scale, window_center):

        #Matrices to update x and y based on the x, y angle rotation
        x_rotation_matrix = np.matrix([[1, 0, 0],
                                       [0, cos(self.xangle), -sin(self.xangle)],
                                       [0, sin(self.xangle), cos(self.xangle)]])
        y_rotation_matrix = np.matrix([[cos(self.yangle), 0, sin(self.yangle)],
                                       [0, 1, 0],
                                       [-sin(self.yangle), 0, cos(self.yangle)]])

        #Projecting x, y, z for each point into 2d, accounting for x, y rotation, and window scale and center
        for i, point in enumerate(self.points):
            #Matrix-vector multiplication to account for changes in y rotation
            yrotated = np.dot(y_rotation_matrix, point.reshape((3, 1)))
            #Matrix-vector multiplication to account for changes in x rotation
            xyrotated = np.dot(x_rotation_matrix, yrotated)
            #Projecting x, y, z to x,y (removing zth)
            projection = np.dot(self.proj_matrix, xyrotated)
            #Accounting for scale of window and center of window to make origin in middle of window
            x = float(projection[0][0]*window_scale ) + window_center[0]
            y = float(projection[1][0]*window_scale ) + window_center[1]
            #Need projected_points just for graphing the projection of x and y to the window
            self.xyprojection[i] = [x, y]

    #Drawing the projected vertex to the window with radius 3
    def draw_vertices(self, screen):
        for point in self.xyprojection:
            pygame.draw.circle(screen, self.edge_vertex_color, (point[0], point[1]), 3)
        
    #Drawing projected edges to the window 
    def draw_edges(self, screen):        
        for face in self.faces:
            #Getting vertices associated with current face
            v1 = face[0]
            v2 = face[1]
            v3 = face[2]
            #Drawing edges of current face
            pygame.draw.line(screen, 
                             self.edge_vertex_color, 
                             (self.xyprojection[v1][0], self.xyprojection[v1][1]), 
                             (self.xyprojection[v2][0], self.xyprojection[v2][1]))
            pygame.draw.line(screen, 
                             self.edge_vertex_color, 
                             (self.xyprojection[v1][0], self.xyprojection[v1][1]), 
                             (self.xyprojection[v3][0], self.xyprojection[v3][1]))
            pygame.draw.line(screen, 
                             self.edge_vertex_color, 
                             (self.xyprojection[v2][0], self.xyprojection[v2][1]), 
                             (self.xyprojection[v3][0], self.xyprojection[v3][1]))

    #Used to calculate the new angle based on the movement of the cursor while the user holds down left click
    def click_drag_angle(self, new_position, position):
        #If mouse cursor has moved right, increase y angle (rotate around y axis to the right)
        if (new_position[0] > (position[0]+1)):
            self.yangle += 0.1
        #If mouse cursor has moved right, increase y angle (rotate around y axis to the right)
        elif (new_position[0] < (position[0]-1)):
            self.yangle -= 0.1
        #If mouse cursor has moved up, decrease x angle (rotate around x axis down)
        #Y axis seems to be flipped for some reason, so doing the opposite
        if (new_position[1] > (position[1]+1)):
            self.xangle -= 0.1
        #If mouse cursor has moved down, increase x angle (rotate around x axis up)
        #Y axis seems to be flipped for some reason, so doing the opposite
        elif (new_position[1] < (position[1]-1)):
            self.xangle += 0.1
        #The +1 and -1 is for margin of error purposes,
        #Seems to make click and drag rotation more smooth from my experience using it
        #0.02 is also the angle value that I determined with trial and error and seeing what worked smoothly