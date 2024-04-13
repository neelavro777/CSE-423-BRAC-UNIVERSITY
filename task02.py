from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

W_Width, W_Height = 500,500
create_new = []
speed = 0.01
flag = False
pause = False 

def convert_coordinate(x,y):
    global W_Width, W_Height
    a = x 
    b = W_Height-y
    return (a,b)

def change_flag(currFlag):
    global flag
    if flag == True:
        flag = False
    elif flag == False:    
        flag =  True
    glutPostRedisplay()

def mouseListener(button, state, x, y):
    global  create_new,pause, flag
    if pause == False:
        if button==GLUT_RIGHT_BUTTON:
            if state == GLUT_DOWN:
                print(x,y) 	
                create_new.append({
                    'position': convert_coordinate(x, y),
                    'direction': (random.choice([-1, 1]), random.choice([-1, 1])),
                    'color': (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))
                })
                print(create_new)
        if button==GLUT_LEFT_BUTTON:
            if state == GLUT_DOWN:
                flag = True
                glutTimerFunc(1000, change_flag,0)
        glutPostRedisplay()

def specialKeyListener(key, x, y):
    global speed, pause
    if pause == False:
        if key==GLUT_KEY_UP:
            speed *= 2
            print("Speed Increased")
        if key== GLUT_KEY_DOWN:		
            speed /= 2
            print("Speed Decreased")  
    glutPostRedisplay()

def keyboardListener(key, x, y):

    global pause
    if key==b' ':
        if pause == False:
            pause = True
        elif pause == True:
            pause = False       

    glutPostRedisplay()

def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    global create_new,speed,flag
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glColor3f(1.0, 1.0, 0.0) #konokichur color set (RGB)
   
    #call the draw methods here
    if len(create_new) > 0:
        for i in create_new:
            m, n = i['position']
            glPointSize(5.0)
            glBegin(GL_POINTS)
            if flag:
                glColor3f(0, 0, 0)
            else:
                glColor3f(i['color'][0], i['color'][1], i['color'][2])    
            glVertex2f(m, n)
            glEnd()
    glutSwapBuffers()

def animate():
    glutPostRedisplay()
    global create_new, speed, W_Width, W_Height, pause
    if pause == False:

        for point in create_new:
            x, y = point['position']
            dir_x, dir_y = point['direction']
            x = x + (dir_x * speed)
            y = y + (dir_y * speed)

            if x < 0 or x > W_Width:
                point['direction'] = (-dir_x, dir_y)
            if y < 0 or y > W_Height:
                point['direction'] = (dir_x, -dir_y)

            point['position'] = (x, y)



glutInit()
glutInitWindowSize(500, 500) 
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
wind = glutCreateWindow(b"OpenGL Coding Practice")

glutDisplayFunc(showScreen)
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutMainLoop()