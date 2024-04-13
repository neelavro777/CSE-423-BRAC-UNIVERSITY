from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random 
import time

speed = 1
points = 0
W_Width, W_Height = 500,500
shooter_pos = [15,15]
shooter_info = {'radius': 10, 'center': [0,0], 'color': [1,1,0]}
shooter_bullet = {'radius': 5, 'center': [0,0], 'color': [1,0,0]}
bullets = []
enemy_circle1 = []
stop = False
isGameOver = False
pause_symbol = False
isfrozen = False
missed_count = 0

arrow_box = {   
        'x': 0,
        'y': 460,
        'width': 40,
        'height': 40
    }

cross_box = {
    'x': 460,
    'y': 460,
    "width": 40,
    "height": 40
}
pause_box = {
    "x": 220,
    "y": 460,
    "width": 40,
    "height": 40
}
pause_box2 = {
    "x": 240,
    "y": 460,
    "width": 20,
    "height": 40
}


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


def draw_arrow():
    eight_way_symmetry(0, 480, 20, 500, (0, 0, 1))
    eight_way_symmetry(0, 480, 20, 460, (0, 0, 1))
    eight_way_symmetry(0, 480, 40, 480, (0, 0, 1))

def draw_pause():
    global pause_symbol, isfrozen #used to represent two different states of pause button
    if pause_symbol and isfrozen:
        eight_way_symmetry(220, 460, 220, 500, (1, 0.75, 0))
        eight_way_symmetry(220, 460, 260, 480, (1, 0.75, 0))
        eight_way_symmetry(260, 480, 220, 500, (1, 0.75, 0))
    else:
        eight_way_symmetry(240, 460, 240, 500, (1, 0.75, 0))
        eight_way_symmetry(260, 460, 260, 500, (1, 0.75, 0))
  


def draw_cross():
    eight_way_symmetry(460, 460, 500, 500, (1, 0, 0))
    eight_way_symmetry(460, 500, 500, 460, (1, 0, 0))


def spawn_enemy_circles():
    global enemy_circle1
    if len(enemy_circle1) < 5:
        new_enemy = generate_new_enemy() 
        collided = False
        for existing in enemy_circle1:
            if has_collided(new_enemy, existing):
                collided = True
                break
        if collided == False:
            enemy_circle1.append(new_enemy)                        

def generate_new_enemy():
    x = random.randint(10, 490)
    y = random.randint(350, 450)
    radius = random.randint(10, 20)
    color = [1, 0, 0]
    return {'radius': radius, 'center': [x, y], 'color': color}

def draw_enemy_circle():
    global enemy_circle1, shooter_info, shooter_bullet
    for circle in enemy_circle1:
        circle['center'][1] -= 0.075
        midpoint_circle(circle['radius'], circle['color'], circle['center'])


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

               
def draw_shooter():
    global shooter_pos, shooter_info
    shooter_info['center'][0] = shooter_pos[0]
    shooter_info['center'][1] = shooter_pos[1]
    midpoint_circle(shooter_info['radius'], shooter_info['color'], shooter_info['center'])

def fire_bullet():
    global shooter_pos, shooter_info, shooter_bullet
    bullet = {'radius': 5, 'center': [shooter_pos[0], shooter_pos[1]+shooter_info['radius']], 'color': [0,1,0], 'speed': 1}
    bullets.append(bullet)
    print(bullets)

def draw_bullets():
    global bullets
    for bullet in bullets:
        bullet['center'][1] += bullet['speed']
        midpoint_circle(bullet['radius'], bullet['color'], bullet['center'])
        if bullet['center'][1] > 500:
            bullets.remove(bullet)
            print(bullets)

def animate():
    global isGameOver, isfrozen
    if not isGameOver and not isfrozen:
        draw_bullets()
        draw_enemy_circle()
        glutPostRedisplay()
        time.sleep(0.001)


def check_bullet_circle_collisions():
    global bullets, enemy_circle1, points
    for bullet in bullets:
        for enemy_circle in enemy_circle1:
            if has_collided(bullet, enemy_circle):
                bullets.remove(bullet)
                enemy_circle1.remove(enemy_circle)
                points += 1
                print(f"Points: {points}")
                return


