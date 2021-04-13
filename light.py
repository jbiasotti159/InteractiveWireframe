"""Example using OpenGL lighting features.

Author: Christian Duncan
Course: CSC345: Computer Graphics
Term: Spring 2021

This code demonstrates how to use the lighting features of OpenGL
to render a lit scene.  Technically, these lighting features are
now deprecated in OpenGL in favor of fasterfvertex/pixel shaders 
but implementing shaders either requires cutting/pasting sample code 
or understanding all of the lighting techniques first anyway as well
as the shader language.

This demo code builds off of previous demos so the scene is similar
but it includes a floor which is illuminated by the light.
There are various types of floors that can be switched around to
see the resulting effect.
"""

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
from utils import *
from camera import *
import math
from PIL import Image

# These parameters describe window properties
win_width = 800
win_height = 800
win_name = b'Lights, cameras, action!'

# These parameters define the camera's lens shape and position
CAM_NEAR = 0.01
CAM_FAR = 1000.0
CAM_ANGLE = 60.0
INITIAL_EYE = Point(0, 2, 30)
INITIAL_LOOK_ANGLE = 0
camera = Camera(CAM_ANGLE, win_width/win_height, CAM_NEAR, CAM_FAR, INITIAL_EYE, INITIAL_LOOK_ANGLE)

# These parameters define simple animation properties
FPS = 60.0
DELAY = int(1000.0 / FPS + 0.5)
DEFAULT_STEP = 0.001
BULLET_SPEED = 0.1
angle_step = 0.1
angle_movement = 45
light_height = 10
light_height_dy = 0.05
LIGHT_TOP = 30
LIGHT_BOTTOM = -5
bullet_distance = 0
time = 0
brightness = 1.0

# Checkerboard dimensions (texture dimensions are powers of 2)
NROWS = 64
NCOLS = 64

# Plane dimensions (not airplane - just a flat sheet)
PLANE_WIDTH = 30
PLANE_HEIGHT = 30

# These parameters are flags that can be turned on and off (for effect)
animate = False
fire = False
is_light_on = True
exiting = False
use_smooth = True
lamp_light = True
red_light = True
blue_light = True
green_light = True
use_lv = GL_FALSE
floor_option = 2

def main():
    """Start the main program running."""
    # Create the initial window.
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(win_width, win_height)
    glutInitWindowPosition(100,100)
    glutCreateWindow(win_name)

    init()

    
    # Setup the callback returns for display and keyboard events.
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_keys)
    glutReshapeFunc(reshape)
    glutTimerFunc(DELAY, timer, 0)
    # Enter the main loop, displaying window and waiting for events.
    glutMainLoop()
    return

def init():
    """Perform basic OpenGL initialization."""
    global tube, ball, faceTextureName, woodTextureName
    tube = gluNewQuadric()
    gluQuadricDrawStyle(tube, GLU_FILL)
    ball = gluNewQuadric()
    gluQuadricDrawStyle(ball, GLU_FILL)

    # Set up lighting and depth-test
    glEnable(GL_LIGHTING)
    glEnable(GL_NORMALIZE)    # Inefficient...
    glEnable(GL_DEPTH_TEST)   # For z-buffering!

    generateCheckerBoardTexture()
    faceTextureName = loadImageTexture("brick.jpg")
    woodTextureName = loadImageTexture("wood.jpg")

def display():
    """Display the current scene."""
    # Set the viewport to the full screen.
    glViewport(0, 0, win_width, win_height)

    camera.setProjection()
    
    # Clear the Screen.
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Set the shading model we want to use.
    glShadeModel(GL_SMOOTH if use_smooth else GL_FLAT)

    # Draw and show the "Scene".
    draw_scene()
    glFlush()
    glutSwapBuffers()

