from imports.files import *
if __name__ == "__main__":

    if not glfw.init():
        sys.exit()

    width = 900
    height = 800
    window = glfw.create_window(width, height, "SNAKE 3D", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    from imports.objects import *

    glfw.set_key_callback(window, controller.on_key)

    from imports.pipelines import *

    glUseProgram(texture_pipeline.shaderProgram)

    glClearColor(0.85, 0.85, 0.85, 1.0)

    glEnable(GL_DEPTH_TEST)

    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    projection = tr.perspective(45, float(width)/float(height), 0.1, 100)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        time=glfw.get_time()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        
        if (Snake.snake_list[0].x-food.x)**2+(Snake.snake_list[0].y-food.y)**2<=0.8:
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
        
        glfw.swap_buffers(window)
    glfw.terminate()