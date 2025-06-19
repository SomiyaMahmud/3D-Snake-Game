from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

window_width= 500
window_height = 700

button_height = 60
button_width = window_width // 3
button_y = 640

gaming_area = window_height - button_height
catcher_width = 80  
catcher_height = 40   
catcher_y = 65
diamond_size = 15

score = 0
game_over = False
paused = False
diamond_x = 0
diamond_y = gaming_area
catcher_x = window_width//2
diamond_color = [random.random(), random.random(), random.random()]
speed = 0.1
diamondAlive = True 

#MIDPOINT ALGORITHM
def findZone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    
    if abs(dx) >= abs(dy):  #zone - 0,3,4,7
        if dx >= 0 and dy >= 0:
            return 0
        elif dx < 0 and dy >= 0:
            return 3
        elif dx < 0 and dy < 0:
            return 4
        else:
            return 7
    else:
        if dx >= 0 and dy >= 0:
            return 1
        elif dx < 0 and dy >= 0:
            return 2
        elif dx < 0 and dy < 0:
            return 5
        else:  
            return 6

def convertToZone0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y

def convertToOriginalZone(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y


def lineDrawing(x1, y1, x2, y2, color):
    zone = findZone(x1, y1, x2, y2)
    x1, y1 = convertToZone0(x1, y1, zone)
    x2, y2 = convertToZone0(x2, y2, zone)
    
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    dE = 2 * dy
    dNE = 2 * (dy - dx)
    x = x1
    y = y1
    
    glColor3f(color[0], color[1], color[2])
    glPointSize(2)
    glBegin(GL_POINTS)
    original_x, original_y = convertToOriginalZone(x, y, zone)
    glVertex2f(original_x, original_y)
    
    while x < x2:
        if d > 0:
            d += dNE
            y += 1
        else:
            d += dE
        x += 1
        original_x, original_y = convertToOriginalZone(x, y, zone)
        glVertex2f(original_x, original_y)
    glEnd()

def diamond(x, y, color):
   lineDrawing(x, y, x - 15, y - 15, color)
   lineDrawing(x - 15, y - 15, x, y - 30, color)
   lineDrawing(x, y - 30, x + 15, y - 15, color)
   lineDrawing(x + 15, y - 15, x, y, color)

def catcher(x, y, color):
    lineDrawing(x - 80, y + 40, x + 80, y + 40, color)
    lineDrawing(x - 40, y, x + 40, y, color)
    lineDrawing(x - 40, y, x - 80, y + 40, color)
    lineDrawing(x + 40, y, x + 80, y + 40, color)

def reset(x, y, color):
   lineDrawing(x + 15, y, x - 15, y, color)
   lineDrawing(x - 15, y, x - 7, y + 15, color)
   lineDrawing(x - 15, y, x - 7, y - 15, color)  

def exit(x, y, color):
   lineDrawing(x - 15, y - 15, x + 15, y + 15, color)
   lineDrawing(x - 15, y + 15, x + 15, y - 15, color)

def play(x, y, color):
    if paused:
       lineDrawing(x - 15, y - 15, x - 15, y + 15, color)
       lineDrawing(x - 15, y - 15, x + 15, y, color)
       lineDrawing(x - 15, y + 15, x + 15, y, color)
    else:
       lineDrawing(x - 15, y - 15, x - 15, y + 15, color)
       lineDrawing(x + 15, y - 15, x + 15, y + 15, color)

def detectCollision():
    diamond_left = diamond_x - diamond_size
    diamond_right = diamond_x + diamond_size
    diamond_bottom = diamond_y - 2*diamond_size

    catcher_left = catcher_x - catcher_width
    catcher_right = catcher_x + catcher_width
    catcher_top = catcher_y + catcher_height
    
    return (diamond_bottom <= catcher_top and 
        diamond_bottom >= catcher_y and 
        diamond_left < catcher_right and 
        diamond_right > catcher_left)

def diamondUpdated():
    new_x = random.randint(diamond_size, window_width - diamond_size)
    new_color = [random.random(), random.random(), random.random()]
    return new_x, gaming_area, new_color

def resetGame():
    global score, game_over, diamond_x, diamond_y, diamond_color, speed, paused, diamondAlive
    score = 0
    game_over = False
    paused = False
    speed = 0.1
    diamondAlive = True
    diamond_x, diamond_y, diamond_color = diamondUpdated()

def createNewDiamond():
    global diamond_x, diamond_y, diamond_color, diamondAlive
    diamond_x, diamond_y, diamond_color = diamondUpdated()
    diamondAlive = True

def specialKeyListener(key, x, y):
    global catcher_x
    if paused or game_over:
        return
    else:
        if key == GLUT_KEY_RIGHT:
            if catcher_x + catcher_width <= window_width:
                catcher_x += 10
        if key == GLUT_KEY_LEFT:
            if catcher_x - catcher_width >= 0:
                catcher_x -= 10
    glutPostRedisplay()

def mouseListener(button, state, x, y):
    global paused, game_over
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        y = window_height - y
        
        if y > button_y:
            if x < button_width: 
                resetGame()
                print(f"Starting Over")
            elif x < 2 * button_width:
                paused = not paused
                print("Game Paused" if paused else "Game Resumed")
            else:
                print(f"Goodbye. Final Score: {score}")
                glutLeaveMainLoop()
    glutPostRedisplay()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)
    reset(25, 670, [0.0, 0.8, 0.8])
    play(window_width // 2, 670, [1.0, 0.7, 0.0])
    exit(window_width - 25, 670, [1.0, 0.0, 0.0])

    if not game_over and diamondAlive:
        diamond(diamond_x, diamond_y, diamond_color)
    
    catcher_color = [1.0, 0.0, 0.0] if game_over else [1.0, 1.0, 1.0]
    catcher(catcher_x, catcher_y, catcher_color)
    glutSwapBuffers()

def animation():
    global diamond_y, score, game_over, speed, diamondAlive
    if game_over or paused:
        return
    
    if diamondAlive:
        diamond_y -= speed
        if detectCollision():
            score += 1
            print(f"Score: {score}")
            speed += 0.02
            diamondAlive = False
            createNewDiamond()
        elif diamond_y <= 0:
            game_over = True
            print(f"Game Over. Final Score: {score}")
    glutPostRedisplay()

def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, window_width, 0, window_height, -1, 1)
    glMatrixMode(GL_MODELVIEW)


glutInit()
glutInitWindowSize(window_width, window_height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutCreateWindow(b"Catch the Diamonds!")
init()
glutDisplayFunc(display)
glutIdleFunc(animation)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
createNewDiamond()  
glutMainLoop()