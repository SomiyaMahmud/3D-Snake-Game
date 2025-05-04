from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time
import math

# Camera-related variables
camera_pos = (0, 500, 500)

fovY = 120  # Field of view
GRID_LENGTH = 600

# Game variables
BOARD_WIDTH = GRID_LENGTH * 2
BOARD_HEIGHT = GRID_LENGTH * 2
CELL_SIZE = 30
snake = []  # List of snake segments (x, y, z)
snake_direction = (CELL_SIZE, 0, 0)  # Initial direction (right)
food_pos = (0, 0, CELL_SIZE/2)
food_exists = False
bonus_food_pos = (0, 0, CELL_SIZE/2)
bonus_food_exists = False
bonus_food_timer = 0
bonus_food_duration = 15  # seconds
food_eaten_count = 0
SCORE = 0
LEVEL = 1
GAME_OVER = False
PAUSE = False
snake_length = 3
last_update_time = 0

# Level transition variables
level_transition_active = False
level_transition_start_time = 0

BOARD_COLORS = {
    "board1": (0.5, 0.8, 0.5),  # Green
    "board2": (0.6, 0.8, 0.6)   # Light green
}
LEVEL_COLORS = {
    1: {
        "head": (0.0, 0.8, 0.2),     # Bright green
        "body": (0.0, 0.7, 0.0),     # Dark green
        "food": (1.0, 0.0, 0.0),   # Red
        "obstacles": (0.55, 0.27, 0.27)  # Brick red
    },
    2: {
        "head": (0.0, 0.5, 0.9),     # Bright blue
        "body": (0.0, 0.3, 0.7),     # Dark blue
        "food": (1.0, 0.5, 0.0),   # Orange
        "obstacles": (0.55, 0.27, 0.27)   # Brick red
    },
    3: {
        "head": (0.8, 0.2, 0.8),     # Bright purple
        "body": (0.6, 0.1, 0.6),     # Dark purple
        "food": (0.7, 0.17, 0.52),   # Pink
        "obstacles": (0.55, 0.27, 0.27)   # Brick red
    }
}
LEVEL_OBSTACLES = {                  # Format: (x, z, width, depth, height)
    1: [
        (-200, 200, 150, 50, 40),
        (200, 200, 150, 50, 40),
        (0, -100, 250, 50, 40)
    ],
    2: [
        (-300, 200, 150, 50, 40),
        (300, 200, 150, 50, 40),
        (0, 0, 300, 50, 40),
        (-200, -200, 150, 50, 40),
        (200, -200, 150, 50, 40)
    ],
    # Level 3: Maze-like obstacles
    3: [
        # Left side obstacles
        (-300, 0, 400, 30, 40),
        (-450, 200, 30, 400, 40),
        (-200, -200, 30, 400, 40),
        # Right side obstacles
        (300, 0, 400, 30, 40),
        (450, 200, 30, 400, 40),
        (200, -200, 30, 400, 40),
        # Center obstacles
        (0, 300, 30, 300, 40),
        (0, -300, 30, 300, 40)
    ]
}

obstacles = LEVEL_OBSTACLES[1]      # Current obstacles based on level

# Portal variables - updated
NUM_PORTALS = 3
portals = []  # Will hold (x, y, z, color_index) for each portal
portal_colors = [(0.0, 0.0, 0.0),]
portal_size = CELL_SIZE * 1.2
portal_rotation = 0
portal_cooldown = 0  # Cooldown to prevent immediate re-teleporting
PORTAL_COOLDOWN_TIME = 2  # seconds
last_teleport_time = 0

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, 1000, 0, 800)  # left, right, bottom, top
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Draw text at (x, y) in screen coordinates
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
    # Restore original projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_board():
    colors = LEVEL_COLORS[LEVEL].copy()
    colors.update(BOARD_COLORS)

    if LEVEL == 1:
        # Solid green board
        glColor3f(*colors["board1"])
        glBegin(GL_QUADS)
        glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
        glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
        glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
        glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
        glEnd()

    elif LEVEL == 2:
        square_size = 60
        rows = cols = GRID_LENGTH // square_size
        start_x = -GRID_LENGTH
        start_y = -GRID_LENGTH

        for row in range(2 * rows):
            for col in range(2 * cols):
                x = start_x + col * square_size
                y = start_y + row * square_size
                if (row + col) % 2 == 0:
                    glColor3f(*colors["board1"])
                else:
                    glColor3f(*colors["board2"])

                glBegin(GL_QUADS)
                glVertex3f(x, y, 0)
                glVertex3f(x + square_size, y, 0)
                glVertex3f(x + square_size, y + square_size, 0)
                glVertex3f(x, y + square_size, 0)
                glEnd()

    elif LEVEL == 3:
        glBegin(GL_QUADS)

        glColor3f(*colors["board1"])
        glVertex3f(0, 0, 0)
        glVertex3f(0, GRID_LENGTH, 0)
        glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
        glVertex3f(GRID_LENGTH, 0, 0)

        glColor3f(*colors["board2"])
        glVertex3f(0, 0, 0)
        glVertex3f(0, GRID_LENGTH, 0)
        glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
        glVertex3f(-GRID_LENGTH, 0, 0)

        glColor3f(*colors["board1"])
        glVertex3f(0, 0, 0)
        glVertex3f(0, -GRID_LENGTH, 0)
        glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
        glVertex3f(-GRID_LENGTH, 0, 0)

        glColor3f(*colors["board2"])
        glVertex3f(0, 0, 0)
        glVertex3f(0, -GRID_LENGTH, 0)
        glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
        glVertex3f(GRID_LENGTH, 0, 0)

    draw_borders()