def timer(alarm):
    """Set a new alarm after DELAY microsecs and animate if needed."""
    # Start alarm clock again.
    glutTimerFunc(DELAY, timer, 0)
    if exiting:
        global brightness
        brightness -= 0.05
        if brightness < 0.01:
            # Enough dimming - terminate!
            glutLeaveMainLoop()
        glutPostRedisplay()
        
    if animate:
        # Advance to the next frame.
        advance()
        glutPostRedisplay()

def advance():
    """Advance the scene one frame."""
    global angle_movement, bullet_distance, fire, time
    time += 1
    angle_movement += angle_step
    if angle_movement >= 360:
        angle_movement -= 360   # So angle doesn't get too large.
    elif angle_movement < 0:
        angle_movement += 360   # So angle doesn't get too small.

    # Move the bullet - if fired.
    if fire:
        bullet_distance += BULLET_SPEED
        if bullet_distance > CAM_FAR:
            bullet_distance = 0
            fire = False
        
def special_keys(key, x, y):
    """Process any special keys that are pressed."""
    global angle_step
    if key == GLUT_KEY_LEFT:
        angle_step += DEFAULT_STEP
    elif key == GLUT_KEY_RIGHT:
        angle_step -= DEFAULT_STEP

def keyboard(key, x, y):
    """Process any regular keys that are pressed."""
    global brightness, floor_option
    if ord(key) == 27:  # ASCII code 27 = ESC-key
        global exiting
        exiting = True
    elif key == b' ':
        global animate
        animate = not animate
    elif key == b'a':
        # Go left
        camera.turn(1)
        glutPostRedisplay()
    elif key == b'd':
        # Go right
        camera.turn(-1)
        glutPostRedisplay()
    elif key == b'w':
        # Go forward
        camera.slide(0, 0, -1)
        glutPostRedisplay()
    elif key == b's':
        # Go backward
        camera.slide(0, 0, 1)
        glutPostRedisplay()
    elif key == b'q':
        # Go up
        camera.slide(0, 1, 0)
        #camera.turn(1)
        glutPostRedisplay()
    elif key == b'e':
        # Go down
        camera.slide(0, -1, 0)
        glutPostRedisplay()
    elif key == b'f':
        global fire
        fire = True
    elif key == b'l':
        global is_light_on
        is_light_on = not is_light_on
        glutPostRedisplay()
    elif key == b'h':
        print("Help Message add more later")
    elif key == b'1':
        global blue_light
        blue_light = not blue_light
        glutPostRedisplay()
    elif key == b'2':
        global red_light
        red_light = not red_light
        glutPostRedisplay()
    elif key == b'3':
        global green_light
        green_light = not green_light
        glutPostRedisplay()
    elif key == b'4':
        global lamp_light
        lamp_light = not lamp_light
        glutPostRedisplay()
    elif key == b'-':
        # Move light down
        global light_height
        light_height -= light_height_dy
        glutPostRedisplay()
    elif key == b'+':
        # Move light up
        light_height += light_height_dy
        glutPostRedisplay()

def drawPlane(width, height, texture):
    """ Draw a textured plane of the specified dimension. """
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)  # try GL_DECAL/GL_REPLACE/GL_MODULATE
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)  # try GL_NICEST/GL_FASTEST
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)  # try GL_CLAMP/GL_REPEAT/GL_CLAMP_TO_EDGE
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)  # try GL_LINEAR/GL_NEAREST
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    # Enable/Disable each time or OpenGL ALWAYS expects texturing!
    glEnable(GL_TEXTURE_2D)

    ex = width / 2
    sx = -ex
    ey = height
    sy = 0
    glBegin(GL_QUADS)
    glNormal3f(0, 0, 1)
    glTexCoord2f(0, 0)
    glVertex3f(sx, sy, 0)
    glTexCoord2f(2, 0)
    glVertex3f(ex, sy, 0)
    glTexCoord2f(2, 2)
    glVertex3f(ex, ey, 0)
    glTexCoord2f(0, 2)
    glVertex3f(sx, ey, 0)
    glEnd()

    glDisable(GL_TEXTURE_2D)

