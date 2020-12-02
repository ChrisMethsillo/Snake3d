from OpenGL.GL import *
import OpenGL.GL.shaders
import random

import lib.transformations as tr
import lib.lighting_shaders as ls
import lib.easy_shaders as es
import lib.basic_shapes as bs
import lib.obj_handler as obj_reader



class floor():
    def __init__(self):
        obj = bs.createTextureCube('models/textures/floor_2.png')
        self.GPUobj= es.toGPUShape(obj, GL_REPEAT, GL_LINEAR)
        self.model= tr.matmul([tr.scale(40,40,1.5),tr.translate(0,0,0)])

    def draw(self,pipeline,view,projection):
        glUseProgram(pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, self.model)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)

        pipeline.drawShape(self.GPUobj)


class food():
    def __init__(self):
        
        self.x=random.uniform(-18.5,18.5)
        self.y=random.uniform(-18.5,18.5)

        obj='models/figure/duck.obj'
        obj_cabeza=obj_reader.readOBJ2(f'{obj}',"models/textures/duck.png")
        self.gpuOBJ = es.toGPUShape( obj_cabeza , GL_REPEAT, GL_LINEAR)
        self.transform=tr.matmul([tr.translate(self.x,self.y,0.8),tr.uniformScale(1),tr.rotationZ(random.uniform(0,2*3.14)),tr.rotationX(3.14/2)])

    def draw(self,texture_pipeline,view,projection):
        glUniform3f(glGetUniformLocation(texture_pipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(texture_pipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(texture_pipeline.shaderProgram, "Ls"), 0.5, 0.5, 0.5)

        # Setting material composition
        glUniform3f(glGetUniformLocation(texture_pipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
        glUniform3f(glGetUniformLocation(texture_pipeline.shaderProgram, "Kd"), 0.9, 0.9, 0.9)
        glUniform3f(glGetUniformLocation(texture_pipeline.shaderProgram, "Ks"), 0.5, 0.5, 0.5)

        # Setting light position, camera position, and other parameters
        # Note that the lightPosition is where we are looking at
        # The view Position is our current position.
        glUniform3f(glGetUniformLocation(texture_pipeline.shaderProgram, "lightPosition"), 50,50 ,50)
        glUniform3f(glGetUniformLocation(texture_pipeline.shaderProgram, "viewPosition"), self.x, self.y, 0)
        glUniform1ui(glGetUniformLocation(texture_pipeline.shaderProgram, "shininess"), 100)
        glUniform1f(glGetUniformLocation(texture_pipeline.shaderProgram, "constantAttenuation"), 0.001)
        glUniform1f(glGetUniformLocation(texture_pipeline.shaderProgram, "linearAttenuation"), 0.0001)
        glUniform1f(glGetUniformLocation(texture_pipeline.shaderProgram, "quadraticAttenuation"), 0.0001)

        glUseProgram(texture_pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(texture_pipeline.shaderProgram, "model"), 1, GL_TRUE, self.transform)
        glUniformMatrix4fv(glGetUniformLocation(texture_pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(texture_pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        texture_pipeline.drawShape(self.gpuOBJ)

    def change_position(self):
        self.x=random.uniform(-18.5,18.5)
        self.y=random.uniform(-18.5,18.5)
        self.transform=tr.matmul([tr.translate(self.x,self.y,0.8),tr.uniformScale(1),tr.rotationZ(random.uniform(0,2*3.14)),tr.rotationX(3.14/2)])

        