def draw_borders():
    segment_count = 20  # Number of segments for the zebra pattern
    segment_length_x = BOARD_WIDTH / segment_count
    segment_length_y = BOARD_HEIGHT / segment_count
    BOARD_EDGE_HEIGHT = 20
    
    # Left
    for i in range(segment_count):
        if i % 2 == 0:
            glColor3f(0.2, 0.2, 0.2)  # Dark black
        else:
            glColor3f(1.0, 1.0, 1.0)  # White
        
        y_start = -BOARD_HEIGHT/2 + i * segment_length_y
        y_end = -BOARD_HEIGHT/2 + (i+1) * segment_length_y

        glBegin(GL_QUADS)
        # Front face
        glVertex3f(-BOARD_WIDTH/2, y_start, 0)
        glVertex3f(-BOARD_WIDTH/2, y_end, 0)
        glVertex3f(-BOARD_WIDTH/2, y_end, BOARD_EDGE_HEIGHT)
        glVertex3f(-BOARD_WIDTH/2, y_start, BOARD_EDGE_HEIGHT)
        
        # Top face
        glVertex3f(-BOARD_WIDTH/2, y_start, BOARD_EDGE_HEIGHT)
        glVertex3f(-BOARD_WIDTH/2, y_end, BOARD_EDGE_HEIGHT)
        glVertex3f(-BOARD_WIDTH/2-20, y_end, BOARD_EDGE_HEIGHT)
        glVertex3f(-BOARD_WIDTH/2-20, y_start, BOARD_EDGE_HEIGHT)
        glEnd()
    
    # Right
    for i in range(segment_count):
        if i % 2 == 0:
            glColor3f(0.2, 0.2, 0.2)
        else:
            glColor3f(1.0, 1.0, 1.0)
        
        y_start = -BOARD_HEIGHT/2 + i * segment_length_y
        y_end = -BOARD_HEIGHT/2 + (i+1) * segment_length_y
        
        glBegin(GL_QUADS)
        # Front face
        glVertex3f(BOARD_WIDTH/2, y_start, 0)
        glVertex3f(BOARD_WIDTH/2, y_end, 0)
        glVertex3f(BOARD_WIDTH/2, y_end, BOARD_EDGE_HEIGHT)
        glVertex3f(BOARD_WIDTH/2, y_start, BOARD_EDGE_HEIGHT)
        
        # Top face
        glVertex3f(BOARD_WIDTH/2, y_start, BOARD_EDGE_HEIGHT)
        glVertex3f(BOARD_WIDTH/2, y_end, BOARD_EDGE_HEIGHT)
        glVertex3f(BOARD_WIDTH/2+20, y_end, BOARD_EDGE_HEIGHT)
        glVertex3f(BOARD_WIDTH/2+20, y_start, BOARD_EDGE_HEIGHT)
        glEnd()
    
    # Top
    for i in range(segment_count):
        if i % 2 == 0:
            glColor3f(0.2, 0.2, 0.2)
        else:
            glColor3f(1.0, 1.0, 1.0)
        
        x_start = -BOARD_WIDTH/2 + i * segment_length_x
        x_end = -BOARD_WIDTH/2 + (i+1) * segment_length_x
        
        glBegin(GL_QUADS)
        # Front face
        glVertex3f(x_start, BOARD_HEIGHT/2, 0)
        glVertex3f(x_end, BOARD_HEIGHT/2, 0)
        glVertex3f(x_end, BOARD_HEIGHT/2, BOARD_EDGE_HEIGHT)
        glVertex3f(x_start, BOARD_HEIGHT/2, BOARD_EDGE_HEIGHT)
        
        # Top face
        glVertex3f(x_start, BOARD_HEIGHT/2, BOARD_EDGE_HEIGHT)
        glVertex3f(x_end, BOARD_HEIGHT/2, BOARD_EDGE_HEIGHT)
        glVertex3f(x_end, BOARD_HEIGHT/2+20, BOARD_EDGE_HEIGHT)
        glVertex3f(x_start, BOARD_HEIGHT/2+20, BOARD_EDGE_HEIGHT)
        glEnd()
    
    # Bottom
    for i in range(segment_count):
        if i % 2 == 0:
            glColor3f(0.2, 0.2, 0.2)
        else:
            glColor3f(1.0, 1.0, 1.0)
        
        x_start = -BOARD_WIDTH/2 + i * segment_length_x
        x_end = -BOARD_WIDTH/2 + (i+1) * segment_length_x
        
        glBegin(GL_QUADS)
        # Front face
        glVertex3f(x_start, -BOARD_HEIGHT/2, 0)
        glVertex3f(x_end, -BOARD_HEIGHT/2, 0)
        glVertex3f(x_end, -BOARD_HEIGHT/2, BOARD_EDGE_HEIGHT)
        glVertex3f(x_start, -BOARD_HEIGHT/2, BOARD_EDGE_HEIGHT)
        
        # Top face
        glVertex3f(x_start, -BOARD_HEIGHT/2, BOARD_EDGE_HEIGHT)
        glVertex3f(x_end, -BOARD_HEIGHT/2, BOARD_EDGE_HEIGHT)
        glVertex3f(x_end, -BOARD_HEIGHT/2-20, BOARD_EDGE_HEIGHT)
        glVertex3f(x_start, -BOARD_HEIGHT/2-20, BOARD_EDGE_HEIGHT)
        glEnd()