def reshape(w, h):
    """Handle window reshaping events."""
    global win_width, win_height
    win_width = w
    win_height = h
    glutPostRedisplay()  # May need to call a redraw...

def draw_scene():
    """Draws a simple scene with a few shapes."""
    # Place the camera
    camera.placeCamera()
    
    
    # Set up the global ambient light.  (Try commenting out.)
    amb = [ 0*brightness, 0*brightness, 0*brightness, 1.0 ]
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, amb)

    # Set up the main light (LIGHT0)... or not.
    if is_light_on:
        place_blue_light()
        place_red_light()
        place_green_light()
        place_lamp_light()
    else:
        glDisable(GL_LIGHT0)
        glDisable(GL_LIGHT1)
        glDisable(GL_LIGHT2)
        glDisable(GL_LIGHT3)

    if lamp_light:
        place_lamp_light()
    else:
        glDisable(GL_LIGHT3)

    # Now spin the world around the y-axis (for effect).
    glRotated(angle_movement, 0, 1, 0)
    draw_objects()


def draw_objects():
    """Draw the objects in the scene: cylinders, spheres, and floor."""
    # if floor_option == 1:
    #     # Draw a floor with bad lighting effects.
    #     draw_floor(30, 2)
    # elif floor_option == 2:
    #     # Draw a floor with improved lighting effects.
    #     draw_floor(30, 30)
    # elif floor_option == 3:
    #     # Draw a wavy floor with decent lighting.
    #     draw_floor(30, 30, wave)
    # else:
    #     # Draw a nice wavy floor with proper surface normals.
    #     draw_floor(30, 30, wave, set_normal_wave)
    #
    # glPushMatrix()
    # glTranslated(0, 6, 0)
    # set_copper(GL_FRONT)   # Make material attributes mimic copper.
    # gluCylinder(tube, 3, 3, 10, 10, 10)
    # gluCylinder(tube, 3, 1, 10, 10, 10)
    # glPushMatrix()
    # glTranslated(0, 0, bullet_distance)
    # glScaled(1, 1, 2)
    # gluSphere(ball, 0.9, 10, 10)

    glPushMatrix()

    glPushMatrix()
    drawFloor(PLANE_WIDTH, PLANE_HEIGHT, checkerBoardName)
    glPopMatrix()

    glPushMatrix()
    glRotated(90, 0, 1, 0)
    glTranslated(0, 0, 15)
    drawPlane(PLANE_WIDTH, PLANE_HEIGHT, faceTextureName)
    glPopMatrix()

    glPushMatrix()
    glRotated(90, 0, 1, 0)
    glTranslated(0, 0, -15)
    drawPlane(PLANE_WIDTH, PLANE_HEIGHT, faceTextureName)
    glPopMatrix()

    glPushMatrix()
    glRotated(180, 0, 1, 0)
    glTranslated(0, 0, 15)
    drawPlane(PLANE_WIDTH, PLANE_HEIGHT, faceTextureName)
    glPopMatrix()

    # fourth wall but blocks view so commented out for now
    glPushMatrix()
    glRotated(180, 0, 1, 0)
    glTranslated(0, 0, -15)
    drawPlane(PLANE_WIDTH, PLANE_HEIGHT, faceTextureName)
    glPopMatrix()

    glPushMatrix()
    glTranslated(0, 1, -2.5)
    glRotated(90,1,0,0)
    drawPlane(10, 5, woodTextureName)
    glPopMatrix()

    glPushMatrix()
    glTranslated(0,.4,0)
    glScale(5,1,2.5)
    glutSolidCube(1.0)
    glPopMatrix()

    
    glPushMatrix()
    glTranslated(0,1,0)
    glutSolidCube(1.0)
    glPopMatrix()

    glPushMatrix()
    glTranslated(-1,1,0)
    glutSolidCube(1.0)
    glPopMatrix()

    glPushMatrix()
    glTranslated(0,2,0)
    glScale(0.1,1,0.1)
    glutSolidCube(1.0)
    glPopMatrix()

    glPushMatrix()
    glTranslated(-.45,2.5,0)
    glRotated(90,0,0,1)
    glScale(0.1,1,0.1)
    glutSolidCube(1.0)
    glPopMatrix()

    glPushMatrix()
    glTranslated(1,1.1,1)
    glScale(.1,.1,.1)
    glutSolidCube(1.0)
    glPopMatrix()

    glPushMatrix()
    glTranslated(1.1,1.1,1.2)
    glScale(.1,.1,.1)
    glutSolidCube(1.0)
    glPopMatrix()


    glPopMatrix()

