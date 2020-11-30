# coding=utf-8

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys

from models.structure import *
import lib.transformations as tr
import lib.lighting_shaders as ls
import lib.easy_shaders as es
import lib.basic_shapes as bs


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 900
    height = 800

    window = glfw.create_window(width, height, "PATO CUBO", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events

    # Assembling the shader program (pipeline) with both shaders
    pipeline = es.SimpleModelViewProjectionShaderProgram()
    texture_pipeline = es.SimpleTextureModelViewProjectionShaderProgram()
    
    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # Using the same view and projection matrices in the whole application
    projection = tr.perspective(45, float(width)/float(height), 0.1, 100)

    # Generaremos diversas cámaras.
    static_view_1 = tr.lookAt(
            np.array([0,-0.1,70]), # eye
            np.array([0,0,0]), # at
            np.array([0,0,1])  # up
        )

    static_view_2 = tr.lookAt(
            np.array([0,-50,40]), # eye
            np.array([0,0,0]), # at
            np.array([0,0,1])  # up
        )
    
    floor=floor()

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        floor.draw(texture_pipeline,static_view_2, projection)

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    
    glfw.terminate()