def draw_obstacles():
    # Get the current level colors
    colors = LEVEL_COLORS[LEVEL]
    
    for x, z, width, depth, height in obstacles:
        glPushMatrix()
        glColor3f(*colors["obstacles"])
        glTranslatef(x, z, height/2)
        glBegin(GL_QUADS)
        # Front face
        glVertex3f(-width/2, -depth/2, -height/2)
        glVertex3f(width/2, -depth/2, -height/2)
        glVertex3f(width/2, -depth/2, height/2)
        glVertex3f(-width/2, -depth/2, height/2)
        
        # Back face
        glVertex3f(-width/2, depth/2, -height/2)
        glVertex3f(width/2, depth/2, -height/2)
        glVertex3f(width/2, depth/2, height/2)
        glVertex3f(-width/2, depth/2, height/2)
        
        # Left face
        glVertex3f(-width/2, -depth/2, -height/2)
        glVertex3f(-width/2, depth/2, -height/2)
        glVertex3f(-width/2, depth/2, height/2)
        glVertex3f(-width/2, -depth/2, height/2)
        
        # Right face
        glVertex3f(width/2, -depth/2, -height/2)
        glVertex3f(width/2, depth/2, -height/2)
        glVertex3f(width/2, depth/2, height/2)
        glVertex3f(width/2, -depth/2, height/2)
        
        # Top face
        glVertex3f(-width/2, -depth/2, height/2)
        glVertex3f(width/2, -depth/2, height/2)
        glVertex3f(width/2, depth/2, height/2)
        glVertex3f(-width/2, depth/2, height/2)
        
        # Bottom face
        glVertex3f(-width/2, -depth/2, -height/2)
        glVertex3f(width/2, -depth/2, -height/2)
        glVertex3f(width/2, depth/2, -height/2)
        glVertex3f(-width/2, depth/2, -height/2)
        glEnd()
        
        glPopMatrix()

def draw_snake_segment(x, y, z, is_head=False):
    colors = LEVEL_COLORS[LEVEL]
    
    glPushMatrix()
    glTranslatef(x, y, z)
    
    if is_head:
        glColor3f(*colors["head"])  # Use level-specific head color
        glPushMatrix()
        glutSolidCube(CELL_SIZE)
        glColor3f(0, 0, 0)  # Black eyes (as smaller cubes)
        
        # Determine eye position based on direction
        dx, dy, dz = snake_direction
        eye_offset = CELL_SIZE/2
        
        if dx > 0:  # Moving right
            eye_y_offset = CELL_SIZE/4
            glPushMatrix()
            glTranslatef(eye_offset, eye_y_offset, eye_offset)
            glutSolidCube(CELL_SIZE/5)
            glPopMatrix()
            
            glPushMatrix()
            glTranslatef(eye_offset, -eye_y_offset, eye_offset)
            glutSolidCube(CELL_SIZE/5)
            glPopMatrix()
        
        elif dx < 0:  # Moving left
            eye_y_offset = CELL_SIZE/4
            glPushMatrix()
            glTranslatef(-eye_offset, eye_y_offset, eye_offset)
            glutSolidCube(CELL_SIZE/5)
            glPopMatrix()
            
            glPushMatrix()
            glTranslatef(-eye_offset, -eye_y_offset, eye_offset)
            glutSolidCube(CELL_SIZE/5)
            glPopMatrix()
        
        elif dy > 0:  # Moving up
            eye_x_offset = CELL_SIZE/4
            glPushMatrix()
            glTranslatef(eye_x_offset, eye_offset, eye_offset)
            glutSolidCube(CELL_SIZE/5)
            glPopMatrix()
            
            glPushMatrix()
            glTranslatef(-eye_x_offset, eye_offset, eye_offset)
            glutSolidCube(CELL_SIZE/5)
            glPopMatrix()
        
        elif dy < 0:  # Moving down
            eye_x_offset = CELL_SIZE/4
            glPushMatrix()
            glTranslatef(eye_x_offset, -eye_offset, eye_offset)
            glutSolidCube(CELL_SIZE/5)
            glPopMatrix()
            
            glPushMatrix()
            glTranslatef(-eye_x_offset, -eye_offset, eye_offset)
            glutSolidCube(CELL_SIZE/5)
            glPopMatrix()
        
        glPopMatrix()
    else:
        # Draw body segment as cube
        glColor3f(*colors["body"])
        glutSolidCube(CELL_SIZE * 0.8)  # Slightly smaller than head
    
    glPopMatrix()