def wave(x, z):
    """Returns a point on a 2-d "wave" trigonemtric function."""
    return math.sin(x+time*0.01)*0.25 + math.sin(z+time*0.001)*0.25

def set_normal_wave(x, z):
    """Sets the normal of a point on the aforementioned wave.

    The calculation is done using the derivatives of the wave function
    and would need to be rewritten if wave function changes.

    Keyword arguments:
    x -- The x position on the "wave"
    z -- The y position on the "wave"
    """
    glNormal3f(-0.25*math.cos(x+time*0.01), 1, 
               -0.25*math.cos(z+time*0.001))

# def draw_floor(size, divisions=1, f=None, df=None):
#     """Draws a floor of a given size and type.
#
#     Keyword arguments:
#     size -- Size of the floor (size x size grid, centered at origin)
#     divisions -- Number of divisions (default 1)
#     f -- Function to apply for the "y-height" (default None => y=0)
#     df -- Procedure to set the normal based on function f (default None)
#
#     A larger number of divisions great improves quality of the floor.
#     If df is None then the normal is set to point directly up.
#     """
#     # Be sure we are talking about correct matrix.
#     glMatrixMode(GL_MODELVIEW)
#     glPushMatrix()
#
#     # Make the floor mimic Pewter material.
#     set_pewter(GL_FRONT_AND_BACK)
#
#     step = size / divisions
#     if f is None:
#         glNormal3f(0, 1, 0)        # Use a vertical normal.
#         glBegin(GL_QUADS)
#         for i in range(0, divisions):
#             x = -size/2 + i*step
#             for j in range(0, divisions):
#                 z = -size/2 + j*step
#                 glVertex3f(x,0,z+step)
#                 glVertex3f(x+step,0,z+step)
#                 glVertex3f(x+step,0,z)
#                 glVertex3f(x,0,z)
#         glEnd()
#     elif df is None:
#         glNormal3f(0, 1, 0)        # Use a vertical normal.
#         glBegin(GL_QUADS)
#         for i in range(0, divisions):
#             x = -size/2 + i*step
#             for j in range(0, divisions):
#                 z = -size/2 + j*step
#                 glVertex3f(x,f(x,z+step),z+step)
#                 glVertex3f(x+step,f(x+step,z+step),z+step)
#                 glVertex3f(x+step,f(x+step,z),z)
#                 glVertex3f(x,f(x,z),z)
#         glEnd()
#     else:
#         for i in range(0, divisions):
#             glBegin(GL_QUAD_STRIP)  # QUAD_STRIPS are more efficient.
#             x = -size/2 + i*step
#             for j in range(0, divisions):
#                 z = -size/2 + j*step
#                 df(x+step, z)
#                 glVertex3f(x+step,f(x+step,z),z)
#                 df(x, z)
#                 glVertex3f(x,f(x,z),z)
#             df(x+step, size/2)
#             glVertex3f(x+step,f(x+step,size/2),size/2)
#             df(x, size/2)
#             glVertex3f(x,f(x,size/2),size/2)
#             glEnd()
#     glPopMatrix()

