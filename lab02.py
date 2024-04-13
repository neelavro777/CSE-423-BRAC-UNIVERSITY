from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random 
import time

speed = 1
points = 0
W_Width, W_Height = 500,500

stop = True
pause_symbol = False
isfrozen = False

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

diamond_x = 75
diamond_color = (1, 0, 0)
diamond_pos = [{"edge1": {"x": diamond_x, "y": 500}, #right_edge
            "edge2": {"x": diamond_x-20, "y": 500}, #left_edge
            "edge3": {"x": diamond_x-10, "y": 510}, #top_edge
            "edge4": {"x": diamond_x-10, "y": 490}},  #bottom_edge
            diamond_color] 

catcher_pos = 0
catcher_color = (1, 1, 0)
catcher_info = [{
    "base": {"x1": 20, "y1": 20, "x2": 100, "y2": 20},
    "left_diagonal": {"x1": 0, "y1": 40, "x2": 20 + 0, "y2": 20},
    "right_diagonal": {"x1": 100 + 0, "y1": 20, "x2": 120 + 0, "y2": 40},
    "above": {"x1": 0, "y1": 40, "x2": 120 + 0, "y2": 40}
}, catcher_color]

def draw_points(x, y, color):
    glColor3f(*color)
    glPointSize(2) #pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glVertex2f(x,y) #jekhane show korbe pixel
    glEnd()


def convert_coordinate(x,y):
    global W_Width, W_Height
    a = x 
    b = W_Height-y
    return (a,b)

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

def catcher():
    global catcher_info, catcher_pos

    catcher_info[0]["base"]["x1"] = 20 + catcher_pos
    catcher_info[0]["base"]["x2"] = 100 + catcher_pos
    catcher_info[0]["left_diagonal"]["x1"] = catcher_pos
    catcher_info[0]["left_diagonal"]["x2"] = 20 + catcher_pos
    catcher_info[0]["right_diagonal"]["x1"] = 100 + catcher_pos
    catcher_info[0]["right_diagonal"]["x2"] = 120 + catcher_pos
    catcher_info[0]["above"]["x1"] = catcher_pos
    catcher_info[0]["above"]["x2"] = 120 + catcher_pos

    eight_way_symmetry(catcher_info[0]["base"]["x1"], catcher_info[0]["base"]["y1"], catcher_info[0]["base"]["x2"], catcher_info[0]["base"]["y2"], catcher_info[1]) #base
    eight_way_symmetry(catcher_info[0]["left_diagonal"]["x1"], catcher_info[0]["left_diagonal"]["y1"], catcher_info[0]["left_diagonal"]["x2"], catcher_info[0]["left_diagonal"]["y2"], catcher_info[1]) #left diagonal
    eight_way_symmetry(catcher_info[0]["right_diagonal"]["x1"], catcher_info[0]["right_diagonal"]["y1"], catcher_info[0]["right_diagonal"]["x2"], catcher_info[0]["right_diagonal"]["y2"], catcher_info[1]) #Right diagonal
    eight_way_symmetry(catcher_info[0]["above"]["x1"], catcher_info[0]["above"]["y1"], catcher_info[0]["above"]["x2"], catcher_info[0]["above"]["y2"], catcher_info[1]) #above    

def diamond():
    global diamond_pos

    eight_way_symmetry(diamond_pos[0]["edge1"]["x"], diamond_pos[0]["edge1"]["y"], diamond_pos[0]["edge4"]["x"], diamond_pos[0]["edge4"]["y"], diamond_pos[1])
    eight_way_symmetry(diamond_pos[0]["edge1"]["x"], diamond_pos[0]["edge1"]["y"], diamond_pos[0]["edge3"]["x"], diamond_pos[0]["edge3"]["y"], diamond_pos[1])
    eight_way_symmetry(diamond_pos[0]["edge2"]["x"], diamond_pos[0]["edge2"]["y"], diamond_pos[0]["edge4"]["x"], diamond_pos[0]["edge4"]["y"],  diamond_pos[1])
    eight_way_symmetry(diamond_pos[0]["edge2"]["x"], diamond_pos[0]["edge2"]["y"], diamond_pos[0]["edge3"]["x"], diamond_pos[0]["edge3"]["y"],  diamond_pos[1])


