try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from vector import *
import math

class Wall:
    def __init__(self, x, border, color, edge):
        self.x = x
        self.border = border
        self.color = color
        self.edge = edge
        if self.edge == 'l':
            self.normal = Vector(1, 0)
        elif self.edge == 'r':
            self.normal = Vector(-1, 0)
        elif self.edge == 'u':
            self.normal = Vector(0, 1)
        elif self.edge == 'd':
            self.normal = Vector(0, -1)
        else:
            raise Exception("Invalid direction")
        self.edge_r = x + self.border

    def draw(self, canvas):
        canvas.draw_line((self.x, 0),
                         (self.x, CANVAS_HEIGHT),
                         self.border*2+1,
                         self.color)

    def hit(self, ball) -> bool:
        if self.edge == 'r':
            h = (ball.offset_l() >= self.edge_r)
        else:
            h = (ball.offset_l() <= self.edge_r)
        return h

class Ball:
    def __init__(self, pos, vel, radius, border, color):
        self.pos = pos
        self.vel = vel
        self.radius = radius
        self.border = border
        self.color = color
        self.in_collision = False

    def offset_l(self):
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
p = Vector(0,200)
v = Vector(-1,0)

# Creating the objects
b = Ball(p, v, 20, 20, 'blue')
w = Wall(0, 5, 'red', 'l')
i = Interaction(w, b)

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("ball-wall", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_draw_handler(i.draw)

# Start the frame animation
frame.start()