def has_collided(circle1, circle2):
    circle1_center_x, circle1_center_y = circle1['center']
    circle2_center_x, circle2_center_y = circle2['center']
    distance = ((circle1_center_x - circle2_center_x) ** 2 + (circle1_center_y - circle2_center_y) ** 2) ** 0.5
    return distance < (circle1['radius'] + circle2['radius'])

def check_game_over():
    global enemy_circle1, shooter_info, isGameOver, missed_count

    for enemy_circle in enemy_circle1:
        if has_collided(enemy_circle, shooter_info):
            print("Game Over: Circle touched the shooter!")
            isGameOver = True
            return
        
    for enemy_circle in enemy_circle1:
        if enemy_circle['center'][1] < 0:
            missed_count += 1
            enemy_circle1.remove(enemy_circle)

            print(f"Remaining Lives: {3 - missed_count}")

            if missed_count >= 3:
                print("Game Over: All of your lives are over")
                isGameOver = True
                return

def specialKeyListener(key, x, y):
    global shooter_pos, shooter_info, isGameOver, isfrozen
    if not isGameOver and not isfrozen:
        if key==GLUT_KEY_RIGHT:
            if shooter_info['center'][0] + shooter_info['radius'] < 490:
                shooter_pos[0] += 10 

        elif key==GLUT_KEY_LEFT:
            if shooter_info['center'][0] - shooter_info['radius'] > 10:
                shooter_pos[0] -= 10


    # print(catcher_info[0])
#     elif key == GLUT_KEY_UP:


#     elif key == GLUT_KEY_DOWN:


    glutPostRedisplay()





  

def keyboardListener(key, x, y):
    global isfrozen, isGameOver
    if not isGameOver and not isfrozen:
        if key==b' ':
            fire_bullet()
        if key==b'a':
            if shooter_info['center'][0] - shooter_info['radius'] > 10:
                shooter_pos[0] -= 25

        if key==b'd':
            if shooter_info['center'][0] + shooter_info['radius'] < 490:
                shooter_pos[0] += 25

        glutPostRedisplay()


def mouseListener(button, state, x, y):
    global shooter_pos, shooter_info, bullets, enemy_circle1, points, isGameOver, pause_symbol, isfrozen, arrow_box, cross_box, pause_box, pause_box2
    if button==GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            adj_x, adj_y = convert_coordinate(x, y)
            if adj_x >= arrow_box['x'] and adj_x <= arrow_box['x'] + arrow_box['width'] and adj_y >= arrow_box['y'] and adj_y <= arrow_box['y'] + arrow_box['height']:
                shooter_pos = [15,15]
                shooter_info = {'radius': 10, 'center': [0,0], 'color': [1,1,0]}
                bullets = []
                enemy_circle1 = []
                points = 0
                isGameOver = False
                pause_symbol = False
                isfrozen = False
            

            if adj_x >= cross_box['x'] and adj_x <= cross_box['x'] + cross_box['width'] and adj_y >= cross_box['y'] and adj_y <= cross_box['y'] + cross_box['height']:
                # print("Cross clicked")
                print("GoodBye")
                glutLeaveMainLoop()

            if pause_symbol:
                if adj_x >= pause_box["x"] and adj_x <= pause_box["x"] + pause_box["width"] and adj_y >= pause_box["y"] and adj_y <= pause_box["y"] + pause_box["height"]:
                    # print("Pause clicked")
                    pause_symbol = not pause_symbol
                    isfrozen = not isfrozen    
            elif adj_x >= pause_box2["x"] and adj_x <= pause_box2["x"] + pause_box2["width"] and adj_y >= pause_box2["y"] and adj_y <= pause_box2["y"] + pause_box2["height"]:
                # print("Pause2 clicked")
                pause_symbol = not pause_symbol
                isfrozen = not isfrozen

                



def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()


def showScreen():
    global shooter_info
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    draw_shooter()
    draw_bullets()
    draw_enemy_circle()
    check_bullet_circle_collisions()
    spawn_enemy_circles()
    check_game_over()
    draw_arrow()
    draw_pause()
    draw_cross()
    if isGameOver:
        print(f"Game Over! Your score is: {points}")
    glutSwapBuffers()

glutInit()
print(enemy_circle1)
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