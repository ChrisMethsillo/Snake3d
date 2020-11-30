from OpenGL.GL import *
import OpenGL.GL.shaders

import lib.transformations as tr
import lib.lighting_shaders as ls
import lib.easy_shaders as es
import lib.basic_shapes as bs


class floor():
    def __init__(self):
        obj = bs.createTextureCube('models/floor.png')
        self.GPUobj= es.toGPUShape(obj, GL_REPEAT, GL_LINEAR)
        self.model= tr.matmul([tr.scale(40,40,1),tr.translate(0,0,0)])

    def draw(self,pipeline,view,projection):
        glUseProgram(pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, self.model)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)

        pipeline.drawShape(self.GPUobj)
        