def drawFloor(width, height, texture):
    """ Draw a textured floor of the specified dimension. """
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)  # try GL_DECAL/GL_REPLACE/GL_MODULATE
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)  # try GL_NICEST/GL_FASTEST
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)  # try GL_CLAMP/GL_REPEAT/GL_CLAMP_TO_EDGE
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)  # try GL_LINEAR/GL_NEAREST
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    sx = width / 2
    ex = -sx
    sz = height / 2
    ez = -sz

    # Enable/Disable each time or OpenGL ALWAYS expects texturing!
    glEnable(GL_TEXTURE_2D)

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(sx, 0, sz)
    glTexCoord2f(0, 1)
    glVertex3f(sx, 0, ez)
    glTexCoord2f(1, 1)
    glVertex3f(ex, 0, ez)
    glTexCoord2f(1, 0)
    glVertex3f(ex, 0, sz)
    glEnd()

    glDisable(GL_TEXTURE_2D)

def place_blue_light():
    """Set up the main light."""
    glMatrixMode(GL_MODELVIEW)
    lx = 3.0
    ly = light_height
    lz = 1.0
    light_position = [ lx, ly, lz, 1.0 ]
    # light_ambient = [ 1*brightness, 1*brightness, 1*brightness, 1.0 ]
    # light_diffuse = [ 1*brightness, 1*brightness, 1*brightness, 1.0 ]
    # light_specular = [ 1*brightness, 1*brightness, 1*brightness, 1.0 ]
    lightb_ambient = [0.0, 0, 1, 1] #blue
    lightr_ambient = [1.0, 0, 0, 1] #red
    lightg_ambient = [0, 1.0, 0, 1] #green
    lightb_diffuse = [0.4, 0.4, 0.6, 1] #blue
    lightb_specular = [0.0, 0, 0.8, 1] #blue
    light_direction = [ 1.0, -1.0, 1.0, 0.0 ]  # Light points down


    # For Light 0 (blue), set position, ambient, diffuse, and specular values
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_AMBIENT, lightb_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightb_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightb_specular)



    # Constant attenuation (for distance, etc.)
    # Only works for fixed light locations!  Otherwise disabled
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1.0)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.0)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.0)

    # Create a spotlight effect (none at the moment)
    if blue_light:
        glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 45.0)
        glLightf(GL_LIGHT0, GL_SPOT_EXPONENT, 0.0)
        glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, light_direction)
    else:
        glLightf(GL_LIGHT0, GL_SPOT_CUTOFF,180.0)
        glLightf(GL_LIGHT0, GL_SPOT_EXPONENT, 0.0)
    
    glLightModeli(GL_LIGHT_MODEL_LOCAL_VIEWER, use_lv)
    glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)
    #  Try GL_TRUE - but then watch what happens when light is low
    
    glEnable(GL_LIGHT0)


    # This part draws a SELF-COLORED sphere (in spot where light is!)
    glPushMatrix()
    glTranslatef(lx,ly,lz)
    glDisable(GL_LIGHTING)
    glColor3f(0, 0, brightness)
    glutSolidSphere(0.5, 20, 20)
    glEnable(GL_LIGHTING)
    glPopMatrix()

