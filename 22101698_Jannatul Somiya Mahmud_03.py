from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math, random, time


GRID_LENGTH = 600
WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 800
fovY = 120

camera_pos = [0, 500, 500]
player_pos = [0, 0, 0]
gun_angle = 0
bullets = []
enemies = []
life = 5
missed_bullets = 0
cheat_mode = False
cheat_vision = False
camera_mode = "third"
game_over = False
rand_var = 423
SCALE_FACTOR = 40
animation_time = 0
enemiesNum = 5
bullet_speed = 10
enemy_speed = 0.3
miss = 10
score = 0

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, 1000, 0, 800)  # left, right, bottom, top

    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_checkerboard():
    square_size = 60
    rows = cols = GRID_LENGTH // square_size

    start_x = -GRID_LENGTH
    start_y = -GRID_LENGTH

    for row in range(2 * rows):
        for col in range(2 * cols):
            x = start_x + col * square_size
            y = start_y + row * square_size
            if (row + col) % 2 == 0:
                 glColor3f(0.6, 0.4, 0.8)
            else:
                glColor3f(1, 1, 1)

            glBegin(GL_QUADS)
            glVertex3f(x, y, 0)
            glVertex3f(x + square_size, y, 0)
            glVertex3f(x + square_size, y + square_size, 0)
            glVertex3f(x, y + square_size, 0)
            glEnd()

def draw_boundaries():
    wall_height = 60
    thickness = 6
    # Front
    glPushMatrix()
    glColor3f(1.0, 1.0, 1.0)
    glTranslatef(0, GRID_LENGTH + thickness / 2, wall_height / 2)
    glScalef(2 * GRID_LENGTH, thickness, wall_height)
    glutSolidCube(1)
    glPopMatrix()
    # Back
    glPushMatrix()
    glColor3f(0.0, 1.0, 1.0)
    glTranslatef(0, -GRID_LENGTH - thickness / 2, wall_height / 2)
    glScalef(2 * GRID_LENGTH, thickness, wall_height)
    glutSolidCube(1)
    glPopMatrix()
    # Left
    glPushMatrix()
    glColor3f(0.0, 1.0, 0.0)
    glTranslatef(-GRID_LENGTH - thickness / 2, 0, wall_height / 2)
    glScalef(thickness, 2 * GRID_LENGTH, wall_height)
    glutSolidCube(1)
    glPopMatrix()
    # Right
    glPushMatrix()
    glColor3f(0.0, 0.0, 1.0)
    glTranslatef(GRID_LENGTH + thickness / 2, 0, wall_height / 2)
    glScalef(thickness, 2 * GRID_LENGTH, wall_height)
    glutSolidCube(1)
    glPopMatrix()

def draw_player():
    global SCALE_FACTOR
    glPushMatrix()
    try:
        player_height = SCALE_FACTOR * 1.75
        glTranslatef(player_pos[0], player_pos[1], player_height)

        if life <= 0:
            glRotatef(90, 0, 0, 1)

        glRotatef(gun_angle, 0, 0, 1)
        glRotatef(90, 1, 0, 0)
        glScalef(SCALE_FACTOR, SCALE_FACTOR, SCALE_FACTOR)

        # Torso
        glPushMatrix()
        glColor3f(0.0, 0.5, 0.0)
        glScalef(1.0, 1.5, 0.5)
        glutSolidCube(1.0)
        glPopMatrix()

        # Head
        glPushMatrix()
        glTranslatef(0.0, 1.2, 0.0)
        glColor3f(0.0, 0.0, 0.0)
        glutSolidSphere(0.4, 32, 32)
        glPopMatrix()

        # Arms
        for side in [-1, 1]:
            glPushMatrix()
            glTranslatef(side * 0.6, 0.6, 0.0)
            glRotatef(180, 0, 1, 0)
            glColor3f(0.9, 0.8, 0.7)
            quad = gluNewQuadric()
            gluCylinder(quad, 0.15, 0.15, 1.0, 32, 32)
            gluDeleteQuadric(quad)
            glTranslatef(0.0, 0.0, 1.0)
            glutSolidSphere(0.15, 32, 32)
            glPopMatrix()

        # gun
        glPushMatrix()
        glTranslatef(0.0, 0.6, 0.0)
        glRotatef(180, 0, 1, 0)
        glColor3f(0.5, 0.5, 0.5)
        quad = gluNewQuadric()
        gluCylinder(quad, 0.15, 0.15, 1.2, 32, 32)
        gluDeleteQuadric(quad)
        glPopMatrix()

        # Legs
        for side in [-0.4, 0.4]:
            glPushMatrix()
            glTranslatef(side, -1.7, 0.0)
            glRotatef(-90, 1, 0, 0)
            glColor3f(0.0, 0.0, 1.0)
            quad = gluNewQuadric()
            gluCylinder(quad, 0.15, 0.15, 1.0, 32, 32)
            gluDeleteQuadric(quad)
            glPopMatrix()
    finally:
        glPopMatrix()