def draw_snake():
    if not snake:
        return
    
    # Draw head
    draw_snake_segment(snake[0][0], snake[0][1], snake[0][2], True)
    
    # Draw body segments
    for i in range(1, len(snake)):
        draw_snake_segment(snake[i][0], snake[i][1], snake[i][2], False)

def draw_food():
    if food_exists:
        colors = LEVEL_COLORS[LEVEL]
        
        glPushMatrix()
        glTranslatef(food_pos[0], food_pos[1], food_pos[2])
        glColor3f(*colors["food"])
        glutSolidCube(CELL_SIZE * 0.7)  # Slightly smaller than snake segments
        
        glPopMatrix()

def draw_bonus_food():
    if bonus_food_exists:
        glPushMatrix()
        glTranslatef(bonus_food_pos[0], bonus_food_pos[1], bonus_food_pos[2])
        
        # Draw bonus food as a golden cube, larger than normal food
        glColor3f(1.0, 0.84, 0.0)  # Gold color (same for all levels)
        glutSolidCube(CELL_SIZE * 1.2)  # Larger than normal food
        
        # Draw timer ring around bonus food
        time_left = bonus_food_duration - (time.time() - bonus_food_timer)
        if time_left > 0:
            # Calculate the completion percentage of the timer (from 1.0 to 0.0)
            completion = time_left / bonus_food_duration
            
            # Draw a circle representing the timer
            glPushMatrix()
            glTranslatef(0, 0, CELL_SIZE/1.5)  # Position above the bonus food
            glColor3f(1.0, 1.0, 1.0)  # White color for the timer
            
            # Draw the timer as segments of a circle
            glBegin(GL_TRIANGLE_FAN)
            glVertex3f(0, 0, 0)  # Center of the circle
            
            radius = CELL_SIZE * 0.8
            segments = 36  # Number of segments in the circle
            segments_to_draw = int(segments * completion)
            
            for i in range(segments_to_draw + 1):
                angle = 2.0 * math.pi * i / segments
                x = radius * math.cos(angle)
                y = radius * math.sin(angle)
                glVertex3f(x, y, 0)
            
            glEnd()
            glPopMatrix()
        
        glPopMatrix()

def draw_timer_bar():
    if bonus_food_exists:
        time_left = bonus_food_duration - (time.time() - bonus_food_timer)
        if time_left > 0:
            # Draw a timer bar on the screen
            completion = time_left / bonus_food_duration
            
            # Save current matrices
            glMatrixMode(GL_PROJECTION)
            glPushMatrix()
            glLoadIdentity()
            gluOrtho2D(0, 1000, 0, 800)
            
            glMatrixMode(GL_MODELVIEW)
            glPushMatrix()
            glLoadIdentity()
            
            # Draw background of timer bar
            glColor3f(0.3, 0.3, 0.3)
            glBegin(GL_QUADS)
            glVertex2f(700, 770)
            glVertex2f(980, 770)
            glVertex2f(980, 750)
            glVertex2f(700, 750)
            glEnd()
            
            # Draw foreground of timer bar (remaining time)
            bar_width = 280 * completion
            glColor3f(1.0, 0.84, 0.0)  # Same gold color as bonus food
            glBegin(GL_QUADS)
            glVertex2f(700, 770)
            glVertex2f(700 + bar_width, 770)
            glVertex2f(700 + bar_width, 750)
            glVertex2f(700, 750)
            glEnd()
            
            # Draw text
            glColor3f(1.0, 1.0, 1.0)
            glRasterPos2f(700, 730)
            text = f"Bonus Food: {int(time_left)}s"
            for ch in text:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(ch))
            
            # Restore matrices
            glPopMatrix()
            glMatrixMode(GL_PROJECTION)
            glPopMatrix()
            glMatrixMode(GL_MODELVIEW)

def draw_portals():
    for x, y, z, color_index in portals:
        glPushMatrix()
        glTranslatef(x, y, z)
        glColor3f(0.0, 0.0, 0.0)
        glutSolidSphere(portal_size, 16, 16)      # Parameters: radius, slices, stack
        glPopMatrix()

