import math
import random

try:
    import simplegui

except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


# vector class
class Vector:

    # initialiser
    def __init__(self, u=0, v=0):
        self.u = u
        self.v = v

    # string representation of the vector
    def __str__(self):
        return "(" + str(self.u) + "," + str(self.v) + ")"

    # testing equality of the vectors
    def __eq__(self, other):
        return self.u == other.u and self.v == other.v

    # testing inequality of vectors
    def __ne__(self, other):
        return not self.__eq__(other)

    # returns with the point corresponding to the vector
    def get_p(self):
        return self.u, self.v

    # returns a copy of the vector
    def copy(self):
        return Vector(self.u, self.v)

    # adds another vector to this vector
    def add(self, other):
        self.u += other.u
        self.v += other.v
        return self

    def __add__(self, other):
        return self.copy().add(other)

    # makes the vector point in the opposite direction
    def negate(self):
        return self.multiply(-1)

    def __neg__(self):
        return self.copy().negate()

    # subtracts another vector from this vector
    def subtract(self, other):
        return self.add(-other)

    def __sub__(self, other):
        return self.copy().subtract(other)

    # multiplies the vector by a scalar
    def multiply(self, k):
        self.u *= k
        self.v *= k
        return self

    def __mul__(self, k):
        return self.copy().multiply(k)

    def __rmul__(self, k):
        return self.copy().multiply(k)

    # divides the vector by a scalar
    def divide(self, k):
        return self.multiply(1 / k)

    def __truediv__(self, k):
        return self.copy().divide(k)

    # normalizes the vector
    def normalize(self):
        return self.divide(self.length())

    # returns a normalized vector
    def get_normalized(self):
        return self.copy().normalize()

    # returns the dot product of this vector with another one
    def dot(self, other):
        return self.u * other.u + self.v * other.v

    # returns vector length
    def length(self):
        return math.sqrt(self.u ** 2 + self.v ** 2)

    # returns the squared length of the vector
    def length_squared(self):
        return self.u ** 2 + self.v ** 2

    # reflect this vector on a normal
    def reflect(self, normal):
        n = normal.copy()
        n.multiply(2 * self.dot(normal))
        self.subtract(n)
        return self

    # returns the angle between this vector and another one
    def angle(self, other):
        return math.acos(self.dot(other) / (self.length() * other.length()))

    # rotates the vector 90 degrees anticlockwise
    def rotate_anti(self):
        self.u, self.v = -self.v, self.u
        return self

    # rotates the vector according to an angle theta given in radians
    def rotate_rad(self, theta):
        rx = self.u * math.cos(theta) - self.v * math.sin(theta)
        ry = self.u * math.sin(theta) + self.v * math.cos(theta)
        self.u, self.v = rx, ry
        return self

    # rotates the vector according to an angle theta given in degrees
    def rotate(self, theta):
        theta_rad = theta / 180 * math.pi
        return self.rotate_rad(theta_rad)

    # project the vector onto a given vector
    def get_proj(self, vec):
        unit = vec.get_normalized()
        return unit.multiply(self.dot(unit))


# ball class
class Ball:
    def __init__(self, positionVector):
        self.positionVector = positionVector
        self.velocityVector = Vector(0, 0)
        self.radius = 50
        self.colour = "Blue"

    def draw(self, canvas):
        if not isinstance(self.positionVector, type(None)):
            canvas.draw_circle(self.positionVector.get_p(), self.radius, 1, self.colour, self.colour)

    def update(self, click):
        if click is not None:
            xCheck = False
            yCheck = False

            if not isinstance(self.positionVector, type(None)):
                xCheck = self.positionVector.u - self.radius - 1 <= click[0] <= self.positionVector.u + self.radius + 1
                yCheck = self.positionVector.v - self.radius - 1 <= click[1] <= self.positionVector.v + self.radius + 1

            if xCheck and yCheck:
                self.velocityVector.u = 0
                self.velocityVector.v = 0

            else:
                self.velocityVector.u = random.randint(-3, 3)
                self.velocityVector.v = random.randint(-3, 3)

        else:
            self.positionVector.add(self.velocityVector)


# mouse class
class Mouse:
    def __init__(self):
        self.lastClick = None

    def click_pos(self):
        last = self.lastClick
        self.lastClick = None

        return last

    def mouse_handler(self, position):
        self.lastClick = position


# interaction class
class Interaction:
    def __init__(self, ballObj, mouseObj):
        self.ballObj = ballObj
        self.mouseObj = mouseObj

    def draw(self, canvas):
        click = self.mouseObj.click_pos()
        self.ballObj.update(click)
        self.ballObj.draw(canvas)


def draw(canvas):
    interactionObj.draw(canvas)


WIDTH = 600
HEIGHT = 600

positionVector = Vector(WIDTH // 2, HEIGHT // 2)

ballObj = Ball(positionVector)
mouseObj = Mouse()
interactionObj = Interaction(ballObj, mouseObj)

frame = simplegui.create_frame("Click", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(mouseObj.mouse_handler)

frame.start()
