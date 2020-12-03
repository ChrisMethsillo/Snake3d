import glfw
from sys import exit
import numpy as np
import lib.transformations as tr

class Controller:
    def __init__(self,Snake):
        self.snake=Snake
        
        self.Snake_view=True
        self.inclinate_view=False
        self.top_view=False

        #Serpiente
    def camera(self):
        if self.top_view:
                return tr.lookAt(
            np.array([0,0,60]), # eye
            np.array([0,0.0001,0]), # at
            np.array([0,0,1])  # up
        )

        elif self.inclinate_view:
                return tr.lookAt(
            np.array([0,-41,41]), # eye
            np.array([0,0.0001,0]), # at
            np.array([0,0,1])  # up
        )
        elif self.Snake_view:
                return tr.lookAt(
                np.array([self.snake.x+np.cos(self.snake.angle)*-10, self.snake.y+np.sin(self.snake.angle)*-10,7]),   # eye
                np.array([self.snake.x+np.cos(self.snake.angle), self.snake.y+np.sin(self.snake.angle),1]),  # at
                np.array([0,0,1])    
        )

    def on_key(self, window, key, scancode, action, mods):
        
        if not (action == glfw.REPEAT or action == glfw.PRESS or action == glfw.RELEASE):
                return

        if key == glfw.KEY_ESCAPE:
            sys.exit()
        
        if (key == glfw.KEY_A or key == glfw.KEY_LEFT) and action == glfw.PRESS:
            self.snake.turn = 1
        
        elif (key == glfw.KEY_A or key == glfw.KEY_LEFT) and action == glfw.RELEASE:
            self.snake.turn = 0
        
        elif (key == glfw.KEY_D or key == glfw.KEY_RIGHT) and action == glfw.PRESS:
            self.snake.turn = -1
        
        elif (key == glfw.KEY_D or key == glfw.KEY_RIGHT) and action == glfw.RELEASE:
            self.snake.turn = 0 

        elif (key == glfw.KEY_W or key == glfw.KEY_UP) and (action == glfw.PRESS or action == glfw.REPEAT):
            pass
        
        elif (key == glfw.KEY_S or key == glfw.KEY_DOWN) and (action == glfw.PRESS or action == glfw.REPEAT):
            pass
        

        if key == glfw.KEY_E and action==glfw.PRESS:
                self.Snake_view=False
                self.inclinate_view=False
                self.top_view=True

        elif key == glfw.KEY_T and action==glfw.PRESS:
                self.Snake_view=False
                self.inclinate_view=True
                self.top_view=False
        elif key == glfw.KEY_R and action==glfw.PRESS:
                self.Snake_view=True
                self.inclinate_view=False
                self.top_view=False

        else:
            pass