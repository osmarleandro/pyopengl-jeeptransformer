# coding: utf8

__author__ = "Afonso Henrique / Osmar Leandro"

from pygame import mixer
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
from PIL import Image

# Ângulo de rotação da roda
angw = 0

# Rotação do ambiente nos eixos X, Y e Z
angX = -60
angY = 0
angZ = 0

# Posição e rotação do ambiente
pos = [0., 0., -30.]
axis = [1., 0, 0.]

# Posição e rotação do carro
angcar = 0
poscar = [0., 0., 0.]
axiscar = [1, 0., 0.]

# Posição membros do transformer
posHead = [2, 2, 1.8]
posArmLeft = [2, 2, 0]
posArmRight = [2, 2, 0]
posLeftLeg = [3, 1.6, 1]
posRightLeg = [3, 2.4, 1]

limLegs = 4.2
limArms = 3
limHead = 0.2
scaleArms = [0.1, 1, 0.75]
scaleLegs = [0.1, 1.1, 1]

name = 'Jeep v1.0 - with pyOPENGL'

STRING_MENU = ['|-------------- MENU --------------|', '|-- w/s para rotacional no eixoX --|',
               '|-- a/d para rotacionar no eixoY --|', '|-- 1/3 para escala horizontal ----|',
               '|-- 2/8 para translacao vertical --|', '|-- 4/6 para movimentar o carro ---|',
               '|--- t para transformar o carro ---|', '|-- p parar a rotacao dos eixos ---|',
               '|----- r para restaurar visao -----|', '|----  x para movimentar eixos ----|',
               '|----------------------------------|']

transformed = 0

COLORS = []
FLOOR_COLOR = [0.3, 0.3, 0.3]
BLACK_COLOR = [0, 0, 0]
WHITE_COLOR = [1, 1, 1]
CABIN_COLOR = [0.12, 0.21, 0.01]
CABIN_STROKE_COLOR = [0.62, 0.9, 0.47]
HEADHIGHTS_COLOR = [0.7, 0.7, 0.05]


def init():
    glEnable(GL_NORMALIZE)
    glLightfv(GL_LIGHT0, GL_POSITION, [.0, 10.0, 10., 0.])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [.0, .0, .0, 1.0]);
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0]);
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0]);
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glShadeModel(GL_SMOOTH)
    glClearColor(1.0, 1.0, 1.0, 0.0)
    glClearDepth(1.0)


def main():
    glutInit(sys.argv)
    glutSound()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1280, 720)
    glutCreateWindow(name)
    init()

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutMouseFunc(mouse)
    glutKeyboardFunc(keyboard)
    glutMainLoop()


def loadTexture(name_path):
    image = Image.open(name_path)

    ix = image.size[0]
    iy = image.size[1]
    image = image.tostring("raw", "RGBX", 0, -1)

    # Create Texture	
    # There does not seem to be support for this call or the version of PyOGL I have is broken.
    # glGenTextures(1, texture)
    # glBindTexture(GL_TEXTURE_2D, texture)   # 2d texture (x and y size)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)


def glutSound():
    mixer.init()
    mixer.music.load('intro.mp3')
    mixer.music.play()
    mixer.music.rewind()


def carSound():
    mixer.music.load('engine-sound2.mp3')
    mixer.music.play(-1)
    mixer.music.rewind()


def transfSound():
    mixer.music.load('transf.mp3')
    mixer.music.play()
    mixer.music.rewind()


def glut_print(x, y, font, text, r, g, b, a):
    blending = False
    if glIsEnabled(GL_BLEND):
        blending = True

    glColor3f(r, g, b)
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ctypes.c_int(ord(ch)))

    if not blending:
        glDisable(GL_BLEND)


def drawFloor():
    glPushMatrix()
    glTranslatef(0, 0, -1.45)
    glScalef(11, 11, 0.25)
    cor(FLOOR_COLOR)
    glutSolidCube(2)
    glPopMatrix()
    glFlush()


