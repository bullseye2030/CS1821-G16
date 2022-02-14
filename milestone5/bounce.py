try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from vector import *


class Wall:
    def __init__(self, x, y, width, color, face):
        self.x = x
        self.y = y
        self.width = width
        self.color = color
        self.face = face
        if self.face == 'l':
            self.normal = Vector(1, 0)
            self.edge = x - self.width
        elif self.face == 'r':
            self.edge = x + self.width
            self.normal = Vector(-1, 0)
        elif self.face == 'u':
            self.normal = Vector(0, 1)
            self.edge = y - self.width
        elif self.face == 'd':
            self.normal = Vector(0, -1)
            self.edge = y + self.width
        else:
            raise Exception("Invalid direction")

    def draw(self, canvas):
        canvas.draw_line((self.x, 0),
                         (self.x, CANVAS_HEIGHT),
                         self.width * 2 + 1,
                         self.color)

    def hit(self, ball) -> bool:
        if self.face == 'l':
            hit = (ball.pos.x - ball.radius <= self.edge)
        elif self.face == "r":
            hit = (ball.pos.x + ball.radius >= self.edge)
        elif self.face == 'u':
            hit = (ball.pos.y - ball.radius <= self.edge)
        elif self.face == "d":
            hit = (ball.pos.y + ball.radius >= self.edge)
        else:
            raise Exception("Invalid direction")
        return hit


class Ball:
    def __init__(self, pos, vel, radius, border, color):
        self.pos = pos
        self.vel = vel
        self.radius = radius
        self.border = border
        self.color = color
        self.in_collision = False

    def offset(self):
        return self.pos.x - self.radius

    def update(self):
        self.pos.add(self.vel)

    def draw(self, canvas):
        canvas.draw_circle(self.pos.get_p(),
                           self.radius,
                           self.border,
                           self.color,
                           self.color)

    def bounce(self, normal):
        self.vel.reflect(normal)


class Interaction:
    def __init__(self, wall, ball):
        self.ball = ball
        self.wall = wall

    def update(self):
        if self.wall.hit(self.ball):
            if self.ball.in_collision:
                self.ball.bounce(self.wall.normal)
                self.ball.in_collision = True
            else:
                self.ball.in_collision = False
        self.ball.update()

    def draw(self, canvas):
        self.update()
        self.ball.draw(canvas)
        self.wall.draw(canvas)


# The canvas dimensions
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 400

# Initial position and velocity of the ball
p = Vector(0, 200)
v = Vector(-1, 0)

# Creating the objects
b = Ball(p, v, 20, 20, 'blue')
w = Wall(0, 0, 5, 'red', 'l')
i = Interaction(w, b)

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("ball-wall", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_draw_handler(i.draw)

# Start the frame animation
frame.start()
