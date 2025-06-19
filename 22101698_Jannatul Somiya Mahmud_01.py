from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

#TASK-1

# W_Width, W_Height = 500, 500
# angle = 0
# raindrops = [(random.uniform(-1, 1), random.uniform(0, 1)) for x in range(100)]
# background_color = 0

# def drawGround():
    
#     glColor3f(133/255, 81/255, 50/255)
#     glBegin(GL_TRIANGLES)
   
#     glVertex2i(0, 0)
#     glVertex2i(500, 0)
#     glVertex2i(500, int(500 * 0.7))

#     glVertex2i(0, 0)
#     glVertex2i(500, int(500 * 0.7))
#     glVertex2i(0, int(500 * 0.7))
#     glEnd()

# def drawTrees():
#     glColor3f(0, 128/255, 0)  
#     tree_y = 250 - int(500 * 0.02)

#     tree_height = 100
#     tree_width = 50  

#     for x in range(0, 500, tree_width):
#         glBegin(GL_TRIANGLES)
#         glVertex2i(x, tree_y)
#         glVertex2i(x + tree_width, tree_y)
#         glVertex2i(x + tree_width // 2, tree_y + tree_height)
#         glEnd()

# def drawHouse():
#     glBegin(GL_TRIANGLES)
#     glColor3f(255, 255, 255)

#     # Body of the house
#     glVertex2i(100, 100)
#     glVertex2i(370, 100)
#     glVertex2i(370, 250)

#     glVertex2i(100, 100)
#     glVertex2i(370, 250)
#     glVertex2i(100, 250)
#     glEnd()

#     #roof
#     glBegin(GL_TRIANGLES)
#     glColor3f(77/255, 0.0, 153/255)
#     glVertex2i(80, 250)
#     glVertex2i(390, 250)
#     glVertex2i(235, 400) 
#     glEnd()

#     #window
#     glBegin(GL_TRIANGLES)
#     glColor3f(52/255, 161/255, 235/255)

#     #window 1
#     glVertex2i(130, 150)
#     glVertex2i(180, 150)
#     glVertex2i(180, 200)

#     glVertex2i(130, 150)
#     glVertex2i(180, 200)
#     glVertex2i(130, 200)

#     #window 2
#     glVertex2i(290, 150)
#     glVertex2i(340, 150)
#     glVertex2i(340, 200)

#     glVertex2i(290, 150)
#     glVertex2i(340, 200)
#     glVertex2i(290, 200)
#     glEnd()

#     #lines inside the window
#     glColor3f(0, 0, 0)
#     glBegin(GL_LINES)
#     #window 1
#     glVertex2i(155, 150)
#     glVertex2i(155, 200)

#     glVertex2i(130, 175)
#     glVertex2i(180, 175)

#     #window 2
#     glVertex2i(315, 150)
#     glVertex2i(315, 200)

#     glVertex2i(290, 175)
#     glVertex2i(340, 175)
#     glEnd()

#     #door
#     glBegin(GL_TRIANGLES)
#     glColor3f(52/255, 161/255, 235/255)
#     glVertex2i(210, 100)
#     glVertex2i(260, 100)
#     glVertex2i(260, 200)

#     glVertex2i(210, 100)
#     glVertex2i(260, 200)
#     glVertex2i(210, 200)
#     glEnd()

#     #door lock
#     glColor3f(0.0, 0.0, 0.0)
#     glPointSize(5)
#     glBegin(GL_POINTS)
#     glVertex2i(250, 150)
#     glEnd()

# def animate():
#     global raindrops
#     for i in range(len(raindrops)):
#         x, y = raindrops[i]
#         x += angle
#         y -= 2

#         if y < 0:
#             x = random.uniform(0, W_Width)
#             y = random.uniform(0, W_Height)

#         raindrops[i] = (x, y)
#     glutPostRedisplay()

# def drawRain():
#     glColor3f(0, 0, 1)
#     glBegin(GL_LINES)
#     for x, y in raindrops:
#         glVertex2f(x, y)
#         glVertex2f(x + angle * 2, y - 10)
#     glEnd()

# def specialKeyListener(key, x, y):
#     global angle, background_color
#     if key == GLUT_KEY_LEFT:
#         angle = max(-5, angle - 0.5)
#     elif key == GLUT_KEY_RIGHT:
#         angle = min(5, angle + 0.5)

#     elif key == GLUT_KEY_UP: 
#         background_color = min(1.0, background_color + 0.1)
#     elif key == GLUT_KEY_DOWN:
#         background_color = max(0.0, background_color - 0.1)
#     glutPostRedisplay()


# def display():
#     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#     glClearColor(background_color, background_color, background_color, 1.0)
#     drawGround()
#     drawTrees()
#     drawHouse()
#     drawRain()
#     glutSwapBuffers()

# def init():
#     glClearColor(0, 0, 0, 0)
#     glMatrixMode(GL_PROJECTION)
#     glLoadIdentity()
#     gluOrtho2D(0, 500, 0, 500) 

# glutInit()
# glutInitWindowSize(W_Width, W_Height)
# glutInitWindowPosition(0, 0)
# glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
# glutCreateWindow(b"Building a House in Rainfall")

# init()

# glutDisplayFunc(display)
# glutIdleFunc(animate)
# glutSpecialFunc(specialKeyListener)

# glutMainLoop()



#TASK-2

W_Width, W_Height = 500,500
points = []
paused = False
speed = 0.01

class point:
    def __init__(self, x, y, color, direction):
        self.x = x
        self.y = y
        self.color = color
        self.dir = direction
        self.is_visible = True  

    def ballDirection(self):
        if not paused:
            self.x += self.dir[0] * speed
            self.y += self.dir[1] * speed
            if self.x <= -W_Width // 2 or self.x >= W_Width // 2:
                self.dir = (-self.dir[0], self.dir[1])
            if self.y <= -W_Height // 2 or self.y >= W_Height // 2:
                self.dir = (self.dir[0], -self.dir[1])
    def drawPoint(self):
        if self.is_visible:
            glPointSize(5)
            glBegin(GL_POINTS)
            glColor3f(random.randint(0,255)/255, random.randint(0,255)/255, random.randint(0,255)/255)
            glVertex2f(self.x, self.y)
            glEnd()

    def blink(self):
        self.is_visible = not self.is_visible

def convert_coordinate(x, y):
    global W_Width, W_Height
    a = x - (W_Width / 2)
    b = (W_Height / 2) - y
    return a, b


def keyboardListener(key, x, y):
    global paused
    if key == b" ":
        paused = not paused
    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global speed
    if key==GLUT_KEY_UP:
        speed *= 2
        print("Speed Increased")
    if key== GLUT_KEY_DOWN:
        speed /= 2
        print("Speed Decreased")
    glutPostRedisplay()

def mouseListener(button, state, x, y):
    global points
    if button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            color = glColor3f(random.randint(0,255)/255, random.randint(0,255)/255, random.randint(0,255)/255)
            direction = random.choice([(-1, -1), (-1, 1), (1, -1), (1, 1)])
            c_x, c_y = convert_coordinate(x, y)
            points.append(point(c_x, c_y, color, direction))

    elif button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            for i in points:
                i.blink()
    glutPostRedisplay()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    for x in points:
        x.drawPoint()
    glutSwapBuffers()

def animate():
    for y in points:
        y.ballDirection()
    glutPostRedisplay()

def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-250, 250, -250, 250)


glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutCreateWindow(b"Building the Amazing Box")

init()

glutDisplayFunc(display)
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)

glutMainLoop()