def draw_score_and_level():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glColor3f(1.0, 1.0, 1.0)  # White text
    glRasterPos2f(20, 750)
    score_text = f"SCORE: {SCORE}"
    for ch in score_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
 
    level_text = f"LEVEL: {LEVEL}"
    text_width = 0
    for ch in level_text:
        text_width += glutBitmapWidth(GLUT_BITMAP_HELVETICA_18, ord(ch))
    
    glRasterPos2f(980 - text_width, 750)
    for ch in level_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def initialize_snake():
    global snake
    snake = [(0, 0, CELL_SIZE/2)]  # Start with head only
    # Add initial body segments
    for i in range(1, 3):
        snake.append((-i * CELL_SIZE, 0, CELL_SIZE/2))

def generate_food():
    global food_pos, food_exists
    
    # Number of attempts to find a valid position
    max_attempts = 50
    attempts = 0
    
    while attempts < max_attempts:
        # Generate random coordinates
        x = random.randint(-GRID_LENGTH + CELL_SIZE, GRID_LENGTH - CELL_SIZE)
        y = random.randint(-GRID_LENGTH + CELL_SIZE, GRID_LENGTH - CELL_SIZE)
        
        # Round to nearest cell
        x = round(x / CELL_SIZE) * CELL_SIZE
        y = round(y / CELL_SIZE) * CELL_SIZE
        
        # Check if food is not inside an obstacle with improved buffer distance
        valid_position = True
        for ox, oz, width, depth, height in obstacles:
            # Add buffer zone around obstacles (half a cell size)
            if (ox - width/2 - CELL_SIZE/2 <= x <= ox + width/2 + CELL_SIZE/2) and \
               (oz - depth/2 - CELL_SIZE/2 <= y <= oz + depth/2 + CELL_SIZE/2):
                valid_position = False
                break
        
        # Check if food is not on snake
        if valid_position:
            valid_on_snake = True
            for segment in snake:
                if abs(segment[0] - x) < CELL_SIZE and abs(segment[1] - y) < CELL_SIZE:
                    valid_on_snake = False
                    break
            
            if valid_on_snake:
                food_pos = (x, y, CELL_SIZE/2)
                food_exists = True
                return
        
        attempts += 1
    
    # If we couldn't find a valid position after max attempts,
    # try far from obstacles
    food_pos = (GRID_LENGTH/2, GRID_LENGTH/2, CELL_SIZE/2)
    food_exists = True

def generate_bonus_food():
    global bonus_food_pos, bonus_food_exists, bonus_food_timer
    
    # Number of attempts to find a valid position
    max_attempts = 50
    attempts = 0
    
    while attempts < max_attempts:
        # Generate random coordinates
        x = random.randint(-GRID_LENGTH + CELL_SIZE, GRID_LENGTH - CELL_SIZE)
        y = random.randint(-GRID_LENGTH + CELL_SIZE, GRID_LENGTH - CELL_SIZE)
        
        # Round to nearest cell
        x = round(x / CELL_SIZE) * CELL_SIZE
        y = round(y / CELL_SIZE) * CELL_SIZE
        
        # Check if bonus food is not inside an obstacle with improved buffer distance
        valid_position = True
        for ox, oz, width, depth, height in obstacles:
            # Add buffer zone around obstacles (half a cell size)
            if (ox - width/2 - CELL_SIZE/2 <= x <= ox + width/2 + CELL_SIZE/2) and \
               (oz - depth/2 - CELL_SIZE/2 <= y <= oz + depth/2 + CELL_SIZE/2):
                valid_position = False
                break
        
        # Check if bonus food is not on snake or regular food
        if valid_position:
            valid_on_snake = True
            for segment in snake:
                if abs(segment[0] - x) < CELL_SIZE and abs(segment[1] - y) < CELL_SIZE:
                    valid_on_snake = False
                    break
                    
            # Check if it's not on regular food
            if food_exists and abs(food_pos[0] - x) < CELL_SIZE and abs(food_pos[1] - y) < CELL_SIZE:
                valid_on_snake = False
            
            if valid_on_snake:
                bonus_food_pos = (x, y, CELL_SIZE/2)
                bonus_food_exists = True
                bonus_food_timer = time.time()  # Start the timer
                return
        
        attempts += 1
    bonus_food_exists = False

