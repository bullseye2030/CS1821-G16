try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

CANVAS_HEIGHT = 600
CANVAS_WIDTH = 600
BACKGROUND = 'gray'
BORDER_COLOUR = 'black'

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

    def generate_map(self):
        return 1 #return complete map from array of numbers


def draw(canvas): #callback function to draw entire map, called in update function
    return 1

frame = simplegui.create_frame("TANKS!", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_draw_handler(draw)

frame.set_canvas_background(BACKGROUND)

frame.start()