def place_red_light():
    """Set up the main light."""
    glMatrixMode(GL_MODELVIEW)
    lx = 4.0
    ly = light_height
    lz = 2.0
    light_position = [lx, ly, lz, 1.0]
    # light_ambient = [ 1*brightness, 1*brightness, 1*brightness, 1.0 ]
    # light_diffuse = [ 1*brightness, 1*brightness, 1*brightness, 1.0 ]
    # light_specular = [ 1*brightness, 1*brightness, 1*brightness, 1.0 ]
    lightb_ambient = [0.0, 0, 1, 1]  # blue
    lightr_ambient = [1.0, 0, 0, 1]  # red
    lightg_ambient = [0, 1.0, 0, 1]  # green
    lightb_diffuse = [0.4, 0.4, 0.6, 1]  # blue
    lightb_specular = [0.0, 0, 0.8, 1]  # blue
    light_direction = [1.0, -1.0, 1.0, 0.0]  # Light points down


    # For Light 1 (red), set position, ambient, diffuse, and specular values
    glLightfv(GL_LIGHT1, GL_POSITION, light_position)
    glLightfv(GL_LIGHT1, GL_AMBIENT, lightr_ambient)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, lightb_diffuse)
    glLightfv(GL_LIGHT1, GL_SPECULAR, lightb_specular)

    # For Light 2 (green), set position, ambient, diffuse, and specular values
    # glLightfv(GL_LIGHT2, GL_POSITION, light_position)
    # glLightfv(GL_LIGHT2, GL_AMBIENT, lightg_ambient)
    # glLightfv(GL_LIGHT2, GL_DIFFUSE, lightb_diffuse)
    # glLightfv(GL_LIGHT2, GL_SPECULAR, lightb_specular)

    # Constant attenuation (for distance, etc.)
    # Only works for fixed light locations!  Otherwise disabled
    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, 2.0)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, 0.0)
    glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, 0.0)

    # glLightf(GL_LIGHT2, GL_CONSTANT_ATTENUATION, 3.0)
    # glLightf(GL_LIGHT2, GL_LINEAR_ATTENUATION, 0.0)
    # glLightf(GL_LIGHT2, GL_QUADRATIC_ATTENUATION, 0.0)

    # Create a spotlight effect (none at the moment)
    if red_light:
        glLightf(GL_LIGHT1, GL_SPOT_CUTOFF, 45.0)
        glLightf(GL_LIGHT1, GL_SPOT_EXPONENT, 0.0)
        glLightfv(GL_LIGHT1, GL_SPOT_DIRECTION, light_direction)
    else:
        glLightf(GL_LIGHT1, GL_SPOT_CUTOFF, 180.0)
        glLightf(GL_LIGHT1, GL_SPOT_EXPONENT, 0.0)

    glLightModeli(GL_LIGHT_MODEL_LOCAL_VIEWER, use_lv)
    glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)
    #  Try GL_TRUE - but then watch what happens when light is low

    glEnable(GL_LIGHT1)
    #glEnable(GL_LIGHT2)

    # This part draws a SELF-COLORED sphere (in spot where light is!)
    glPushMatrix()
    glTranslatef(lx, ly, lz)
    glDisable(GL_LIGHTING)
    glColor3f(brightness, 0, 0)
    glutSolidSphere(0.5, 20, 20)
    glEnable(GL_LIGHTING)
    glPopMatrix()