def move_snake():
    global snake, snake_length, SCORE, food_exists, bonus_food_exists, food_eaten_count, GAME_OVER
    
    # Get current head position
    head_x, head_y, head_z = snake[0]
    
    # Calculate new head position
    dx, dy, dz = snake_direction
    new_head = (head_x + dx, head_y + dy, head_z)
    
    # Check for portal collision
    portal_teleport = check_portal_collision(new_head)
    if portal_teleport:
        new_head = portal_teleport
    
    # Check for self-collision
    if check_self_collision(new_head):
        GAME_OVER = True
        return
    
    # Check for obstacle collision with penetration allowance
    for ox, oz, width, depth, height in obstacles:
        # Calculate the penetration distance (allow 1/3 of cell size)
        penetration_allowed = CELL_SIZE / 3
        
        # Calculate distances from head center to obstacle edges
        dist_x = abs(new_head[0] - ox) - (width/2 + CELL_SIZE/2)
        dist_y = abs(new_head[1] - oz) - (depth/2 + CELL_SIZE/2)
        
        # If distances are negative, there's overlap
        if dist_x < -penetration_allowed and dist_y < -penetration_allowed and new_head[2] <= height:
            GAME_OVER = True
            return
    
    # Check if snake goes outside the board
    new_x, new_y, new_z = new_head
    if new_x < -GRID_LENGTH or new_x > GRID_LENGTH or new_y < -GRID_LENGTH or new_y > GRID_LENGTH:
        # Wrap around to the opposite side
        if new_x < -GRID_LENGTH:
            new_x = GRID_LENGTH - CELL_SIZE
        elif new_x > GRID_LENGTH:
            new_x = -GRID_LENGTH + CELL_SIZE
        
        if new_y < -GRID_LENGTH:
            new_y = GRID_LENGTH - CELL_SIZE
        elif new_y > GRID_LENGTH:
            new_y = -GRID_LENGTH + CELL_SIZE
        
        new_head = (new_x, new_y, new_z)
    
    # Add the new head
    snake.insert(0, new_head)
    
    # Check if snake ate food
    head_x, head_y, head_z = new_head
    food_x, food_y, food_z = food_pos
    distance = ((head_x - food_x)**2 + (head_y - food_y)**2 + (head_z - food_z)**2)**0.5
    
    if food_exists and distance < CELL_SIZE:
        snake_length += 1
        SCORE += 10
        food_exists = False
        food_eaten_count += 1
        
        # Check if we need to level up
        check_level_up()
        
        # After every 5 normal foods, generate a bonus food
        if food_eaten_count % 5 == 0 and not bonus_food_exists:
            generate_bonus_food()
        
        generate_food()
    
    # Check if snake ate bonus food
    if bonus_food_exists:
        bonus_x, bonus_y, bonus_z = bonus_food_pos
        bonus_distance = ((head_x - bonus_x)**2 + (head_y - bonus_y)**2 + (head_z - bonus_z)**2)**0.5
        
        if bonus_distance < CELL_SIZE:
            snake_length += 2  # Bonus food gives more length
            SCORE += 20
            bonus_food_exists = False
            
            # Check if we need to level up
            check_level_up()
    
    # Remove tail if snake exceeds target length
    while len(snake) > snake_length:
        snake.pop()

def check_self_collision(head_pos):
    """Check if the snake's head collides with any part of its body."""
    # Skip the head (index 0) and check if the new head position collides with any body segment
    # We start from index 1 because checking against the current head is not needed
    for i in range(1, len(snake)):
        segment = snake[i]
        # Check if the positions are the same (direct collision)
        if head_pos == segment:
            return True
    
    return False