def specialKeyListener(key, x, y):
    global catcher_info, catcher_pos, stop, isfrozen
    if key==GLUT_KEY_RIGHT:
        if catcher_info[0]["right_diagonal"]["x2"] and catcher_info[0]["above"]["x2"]< 490 and stop and isfrozen == False:
            catcher_pos += 20
        else:
            pass
    elif key==GLUT_KEY_LEFT:
        if catcher_pos > 0 and stop and isfrozen == False:
            catcher_pos -= 20
        else:
            pass
    # print(catcher_info[0])
#     elif key == GLUT_KEY_UP:


#     elif key == GLUT_KEY_DOWN:


    glutPostRedisplay()

def has_collided(box1, box2):
    return (box1['x'] < box2['x'] + box2['width'] and
            box1['x'] + box1['width'] > box2['x'] and
            box1['y'] < box2['y'] + box2['height'] and
            box1['y'] + box1['height'] > box2['y'])



def draw_arrow():
    eight_way_symmetry(0, 480, 20, 500, (0, 0, 1))
    eight_way_symmetry(0, 480, 20, 460, (0, 0, 1))
    eight_way_symmetry(0, 480, 40, 480, (0, 0, 1))

def draw_pause():
    global pause_symbol #used to represent two different states of pause button
    if pause_symbol and isfrozen:
        eight_way_symmetry(220, 460, 220, 500, (1, 1, 0))
        eight_way_symmetry(220, 460, 260, 480, (1, 1, 0))
        eight_way_symmetry(260, 480, 220, 500, (1, 1, 0))
    else:
        eight_way_symmetry(240, 460, 240, 500, (1, 1, 0))
        eight_way_symmetry(260, 460, 260, 500, (1, 1, 0))
  


def draw_cross():
    eight_way_symmetry(460, 460, 500, 500, (1, 0, 0))
    eight_way_symmetry(460, 500, 500, 460, (1, 0, 0))



def mouseListener(button, state, x, y):
    global  arrow_box, cross_box, pause_box, pause_box2, pause_symbol, diamond_pos, catcher_info, diamond_x, diamond_color, stop, speed, points, catcher_pos, isfrozen
    # if pause == False:
    if button==GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            adj_x, adj_y = convert_coordinate(x, y)	
            # print(adj_x, adj_y)
            if adj_x >= arrow_box["x"] and adj_x <= arrow_box["x"] + arrow_box["width"] and adj_y >= arrow_box["y"] and adj_y <= arrow_box["y"] + arrow_box["height"]:
                # print("Arrow clicked")
                diamond_x = random.randint(20, 500)
                if diamond_x <= arrow_box['x'] + arrow_box["width"]:
                    diamond_x = 65
                elif diamond_x >= cross_box['x']:
                    diamond_x = cross_box['x'] - 25    
                elif diamond_x >= pause_box2['x'] and diamond_x <= pause_box2['x'] + pause_box2['width']:
                    if pause_box2['x'] <= diamond_x <= (pause_box2['x'] + pause_box2['x'] +pause_box2["width"])//2:
                        diamond_x = pause_box2['x']  - pause_box2['width'] - 30 
                    else:
                        diamond_x = pause_box2['x']  + pause_box2['width'] + 30
                diamond_pos = [{"edge1": {"x": diamond_x, "y": 490}, #right_edge
                                "edge2": {"x": diamond_x-20, "y": 490}, #left_edge
                                "edge3": {"x": diamond_x-10, "y": 500}, #top_edge
                                "edge4": {"x": diamond_x-10, "y": 480}},  #bottom_edge
                                diamond_color] 
                catcher_color = (1, 1, 0)
                catcher_info = [{
                    "base": {"x1": 20, "y1": 20, "x2": 100, "y2": 20},
                    "left_diagonal": {"x1": 0, "y1": 40, "x2": 20 + 0, "y2": 20},
                    "right_diagonal": {"x1": 100 + 0, "y1": 20, "x2": 120 + 0, "y2": 40},
                    "above": {"x1": 0, "y1": 40, "x2": 120 + 0, "y2": 40}
                }, catcher_color]
                catcher_pos = 0
                points = 0
                speed = 1
                stop = True
                isfrozen = False

            elif adj_x >= cross_box["x"] and adj_x <= cross_box["x"] + cross_box["width"] and adj_y >= cross_box["y"] and adj_y <= cross_box["y"] + cross_box["height"]:
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

                