def drawRoad():
    loadTexture("road.bmp")
    glPushMatrix()
    glTranslatef(28, -1, -1.1)
    glScalef(200, 5, 0.25)
    glRotatef(90, 0., 0., 1.)
    glEnable(GL_TEXTURE_2D)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0);
    glVertex3f(0.0, 0.0, 0.0)  # Bottom Left Of The Texture and Quad
    glTexCoord2f(1.0, 0.0);
    glVertex3f(2.0, 0.0, 0.0)  # Bottom Right Of The Texture and Quad
    glTexCoord2f(1.0, 10.0);
    glVertex3f(2.0, 10.0, 0.0)  # Top Right Of The Texture and Quad
    glTexCoord2f(0.0, 10.0);
    glVertex3f(0.0, 10.0, 0.0)  # Top Left Of The Texture and Quad
    glEnd();  # Done Drawing The Cube
    glPopMatrix()

    glFlush()
    glDisable(GL_TEXTURE_2D)


def cor(COLORS):
    glMaterialfv(GL_FRONT, GL_DIFFUSE, COLORS)


def drawWheel(trans_x, trans_y, trans_z):
    glPushMatrix()

    glTranslatef(trans_x, trans_y, trans_z)
    glRotated(angw, 0, 1, 0)
    glScalef(1, 0.25, 1)
    cor(BLACK_COLOR)
    glutSolidSphere(1, 20, 20)

    glScalef(1, 2, 1)
    cor(WHITE_COLOR)
    glutSolidSphere(0.8, 20, 20)
    glPopMatrix()


def drawChassis():
    glPushMatrix()
    glTranslatef(2, 2, 0)
    cor(CABIN_COLOR)
    glScalef(3, 1, 0.25)
    glutSolidCube(2)
    cor(CABIN_STROKE_COLOR)
    glutWireCube(2)
    glPopMatrix()


def drawCabin():
    glPushMatrix()
    glTranslatef(3.25, 2, 1.375)
    cor(CABIN_COLOR)
    glScalef(2.25, 1, 1.125)
    glutSolidCube(2)
    cor(CABIN_STROKE_COLOR)
    glutWireCube(2)
    glPopMatrix()


def drawEngineBox():
    glPushMatrix()
    glTranslatef(0, 2, 0.75)
    cor(CABIN_COLOR)
    glScalef(1, 1, 0.5)
    glutSolidCube(2)
    cor(CABIN_STROKE_COLOR)
    glutWireCube(2)
    glPopMatrix()


def drawHeadlight(trans_x, trans_y, trans_z):
    quad = gluNewQuadric()
    glPushMatrix()
    glTranslatef(trans_x, trans_y, trans_z)
    glRotatef(-90.0, 0, 1.0, 0)
    cor(HEADHIGHTS_COLOR)
    glScalef(1, 1, 0.5)
    gluCylinder(quad, 0.3, 0.25, 0.3, 20, 2)
    glPopMatrix()


def drawArm(trans_x, trans_y, trans_z):
    glPushMatrix()
    glTranslatef(trans_x, trans_y, trans_z)
    cor(HEADHIGHTS_COLOR)
    glScalef(*scaleArms)
    glutSolidCube(1)
    glPopMatrix()


def drawLeg(trans_x, trans_y, trans_z):
    glPushMatrix()
    glTranslatef(trans_x, trans_y, trans_z)
    cor(HEADHIGHTS_COLOR)
    glScalef(*scaleLegs)
    glutSolidCube(1)
    glPopMatrix()


