from OpenGL.GL import *
import OpenGL.GL.shaders
import random
import numpy as np

import lib.transformations as tr
import lib.lighting_shaders as ls
import lib.easy_shaders as es
import lib.basic_shapes as bs
import lib.obj_handler as obj_reader


class jungle():
    def __init__(self):
        obj = bs.createTextureCube('models/textures/jungle.png')
        self.GPUobj= es.toGPUShape(obj, GL_REPEAT, GL_LINEAR)
        self.model= tr.matmul([tr.translate(0,0,29),tr.uniformScale(60)])

    def draw(self,pipeline,view,projection):
        glUseProgram(pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, self.model)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)

        pipeline.drawShape(self.GPUobj)

class jungle_floor():
    def __init__(self):
        obj = bs.createTextureCube('models/textures/jungle_floor.png')
        self.GPUobj= es.toGPUShape(obj, GL_REPEAT, GL_LINEAR)
        self.model= tr.matmul([tr.translate(0,0,0),tr.scale(82,82,0.1)])

    def draw(self,pipeline,view,projection):
        glUseProgram(pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, self.model)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)

        pipeline.drawShape(self.GPUobj)

class floor():
    def __init__(self):
        obj = bs.createTextureNormalsCube('models/textures/floor_2.png')
        self.GPUobj= es.toGPUShape(obj, GL_REPEAT, GL_LINEAR)
        self.model= tr.matmul([tr.scale(40,40,1.5),tr.translate(0,0,0)])

    def draw(self,pipeline,view,projection,x,y,ka):
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

            # Object is barely visible at only ambient. Bright white for diffuse and specular components.
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), ka, ka, ka)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 0.9, 0.9, 0.9)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

        # Here we can see how we can change the light position and view position at the same time.
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition"), 0, 0, 50)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), x,y,1.6)
        glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), 1)

        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), 0.01)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), 1)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), 0.01)
        
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, self.model)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)

        pipeline.drawShape(self.GPUobj)


class food():
    def __init__(self):
        
        self.x=random.uniform(-18.5,18.5)
        self.y=random.uniform(-18.5,18.5)

        obj='models/figure/coin.obj'
        obj_cabeza=obj_reader.readOBJ2(f'{obj}',"models/textures/coin.png")
        self.gpuOBJ = es.toGPUShape( obj_cabeza , GL_REPEAT, GL_LINEAR)

    def draw(self,pipeline,view,projection,ka,dt):
        self.transform=tr.matmul([tr.translate(self.x,self.y,0.8),tr.uniformScale(0.1),tr.rotationZ(2*np.pi*(dt)),tr.rotationX(3.14/2)])
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 0.5, 0.5, 0.5)

        # Setting material composition
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), ka, ka, ka)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 0.9, 0.9, 0.9)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 0.5, 0.5, 0.5)

        # Setting light position, camera position, and other parameters
        # Note that the lightPosition is where we are looking at
        # The view Position is our current position.
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition"), self.x,self.y,70)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), self.x, self.y, 0)
        glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), 20)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), 0.001)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), 0.0001)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), 0.0001)

        glUseProgram(pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, self.transform)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        pipeline.drawShape(self.gpuOBJ)

    def change_position(self):
        self.x=random.uniform(-18.5,18.5)
        self.y=random.uniform(-18.5,18.5)



class game_over():
    def __init__(self):
        self.x,self.y,self.z=0,0,20
        obj='models/figure/game_over.obj'
        obj_cabeza=obj_reader.readOBJ(f'{obj}',(1,0.1,0.1))
        self.gpuOBJ = es.toGPUShape( obj_cabeza)

    def draw(self,pipeline,projection,dt):
        self.transform=tr.matmul([tr.translate(self.x,self.y,self.z),tr.uniformScale(1.5),tr.rotationY(np.pi/2),tr.rotationZ(np.pi/2),tr.rotationX((np.pi/20)*np.sin(dt))])
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 0.5, 0.5, 0.5)

        # Setting material composition
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), 0.9, 0.9, 0.9)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 0.9, 0.9, 0.9)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 0.5, 0.5, 0.5)

        # Setting light position, camera position, and other parameters
        # Note that the lightPosition is where we are looking at
        # The view Position is our current position.
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition"), self.x+10, self.y, self.z)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), self.x, self.y, self.z)
        glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), 100)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), 0.001)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), 0.0001)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), 0.0001)

        glUseProgram(pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, self.transform)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, tr.lookAt(np.array([self.x+10, self.y, self.z]),np.array([self.x, self.y, self.z]),np.array([0, 0, 1])))
        pipeline.drawShape(self.gpuOBJ)
        

        