def draw_level_transition():
    global level_transition_active
    
    # Calculate how long the transition has been active
    elapsed_time = time.time() - level_transition_start_time
    transition_duration = 5.0  # 3 seconds freeze
    
    # End transition if time is up
    if elapsed_time > transition_duration:
        level_transition_active = False
        return
    
    # Save current matrices
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    
    # Dark semi-transparent overlay
    glColor4f(0.0, 0.0, 0.0, 0.8)  # Black with 80% opacity
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(1000, 0)
    glVertex2f(1000, 800)
    glVertex2f(0, 800)
    glEnd()
    
    # Level transition messages
    glColor3f(1.0, 1.0, 1.0)  # White text
    
    # Calculate text width for centering
    large_font = GLUT_BITMAP_TIMES_ROMAN_24
    title_text = "LEVEL UP!"
    title_width = 0
    for ch in title_text:
        title_width += glutBitmapWidth(large_font, ord(ch))
    
    # Draw title
    glRasterPos2f((1000 - title_width) / 2, 450)
    for ch in title_text:
        glutBitmapCharacter(large_font, ord(ch))
    
    # Draw level message
    level_text = f"Welcome to Level {LEVEL}"
    level_width = 0
    for ch in level_text:
        level_width += glutBitmapWidth(large_font, ord(ch))
    
    glRasterPos2f((1000 - level_width) / 2, 400)
    for ch in level_text:
        glutBitmapCharacter(large_font, ord(ch))
    
    # Draw level descriptions
    descriptions = [
        "Beginning your journey...",
        "The challenge increases!",
        "Master level - navigate the maze!"
    ]
    
    desc_text = descriptions[LEVEL - 1]
    desc_width = 0
    small_font = GLUT_BITMAP_HELVETICA_18
    for ch in desc_text:
        desc_width += glutBitmapWidth(small_font, ord(ch))
    
    glRasterPos2f((1000 - desc_width) / 2, 350)
    for ch in desc_text:
        glutBitmapCharacter(small_font, ord(ch))
    
    # Display countdown
    time_left = int(transition_duration - elapsed_time) + 1
    countdown_text = f"Game continues in {time_left}..."
    countdown_width = 0
    for ch in countdown_text:
        countdown_width += glutBitmapWidth(small_font, ord(ch))
    
    glRasterPos2f((1000 - countdown_width) / 2, 300)
    for ch in countdown_text:
        glutBitmapCharacter(small_font, ord(ch))
    
    # Disable blend after drawing
    glDisable(GL_BLEND)
    
    # Restore matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def check_level_up():
    global LEVEL, SCORE, obstacles, level_transition_active, level_transition_start_time
    
    # Level up logic
    new_level = min(3, (SCORE // 100) + 1)
    
    if new_level > LEVEL:
        LEVEL = new_level
        obstacles = LEVEL_OBSTACLES[LEVEL]
        
        # Activate level transition screen
        level_transition_active = True
        level_transition_start_time = time.time()
    
        print(f"Level up! Now at level {LEVEL}")

def initialize_portals():
    global portals   
    portals = []
    max_attempts = 100
    
    for i in range(NUM_PORTALS):
        attempts = 0
        while attempts < max_attempts:
            # Generate random coordinates
            x = random.randint(-GRID_LENGTH + CELL_SIZE*2, GRID_LENGTH - CELL_SIZE*2)
            y = random.randint(-GRID_LENGTH + CELL_SIZE*2, GRID_LENGTH - CELL_SIZE*2)
            
            # Round to nearest cell
            x = round(x / CELL_SIZE) * CELL_SIZE
            y = round(y / CELL_SIZE) * CELL_SIZE
            
            # Check if portal is not inside an obstacle with buffer
            valid_position = True
            for ox, oz, width, depth, height in obstacles:
                if (ox - width/2 - CELL_SIZE*2 <= x <= ox + width/2 + CELL_SIZE*2) and \
                   (oz - depth/2 - CELL_SIZE*2 <= y <= oz + depth/2 + CELL_SIZE*2):
                    valid_position = False
                    break
            
            # Check if portal is not on snake
            if valid_position:
                for segment in snake:
                    if abs(segment[0] - x) < CELL_SIZE*2 and abs(segment[1] - y) < CELL_SIZE*2:
                        valid_position = False
                        break
            
            # Check if portal is not on food
            if valid_position and food_exists:
                if abs(food_pos[0] - x) < CELL_SIZE*2 and abs(food_pos[1] - y) < CELL_SIZE*2:
                    valid_position = False
            
            # Check if portal is not on bonus food
            if valid_position and bonus_food_exists:
                if abs(bonus_food_pos[0] - x) < CELL_SIZE*2 and abs(bonus_food_pos[1] - y) < CELL_SIZE*2:
                    valid_position = False
            
            # Check if portal is not on another portal
            if valid_position:
                for px, py, pz, _ in portals:
                    if abs(px - x) < CELL_SIZE*3 and abs(py - y) < CELL_SIZE*3:
                        valid_position = False
                        break
            
            if valid_position:
                # All portals are now black (color index 0)
                portals.append((x, y, CELL_SIZE/2, 0))
                break
            
            attempts += 1
        
        # If we couldn't find a valid position, place it at a predefined location
        if attempts >= max_attempts:
            # Place in one of the corners
            corners = [
                (-GRID_LENGTH + CELL_SIZE*3, -GRID_LENGTH + CELL_SIZE*3, CELL_SIZE/2),
                (-GRID_LENGTH + CELL_SIZE*3, GRID_LENGTH - CELL_SIZE*3, CELL_SIZE/2),
                (GRID_LENGTH - CELL_SIZE*3, -GRID_LENGTH + CELL_SIZE*3, CELL_SIZE/2)
            ]
            corner = corners[i % len(corners)]
            portals.append((corner[0], corner[1], corner[2], 0))  # All portals are black (index 0)


def check_portal_collision(head_pos):
    """Check if the snake's head collides with a portal and handle teleportation."""
    global last_teleport_time
    
    # Skip if teleport is on cooldown
    current_time = time.time()
    if current_time - last_teleport_time < PORTAL_COOLDOWN_TIME:
        return None
    
    head_x, head_y, head_z = head_pos
    
    for i, (x, y, z, _) in enumerate(portals):
        # Calculate distance from head to portal
        distance = math.sqrt((head_x - x)**2 + (head_y - y)**2)
        
        if distance < portal_size:
            # Find a different portal to teleport to
            available_destinations = [j for j in range(len(portals)) if j != i]
            if not available_destinations:
                return None  # No other portals to teleport to
            
            # Select a random destination portal
            dest_index = random.choice(available_destinations)
            dest_x, dest_y, dest_z, _ = portals[dest_index]
            
            # Update last teleport time
            last_teleport_time = current_time
            
            # Generate a small random offset to prevent landing exactly on the destination portal
            offset_x = random.randint(-1, 1) * CELL_SIZE
            offset_y = random.randint(-1, 1) * CELL_SIZE
            
            # Return the new head position after teleportation
            return (dest_x + offset_x, dest_y + offset_y, head_z)
    
    return None

def draw_shapes():
    draw_board()
    draw_obstacles()
    draw_portals()

    if not GAME_OVER:
        draw_snake()
        draw_food()
        if bonus_food_exists:
            draw_bonus_food()

def initialize_game():
    global GAME_OVER, PAUSE, SCORE, snake_length, LEVEL, obstacles, food_eaten_count, snake_direction
    global bonus_food_exists, food_exists, last_update_time
    
    # Reset game state
    GAME_OVER = False
    PAUSE = False
    SCORE = 0
    snake_length = 3
    LEVEL = 1  # Reset to level 1
    obstacles = LEVEL_OBSTACLES[LEVEL]  # Reset obstacles for level 1
    food_eaten_count = 0
    snake_direction = (CELL_SIZE, 0, 0)  # Initial direction (right)
    bonus_food_exists = False
    food_exists = False
    last_update_time = time.time()
    
    initialize_snake()
    initialize_portals()
    generate_food()

def update_game():
    global last_update_time, food_exists, bonus_food_exists, bonus_food_timer, level_transition_active, SCORE, last_reached_milestone
    
    current_time = time.time() * 1000  # Convert to milliseconds
    
    # Check if bonus food timer has expired
    if bonus_food_exists and time.time() - bonus_food_timer > bonus_food_duration:
        bonus_food_exists = False
    
    # Don't update game during level transition
    if level_transition_active:
        return    
    
    # Move snake at regular intervals if not paused or game over
    if not PAUSE and not GAME_OVER:
        # Adjust snake speed based on level
        speed_delay = 150 - ((LEVEL - 1) * 30)  # Level 1: 150ms, Level 2: 120ms, Level 3: 90ms
        
        if current_time - last_update_time > speed_delay:
            move_snake()
            last_update_time = current_time
            
            # Generate food if none exists
            if not food_exists:
                generate_food()
def idle():
    update_game()
    glutPostRedisplay()

def keyboardListener(key, x, y):
    global snake_direction, GAME_OVER, snake, snake_length, SCORE, PAUSE, food_eaten_count, LEVEL, obstacles, bonus_food_exists, food_exists, last_update_time
    
    if isinstance(key, bytes):
        key = key.decode('utf-8')
    
    if key.lower() == 'b' and snake_direction != (0, -CELL_SIZE, 0):  # Up, can't go opposite direction
        snake_direction = (0, CELL_SIZE, 0)
    elif key.lower() == 'y' and snake_direction != (0, CELL_SIZE, 0):  # Down
        snake_direction = (0, -CELL_SIZE, 0)
    elif key.lower() == 'h' and snake_direction != (CELL_SIZE, 0, 0):  # Left
        snake_direction = (-CELL_SIZE, 0, 0)
    elif key.lower() == 'g' and snake_direction != (-CELL_SIZE, 0, 0):  # Right
        snake_direction = (CELL_SIZE, 0, 0)
    elif key.lower() == 'p':  # Pause/resume game
        PAUSE = not PAUSE
    elif key.lower() == 'r' and GAME_OVER:  # Restart game
        initialize_game()


def specialKeyListener(key, x, y):
    global camera_pos
    
    # Camera movement controls
    x, y, z = camera_pos
    
    # moving camera left (LEFT arrow key)
    if key == GLUT_KEY_LEFT:
        x -= 10
    
    # moving camera right (RIGHT arrow key)
    if key == GLUT_KEY_RIGHT:
        x += 10
    
    # Add up/down camera movement
    if key == GLUT_KEY_UP:
        z -= 10
    
    if key == GLUT_KEY_DOWN:
        z += 10
    
    camera_pos = (x, y, z)

def mouseListener(button, state, x, y):
    pass

def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    # Third-person view only
    x, y, z = camera_pos
    gluLookAt(x, y, z,
              0, 0, 0,
              0, 0, 1)

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    setupCamera()
    draw_shapes()

    if GAME_OVER:
        draw_text(400, 400, "GAME OVER - Press R to restart")
        # Also display final score
        draw_text(400, 350, f"Final Score: {SCORE}")
        draw_text(400, 320, f"Final Level: {LEVEL}")
    
    # Display controls at the bottom of the screen
    draw_text(10, 650, f"Level: {LEVEL}")
    draw_text(10, 620, f"Game Score: {SCORE}")
    
    # Draw bonus food timer if bonus food exists
    draw_timer_bar()
    draw_score_and_level()
    
    # Draw level transition screen if active
    if level_transition_active:
        draw_level_transition()
    
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow(b"3D Snake Game")

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)

    initialize_snake()
    initialize_portals()  
    generate_food()
    
    glutMainLoop()

if __name__ == "__main__":
    main()