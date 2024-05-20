from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

fps = 30
freeze=False
lives = 3
game_over=False
game_win = False
fire_ball = False
magnetic_bat=False
shooter_powerup=False
unstoppable = False

previous_time = time.time()
W_Width, W_Height = 500,500

dx_bat_speed = 30
dx_bat = {
    "x1": 0,
    "y1": 0,
    'width': 100,
    'height': 15
}
dx_bat_color = [1, 1, 1]

# dx_ball_center = (250, 30)
dx_ball_radius = 5
dx_ball_center = (dx_bat['x1'] + dx_bat['width'] // 2, dx_bat['y1'] + dx_bat['height'] + dx_ball_radius)
dx_ball_speed = (5, 5)
dx_ball_color = [1, 1, 1]

dx_ball_deviation = 5
bullets = []
dx_stages_dictionary = {}
current_stage = 1

dx_pattern_dictionary = {}
powerups=["increase_ball_speed", "decrease_ball_speed", "increase_bat_size", "decrease_bat_size", "shooter", "unstoppable", "magnet"]
solid_prob = 0.2
powerup_prob = 0.2


powerup_info_dict = {
    "increase_bat_size": {
        "color": [1, 0, 1],
        "effect": "increase_bat_size",
        "value": 50
    },
    "decrease_bat_size": {
        "color": [0, 1, 0],
        "effect": "decrease_bat_size",
        "value": -30
    },
    "increase_ball_speed": {
        "color": [0, 0, 1],
        "effect": "increase_ball_speed",
        "value": 1.5
    },
    "decrease_ball_speed": {
        "color": [1, 1, 0],
        "effect": "decrease_ball_speed",
        "value": 3
    },
    "shooter": {
        "color": [1, 0, 0],
        "effect": "shooter",
        "value": True
    },
    "unstoppable": {
        "color": [1, 0.5, 0],
        "effect": "unstoppable",
        "value": True
    },
    "magnet": {
        "color": [1, 1, 1],
        "effect": "magnet",
        "value": True
    }

}
current_poweruplist = []

def assign_powerup(probability):
    global powerups, dx_pattern_dictionary
    rand_num = random.randint(0, int(1/probability))
    if rand_num == 0:
        powerup = random.choice(powerups)
        print(f"Assigned Powerup {powerup}")
        # dx_pattern_dictionary[(x, y)][1] = powerup
    else:
        powerup = None
    return powerup

# Stage 1:
for y in range(380, 321, -20):
    for x in range(100, 351, 50):
        rand_num = random.randint(0, int(1/solid_prob))
        
        if rand_num == 0:
            dx_pattern_dictionary[(x, y)] = ["solid", assign_powerup(powerup_prob)]
        else:
            dx_pattern_dictionary[(x, y)] = ["hollow", assign_powerup(powerup_prob)]
dx_stages_dictionary[1] = dx_pattern_dictionary


# Stage 2:
dx_pattern_dictionary = {}
pyramid_top = (225, 380)
pyramid_height = 5
for i in range(pyramid_height):
    y = 380 - i*20
    for x in range(pyramid_top[0] - i*50, pyramid_top[0] + i*50 + 1, 50):
        rand_num = random.randint(0, int(1/solid_prob))
        if rand_num == 0:
            dx_pattern_dictionary[(x, y)] = ["solid", assign_powerup(powerup_prob)]
        else:
            dx_pattern_dictionary[(x, y)] = ["hollow", assign_powerup(powerup_prob)]
dx_stages_dictionary[2] = dx_pattern_dictionary


# Stage 3:
dx_pattern_dictionary = {}
top = (225, 380)
bottom = (225, 260)
radius = 3
for i in range(radius+1):
    y = 380 - i*20
    for x in range(pyramid_top[0] - i*50, pyramid_top[0] + i*50 + 1, 50):
        rand_num = random.randint(0, int(1/solid_prob))
        if rand_num == 0:
            dx_pattern_dictionary[(x, y)] = ["solid", assign_powerup(powerup_prob)]
        else:
            dx_pattern_dictionary[(x, y)] = ["hollow", assign_powerup(powerup_prob)]

for i in range(radius, -1, -1):
    y = 240 + i*20
    for x in range(pyramid_top[0] - i*50, pyramid_top[0] + i*50 + 1, 50):
        rand_num = random.randint(0, int(1/solid_prob))
        if rand_num == 0:
            dx_pattern_dictionary[(x, y)] = ["solid", assign_powerup(powerup_prob)]
        else:
            dx_pattern_dictionary[(x, y)] = ["hollow", assign_powerup(powerup_prob)]        

dx_stages_dictionary[3] = dx_pattern_dictionary


powerup_deactivate_dict={'magnet': 0, 'shooter': 1, 'unstoppable': 2, 'increase_bat_size': 3, 'decrease_bat_size': 4, "increase_ball_speed": 5, "decrease_ball_speed": 6}



def powerup_deactivate(powerup):
    global dx_bat, dx_ball_speed, fire_ball, magnetic_bat,powerup_deactivate_dict, shooter_powerup, dx_ball_color, dx_bat_color, unstoppable
    if powerup == powerup_deactivate_dict['magnet']:
        magnetic_bat = False
        dx_bat_color = [1, 1, 1]
        print("Magnetic Bat Deactivated")
    elif powerup == powerup_deactivate_dict['shooter']:
        shooter_powerup = False
        dx_bat_color = [1, 1, 1]
        print("Shooter Powerup Deactivated")
    elif powerup == powerup_deactivate_dict['increase_bat_size']:
        dx_bat['width'] = 100
        print("Bat size reset")
    elif powerup == powerup_deactivate_dict['decrease_bat_size']:
        dx_bat['width'] = 100
        print("Bat size reset")
    elif powerup == powerup_deactivate_dict['increase_ball_speed']:
        val =  powerup_info_dict['increase_ball_speed']['value']
        dx_ball_speed = [dx_ball_speed[0]/val , dx_ball_speed[1]/val]
        print("Ball Speed Reset")
    elif powerup == powerup_deactivate_dict['decrease_ball_speed']:
        val =  powerup_info_dict['increase_ball_speed']['value']
        dx_ball_speed = [dx_ball_speed[0]*val , dx_ball_speed[1]*val]
        print("Ball Speed Reset")
    elif powerup == powerup_deactivate_dict['unstoppable']:
        unstoppable = False
        dx_ball_color = [1, 1, 1]
        print("Ball is stoppable now")    



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

def has_collided(box1, box2):
    return (box1['x'] < box2['x'] + box2['width'] and
            box1['x'] + box1['width'] > box2['x'] and
            box1['y'] < box2['y'] + box2['height'] and
            box1['y'] + box1['height'] > box2['y'])


# FPS
FIXED_TIME_STEP = 1.0 / fps
previous_time = time.time()
accumulator = 0.0

def animate():

    global dx_ball_center, dx_ball_speed, dx_ball_radius, dx_bat, dx_ball_deviation, previous_time, accumulator, freeze, game_over, fire_ball
    current_time = time.time()
    elapsed = current_time - previous_time
    previous_time = current_time
    accumulator += elapsed

    while accumulator >= FIXED_TIME_STEP:
        if not freeze and not game_over and not game_win:
                update_game_state()
                
        accumulator -= FIXED_TIME_STEP


    glutPostRedisplay()


def draw_powerup(powerup, x, y):
    global powerup_info_dict, current_poweruplist
    powerup_info = powerup_info_dict[powerup]
    current_poweruplist.append([x, y, powerup_info['color'], powerup_info])


def draw_powerup_falling():
    global current_poweruplist, dx_bat, dx_ball_speed, powerup_info_dict, fire_ball, magnetic_bat, powerup_deactivate_dict,shooter_powerup, dx_bat_color, dx_ball_color, unstoppable  
    fall_speed = 3 
    bat_box = {"x": dx_bat['x1'], "y": dx_bat['y1'], "width": dx_bat['width'], "height": dx_bat['height']}
    for i in range(len(current_poweruplist)):
        powerup_info = current_poweruplist[i][3]
        powerup_box = {"x": current_poweruplist[i][0]-7, "y": current_poweruplist[i][1]- 7, "width": 14, "height": 14}
        current_poweruplist[i][1] -= fall_speed
        if current_poweruplist[i][1] < 0:
            current_poweruplist.pop(i)
            break
        elif has_collided(powerup_box, bat_box):
            if powerup_info['effect'] == "increase_bat_size":
                dx_bat['width'] += powerup_info['value']
                print("Bat size increased")
                glutTimerFunc(10000, powerup_deactivate, powerup_deactivate_dict['increase_bat_size'])

            elif powerup_info['effect'] == "decrease_bat_size":
                dx_bat['width'] += powerup_info['value']
                print("Bat size decreased")
                glutTimerFunc(10000, powerup_deactivate, powerup_deactivate_dict['decrease_bat_size']) 


            elif powerup_info['effect'] == "increase_ball_speed":
                dx_ball_speed = (dx_ball_speed[0] * powerup_info['value'], dx_ball_speed[1] * powerup_info['value'])
                print("Ball speed increased")
                glutTimerFunc(10000, powerup_deactivate, powerup_deactivate_dict['increase_ball_speed'])

            
            elif powerup_info['effect'] == "decrease_ball_speed":
                dx_ball_speed = (dx_ball_speed[0] / powerup_info['value'], dx_ball_speed[1] / powerup_info['value'])
                print("Ball speed decreased")
                glutTimerFunc(10000, powerup_deactivate, powerup_deactivate_dict['decrease_ball_speed'])



            elif powerup_info['effect'] == "shooter":
                shooter_powerup = True
                dx_bat_color = [1, 0, 0]
                glutTimerFunc(10000, powerup_deactivate, powerup_deactivate_dict['shooter'])

            elif powerup_info['effect'] == "unstoppable":
                unstoppable = True
                dx_ball_color = [1, 0.5, 0]
                glutTimerFunc(10000, powerup_deactivate, powerup_deactivate_dict['unstoppable'])

            elif powerup_info['effect'] == "magnet":
                magnetic_bat = True
                dx_bat_color = [0, 0, 1]
                glutTimerFunc(10000, powerup_deactivate, powerup_deactivate_dict['magnet'])

                

            current_poweruplist.pop(i)
            break
        # print(powerup_info)


def fire_bullet():
    global bullets, dx_bat
    # Create two separate bullet instances
    bullet1 = {'radius': 3, 'center': [dx_bat['x1'], dx_bat['y1'] + dx_bat['height']], 'speed': 5, 'color': [1, 0, 0]}
    bullet2 = {'radius': 3, 'center': [dx_bat['x1'] + dx_bat['width'], dx_bat['y1'] + dx_bat['height']], 'speed': 5, 'color': [1, 0, 0]}
    bullets.append(bullet1)
    bullets.append(bullet2)

def draw_bullets():
    global bullets, W_Height, freeze, game_over
    for bullet in bullets:
        midpoint_circle(bullet['radius'], bullet['color'], bullet['center'])

def update_bullets():
    global bullets, W_Height, freeze, game_over
    for bullet in bullets:
        bullet['center'][1] += bullet['speed']
        if bullet['center'][1] > W_Height:
            bullets.remove(bullet)

def check_bullet_block_collision():
    global bullets, dx_pattern_dictionary
    for bullet in bullets:
        for coordinate, block_powerup in dx_pattern_dictionary.items():
            block, powerup = block_powerup
            block_box = {"x": coordinate[0], "y": coordinate[1], "width": 50, "height": 20}
            bullet_box = {"x": bullet['center'][0] - bullet['radius'], "y": bullet['center'][1] - bullet['radius'], "width": 2*bullet['radius'], "height": 2*bullet['radius']}
            if has_collided(block_box, bullet_box):
                dx_pattern_dictionary.pop(coordinate)
                if powerup:
                    draw_powerup(powerup, coordinate[0], coordinate[1])
                bullets.remove(bullet)    
                break

def update_game_state():
    global dx_ball_center, dx_ball_speed, dx_ball_radius, dx_bat, dx_ball_deviation, current_stage, dx_stages_dictionary, lives, game_over, dx_pattern_dictionary, fire_ball, magnetic_bat, unstoppable, bullets, game_win
    if fire_ball:
        dx_pattern_dictionary = dx_stages_dictionary[current_stage]
        if dx_ball_center[1] - dx_ball_radius <= 0:
            lives -= 1
            dx_ball_center = (dx_bat['x1'] + dx_bat['width'] // 2, dx_bat['y1'] + dx_bat['height'] + dx_ball_radius)
            fire_ball = False
            print("Lives remaining:", lives)
            if lives <= 0:
                print("Game Over")
                game_over = True
                return
        if dx_ball_center[0] + dx_ball_radius > W_Width or dx_ball_center[0] - dx_ball_radius < 0:
            dx_ball_speed = (-dx_ball_speed[0], dx_ball_speed[1])
        if dx_ball_center[1] + dx_ball_radius > W_Height or dx_ball_center[1] - dx_ball_radius < 0:
            dx_ball_speed = (dx_ball_speed[0], -dx_ball_speed[1])

        # Collision with Block
        for coordinate, block_powerup in dx_pattern_dictionary.items():
            block, powerup = block_powerup
            
            block_box = {"x": coordinate[0], "y": coordinate[1], "width": 50, "height": 20}
        
            if has_collided(block_box, {"x": dx_ball_center[0] - dx_ball_radius, "y": dx_ball_center[1] - dx_ball_radius, "width": 2*dx_ball_radius, "height": 2*dx_ball_radius}):
                if block == "hollow":
                    dx_pattern_dictionary.pop(coordinate)


                elif block == "solid":
                    dx_pattern_dictionary[coordinate] = ["hollow", None]
                if powerup:
                    draw_powerup(powerup, coordinate[0], coordinate[1])

                if not unstoppable:
                    dx_ball_speed = (dx_ball_speed[0], -dx_ball_speed[1])
                break

        if len(dx_pattern_dictionary) == 0: 
            next_stage = current_stage + 1
            if current_stage + 1 <= len(dx_stages_dictionary.keys()):
                current_stage += 1
            if next_stage in dx_stages_dictionary:
                load_stage(next_stage)
                dx_ball_center = (dx_bat['x1'] + dx_bat['width'] // 2, dx_bat['y1'] + dx_bat['height'] + dx_ball_radius)
                bullets = []
            else:
                game_win = True
                print("Congratulations! All stages completed!")

        

        # Collision detection with bat
        ball_box = {"x": dx_ball_center[0] - dx_ball_radius, "y": dx_ball_center[1] - dx_ball_radius, "width": 2*dx_ball_radius, "height": 2*dx_ball_radius}
        bat_box = {"x": dx_bat['x1'], "y": dx_bat['y1'], "width": dx_bat['width'], "height": dx_bat['height']}

        if has_collided(ball_box, bat_box):
            if magnetic_bat:
                fire_ball = False
            else:
                hit_point = dx_ball_center[0]
                bat_center = dx_bat['x1'] + dx_bat['width'] / 2
                offset = hit_point - bat_center
                
                influence = offset / (dx_bat['width'] / 2) 
                new_dx = influence*dx_ball_deviation 

                dx_ball_speed = (new_dx, -dx_ball_speed[1])

        dx_ball_center = (dx_ball_center[0] + dx_ball_speed[0], dx_ball_center[1] + dx_ball_speed[1])
    draw_powerup_falling()
    update_bullets()
    glutPostRedisplay()

def keyboardListener(key, x, y):
    global fire_ball, dx_ball_center, dx_ball_speed, dx_bat, dx_ball_radius
    if key == b' ':
        print("Space pressed")
        if not fire_ball or magnetic_bat: 
            fire_ball = True
            if magnetic_bat:  
                dx_ball_center = (dx_bat['x1'] + dx_bat['width'] // 2, dx_bat['y1'] + dx_bat['height'] + dx_ball_radius)
                dx_ball_speed = (dx_ball_speed[0], -dx_ball_speed[1])

    if key == b'a':
        print("a pressed")
    if key == b'd':
        print("d pressed")
    if key == b'x':
        if shooter_powerup:
            fire_bullet()

    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global dx_bat_speed , freeze, game_over, fire_ball,dx_ball_center
    if freeze==False and game_over==False:
        if key==GLUT_KEY_RIGHT:
            if dx_bat['x1'] + dx_bat['width'] < 500:
                dx_bat['x1'] += dx_bat_speed
                if not fire_ball:  
                    dx_ball_center = (dx_bat['x1'] + dx_bat['width'] // 2, dx_bat['y1'] + dx_bat['height'] + dx_ball_radius)



        elif key==GLUT_KEY_LEFT:
            if dx_bat['x1'] > 0:
                dx_bat['x1'] -= dx_bat_speed
                if not fire_ball:  
                    dx_ball_center = (dx_bat['x1'] + dx_bat['width'] // 2, dx_bat['y1'] + dx_bat['height'] + dx_ball_radius)




    glutPostRedisplay()

def reset():
    global dx_bat, dx_ball_center, dx_ball_speed, dx_ball_radius, dx_pattern_dictionary, current_stage, lives, game_over, fire_ball, magnetic_bat, current_poweruplist, dx_stages_dictionary, bullets
    


    dx_bat['x1'] = 0
    dx_ball_center = (dx_bat['x1'] + dx_bat['width'] // 2, dx_bat['y1'] + dx_bat['height'] + dx_ball_radius)
    dx_ball_speed = (5, 5)
    dx_ball_radius = 5
    current_stage = 1
    lives = 3
    game_over = False
    game_win = False
    fire_ball = False
    magnetic_bat = False
    current_poweruplist = []
    dx_stages_dictionary = {}
    dx_pattern_dictionary = {}
    for y in range(380, 321, -20):
        for x in range(100, 351, 50):
            rand_num = random.randint(0, int(1/solid_prob))

            if rand_num == 0:
                dx_pattern_dictionary[(x, y)] = ["solid", assign_powerup(powerup_prob)]
            else:
                dx_pattern_dictionary[(x, y)] = ["hollow", assign_powerup(powerup_prob)]
    dx_stages_dictionary[1] = dx_pattern_dictionary


    # Stage 2:
    dx_pattern_dictionary = {}
    pyramid_top = (225, 380)
    pyramid_height = 5
    for i in range(pyramid_height):
        y = 380 - i*20
        for x in range(pyramid_top[0] - i*50, pyramid_top[0] + i*50 + 1, 50):
            rand_num = random.randint(0, int(1/solid_prob))
            if rand_num == 0:
                dx_pattern_dictionary[(x, y)] = ["solid", assign_powerup(powerup_prob)]
            else:
                dx_pattern_dictionary[(x, y)] = ["hollow", assign_powerup(powerup_prob)]


    dx_stages_dictionary[2] = dx_pattern_dictionary

        
    # Stage 3:
    dx_pattern_dictionary = {}
    top = (225, 380)
    bottom = (225, 260)
    radius = 3
    for i in range(radius+1):
        y = 380 - i*20
        for x in range(pyramid_top[0] - i*50, pyramid_top[0] + i*50 + 1, 50):
            rand_num = random.randint(0, int(1/solid_prob))
            if rand_num == 0:
                dx_pattern_dictionary[(x, y)] = ["solid", assign_powerup(powerup_prob)]
            else:
                dx_pattern_dictionary[(x, y)] = ["hollow", assign_powerup(powerup_prob)]

    for i in range(radius, -1, -1):
        y = 240 + i*20
        for x in range(pyramid_top[0] - i*50, pyramid_top[0] + i*50 + 1, 50):
            rand_num = random.randint(0, int(1/solid_prob))
            if rand_num == 0:
                dx_pattern_dictionary[(x, y)] = ["solid", assign_powerup(powerup_prob)]
            else:
                dx_pattern_dictionary[(x, y)] = ["hollow", assign_powerup(powerup_prob)]        

    dx_stages_dictionary[3] = dx_pattern_dictionary

    bullets = []


def mouseListener(button, state, x, y):
    global freeze  
    if button == GLUT_LEFT_BUTTON:
        if (state == GLUT_DOWN):  
            c_X, c_y = convert_coordinate(x, y)
            if c_X <= 50 and (c_y >= 450 and c_y <= 500):
                reset()
                print('Starting Over!')
            elif c_X >= 440 and (c_y >= 450 and c_y <= 500):
                print('Goodbye! Score:')
                glutLeaveMainLoop()
            elif (c_X >= 230 and c_X <= 270) and (c_y >= 450 and c_y <= 500):
                print(freeze)

                freeze = not freeze
                #print(freeze)
                print(freeze)

    glutPostRedisplay()

def pause_icon(x1,y1,x2,y2,color):
    global freeze, game_over
    if freeze==True:
        #print(x1,y1,x2,y2,s,c)
        draw_line(x1,y1,x2,y2,color)
        draw_line(x1,y1,x2+40,y2-25,color)
        draw_line(x1,y1+50,x2+40,y2-25,color)
    else:   
        draw_line(x1, y1, x2, y2,color) 
        draw_line(x1+20,y1,x2+20,y2,color)   


def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()




def draw_rectangle_block(rectangle_block,color):
    x1, y1 = rectangle_block['x1'], rectangle_block['y1']
    x2, y2 = x1 + rectangle_block['width'], y1
    x3, y3 = x2, y1 + rectangle_block['height']
    x4, y4 = x1, y1 + rectangle_block['height']
    eight_way_symmetry(x1, y1, x2, y2, color)
    eight_way_symmetry(x2, y2, x3, y3, color)
    eight_way_symmetry(x3, y3, x4, y4, color)
    eight_way_symmetry(x4, y4, x1, y1, color)

def draw_rectangle_block_filled(rectangle_block, color):
    x1, y1 = rectangle_block['x1'], rectangle_block['y1']
    width = rectangle_block['width']
    height = rectangle_block['height']

    for y in range(y1, y1 + height):
        for x in range(x1, x1 + width):
            draw_points(x, y, color)

def draw_solid_block(rectangle_block, color):
    x1 = rectangle_block['x1']
    y1 = rectangle_block['y1']
    width = rectangle_block['width']
    height = rectangle_block['height']
    x2, y2 = x1 + width, y1
    x3, y3 = x1 + width, y1 + height
    x4, y4 = x1, y1 + height

    # for y in range(y1, y1 + height):
    #     for x in range(x1, x1 + width):
    #         draw_points(x, y, color)

    eight_way_symmetry(x1, y1, x3, y3, color)
    eight_way_symmetry(x4, y4, x2, y2, color)



def draw_line(x1, y1, x2, y2, color):
    eight_way_symmetry(x1, y1, x2, y2, color)

def load_stage(stage_number):
    global dx_pattern_dictionary, dx_stages_dictionary, current_stage
    if stage_number in dx_stages_dictionary:
        dx_pattern_dictionary = dx_stages_dictionary[stage_number]
        current_stage = stage_number
    else:
        print("Stage not found:", stage_number)



def showScreen():
    global rectangle_block, dx_bat, dx_ball_center, dx_pattern_dictionary, current_stage, freeze, game_over,  dx_ball_color, dx_bat_color
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    load_stage(current_stage)
    check_bullet_block_collision()    
    draw_bullets()
    # Draw all blocks for the current stage
    for coordinate, block_info in dx_pattern_dictionary.items():
        block_type, powerup = block_info
        if powerup:
            draw_rectangle_block_filled({"x1": coordinate[0], "y1": coordinate[1], 'width': 50, 'height': 20}, [0,0.5,0.75])
        if block_type == "hollow":
            draw_rectangle_block({"x1": coordinate[0], "y1": coordinate[1], 'width': 50, 'height': 20}, [1,1,1])
        elif block_type == "solid":
            draw_rectangle_block({"x1": coordinate[0], "y1": coordinate[1], 'width': 50, 'height': 20}, [1, 1, 1])
            draw_solid_block({"x1": coordinate[0], "y1": coordinate[1], 'width': 50, 'height': 20}, [1, 1, 1])

    for powerup in current_poweruplist:
        x, y, color, powerup_info = powerup
        midpoint_circle(7, color, (x, y))
    # draw bat
    draw_rectangle_block(dx_bat, dx_bat_color)

    # draw ball
    midpoint_circle(dx_ball_radius, dx_ball_color, dx_ball_center)

    # STOP button

    draw_line(440, 450, 490, 500,[1,0,0])
    draw_line(490, 450, 440, 500,[1,0,0])

    # Pause button
    pause_icon(240, 450, 240, 500, [1, 0.75, 0])


    # Reset button
    draw_line(10, 475, 50, 475, [0, 0.98, 0.78])
    draw_line(10, 475, 40, 500, [0, 0.98, 0.78])
    draw_line(10, 475, 40, 450, [0, 0.98, 0.78])

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