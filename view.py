# coding=utf-8

import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import OpenGL.GL.shaders
import numpy as np
import sys
import time

from models.structure import *
from models.snake import *
from lib.controller import *


import lib.transformations as tr
import lib.lighting_shaders as ls
import lib.easy_shaders as es
import lib.basic_shapes as bs
import lib.lighting_shaders as ls


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
    
    floor=floor()
    cabeza=cabeza()
    food=food()
    Snake=snake()

    controller=Controller(Snake.snake_list[0])
    
    
    glfw.set_key_callback(window, controller.on_key)

    # Connecting the callback function 'on_key' to handle keyboard events

    # Assembling the shader program (pipeline) with both shaders
    pipeline = es.SimpleModelViewProjectionShaderProgram()
    texture_pipeline = es.SimpleTextureModelViewProjectionShaderProgram()
    obj_pipeline = ls.SimpleTextureGouraudShaderProgram()

 
    # Telling OpenGL to use our shader program
    glUseProgram(texture_pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # Using the same view and projection matrices in the whole application
    projection = tr.perspective(45, float(width)/float(height), 0.1, 100)

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()
        

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        if ((Snake.snake_list[0].x)>=(food.x)-0.85 
        and (Snake.snake_list[0].x)<=(food.x)+0.85 
        and (Snake.snake_list[0].y)>=(food.y)-0.85 
        and (Snake.snake_list[0].y)<=(food.y)+0.85):
            food.change_position()
            Snake.grow()
        
        
        camara=controller.camera()

        glUseProgram(texture_pipeline.shaderProgram)

        Snake.snake_list[0].move()
        Snake.snake_list[0].update()
        Snake.move_snake()

        food.draw(texture_pipeline, camara ,projection)
        floor.draw(texture_pipeline, camara ,projection)
        Snake.draw(texture_pipeline, camara ,projection)
        

      
        glUseProgram(obj_pipeline.shaderProgram)
        cabeza.draw(obj_pipeline, camara ,projection)
        
       
        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    
    glfw.terminate()