#==============================
# Christian Duncan
# CSC345: Computer Graphics
#   Spring 2021
# Hello World
#   Displays a simple polyline on the screen
#==============================

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys

# These parameters define the camera's lens shape
CAM_NEAR = 0.01
CAM_FAR = 1000.0
CAM_ANGLE = 60.0

# These parameters define simple animation properties
MIN_STEP = 0.1
DEFAULT_STEP = 0.001
ANGLE_STEP = DEFAULT_STEP
FPS = 60.0
DELAY = int(1000.0 / FPS + 0.5)

# Global variables
winWidth = 1000
winHeight = 1000
name = b'Wireframe Scene!'

def main():
    # Create the initial window
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(winWidth, winHeight)
    glutInitWindowPosition(100,100)
    glutCreateWindow(name)

    init()

    # This callback is invoked when window needs to be drawn or redrawn
    glutDisplayFunc(display)

    # This callback is invoked when a keyboard event happens
    glutKeyboardFunc(keyboard);

    # Enters the main loop.
    # Displays the window and starts listening for events.
    glutMainLoop()
    return

# Initialize some of the OpenGL matrices
def init():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, 1.0, 0.0, 1.0)

# Callback function used to display the scene
# Currently it just draws a simple polyline (LINE_STRIP)
def display():

    glViewport(0,0, winWidth, winHeight)
    glClearColor(1.0, 1.0, 1.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)

    # Try other shapes, GL_TRIANGLES, GL_TRIANGLE_STRIP, GL_TRIANGLE_FAN, GL_QUADS, GL_QUAD_STRIP, GL_POLYGON, GL_POINTS
    glBegin(GL_TRIANGLES)
    glColor3f(1.0,0.0,0.0)   # Set color state to Red
    # glVertex*(x,y,z)
    glVertex2f(0.25, 0.75)
    # glVertex3f(0.25,0.75,0)
    # glColor3f(0.0,1.0,0.0)   # Set color state to Green
    glVertex3f(0.25,0.25,0)
    # glColor3f(0.0,0.0,1.0)   # Set color state to Blue
    glVertex3f(0.75,0.25,0)
    # glColor3f(0.0,0.0,0.0)   # Set color state to Black
    glVertex3f(0.75,0.75,0)
    glEnd()
    glFlush()

# Callback function used to handle any key events
# Currently, it just responds to the ESC key (which quits)
# key: ASCII value of the key that was pressed
# x,y: Location of the mouse (in the window) at time of key press)
def keyboard(key, x, y):
    print("Key [{0}] pressed at location {1},{2}".format(key, x, y))
    if ord(key) == 27:  # ASCII code 27 = ESC-key
        glutLeaveMainLoop()  # Will leave main loop and then exit program

if __name__ == '__main__': main()
