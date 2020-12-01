  
import numpy as np
from OpenGL.GL import *
import random

import lib.basic_shapes as bs
import lib.easy_shaders as es
import lib.transformations as tr

class head():
    def __init__(self):
        self.x, self.y = 0, 0
        self.angle = 0
        self.bend= 0.085
        self.front = 0.1
        self.turn = 0

        ran=str(random.randint(1,4))

        self.GPUsnake=(es.toGPUShape(bs.generateTextureSphere(7,7,"models/snake"+ran+".png"), GL_REPEAT, GL_LINEAR))
        self.transform = tr.matmul([tr.translate(0.0,0.0,1.5),tr.uniformScale(0.5),tr.rotationZ(self.angle)])
    def draw(self, texture_pipeline, view, projection):
        glUseProgram(texture_pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(texture_pipeline.shaderProgram, "model"), 1, GL_TRUE, self.transform)
        glUniformMatrix4fv(glGetUniformLocation(texture_pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(texture_pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        texture_pipeline.drawShape(self.GPUsnake)
    
    def move(self):
        self.x += self.front*np.cos(self.angle)
        self.y += self.front*np.sin(self.angle)
        self.transform = tr.matmul([tr.translate(self.x,self.y,1.5),tr.uniformScale(0.5),tr.rotationZ(self.angle)])
    def update(self):
        self.angle += self.bend*self.turn

class body():
    def __init__(self):
        self.x , self.y = 0,0
        self.angle = 0
        ran=str(random.randint(1,4))

        self.GPUsnake=(es.toGPUShape(bs.generateTextureSphere(7,7,"models/snake"+ran+".png"), GL_REPEAT, GL_LINEAR))
        self.transform = tr.matmul([tr.translate(self.x,self.y,1.5),tr.uniformScale(0.5),tr.rotationZ(self.angle)])
    
    def draw(self, texture_pipeline, view, projection):
        glUseProgram(texture_pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(texture_pipeline.shaderProgram, "model"), 1, GL_TRUE, self.transform)
        glUniformMatrix4fv(glGetUniformLocation(texture_pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(texture_pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        texture_pipeline.drawShape(self.GPUsnake)
    
    def move(self):
        self.transform = tr.matmul([tr.translate(self.x,self.y,1.5),tr.uniformScale(0.5),tr.rotationZ(self.angle)])

class snake():
    def __init__(self):
        self.snake_list=[
            head(),body(),body(),body(),body(),
            body(),body(),body(),body(),body(),
            body(),body(),body(),body(),body(),
            body(),body(),body(),body(),body(),
            body(),body(),body(),body(),body(),
            body(),body(),body(),body(),body(),
            body(),body(),body(),body(),body(),
            body(),body(),body(),body(),body(),
            body(),body(),body(),body(),body()]

        self.snake_list[1].x=-0.3
        self.snake_list[1].move()
        i=1
        for part in self.snake_list[2:]:
            part.x+=-0.3*i
            part.move()
            i+=1

    def draw(self, texture_pipeline, view, projection):
        for element in self.snake_list:
            element.draw(texture_pipeline, view, projection)
   
    def grow(self):
        self.snake_list[0].front+=0.005
        self.snake_list[0].bend+= 0.0011




    def move_snake(self):
        i=len(self.snake_list)-1
        while i>0:
            x=self.snake_list[i-1].x
            y=self.snake_list[i-1].y
            angle=self.snake_list[i-1].angle
            self.snake_list[i].x=x
            self.snake_list[i].y=y
            self.snake_list[i].angle=angle
            self.snake_list[i].move()
            i-=1
        self.snake_list[0].move()


""" class Snake():
    
    def __init__(self):
        self.x, self.y = 0, 0
        self.theta = 0
        self.bend = 0.10
        self.front = 0.075
        self.turn = 0
        self.GPU = es.toGPUShape(bs.createTextureCube('models/floor.png'), GL_REPEAT, GL_NEAREST)
        self.transform = tr.matmul([tr.translate(0.0,0.0,-8.0),tr.uniformScale(30),tr.rotationZ(self.theta)])
    
    def draw(self, texture_pipeline, projection, view):
        glUseProgram(texture_pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(texture_pipeline.shaderProgram, "model"), 1, GL_TRUE, self.transform)
        glUniformMatrix4fv(glGetUniformLocation(texture_pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(texture_pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        texture_pipeline.drawShape(self.GPU)
    def move(self):
        self.x += self.front*np.cos(self.theta)
        self.y += self.front*np.sin(self.theta)
        self.transform = tr.matmul([tr.translate(self.x,self.y,-8.0),tr.uniformScale(2),tr.rotationZ(self.theta)])
    def update(self):
        self.theta += self.bend*self.turn """