def drawHead(trans_x, trans_y, trans_z):
    loadTexture("new_head_face.bmp")
    glPushMatrix()
    glTranslatef(trans_x, trans_y, trans_z)
    glScalef(0.8, 0.6, 0.6)
    glRotatef(90, 1., 0., 0.)
    glRotatef(90, 0, 1., 0.)
    glEnable(GL_TEXTURE_2D)
    glColor3f(0.7, 0.7, 0.05)
    glBegin(GL_QUADS)

    # Front Face
    glVertex3f(-1.0, -1.0, 1.0)  # Bottom Left Of The Texture and Quad
    glVertex3f(1.0, -1.0, 1.0)  # Bottom Right Of The Texture and Quad
    glVertex3f(1.0, 1.0, 1.0)  # Top Right Of The Texture and Quad
    glVertex3f(-1.0, 1.0, 1.0)  # Top Left Of The Texture and Quad

    # Back Face
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(1.0, 1.0, -1.0)
    glVertex3f(1.0, -1.0, -1.0)

    # Top Face
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(1.0, 1.0, 1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(1.0, 1.0, -1.0)

    # Bottom Face
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(1.0, -1.0, -1.0)
    glVertex3f(1.0, -1.0, 1.0)
    glVertex3f(-1.0, -1.0, 1.0)

    glEnd()
    loadTexture("new_head_left.bmp")
    glBegin(GL_QUADS)

    # Right face (robot_left_face)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(1.0, -1.0, -1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(1.0, 1.0, -1.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(1.0, -1.0, 1.0)

    glEnd()
    loadTexture("new_head_right.bmp")
    glBegin(GL_QUADS)


    # Left Face (robot_right_face)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-1.0, 1.0, -1.0)

    glEnd();  # Done Drawing The Cube
    glPopMatrix()

    glFlush()
    glDisable(GL_TEXTURE_2D)


def display():
    global angZ
    global angY
    global angX
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    showTextMsg()
    glutPostRedisplay()

    glLoadIdentity()

    glTranslatef(*pos)
    glRotatef(angX, 1., 0., 0.)
    glRotatef(angY, 0., 1, 0.)
    glRotatef(angZ, 0., 0, 1.)
    # drawFloor()
    drawRoad()

    glTranslatef(*poscar)
    glRotatef(angcar, *axiscar)
    drawWheel(0, 1, 0)
    drawWheel(0, 3, 0)
    drawWheel(4, 1, 0)
    drawWheel(4, 3, 0)
    drawChassis()
    drawCabin()
    drawEngineBox()
    drawHeadlight(-1, 1.4, 0.89)
    drawHeadlight(-1, 2.6, 0.89)

    # Membros do transformer
    drawArm(*posArmLeft)
    drawArm(*posArmRight)

    drawLeg(*posRightLeg)
    drawLeg(*posLeftLeg)

    drawHead(*posHead)

    glutSwapBuffers()
    glFlush()


def showTextMsg():
    gluOrtho2D(0.0, 1.0, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    cor(BLACK_COLOR)
    glTranslatef(-10.0, 0.0, -8.0)
    for index in range(len(STRING_MENU)):
        glTranslatef(0, 0, 1)
        glut_print(10, 10, GLUT_BITMAP_9_BY_15, STRING_MENU[index], 1.0, 1.0, 1.0, 1.0)


def makeTranform():
    global posHead
    global angcar
    global axiscar
    global poscar

    global posArmLeft
    global posArmRight

    global posLeftLeg
    global posRightLeg

    transfSound()
    #angcar = 90
    axiscar = [0, 1., 0.]
    #poscar = [0., 0., 7.]

    # mudar a posicao dos braços, pernas e cabeça
    # posHead = [0.2, 2.0, 1.8]
    posArmLeft = [2, 0.5, 1]
    posArmRight = [2, 3.5, 1]

    posLeftLeg = [6, 1.2, 1]
    posRightLeg = [6, 2.8, 1]

    glutPostRedisplay()
    glutIdleFunc(animateRobot)
    glFlush()


def unTransform():
    global posHead
    global angcar
    global axiscar
    global poscar
    global scaleLegs
    global scaleArms

    global posArmLeft
    global posArmRight

    global posLeftLeg
    global posRightLeg

    angcar = 0
    poscar = [0., 0., 0.]
    axiscar = [1, 0., 0.]

    # mudar a posicao dos braços, pernas e cabeça
    posHead = [2, 2.0, 1.8]
    posArmLeft = [2, 2, 0]
    posArmRight = [2, 2, 0]
    posLeftLeg = [3, 1.6, 1]
    posRightLeg = [3, 2.4, 1]

    scaleArms = [0.1, 1, 0.75]
    scaleLegs = [0.1, 1.1, 1]

    glutPostRedisplay()
    glFlush()


def transform():
    global transformed

    if (transformed == 0):
        makeTranform()
        transformed = 1
        print "Transformando..."

    elif (transformed == 1):
        unTransform()
        transformed = 0
        print "Restaurando Transformação..."


def animateRobot():
    global scaleLegs
    global scaleArms
    global posHead
    global angcar
    global poscar

    if (scaleLegs[0] < limLegs):
        scaleLegs[0] += 0.05

    if (scaleArms[0] < limArms):
        scaleArms[0] += 0.04

    if (posHead[0] > limHead):
        posHead[0] -= 0.02
        
    if(angcar <= 90):
        angcar += 1.5
        
    if(poscar[2] <= 7):
        poscar[2] +=0.1
        
    else:
        glutIdleFunc(rotateAxixZ)
    glutPostRedisplay()


def driveCarFront():
    global angw
    if (poscar[0] > -70):
        poscar[0] -= 0.08
        angw = (angw + 15) % 360
    else:
        mixer.music.stop()
    glutPostRedisplay()


def driveCarBack():
    global angw
    if (poscar[0] < 20):
        poscar[0] += 0.08
        angw = (angw + 15) % 360
    else:
        mixer.music.stop()
    glutPostRedisplay()

def rotateAxixZ():
    global angZ
    angZ -= .1
    glutPostRedisplay()


def resetView():
    global angX
    global angY
    global angZ
    angX = -75
    angY = 0
    angZ = 0
    glutPostRedisplay()


def dance():
    global angX
    global angY
    global angZ
    angX -= .1
    angY -= .1
    angZ -= .1
    glutPostRedisplay()


def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(w) / float(h), 0.1, 100.0)
    gluLookAt(0.0, 0.0, 0.1,  # define a posição da câmera
              0.0, 0.0, 0.0,  # posição para onde a câmera aponta
              0.0, 1.0, 0.0)  # defina a parte de cima do cenário 3D
    glMatrixMode(GL_MODELVIEW)


def mouse(button, state, x, y):
    global angw
    if button == GLUT_LEFT_BUTTON:
        angw = (angw + 15) % 360
    glutPostRedisplay()


def keyboard(key, x, y):
    global angX
    global angY
    global angZ
    global angw
    global axis

    if key == '\x1B':  # ESC
        sys.exit(0)

    # Translação
    elif key == '2':
        pos[1] -= 0.1
    elif key == '8':
        pos[1] += 0.1

    # Movimentação do carro
    elif key == '4':
        carSound()
        glutIdleFunc(driveCarFront)

    elif key == '6':
        carSound()
        glutIdleFunc(driveCarBack)

    # Escala
    elif key == '3':
        pos[2] -= 0.1
    elif key == '1':
        pos[2] += 0.1

    # Rotação
    elif key == 'w':
        angX += 1.0
    elif key == 's':
        angX -= 1.0

    elif key == 'q':
        angY += 1.0
    elif key == 'e':
        angY -= 1.0

    elif key == 'a':
        angZ += 1.0
    elif key == 'd':
        angZ -= 1.0

    # Transformer
    elif key == 't':
        transform()

    # Para para a execução de rendenização automática
    elif key == 'p':
        glutIdleFunc(display)

        # Rotação automática
    elif key == 'x':
        glutIdleFunc(dance)

    # Restaurar os eixos
    elif key == 'r':
        resetView()

    glutPostRedisplay()


if __name__ == '__main__': main()
