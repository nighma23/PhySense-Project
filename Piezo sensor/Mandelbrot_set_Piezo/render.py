from __future__ import division
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GL import shaders
# from OpenGL.GLU import *

from sys import exit as exitsystem

from numpy import array, count_nonzero
import time


# Define the serial port and baud rate


WIDTH, HEIGHT = 1920, 1080

zoomOut = 1.003
zoomIn = 0.996
movementSpeed = 0.005
movement_speed_y = 0.005


def ReadFile(filename):
    data = ""
    with open(filename, 'r') as f:
        data = f.read()
    return data


VERTEX_SHADER = ReadFile('./vertexShader.glsl')
FRAGMENT_SHADER = ReadFile('./fragmentShader.glsl')


class Render(object):
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

        # Create the fullscreen quad for drawing
        self.vertices = array([-1.0, -1.0, 0.0,
                                1.0, -1.0, 0.0,
                                1.0,  1.0, 0.0,
                                -1.0, 1.0, 0.0
                               ], dtype='float32')

        # Generate VAO
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        # Generate VBO which is stored in the VAO state
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)


        self.clock = pygame.time.Clock()
        self.CenterX = glGetUniformLocation(self.shader, 'CenterX')
        self.CenterY = glGetUniformLocation(self.shader, 'CenterY')
        self.ZoomScale = glGetUniformLocation(self.shader, 'ZoomScale')
        self.ColorRanges = glGetUniformLocation(self.shader, "ColorRanges")


    def render(self, q):

        x, y, z = 0.0, 0.0, 1.0

        #px_data =[WIDTH * HEIGHT, 0.1]

        cr = (0.0001, 0.33333, 0.66667, 1.00)

        i = 0
        j = 0
        previous_directions = []
        direction = ""
        new_direction = ""
        while True:
            delta = self.clock.tick(8192)
            glClearColor(0.0, 0.0, 0.0, 1.0)
            glClear(GL_COLOR_BUFFER_BIT)

            #Handle Inputs
            keys = pygame.key.get_pressed()

            # if True: # check if there are new data in the input buffer
            if q.qsize() > 0:
                new_direction = q.get()
            if new_direction != "":
                direction = new_direction
            print(f"Redner: {direction=}")


            if keys[pygame.K_UP] or direction == "MoveUp":
                y = y + movementSpeed * z
                if y > 1.0:
                    y = 1.0

            if keys[pygame.K_DOWN] or direction == "MoveDown":
                y = y - movementSpeed * z
                if y < -1.0:
                    y = -1.0

            if keys[pygame.K_LEFT] or direction == "MoveLeft":
                x = x - movementSpeed * z
                if x < -1.0:
                    x = -1.0

            if keys[pygame.K_RIGHT] or direction == "MoveRight":
                x = x + movementSpeed * z
                if x > 1.0:
                    x = 1.0

            if keys[pygame.K_j] or direction == "ZoomIn":
                z = z * zoomIn
                if z > 1.0:
                    z = 1.0

            if keys[pygame.K_k] or direction == "ZoomOut":
                z = z * zoomOut
                if z > 1.0:
                    z = 1.0

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