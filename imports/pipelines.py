
import lib.transformations as tr
import lib.lighting_shaders as ls
import lib.easy_shaders as es
import lib.basic_shapes as bs
import lib.lighting_shaders as ls

pipeline = es.SimpleModelViewProjectionShaderProgram()
texture_pipeline = es.SimpleTextureModelViewProjectionShaderProgram()
obj_pipeline = ls.SimpleTextureGouraudShaderProgram()
light_pipeline=ls.SimpleFlatShaderProgram()