def draw_enemy(x, y):
    global animation_time
    glPushMatrix()
    try:
        scale = 0.5 + 0.2 * math.sin(animation_time * 3)
        hover_height = 15
        glTranslatef(x, y, hover_height)
        glColor3f(1, 0, 0)
        glutSolidSphere(SCALE_FACTOR * scale, 16, 16)
        glPushMatrix()
        glTranslatef(0, 0, SCALE_FACTOR * 0.8)
        glColor3f(0, 0, 0)
        glutSolidSphere(SCALE_FACTOR * 0.3, 16, 16)
        glPopMatrix()
    finally:
        glPopMatrix()

def generate_spawn_position():
    while True:
        x, y = random.randint(-GRID_LENGTH + 100, GRID_LENGTH - 100), random.randint(-GRID_LENGTH + 100, GRID_LENGTH - 100)
        dx = player_pos[0] - x
        dy = player_pos[1] - y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist > 200:
            return [x, y]

def spawn_enemy():
    return {
        'pos': generate_spawn_position(),
    }

def maintain_enemies():
    while len(enemies) < enemiesNum:
        enemies.append(spawn_enemy())

def move_enemies():
    global life, game_over
    for enemy in enemies[:]:
        dx = player_pos[0] - enemy['pos'][0]
        dy = player_pos[1] - enemy['pos'][1]
        dist = math.sqrt(dx*dx + dy*dy)
        if dist < 10:
            life -= 1
            enemies.remove(enemy)
            if life <= 0:
                game_over = True
            continue
        next_x = enemy['pos'][0] + enemy_speed * dx / dist
        next_y = enemy['pos'][1] + enemy_speed * dy / dist
        if -GRID_LENGTH <= next_x <= GRID_LENGTH and -GRID_LENGTH <= next_y <= GRID_LENGTH:
            enemy['pos'][0] = next_x
            enemy['pos'][1] = next_y

        
def draw_bullet(bullet):
    glPushMatrix()
    glTranslatef(*bullet['pos'])
    glColor3f(0, 1, 1)
    glutSolidCube(10)
    glPopMatrix()


def move_bullets():
    global missed_bullets, game_over,score
    new_bullets = []
    for bullet in bullets:
        bullet['pos'][0] += bullet_speed * math.cos(math.radians(bullet['angle']))
        bullet['pos'][1] += bullet_speed * math.sin(math.radians(bullet['angle']))
        if abs(bullet['pos'][0]) > GRID_LENGTH or abs(bullet['pos'][1]) > GRID_LENGTH:
            missed_bullets += 1
            if missed_bullets >= miss:
                game_over = True
            continue
        hit = False
        for enemy in enemies:
            dx = bullet['pos'][0] - enemy['pos'][0]
            dy = bullet['pos'][1] - enemy['pos'][1]
            if dx*dx + dy*dy < (SCALE_FACTOR * 1.5) ** 2:
                enemies.remove(enemy)
                score += 1
                hit = True
                break
        if not hit:
            new_bullets.append(bullet)
    return new_bullets

def fire_bullet():
    bullets.append({
        'pos': list(player_pos),
        'angle': gun_angle
    })