def place_green_light():
    """Set up the main light."""
    glMatrixMode(GL_MODELVIEW)
    lx = 5.0
    ly = light_height
    lz = 3.0
    light_position = [lx, ly, lz, 1.0]
    # light_ambient = [ 1*brightness, 1*brightness, 1*brightness, 1.0 ]
    # light_diffuse = [ 1*brightness, 1*brightness, 1*brightness, 1.0 ]
    # light_specular = [ 1*brightness, 1*brightness, 1*brightness, 1.0 ]
    lightb_ambient = [0.0, 0, 1, 1]  # blue
    lightr_ambient = [1.0, 0, 0, 1]  # red
    lightg_ambient = [0, 1.0, 0, 1]  # green
    lightb_diffuse = [0.4, 0.4, 0.6, 1]  # blue
    lightb_specular = [0.0, 0, 0.8, 1]  # blue
    light_direction = [1.0, -1.0, 1.0, 0.0]  # Light points down


    # For Light 1 (red), set position, ambient, diffuse, and specular values
    # glLightfv(GL_LIGHT1, GL_POSITION, light_position)
    # glLightfv(GL_LIGHT1, GL_AMBIENT, lightr_ambient)
    # glLightfv(GL_LIGHT1, GL_DIFFUSE, lightb_diffuse)
    # glLightfv(GL_LIGHT1, GL_SPECULAR, lightb_specular)

    # For Light 2 (green), set position, ambient, diffuse, and specular values
    glLightfv(GL_LIGHT2, GL_POSITION, light_position)
    glLightfv(GL_LIGHT2, GL_AMBIENT, lightg_ambient)
    glLightfv(GL_LIGHT2, GL_DIFFUSE, lightb_diffuse)
    glLightfv(GL_LIGHT2, GL_SPECULAR, lightb_specular)

    # Constant attenuation (for distance, etc.)
    # Only works for fixed light locations!  Otherwise disabled
    # glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, 2.0)
    # glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, 0.0)
    # glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, 0.0)

    glLightf(GL_LIGHT2, GL_CONSTANT_ATTENUATION, 3.0)
    glLightf(GL_LIGHT2, GL_LINEAR_ATTENUATION, 0.0)
    glLightf(GL_LIGHT2, GL_QUADRATIC_ATTENUATION, 0.0)

    # Create a spotlight effect (none at the moment)
    if green_light:
        glLightf(GL_LIGHT2, GL_SPOT_CUTOFF, 45.0)
        glLightf(GL_LIGHT2, GL_SPOT_EXPONENT, 0.0)
        glLightfv(GL_LIGHT2, GL_SPOT_DIRECTION, light_direction)
    else:
        glLightf(GL_LIGHT2, GL_SPOT_CUTOFF, 180.0)
        glLightf(GL_LIGHT2, GL_SPOT_EXPONENT, 0.0)

    glLightModeli(GL_LIGHT_MODEL_LOCAL_VIEWER, use_lv)
    glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)
    #  Try GL_TRUE - but then watch what happens when light is low


    glEnable(GL_LIGHT2)

    # This part draws a SELF-COLORED sphere (in spot where light is!)
    glPushMatrix()
    glTranslatef(lx, ly, lz)
    glDisable(GL_LIGHTING)
    glColor3f(0, brightness, 0)
    glutSolidSphere(0.5, 20, 20)
    glEnable(GL_LIGHTING)
    glPopMatrix()

def place_lamp_light():
    glMatrixMode(GL_MODELVIEW)
    lx = -0.7
    ly = 2.5
    lz = 0.8
    light_position = [ lx, ly, lz, 1.0 ]
    lightb_ambient = [1, 1, 1, 1]  # blue
    lightr_ambient = [1, 1, 1, 1]  # red
    lightg_ambient = [1, 1.0, 1, 1]  # green
    lightb_diffuse = [1, 1, 1, 1]  # blue
    lightb_specular = [1, 1, 1, 1]  # blue
    light_direction = [0.0, -1.0, 0.0, 1.0]  # Light points down


    # For Light 0 (blue), set position, ambient, diffuse, and specular values
    glLightfv(GL_LIGHT3, GL_POSITION, light_position)
    glLightfv(GL_LIGHT3, GL_AMBIENT, lightb_ambient)
    glLightfv(GL_LIGHT3, GL_DIFFUSE, lightb_diffuse)
    glLightfv(GL_LIGHT3, GL_SPECULAR, lightb_specular)



    # Constant attenuation (for distance, etc.)
    # Only works for fixed light locations!  Otherwise disabled
    glLightf(GL_LIGHT3, GL_CONSTANT_ATTENUATION, 4.0)
    glLightf(GL_LIGHT3, GL_LINEAR_ATTENUATION, 0.0)
    glLightf(GL_LIGHT3, GL_QUADRATIC_ATTENUATION, 0.0)

    # Create a spotlight effect (none at the moment)
    if lamp_light:
        glLightf(GL_LIGHT3, GL_SPOT_CUTOFF, 45.0)
        glLightf(GL_LIGHT3, GL_SPOT_EXPONENT, 0.0)
        glLightfv(GL_LIGHT3, GL_SPOT_DIRECTION, light_direction)
    else:
        glLightf(GL_LIGHT3, GL_SPOT_CUTOFF,180.0)
        glLightf(GL_LIGHT3, GL_SPOT_EXPONENT, 0.0)
    
    glLightModeli(GL_LIGHT_MODEL_LOCAL_VIEWER, use_lv)
    glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)
    #  Try GL_TRUE - but then watch what happens when light is low
    
    glEnable(GL_LIGHT3)


    # This part draws a SELF-COLORED sphere (in spot where light is!)
    glPushMatrix()
    glTranslatef(lx,ly,lz)
    glDisable(GL_LIGHTING)
    glColor3f(brightness, brightness, brightness)
    glutSolidSphere(0.17, 20, 2)
    glEnable(GL_LIGHTING)
    glPopMatrix()
    

    
