import random

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from vector import *


class Wall:
    def __init__(self, x, y, width, color, face):
        self.x = x
        self.y = y
        self.width = width * 2 + 1
        self.color = color
        self.face = face
        if self.face == 'l':
            self.normal = Vector(1, 0)
            self.edge = 0 + self.width
        elif self.face == 'r':
            self.edge = CANVAS_WIDTH - self.width
            self.normal = Vector(-1, 0)
        elif self.face == 't':
            self.normal = Vector(0, 1)
            self.edge = 0 + self.width
        elif self.face == 'b':
            self.normal = Vector(0, -1)
            self.edge = CANVAS_HEIGHT - self.width
        else:
            raise Exception("Invalid direction")

    def draw(self, canvas):
        start_xy = (0, 0)
        end_xy = (0, 0)
        if self.face == 'l':
            start_xy = (0, 0)
            end_xy = (0, CANVAS_HEIGHT)
        elif self.face == 'r':
            start_xy = (CANVAS_WIDTH, 0)
            end_xy = (CANVAS_WIDTH, CANVAS_HEIGHT)
        elif self.face == 't':
            start_xy = (0, 0)
            end_xy = (CANVAS_WIDTH, 0)
        elif self.face == 'b':
            start_xy = (0, CANVAS_HEIGHT)
            end_xy = (CANVAS_WIDTH, CANVAS_HEIGHT)
        canvas.draw_line(start_xy, end_xy, self.width, self.color)

    def hit(self, ball) -> bool:
        if self.face == 'l':
            hit = (ball.pos.x - ball.radius <= self.edge)
        elif self.face == "r":
            hit = (ball.pos.x + ball.radius >= self.edge)
        elif self.face == 't':
            hit = (ball.pos.y - ball.radius <= self.edge)
        elif self.face == "b":
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
    def __init__(self, wall_list, ball):
        self.ball = ball
        self.walls = wall_list

    def update(self):
        for wall in self.walls:
            if wall.hit(self.ball) and not self.ball.in_collision:
                self.ball.in_collision = True
                if self.ball.in_collision:
                    self.ball.bounce(wall.normal)
            if not wall.hit(self.ball) and self.ball.in_collision:
                self.ball.in_collision = False
            self.ball.update()

    def draw(self, canvas):
        self.update()
        self.ball.draw(canvas)
        for wall in self.walls:
            wall.draw(canvas)


# The canvas dimensions
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 400

# Initial position and velocity of the ball
p = Vector(80, 200)
v = Vector(-1, 1)

# Creating the objects
ball = Ball(p, v, 20, 20, 'blue')
l = Wall(0, 0, 5, 'red', 'l')
r = Wall(0, CANVAS_WIDTH, 5, 'red', 'r')
t = Wall(0, 0, 5, 'red', 't')
b = Wall(0, CANVAS_HEIGHT, 5, 'red', 'b')
walls = [l, r, t, b]
i = Interaction(walls, ball)


# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("ball-wall", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_draw_handler(i.draw)

# Start the frame animation
frame.start()
