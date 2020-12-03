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

    width = 1000
    height = 900

    window = glfw.create_window(width, height, "SNAKE 3D", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    reset=False
    jungle=jungle()
    jungle_floor=jungle_floor()
    floor=floor()
    food=food()
    Snake=snake()
    cabeza=Snake.snake_list[0]
    game_over=game_over()

    controller=Controller(Snake)
    
    
    glfw.set_key_callback(window, controller.on_key)

    # Connecting the callback function 'on_key' to handle keyboard events

    # Assembling the shader program (pipeline) with both shaders
    pipeline = es.SimpleModelViewProjectionShaderProgram()
    texture_pipeline = es.SimpleTextureModelViewProjectionShaderProgram()
    obj_pipeline = ls.SimpleTextureGouraudShaderProgram()
    light_pipeline=ls.SimpleFlatShaderProgram()

 
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
        time=glfw.get_time()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        if ((Snake.snake_list[0].x)>=(food.x)-0.85 
        and (Snake.snake_list[0].x)<=(food.x)+0.85 
        and (Snake.snake_list[0].y)>=(food.y)-0.85 
        and (Snake.snake_list[0].y)<=(food.y)+0.85):
            food.change_position()
            Snake.grow()
        
        if Snake.live==False:
            glUseProgram(light_pipeline.shaderProgram)
            game_over.draw(light_pipeline,projection,time)

            camara=tr.lookAt(
                np.array([game_over.x+30,game_over.y, game_over.z+10]),
                np.array([game_over.x, game_over.y, game_over.z]),
                np.array([0,0,1]))

            glUseProgram(texture_pipeline.shaderProgram)
            jungle.draw(texture_pipeline, camara ,projection)
            jungle_floor.draw(texture_pipeline, camara ,projection)

            glUseProgram(obj_pipeline.shaderProgram)
            floor.draw(obj_pipeline, camara ,projection,food.x,food.y,0.2+np.abs(0.7*(np.sin(2*np.pi*time/60))))

        else:
            camara=controller.camera()

            glUseProgram(texture_pipeline.shaderProgram)

            Snake.snake_list[0].move()
            Snake.snake_list[0].update()
            Snake.move_snake()
      
            Snake.draw(texture_pipeline, camara ,projection)
            jungle.draw(texture_pipeline, camara ,projection)
            jungle_floor.draw(texture_pipeline, camara ,projection)
        
            glUseProgram(obj_pipeline.shaderProgram)
            cabeza.draw(obj_pipeline, camara ,projection)
            food.draw(obj_pipeline, camara ,projection,np.abs(0.4*(np.sin(2*np.pi*time/60))),time)
            floor.draw(obj_pipeline, camara ,projection,food.x,food.y,0.2+np.abs(0.7*(np.sin(2*np.pi*time/60))))

            Snake.die()
        
        
       
        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    
    glfw.terminate()