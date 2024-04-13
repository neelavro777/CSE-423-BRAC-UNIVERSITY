from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

W_Width, W_Height = 500,500

def convert_coordinate(x,y):
    global W_Width, W_Height
    a = x 
    b = W_Height-y
    return (a,b)

def draw_points(x, y, color):
    glColor3f(*color)
    glPointSize(2) #pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glVertex2f(x,y) #jekhane show korbe pixel
    glEnd()

def midpoint_line(x1, y1, x2, y2, zone, color):
    dx = x2 - x1
    dy = y2 - y1
    d = 2*dy - dx
    incE = 2*dy
    incNE = 2*(dy-dx)  
    y = y1
    # print(x1, y1, x2, y2, zone)
    for x in range(x1, x2+1):
        oz_x, oz_y = convertzoneM(x, y, zone)

        draw_points(oz_x , oz_y, color) 
        if d <= 0:
            d += incE
        else:
            d += incNE
            y += 1

def findzone(x1, y1, x2, y2):    
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) > abs(dy):
        if dx >= 0 and dy >= 0:
            return 0
        elif dx <= 0 and dy >= 0:
            return 3
        elif dx <= 0 and dy <= 0:
            return 4
        elif dx >= 0 and dy <= 0:
            return 7
    else:
        if dx >= 0 and dy >= 0:
            return 1
        elif dx <= 0 and dy >= 0:
            return 2
        elif dx <= 0 and dy <= 0:
            return 5
        elif dx >= 0 and dy <= 0:
            return 6 
               
def convertzone0(x, y, zone):  
    if zone == 0:
        return (x, y)
    elif zone == 1:
        return (y, x)
    elif zone == 2:
        return (y, -x)
    elif zone == 3:
        return (-x, y)
    elif zone == 4:
        return (-x, -y)
    elif zone == 5:
        return (-y, -x)
    elif zone == 6:
        return (-y, x)
    elif zone == 7:
        return (x, -y)

def convertzoneM(x,y, zone):
    if zone == 0:
        return (x, y)
    elif zone == 1:
        return (y, x)
    elif zone == 2:
        return (-y, x)
    elif zone == 3:
        return (-x, y)
    elif zone == 4:
        return (-x, -y)
    elif zone == 5:
        return (-y, -x)
    elif zone == 6:
        return (y, -x)
    elif zone == 7:
        return (x, -y)

def eight_way_symmetry(x1, y1, x2, y2, color = (1, 1, 0)):
    zone = findzone(x1, y1, x2, y2)
    # print(zone)
    x1, y1 = convertzone0(x1, y1, zone)
    x2, y2 = convertzone0(x2, y2, zone)
    midpoint_line(x1, y1, x2, y2, zone, color)               


def midpoint_circle(radius, color, center = (0,0)):
    x = 0
    y = radius
    d = 1 - radius
    Circlepoints(x, y, color, center)
    while x < y:
        if d < 0:
            d = d + 2*x+3
            x = x+1 
        else:
            d = d + 2*(x-y)+5
            x = x+1
            y = y-1
        Circlepoints(x, y, color, center)   

def Circlepoints(x, y, color, center):
    draw_points(x+center[0], y+center[1], color)
    draw_points(-x+center[0], y+center[1], color)
    draw_points(x+center[0], -y+center[1], color)
    draw_points(-x+center[0], -y+center[1], color)
    draw_points(y+center[0], x+center[1], color)
    draw_points(-y+center[0], x+center[1], color)
    draw_points(y+center[0], -x+center[1], color)
    draw_points(-y+center[0], -x+center[1], color)

def animate():
    pass
    glutPostRedisplay()
  

def keyboardListener(key, x, y):
    if key==b' ':
        print("Space pressed")
    if key==b'a':
        print("a pressed")

    if key==b'd':
        print("d pressed")

    glutPostRedisplay()

def specialKeyListener(key, x, y):
    if key==GLUT_KEY_RIGHT:
        print("Right arrow pressed")

    elif key==GLUT_KEY_LEFT:
        print("Left arrow pressed")


    # print(catcher_info[0])
#     elif key == GLUT_KEY_UP:


#     elif key == GLUT_KEY_DOWN:


    glutPostRedisplay()

def mouseListener(button, state, x, y):
    if button==GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            pass


def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def draw_line(x1, y1, x2, y2, color):
    eight_way_symmetry(x1, y1, x2, y2, color)

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    eight_way_symmetry(0, 0, 100, 100)
    midpoint_circle(100, (1, 1, 0), (250, 250))
    draw_line(0, 0, 500, 500, (1, 0, 0))
    glutSwapBuffers()

glutInit()

glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice")
glutDisplayFunc(showScreen)
glutIdleFunc(animate)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutKeyboardFunc(keyboardListener)
glutMainLoop()