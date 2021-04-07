# ==============================
# Christian Duncan
# CSC345: Computer Graphics
#   Spring 2021
# Description:
#   Demonstrates use of gluCylinder and gluSphere to draw
#   3-d objects.
#
# THIS FILE IS FOR REFERENCE/STUDY ONLY!!!
# ==============================

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from PIL import Image
import sys
from utils import *

# These parameters define the camera's lens shape
CAM_NEAR = 0.01
CAM_FAR = 1000.0
CAM_ANGLE = 60.0

# These parameters define simple animation properties
MIN_STEP = 0.1
# Controls the rotation speed, how much camera rotation will increment by
DEFAULT_STEP = 0.2
ANGLE_STEP = DEFAULT_STEP
FPS = 60.0
DELAY = int(1000.0 / FPS + 0.5)

# Checkerboard dimensions (texture dimensions are powers of 2)
NROWS = 64
NCOLS = 64

# Plane dimensions (not airplane - just a flat sheet)
PLANE_WIDTH = 10
PLANE_HEIGHT = 10


# Global (Module) Variables 
winWidth = 1000
winHeight = 1000
name = b'Shapes...'
step = MIN_STEP
animate = False
angleMovement = 0
perspectiveMode = True

#Car animation/ Wheel animation global variables
#Dis=Displacement
carPosX = 0
carDis = 0.05
wheelRotation = 0
wheelDis = -1.8
MAX_BOUND = 5
MIN_BOUND = -5

def main():
    # Create the initial window
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(winWidth, winHeight)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(name)

    init()

    # Setup the callback returns for display and keyboard events
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(specialKeys)
    glutTimerFunc(0, timer, DELAY)

    # Enters the main loop.
    # Displays the window and starts listening for events.
    glutMainLoop()
    return



def init():
    global cone, cone2, wheel, faceTextureName
    # Cones for 
    cone = gluNewQuadric()
    cone2 = gluNewQuadric()
    wheel = gluNewQuadric()
    
    gluQuadricDrawStyle(cone, GLU_LINE)
    gluQuadricDrawStyle(cone2, GLU_LINE)
    gluQuadricDrawStyle(wheel, GLU_LINE)

    generateCheckerBoardTexture()
    faceTextureName = loadImageTexture("brick.jpg")




# Callback function used to display the scene
# Currently it just draws a simple polyline (LINE_STRIP)
def display():
    # Set the viewport to the full screen
    # For Mac: Multiply window width & height by 2
    glViewport(0, 0, 2*winWidth, 2*winHeight)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if perspectiveMode:
        # Set view to Perspective Proj. (angle, aspect ratio, near/far planes)
        gluPerspective(CAM_ANGLE, winWidth/winHeight, CAM_NEAR, CAM_FAR)
    else:
        glOrtho(-winWidth/40, winWidth/40, -
                winHeight/40, winHeight/40, -100, 100)

    # Clear the Screen
    # Clears the screen with white, speficially white
    glClearColor(1.0, 1.0, 1.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)

    # And draw the "Scene"
    glColor3f(1.0, 1.0, 1.0)
    drawScene()

    # And show the scene
    glFlush()
    glutSwapBuffers()  # needed for double buffering!

# Timer: Used to animate the scene when activated:


def timer(alarm):
    glutTimerFunc(0, timer, DELAY)   # Start alarm clock agani
    if animate:
        # Advance to the next frame
        advance()
        glutPostRedisplay()

# Controls the animation. Advances the scene by a single frame
def advance():
    #Gloabl variable call to get car and wheel x value, displacement modifier, and angle modifier
    #Gets the min and max values for the displacment
    global carPosX, carDis, MAX_BOUND, MIN_BOUND, wheelDis, wheelRotation
    
    #Moves the car and wheels 
    carPosX += carDis
    wheelRotation += wheelDis
    if(carPosX>MAX_BOUND or carPosX<MIN_BOUND):
        carDis *= -1
        wheelDis *= -1
    glutPostRedisplay()
            


def specialKeys(key, x, y):
    global angleMovement
    if key == GLUT_KEY_LEFT:
        angleMovement += ANGLE_STEP
        glutPostRedisplay()

    elif key == GLUT_KEY_RIGHT:
        angleMovement -= ANGLE_STEP
    glutPostRedisplay()

# Defines Keyboard controls (Space bar starts animation)
def keyboard(key, x, y):
    global angleMovement
    if ord(key) == 27:  
        glutLeaveMainLoop()
    elif ord(key) == ord(' '):
        global animate
        animate = not animate  # not animate = True


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

