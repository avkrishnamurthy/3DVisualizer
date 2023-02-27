from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import numpy as np
import argparse
from math import *
from pynput.mouse import Listener, Button, Controller
from Model import Object3D
from ShadedModel import ShadedObject3D

#Window size
WIDTH, HEIGHT = 800, 600
#Window center
CENTER = [WIDTH/2, HEIGHT/2]

#Edge/Vertex Color
BLUE = (0, 0, 255)
#Screen color
WHITE = (255, 255, 255)

#Mouse object used for click and drag rotation
mouse = Controller()
#Boolean for if mouse is currently being left clicked
mouseDown = False
#pynput function to determine if mouse is being left clicked

def on_click(*args):
    global mouseDown
    if args[-1] and args[-2].name == 'left':
        mouseDown = True
    elif not args[-1] and args[-2].name == 'left':
        mouseDown = False

#Function to parse object file into lists of points and faces
def parse_file(file):
    #Opening object file
    with open(file) as f:
        #Reading first line and splitting by comma to get the num vertices and faces
        verts_faces = (f.readline()).split(",")
        num_vertex = int(verts_faces[0])
        num_faces = int(verts_faces[1])
        max_length = 0
        #Reading through num_vertex lines and creating a vector of x, y, and z coordinates for each vertex
        o_points = [None]*(num_vertex)
        for i in range(num_vertex):
            #Splitting by ',' to easily parse x, y, z
            data = (f.readline()).split(",")
            x = float(data[1])
            y = float(data[2])
            z = float(data[3])
            max_length = max(abs(x-y), abs(x-z), (abs(y-z)), max_length)
            #Negating y to make positive y axis upwards
            o_points[i] = np.matrix([x, -y, z])

        #Reading through num_faces lines and adding tuples of the vertex numbers to the o_faces list
        o_faces = []
        for i in range(num_faces):
            data = (f.readline()).split(",")
            #Subtracting 1 from each vertex number to have it match the indexes of an array (specifically for o_points)
            o_faces.append((int(data[0])-1, int(data[1])-1, int(data[2])-1))
        f.close()
    return o_points, o_faces, max_length

#Parse command line input
def parse_cl():
    parser = argparse.ArgumentParser(description='Run main')
    parser.add_argument('-i', '--input',
                    help='Object Text File', default='object.txt')
    parser.add_argument("--shaded", action="store_true", default=False,
                              help='To view shaded faces')
    args = vars(parser.parse_args())
    return args['input'], args['shaded']

def main():
    #Parsing command line input for object file
    #Opted for this so that user can input whatever file name they want and it will use it
    file, shaded = parse_cl()
    #Parsing object file to get lists of the points and faces
    points, faces, max_length = parse_file(file)

    #Creating my 3D object from the points and faces data
    if shaded:
        my_obj = ShadedObject3D(points, faces, edge_vertex_color=BLUE)
    else:
        my_obj = Object3D(points, faces, edge_vertex_color=BLUE)
    #Set caption
    pygame.display.set_caption("3D Visualization")
    #Creating screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    #Starting pygame clock for window visual fps
    clock = pygame.time.Clock()
    #Used to monitor mouse/cursor data
    with Listener(on_click=on_click) as listener:
        #Initializing cursor position before entering graphical loop
        position = mouse.position
        #Loop to update/display graphics of my object
        while True:
            #Clearing to prevent displaying pre-current-rotation objects
            screen.fill(WHITE)
            #Limiting to 60 fps max
            clock.tick(60)
            #pygame events to end window display/program
            #Escape or closing window stops program
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()

            #If mouse is down, user wants to click and drag to rotate object, so
            if mouseDown: 
                #Calculate new mouse cursor position
                new_position = mouse.position
                #Update new xangle and yangle
                my_obj.click_drag_angle(new_position, position)
                #Update position to match new position (keeping a pointer to the previous cursor position)
                position = new_position

            scale = 200/max_length
            #Determine object projection into 2D
            my_obj.project(scale, CENTER)
            #Shade faces of projected object
            #Doing this before drawing vertices and edges because it makes it much easier to see the shape of the object
            
            if shaded: my_obj.shade_faces(screen)
            #Drawing object vertices and edges
            my_obj.draw_edges(screen)
            my_obj.draw_vertices(screen)
            

            #Updating window display
            pygame.display.update()

if __name__ == '__main__':
    main()


    