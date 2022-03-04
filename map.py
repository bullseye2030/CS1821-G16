try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from vector import *
from random import randint

CANVAS_HEIGHT = 600
CANVAS_WIDTH = 600
BACKGROUND = 'gray'
BORDER_COLOUR = 'black'
BORDER_THICKNESS = 15

EMPTY_GRID = [[], []]

ITEMS = []  #items to be drawn

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


def create_map(rows,columns): #return array of 0's to represent map
    temp = [[0 for row in range(rows+1)] for x in range(columns+1)]
    return temp


class Map:

    def __init__(self, items, rows, columns, obstacle_rate, debug = False):
        self.items = items
        self.rows = rows
        self.columns = columns
        self.heat_map = [[], []]    #2d array of 1's and 0's
        self.grid = [[], []] #2d array of grid coordinates
        self.obstacle_rate = obstacle_rate
        self.debug = debug #if true then lines will be drawn to show the grid


    def draw(self, canvas): #callback function to draw entire map, called in update function
        for item in self.items:
            item.draw(canvas)

    def build_corner(self, gamemap):
        for y in range(self.rows):  # y because go down columns first then pick a row number
            for x in range(self.columns):
                if gamemap[y][x] != 0:  #check if map already has an obstacle there; if it is 1 then ignore
                    #do checks here

                    gamemap[y][x] = 1  #change gamemap after everything else is done


    def generate_heat_map(self):    #return 2d array of numbers
        temp_map = create_map(self.rows, self.columns)
        for y in range(self.rows):  #y because go down columns first then pick a row number
            for x in range(self.columns):
                if randint(1, self.obstacle_rate) == 1:     #a 1/obstacle rate chance of creating an obstacles
                    obstacle = randint(1, 4)
                    if obstacle == 1:
                        build_corner(temp_map)
                    elif obstacle == 2:
                        build_block(temp_map)
                    elif obstacle == 3:
                        build_line(temp_map)
                    elif obstacle == 4:
                        build_plus(temp_map)


l = Wall(0, 0, BORDER_THICKNESS, BORDER_COLOUR, 'l')
r = Wall(0, CANVAS_WIDTH, BORDER_THICKNESS, BORDER_COLOUR, 'r')
t = Wall(0, 0, BORDER_THICKNESS, BORDER_COLOUR, 't')
b = Wall(0, CANVAS_HEIGHT, BORDER_THICKNESS, BORDER_COLOUR, 'b')
ITEMS = [l, r, t, b]


gamemap = Map(ITEMS)

frame = simplegui.create_frame("TANKS!", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_draw_handler(gamemap.draw)

frame.set_canvas_background(BACKGROUND)

frame.start()