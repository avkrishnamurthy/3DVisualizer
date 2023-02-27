from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import numpy as np
from math import *
from Model import Object3D

class ShadedObject3D(Object3D):
    def __init__(self, points, faces, edge_vertex_color):
        super().__init__(points, faces, edge_vertex_color)
        self.xyzprojection = [None] * len(points)

    def project(self, window_scale, window_center):
        #Matrices to update x and y based on the x, y angle rotation
        x_rotation_matrix = np.matrix([
            [1, 0, 0],
            [0, cos(self.xangle), -sin(self.xangle)],
            [0, sin(self.xangle), cos(self.xangle)],
        ])
        y_rotation_matrix = np.matrix([
            [cos(self.yangle), 0, sin(self.yangle)],
            [0, 1, 0],
            [-sin(self.yangle), 0, cos(self.yangle)],
        ])

        #Projecting x, y, z for each point into 2d, accounting for x, y rotation, and window scale and center
        for i, point in enumerate(self.points):
            #Matrix-vector multiplication to account for changes in y rotation
            yrotated = np.dot(y_rotation_matrix, point.reshape((3, 1)))
            #Matrix-vector multiplication to account for changes in x rotation
            xyrotated = np.dot(x_rotation_matrix, yrotated)
            #Projecting x, y, z to x,y (removing zth)
            projection = np.dot(self.proj_matrix, xyrotated)
            #Accounting for scale of window and center of window to make origin in middle of window
            x = float(projection[0][0] * window_scale) + window_center[0]
            y = float(projection[1][0] * window_scale) + window_center[1]
            z = float(xyrotated[2][0]*window_scale)
            #Need projected_points just for graphing the projection of x and y to the window
            self.xyprojection[i] = [x, y]
            #Need to keep z for shading (need to know changes in z when rotating with click and drag)
            self.xyzprojection[i] = [x, y, z]

    def shade_faces(self, screen):
        #Calculating unit normal vector of face
        def get_unit_normal(v1, v2, v3, points):
            #Calculating vectors making up two edges of a face
            edge1 = np.subtract(points[v2],points[v1])
            edge2 = np.subtract(points[v3],points[v1])
            #Taking their cross product to get the normal vector of the face
            normal = (np.cross(edge1, edge2))
            #Returning the unit normal vector to simplify downstream calculations with dot product
            return normal/np.linalg.norm(normal)

        #Calculating angle of face's normal vector with z-axis
        def get_angle_z(unit_normal):
            #Taking the dot product of the normal vector with vector for the z-axis
            dot_product = np.dot(unit_normal, np.array([0, 0, 1]))
            #Cosine formula for the dot product to get the angle between the z-axis and face's normal vector
            angle = acos(dot_product)

            #Bounding the angle to be within pi/2 to ensure that a face that
            #makes an angle of 3pi/4 with the z-axis is considered the same as a face that
            #makes an angle of pi/4 with the z-axis for shading purposes
            if (angle > (pi/2)): angle = pi-angle
            return angle
        
        #Getting vertices associated with current face
        for face in self.faces:
            vert_1 = face[0]
            vert_2 = face[1]
            vert_3 = face[2]

            #Calculate normal vector of face
            normal = get_unit_normal(vert_1, vert_2, vert_3, self.xyzprojection)
            #Get angle of normal vector with z-axis
            angle = get_angle_z(normal)
            #Range of values that angle can take
            value_range = [0, pi/2]
            #Range of colors to map to from angle
            color_range = [(0, 0, 255), (0, 0, 95)]
            #Using interpolation to make color vary smoothly between color range for values in angle range 
            color = tuple(int(np.interp(angle, value_range, color_channel_range)) for color_channel_range in zip(*color_range))

            #For testing
            #print(color)

            #Using pygame draw polygon to draw the face with the corresponding color
            pygame.draw.polygon(screen, color, [self.xyprojection[vert_1], self.xyprojection[vert_2], self.xyprojection[vert_3]])