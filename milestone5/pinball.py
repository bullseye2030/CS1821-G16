try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from vector import *
import math
from random import randint

# The canvas dimensions
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 400


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
    def __init__(self, pos, vel, radius, border, color, isStationary = False):
        self.pos = pos
        self.vel = vel
        self.radius = radius
        self.border = border
        self.color = color
        self.isStationary = isStationary
        if isStationary:
            self.vel = Vector(0,0)
        self.in_collision = False

    def offset_l(self):
        return self.pos.x - self.radius

    def update(self):
        if not self.isStationary:
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
    def __init__(self, items, walls):
        self.items = items
        self.walls = walls

    def collide(self, ball1, ball2):
        normal = ball1.pos.copy().subtract(ball2.pos).normalize()

        v1_x = ball1.vel.get_proj(normal)   #calculate velocity of ball 1 in x axis
        v1_y = ball1.vel.copy().subtract(v1_x)  #calculate velocity of ball 1 in y axis

        v2_x = ball2.vel.get_proj(normal)   #calculate velocity of ball 2 in x axis
        v2_y = ball2.vel.copy().subtract(v2_x)  #calculate velocity of ball 2 in y axis

        ball1.vel = v2_x + v1_y     #calculate new velocities
        ball2.vel = v1_x + v2_y

        print("here")

    def update(self):
        for item in self.items: #for each ball
            for sub_item in self.items: #check if every other ball is colliding
                if item == sub_item:    #if it is the same ball
                    continue
                dist = item.pos.copy().subtract(sub_item.pos).length()
                if dist <= item.radius + sub_item.radius and not item.in_collision:
                    if item.isStationary:
                        normal = item.pos.copy().subtract(sub_item.pos).normalize()
                        sub_item.bounce(normal)
                    self.collide(item, sub_item)
                    item.in_collision = True
                if not dist <= item.radius + sub_item.radius and item.in_collision:
                    item.in_collision = False
            item.update()
            for wall in self.walls:
                if wall.hit(item) and not item.in_collision:
                    item.in_collision = True
                    if item.in_collision:
                        item.bounce(wall.normal)
                if not wall.hit(item) and item.in_collision:
                    item.in_collision = False


    def draw(self, canvas):
        self.update()
        for item in self.items:
            item.draw(canvas)
        for wall in self.walls:
            wall.draw(canvas)

ITEMS = []

for x in range(15):
    new_pos = Vector(randint(20, CANVAS_WIDTH), randint(20, CANVAS_HEIGHT))
    new_vel = Vector(0,0)
    new_radius = randint(5, 20)
    new_pinball = Ball(new_pos, new_vel, new_radius, 5, 'Blue', True)
    ITEMS.append(new_pinball)


#create new ball
for i in range(5):
    new_pos = Vector(randint(11, CANVAS_WIDTH-11), randint(11, CANVAS_HEIGHT-11))
    new_vel = Vector(randint(0, 10), randint(0, 10))
    new_radius = randint(3, 8)
    for item in ITEMS:
        # check if the pinballs will spawn inside the balls
        pass
    new_ball = Ball(new_pos, new_vel, new_radius, 5, 'Green', False)
    ITEMS.append(new_ball)


l = Wall(0, 0, 5, 'red', 'l')
r = Wall(0, CANVAS_WIDTH, 5, 'red', 'r')
t = Wall(0, 0, 5, 'red', 't')
b = Wall(0, CANVAS_HEIGHT, 5, 'red', 'b')
walls = [l, r, t, b]

i = Interaction(ITEMS, walls)

frame = simplegui.create_frame("pinball", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_draw_handler(i.draw)

# Start the frame animation
frame.start()