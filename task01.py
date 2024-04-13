from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random


rain_angle = 0.0
background_color = [0.0, 0.0, 0.0]
house_color = [1.0, 1.0, 1.0]
rain_speed = 2
rain_coordinates = [(random.uniform(0, 500), random.uniform(150, 500)) for i in range(1000)]




def diagonal_line1(x,y):
    x1, y1, x2, y2 = 150, 150, 250, 250
    dx = x2 - x1
    dy = y2 - y1
    m = dy/dx
    c = y1 - m*x1
    eqn = m*x + c
    if y-10 > eqn:
        return True
    else:
        return False
    

    
def diagonal_line2(x,y):
    x1, y1, x2, y2 = 250, 250, 350, 150
    dx = x2 - x1
    dy = y2 - y1
    m = dy/dx
    c = y1 - m*x1
    eqn = m*x + c
    if y-10 > eqn:
        return True
    else:
        return False    

def drawRaindrop(x, y):
    global rain_angle
    length = 10
    rotated_x = x + rain_angle
    glBegin(GL_LINES)
    glVertex2f(rotated_x, y)
    glVertex2f(x, y + length)  
    glEnd()

def drawRain():
    glColor3f(0.0, 0.0, 1.0) 
    for x,y  in rain_coordinates:  
        if diagonal_line1(x, y) or diagonal_line2(x, y):
            glLineWidth(1)
            drawRaindrop(x, y)
        else:
            pass



def drawShapes():

    glLineWidth(5)

    #Code for Triangle
    glBegin(GL_LINES)
    glVertex2d(150, 150)
    glVertex2d(250, 250)

    glVertex2d(250, 250)
    glVertex2d(350, 150)

    glVertex2d(350, 150)
    glVertex2d(150, 150)
    glEnd()


    #Code for Rectangle
    glBegin(GL_LINES)
    glVertex2d(150, 150)
    glVertex2d(350, 150)

    glVertex2d(350, 150)
    glVertex2d(350, 50)

    glVertex2d(350, 50)
    glVertex2d(150, 50)

    glVertex2d(150, 50)
    glVertex2d(150, 150)
    glEnd()

    #Code for Door
    glBegin(GL_LINES)
    glVertex2d(200, 100)
    glVertex2d(230, 100)

    glVertex2d(230, 100)
    glVertex2d(230, 50)

    glVertex2d(230, 50)
    glVertex2d(200, 50)

    glVertex2d(200, 50)
    glVertex2d(200, 100)
    glEnd()

    #Code for DoorLock
    glPointSize(2.0)
    glBegin(GL_POINTS)
    glVertex2d(225, 70)
    glEnd()

    #Code for Window
    glBegin(GL_LINES)
    glVertex2d(300, 130)
    glVertex2d(330, 130)

    glVertex2d(330, 130)
    glVertex2d(330, 90)

    glVertex2d(330, 90)
    glVertex2d(300, 90)

    glVertex2d(300, 90)
    glVertex2d(300, 130)

    glVertex2d(315, 130)
    glVertex2d(315, 90)

    glVertex2d(300, 110)
    glVertex2d(330, 110)

    glEnd()

def specialKeyListener(key, x, y):
    global rain_angle
    if key==GLUT_KEY_RIGHT:
        rain_angle += 10
        
    elif key==GLUT_KEY_LEFT:
        rain_angle -= 10

    elif key == GLUT_KEY_UP:
        background_color[0] += 0.1 
        background_color[1] += 0.1
        background_color[2] += 0.1
        house_color[0] -= 0.1 
        house_color[1] -= 0.1
        house_color[2] -= 0.1

    elif key == GLUT_KEY_DOWN:
        if sum(background_color) == 0 and sum (house_color) == 3:
            pass 
        else:  
            background_color[0] -= 0.1 
            background_color[1] -= 0.1
            background_color[2] -= 0.1 
            house_color[0] += 0.1
            house_color[1] += 0.1
            house_color[2] += 0.1 

    glutPostRedisplay()

def animate():
    glutPostRedisplay()
    global rain_coordinates, rain_speed
    for i in range(len(rain_coordinates)):
        x, y = rain_coordinates[i]
        rain_coordinates[i] = (x, y - rain_speed)
        if y - rain_speed < 150:
            rain_coordinates[i] = (random.uniform(0, 500), random.uniform(150, 500))


def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()


def showScreen():
    global background_color, house_color
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glClearColor(*background_color, 1.0)
    glColor3f(house_color[0], house_color[0], house_color[0])
    drawShapes()
    drawRain()
    glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice")
glutDisplayFunc(showScreen)
glutIdleFunc(animate)
glutSpecialFunc(specialKeyListener)
glutMainLoop()