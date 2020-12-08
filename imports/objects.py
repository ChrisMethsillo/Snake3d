from models.structure import *
from models.snake import *
from lib.controller import *
from imports.pipelines import *

import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import OpenGL.GL.shaders

jungle=jungle()
jungle_floor=jungle_floor()
floor=floor()
food=food()
Snake=snake()
cabeza=Snake.snake_list[0]
game_over=game_over()
controller=Controller(Snake)   