def fire_cheat_bullet():
    global gun_angle
    if not enemies:
        return
    closest_enemy = min(enemies, key=lambda e: (e['pos'][0] - player_pos[0])**2 + (e['pos'][1] - player_pos[1])**2)
    dx = closest_enemy['pos'][0] - player_pos[0]
    dy = closest_enemy['pos'][1] - player_pos[1]
    angle = math.degrees(math.atan2(dy, dx))
    gun_angle = angle
    fire_bullet()

def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    if camera_mode == "first" and cheat_vision:
        angle_rad = math.radians(gun_angle)
        eyeX = player_pos[0] + 40 * math.cos(angle_rad)
        eyeY = player_pos[1] + 40 * math.sin(angle_rad)
        eyeZ = player_pos[2] + 20
        gluLookAt(eyeX, eyeY, eyeZ,
                  eyeX + math.cos(angle_rad), eyeY + math.sin(angle_rad), eyeZ,
                  0, 0, 1)
    else:
        gluLookAt(*camera_pos, 0, 0, 0, 0, 0, 1)


def idle():
    global bullets, gun_angle
    if not game_over:
        bullets = move_bullets()
        move_enemies()
        maintain_enemies()
        if cheat_mode and len(bullets) == 0:
            fire_cheat_bullet()
    glutPostRedisplay()


def keyboardListener(key, x, y):
    global gun_angle, player_pos, cheat_mode, cheat_vision, life, missed_bullets, bullets, game_over, score
    move_dist = 10
    if key == b'w':
        new_x = player_pos[0] + move_dist * math.cos(math.radians(gun_angle))
        new_y = player_pos[1] + move_dist * math.sin(math.radians(gun_angle))
        if -GRID_LENGTH <= new_x <= GRID_LENGTH and -GRID_LENGTH <= new_y <= GRID_LENGTH:
            player_pos[0] = new_x
            player_pos[1] = new_y
    if key == b's':
        new_x = player_pos[0] - move_dist * math.cos(math.radians(gun_angle))
        new_y = player_pos[1] - move_dist * math.sin(math.radians(gun_angle))
        if -GRID_LENGTH <= new_x <= GRID_LENGTH and -GRID_LENGTH <= new_y <= GRID_LENGTH:
            player_pos[0] = new_x
            player_pos[1] = new_y
    if key == b'a':
        gun_angle += 5
    if key == b'd':
        gun_angle -= 5
    if key == b'c':
        cheat_mode = not cheat_mode
    if key == b'v':
        cheat_vision = not cheat_vision
    if key == b'r' and game_over:
        life = 5
        missed_bullets = 0
        bullets = []
        enemies.clear()
        player_pos[:] = [0, 0, 0]
        game_over = False
        score = 0


def specialKeyListener(key, x, y):
    if key == GLUT_KEY_UP:
        camera_pos[2] += 10
    if key == GLUT_KEY_DOWN:
        camera_pos[2] -= 10
    if key == GLUT_KEY_LEFT:
        camera_pos[0] -= 10
    if key == GLUT_KEY_RIGHT:
        camera_pos[0] += 10


def mouseListener(button, state, x, y):
    global camera_mode
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and not game_over:
        fire_bullet()
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        camera_mode = "first" if camera_mode == "third" else "third"

def showScreen():
    global bullets, animation_time, score
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setupCamera()
    draw_checkerboard()
    draw_boundaries()
    draw_player()
    for enemy in enemies:
        draw_enemy(*enemy['pos'])
    for bullet in bullets:
        draw_bullet(bullet)
    
    draw_text(10, WINDOW_HEIGHT - 30, f"Player Life Remaining: {life}    Game Score: {score}    Player Bullet Missed: {missed_bullets}")
    if game_over:
        draw_text(WINDOW_WIDTH // 2 - 80, WINDOW_HEIGHT // 2, "GAME OVER - Press R to Restart")
    
    glutSwapBuffers()
    animation_time = time.time() % 10

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow(b"Bullet Frenzy 3D Game")
    glEnable(GL_DEPTH_TEST)

    for _ in range(enemiesNum):
        enemies.append(spawn_enemy())

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    glutMainLoop()

if __name__ == "__main__":
    main()
 