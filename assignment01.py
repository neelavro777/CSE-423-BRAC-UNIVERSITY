from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

speed = 0.01


def draw_rooftop(x2, y2, x1, y1, x0,y0):
    glPointSize(5) #pixel size. by default 1 thake
    glBegin(GL_TRIANGLES)
    glVertex2f(x2, y2) #jekhane show korbe pixel
    glVertex2f(x1, y1)
    glVertex2f(x0, y0)
    glEnd()


def draw_base(x1,y1, x0,y0):
    glPointSize(5) #pixel size. by default 1 thake
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x0, y0)
    glEnd()

def draw_point(x0,y0):
    glPointSize(5) #pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glVertex2f(x0, y0)
    glEnd()


def draw_rain(x1,y1,x0,y0):
    glPointSize(5) #pixel size. by default 1 thake
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x0, y0)
    glEnd()


def animate():
    #//codes for any changes in Models, Camera
    glutPostRedisplay()


def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    global speed
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glColor3f(1.0, 1.0, 0.0) #konokichur color set (RGB)
    #call the draw methods here
    draw_rooftop(100, 200, 500, 200, 300, 300)
    #base
    draw_base(100,200, 100,50)
    draw_base(100,50,500,50)
    draw_base(500,50, 500,200)
    #windowR
    draw_base(450,125, 450,175)
    draw_base(450,175,400,175)
    draw_base(400,175,400,125)
    draw_base(400,125,450,125)
    draw_base(400,150,450,150)
    draw_base(425,175,425,125)
    #windowL
    draw_base(200,125, 200,175)
    draw_base(200,175,150,175)
    draw_base(150,175,150,125)
    draw_base(150,125,200,125)
    draw_base(150, 150, 200, 150)
    draw_base(175, 175, 175, 125)
    #door
    draw_base(275,150, 325,150)
    draw_base(275,150,275,50)
    draw_base(275,50,325,50)
    draw_base(325,50,325,150)
    draw_point(315,100)
    #rain
    rain_param=[[5,500], [5,450]]
    while True:
        draw_rain(rain_param[0][0],rain_param[0][1]-speed,rain_param[1][0],rain_param[1][1]-speed)
        rain_param[0][0]+=(5)
        rain_param[1][0]+=(5)
        if rain_param[0][0]>500:
            break


    


    glutSwapBuffers()



glutInit()
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(500, 500) #window size
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice") #window name
glutDisplayFunc(showScreen)
glutIdleFunc(animate)

glutMainLoop()