def set_copper(face):
    """Set the material properties of the given face to "copper"-esque.

    Keyword arguments:
    face -- which face (GL_FRONT, GL_BACK, or GL_FRONT_AND_BACK)
    """
    ambient = [ 0.19125, 0.0735, 0.0225, 1.0 ]
    diffuse = [ 0.7038, 0.27048, 0.0828, 1.0 ]
    specular = [ 0.256777, 0.137622, 0.086014, 1.0 ]
    shininess = 128.0
    glMaterialfv(face, GL_AMBIENT, ambient);
    glMaterialfv(face, GL_DIFFUSE, diffuse);
    glMaterialfv(face, GL_SPECULAR, specular);
    glMaterialf(face, GL_SHININESS, shininess);
    
def set_pewter(face):
    """Set the material properties of the given face to "pewter"-esque.

    Keyword arguments:
    face -- which face (GL_FRONT, GL_BACK, or GL_FRONT_AND_BACK)
    """
    ambient = [ 0.10588, 0.058824, 0.113725, 1.0 ]
    diffuse = [ 0.427451, 0.470588, 0.541176, 1.0 ]
    specular = [ 0.3333, 0.3333, 0.521569, 1.0 ]
    shininess = 9.84615
    glMaterialfv(face, GL_AMBIENT, ambient);
    glMaterialfv(face, GL_DIFFUSE, diffuse);
    glMaterialfv(face, GL_SPECULAR, specular);
    glMaterialf(face, GL_SHININESS, shininess);

def generateCheckerBoardTexture():
    """
    * Generate a texture in the form of a checkerboard
    * Why?  Simple to do...
    """
    global checkerBoardName
    texture = [0] * (NROWS * NCOLS * 4)
    for i in range(NROWS):
        for j in range(NCOLS):
            c = 135 if ((i & 8) ^ (j & 8)) else 255
            idx = (i * NCOLS + j) * 4
            texture[idx] = c  # Red
            texture[idx + 1] = c  # Green
            texture[idx + 2] = c  # Blue
            texture[idx + 3] = 150  # Alpha (transparency)

    # Generate a "name" for the texture.
    # Bind this texture as current active texture
    # and sets the parameters for this texture.
    checkerBoardName = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, checkerBoardName)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, NCOLS, NROWS, 0, GL_RGBA,
                 GL_UNSIGNED_BYTE, texture)

def loadImageTexture(filename):
    # Load the image from the file and return as a texture
    im = Image.open(filename)
    print("Concrete dimensions: {0}".format(im.size))  # If you want to see the image's original dimensions
    # dim = 128
    # size = (0,0,dim,dim)
    # texture = im.crop(size).tobytes("raw")   # The cropped texture
    texture = im.tobytes("raw")  # The cropped texture
    dimX = im.size[0]
    dimY = im.size[1]

    returnTextureName = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, returnTextureName)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, dimX, dimY, 0, GL_RGB,
                 GL_UNSIGNED_BYTE, texture)
    return returnTextureName


if __name__ == '__main__': main()