def animate():
    global diamond_pos, diamond_color, diamond_x, stop, speed, points, isfrozen, arrow_box, cross_box, pause_box
    if stop and isfrozen != True:    
            catcher_box = {
            'x': catcher_info[0]["base"]["x1"],
            'y': catcher_info[0]["base"]["y1"],
            'width': catcher_info[0]["above"]["x2"] - catcher_info[0]["above"]["x1"],
            'height': catcher_info[0]["above"]["y2"] - catcher_info[0]["base"]["y1"]
            }

            diamond_box = {
            'x': diamond_pos[0]["edge1"]["x"],
            'y': diamond_pos[0]["edge4"]["y"],
            'width': abs(diamond_pos[0]["edge1"]["x"] - diamond_pos[0]["edge2"]["x"]),
            'height': abs(diamond_pos[0]["edge3"]["y"] - diamond_pos[0]["edge4"]["y"])
            }
            if has_collided(diamond_box, catcher_box):
                # print("collided")
                diamond_x = random.randint(20, 500) 
                if diamond_x <= arrow_box['x'] + arrow_box["width"]:
                    diamond_x = 65
                elif diamond_x >= cross_box['x']:
                    diamond_x = cross_box['x'] - 25    
                elif diamond_x >= pause_box2['x'] and diamond_x <= pause_box2['x'] + pause_box2['width']:
                    if pause_box2['x'] <= diamond_x <= (pause_box2['x'] + pause_box2['x'] +pause_box2["width"])//2:
                        diamond_x = pause_box2['x']  - pause_box2['width'] - 30  
                    else:
                        diamond_x = pause_box2['x']  + pause_box2['width'] + 30 
                diamond_color = (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))
                diamond_pos = [{"edge1": {"x": diamond_x, "y": 500}, #right_edge
                    "edge2": {"x": diamond_x-20, "y": 500}, #left_edge
                    "edge3": {"x": diamond_x-10, "y": 510}, #top_edge
                    "edge4": {"x": diamond_x-10, "y": 490}},#bottom_edge 
                    diamond_color]
                diamond_box = {
                    'x': diamond_pos[0]["edge1"]["x"],
                    'y': diamond_pos[0]["edge4"]["y"],
                    'width': abs(diamond_pos[0]["edge1"]["x"] - diamond_pos[0]["edge2"]["x"]),
                    'height': abs(diamond_pos[0]["edge3"]["y"] - diamond_pos[0]["edge4"]["y"])
                    }
                
                points += 1
                speed += 1
                print(points)
            else:
                for edge in diamond_pos[0]:    
                    diamond_pos[0][edge]["y"] -= speed
                    if diamond_pos[0][edge]["y"] < catcher_info[0]["base"]["y1"]:
                        if diamond_pos[0][edge]["y"] < 0:
                            stop = False #stop is used when diamond misses catcher
                            catcher_info[1] = [1,0,0]
                            diamond_pos[1] = [0, 0, 0]
                            print("Game Over")
                            print("Your Score: ", points)


    glutPostRedisplay()
    time.sleep(0.01)

def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    catcher()
    diamond()
    draw_arrow()
    draw_pause()
    draw_cross()
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
glutMainLoop()