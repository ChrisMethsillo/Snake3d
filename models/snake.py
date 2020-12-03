  
import numpy as np
from OpenGL.GL import *
import random

import lib.basic_shapes as bs
import lib.easy_shaders as es
import lib.transformations as tr
import lib.obj_handler as obj_reader



class head():
    def __init__(self):
        self.x, self.y = 0, 0
        self.angle = 0
        self.bend= 0.12
        self.front = 0.1
        self.turn = 0

        obj='models/figure/headsnake.obj'
        obj_cabeza=obj_reader.readOBJ2(f'{obj}',"models/textures/snake_skin.png")
        self.gpuOBJ = es.toGPUShape( obj_cabeza , GL_REPEAT, GL_LINEAR)
        self.transform=tr.matmul([tr.translate(self.x,self.y,1.5),tr.uniformScale(0.3),tr.rotationX(3.14/2),tr.rotationY(-3.14/2),tr.rotationZ(self.angle)])

    def draw(self, pipeline, view, projection):
        # Setting light intensity
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 0.5, 0.5, 0.5)

        # Setting material composition
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), 0.4, 0.4, 0.4)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 0.9, 0.9, 0.9)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 0.9, 0.9, 0.9)

        # Setting light position, camera position, and other parameters
        # Note that the lightPosition is where we are looking at
        # The view Position is our current position.
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition"), 50,50 ,50)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), self.x, self.y, 0)
        glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), 100000)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), 0.001)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), 0.0001)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), 0.0001)

        glUseProgram(pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, self.transform)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        pipeline.drawShape(self.gpuOBJ)
    
    def move(self):
        self.x += self.front*np.cos(self.angle)
        self.y += self.front*np.sin(self.angle)
        self.transform=tr.matmul([tr.translate(self.x,self.y,1.5),tr.uniformScale(0.25),tr.rotationZ(self.angle),tr.rotationX(3.14/2),tr.rotationY(-3.14/2)])

    def update(self):
        self.angle += self.bend*self.turn

class body():
    def __init__(self):
        self.x , self.y = 0,0
        self.angle = 0

        self.GPUsnake=(es.toGPUShape(bs.generateTextureSphere(7,7,"models/textures/snake_skin.png"), GL_REPEAT, GL_LINEAR))
        self.transform = tr.matmul([tr.translate(self.x,self.y,1.2),tr.uniformScale(0.43),tr.rotationZ(self.angle)])
    
    def draw(self, pipeline, view, projection):
        glUseProgram(pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, self.transform)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        pipeline.drawShape(self.GPUsnake)
    
    def move(self):
        self.transform = tr.matmul([tr.translate(self.x,self.y,1.2),tr.uniformScale(0.43),tr.rotationZ(self.angle)])

class snake():
    def __init__(self):
        self.live=True
        self.count=0
        self.snake_list=[
            head(),body(),body(),body(),body(),
            body(),body(),body(),body(),body(),
            body(),body(),body(),body(),body(),
            body(),body(),body(),body(),body(),
            body(),body(),body(),body(),body(),
            body(),body(),body(),body(),body(),
            body(),body(),body(),body(),body(),
            body(),body(),body(),body(),body(),
            body(),body(),body(),body(),body(),
            body(),body(),body(),body(),body()] 

        self.snake_list[1].x=-0.25
        self.snake_list[1].move()
        i=1
        for part in self.snake_list[2:]:
            part.x+=-0.25*i
            part.move()
            i+=1

    def draw(self, pipeline,view, projection):
        for i in range(1,len(self.snake_list)):
            self.snake_list[i].draw(pipeline, view, projection)
   
    def grow(self):
        new=body()
        new.x=self.snake_list[-1].x
        new.y=self.snake_list[-1].y
        new.angle=self.snake_list[-1].angle
        new.move()
        self.count+=1
        self.snake_list.append(new)

        self.snake_list[0].front+=0.0008
        self.snake_list[0].bend+= 0.0007
    
    def die(self):
        x,y=self.snake_list[0].x,self.snake_list[0].y
        for i in range(6,len(self.snake_list)):
            if (x-self.snake_list[i].x)**2+(y-self.snake_list[i].y)**2<0.5:
                self.live=False

        if (self.snake_list[0].x)**2>360 or (self.snake_list[0].y)**2>360:
            self.live=False

    def isDeath(self):
        if self.live==False:
            for i in range(self.count):
                self.snake_list.pop(-1)
            self.count=0
            self.snake_list[0].x,self.snake_list[0].y=0,0
            self.snake_list[0].angle = 0
            self.snake_list[0].bend= 0.12
            self.snake_list[0].front = 0.1
            self.snake_list[0].turn = 0

            self.snake_list[1].x=-0.3
            self.snake_list[1].y=0
            self.snake_list[1].move()
            i=1
            for part in self.snake_list[2:]:
                part.x=-0.3*i
                part.y=0
                part.move()
                i+=1
            self.live=True

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


