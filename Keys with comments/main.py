from __future__ import division
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GL import shaders
#from OpenGL.GLU import *

from sys import exit as exitsystem

from numpy import array, count_nonzero


from receive_data import *

# Define the serial port and baud rate


WIDTH, HEIGHT = 1920, 1080

zoomOut = 1.001
zoomIn = 0.997
movementSpeed = 0.002
movement_speed_y = 0.002

def ReadFile(filename):
    data = ""
    with open(filename, 'r') as f:
        data = f.read()
    return data

VERTEX_SHADER = ReadFile('./vertexShader.glsl')
FRAGMENT_SHADER = ReadFile('./fragmentShader.glsl')



class Main(object):
    def __init__(self):
        pygame.init()
        self.resolution = WIDTH, HEIGHT
        pygame.display.set_mode(self.resolution, DOUBLEBUF | OPENGL)
        pygame.display.set_caption('PyShadeToy')

        # Shaders
        self.vertex_shader = shaders.compileShader(VERTEX_SHADER, GL_VERTEX_SHADER)
        self.fragment_shader = shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)

        # Shader program which hosts the vertex and fragment shader
        self.shader = shaders.compileProgram(self.vertex_shader, self.fragment_shader)

        # Get the uniform locations
        self.uni_mouse = glGetUniformLocation(self.shader, 'iMouse')
        self.uni_ticks = glGetUniformLocation(self.shader, 'iTime')

        glUseProgram(self.shader)   # Need to be enabled before sending uniform variables
        # Resolution doesn't change. Send it once
        glUniform2f(glGetUniformLocation(self.shader, 'iResolution'), *self.resolution)

        # Define a shape to draw. Then send it to vertexShader.glsl
        # In that case square. Vertex in following points
        # For example if we would have 3 vertex it would be triangle
        self.vertices = array([-1.0, -1.0, 0.0, # x, y, z for vertex 1
                                1.0, -1.0, 0.0, # for vertex 2
                                1.0,  1.0, 0.0, # for vertex 3
                                -1.0, 1.0, 0.0  # for vertex 4
                               ], dtype='float32')

        # VAO and VBO used for manage vetrices
        # Generate VAO
        # VBO is a buffer that stores vertex data (such as positions,
        # normals, texture coordinates, and color):w
        # VAO is an object that encapsulates the state of one or more VBOs
        self.vao = glGenVertexArrays(1) # generate 1 vetex array
        glBindVertexArray(self.vao)

        # Generate VBO which is stored in the VAO state
        self.vbo = glGenBuffers(1) #generates a buffer object ID for a new VBO
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        # populates the VBO with vertex data
        glBufferData(GL_ARRAY_BUFFER, self.vertices, GL_STATIC_DRAW)

        # data can now be supplied to the shader program using this attribute index,
        # index 0 corresponds to the vPos
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)


        # get shader variables
        self.clock = pygame.time.Clock()
        self.CenterX = glGetUniformLocation(self.shader, 'CenterX')
        self.CenterY = glGetUniformLocation(self.shader, 'CenterY')
        self.ZoomScale = glGetUniformLocation(self.shader, 'ZoomScale')
        self.ColorRanges = glGetUniformLocation(self.shader, 'ColorRanges')


    def mainloop(self):

        x, y, z = 0.0, 0.0, 1.0

        #px_data =[WIDTH * HEIGHT, 0.1]

        cr = (0.0001, 0.33333, 0.66667, 1.00)

        i = 0
        j = 0
        while True:
            delta = self.clock.tick(8192)
            glClearColor(0.0, 0.0, 0.0, 1.0)
            glClear(GL_COLOR_BUFFER_BIT)

            #Handle Inputs
            keys = pygame.key.get_pressed()

            # if True: # check if there are new data in the input buffer
            # new_direction = receive_data_from_arduino()
            # previous_directions.append(new_direction)
            # if(len(previous_directions) > 5):
            #     if(len(set(previous_directions)) == 1 and previous_directions[0] != ""):  # all members of set a unique
            #         direction = new_direction
            #     previous_directions = []

            if keys[pygame.K_UP]:
                y = y + movementSpeed * z
                if y > 1.0:
                    y = 1.0

            if keys[pygame.K_DOWN]:
                y = y - movementSpeed * z
                if y < -1.0:
                    y = -1.0

            if keys[pygame.K_LEFT]:
                x = x - movementSpeed * z
                if x < -1.0:
                    x = -1.0

            if keys[pygame.K_RIGHT]:
                x = x + movementSpeed * z
                if x > 1.0:
                    x = 1.0

            if keys[pygame.K_j]:
                z = z * zoomIn
                if z > 1.0:
                    z = 1.0

            if keys[pygame.K_k]:
                z = z * zoomOut
                if z > 1.0:
                    z = 1.

            for event in pygame.event.get():
                if (event.type == QUIT) or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    # ser.close()
                    exitsystem()

            glUseProgram(self.shader)

            # Send uniform values
            glUniform2f(self.uni_mouse, *pygame.mouse.get_pos())
            glUniform1f(self.uni_ticks, pygame.time.get_ticks() / 1000.0)
            glUniform1f(self.CenterX, x)
            glUniform1f(self.CenterY, y)
            glUniform1f(self.ZoomScale, z)
            glUniform4f(self.ColorRanges, *cr)

            # Bind the vao (which stores the VBO with all the vertices)
            glBindVertexArray(self.vao)
            glDrawArrays(GL_QUADS, 0, 4)

            pygame.display.set_caption("FPS: {}".format(self.clock.get_fps()))
            pygame.display.flip()


if __name__ == '__main__':
    # ser.readline()
    time.sleep(1)
    # ser.readline()
    Main().mainloop()