def drawScene():
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslate(0, -3, -20)
    glRotated(angleMovement, 0, 1, 0) 
    glColor3f(0, 0, 0)
    draw()

def draw():
    glPushMatrix()
   
    # #cone1
    # glPushMatrix()
    # glTranslated(0, -5, -5)
    # glRotated(-90, 1, 0, 0)
    # gluCylinder(cone2, 1, 0.25, 5, 10, 10)
    # glPopMatrix()
    #
    # #cone2
    # glPushMatrix()
    # glTranslated(0, -5, 5)
    # glRotated(-90, 1, 0, 0)
    # gluCylinder(cone2, 1, 0.25, 5, 10, 10)
    # glPopMatrix()
    #
    # #car body
    # glPushMatrix()
    # glTranslated(carPosX, -4, 0)
    # glScaled(5, 1, 3)
    # glutWireCube(1.0)
    # glPopMatrix()
    #
    # #car bar
    # glPushMatrix()
    # glTranslated(carPosX + 1.5, -3, 0)
    # glScaled(1, 1, 3)
    # glutWireCube(1.0)
    # glPopMatrix()
    #
    # #tire front right
    # glPushMatrix()
    # glTranslated(carPosX + 1.5, -4, 1.5)
    # glRotated(wheelRotation, 0, 0, 1)
    # gluCylinder(wheel, .5, .5, .5, 20, 5)
    # glPopMatrix()
    #
    # #tire front left
    # glPushMatrix()
    # glTranslated(carPosX + 1.5, -4, -2)
    # glRotated(wheelRotation, 0, 0, 1)
    # gluCylinder(wheel, .5, .5, .5, 20, 5)
    # glPopMatrix()
    #
    # #tire back right
    # glPushMatrix()
    # glTranslated(carPosX +  -1.5, -4, 1.5)
    # glRotated(wheelRotation, 0, 0, 1)
    # gluCylinder(wheel, .5, .5, .5, 20, 5)
    # glPopMatrix()
    #
    # #tire back left
    # glPushMatrix()
    # glTranslated(carPosX +  -1.5, -4, -2)
    # glRotated(wheelRotation, 0, 0, 1)
    # gluCylinder(wheel, .5, .5, .5, 20, 5)
    # glPopMatrix()

    glPushMatrix()
    drawFloor(PLANE_WIDTH, PLANE_HEIGHT, checkerBoardName)
    glPopMatrix()

    glPushMatrix()
    glRotated(90, 0, 1, 0)
    glTranslated(0, 0, 5)
    drawPlane(PLANE_WIDTH, PLANE_HEIGHT, faceTextureName)
    glPopMatrix()

    glPushMatrix()
    glRotated(90, 0, 1, 0)
    glTranslated(0, 0, -5)
    drawPlane(PLANE_WIDTH, PLANE_HEIGHT, faceTextureName)
    glPopMatrix()

    glPushMatrix()
    glRotated(180, 0, 1, 0)
    glTranslated(0, 0, 5)
    drawPlane(PLANE_WIDTH, PLANE_HEIGHT, faceTextureName)
    glPopMatrix()

    # fourth wall but blocks view so commented out for now
    # glPushMatrix()
    # glRotated(180, 0, 1, 0)
    # glTranslated(0, 0, -5)
    # drawPlane(PLANE_WIDTH, PLANE_HEIGHT, faceTextureName)
    # glPopMatrix()

    glPopMatrix()


def generateCheckerBoardTexture():
    """
    * Generate a texture in the form of a checkerboard
    * Why?  Simple to do...
    """
    global checkerBoardName
    texture = [0] * (NROWS * NCOLS * 4)
    for i in range(NROWS):
        for j in range(NCOLS):
            c = 0 if ((i & 8) ^ (j & 8)) else 255
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


def loadConcreteTexture():
    global concreteTextureName

    # Load the image and crop it to the proper 128x128 (or edit the file!)
    im = Image.open("concrete.jpg")
    print("Concrete dimensions: {0}".format(im.size))  # If you want to see the image's original dimensions
    dim = 128
    size = (0, 0, dim, dim)
    texture = im.crop(size).tobytes("raw")  # The cropped texture

    concreteTextureName = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, concreteTextureName)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, dim, dim, 0, GL_RGB,
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

if __name__ == '__main__':
    main()
