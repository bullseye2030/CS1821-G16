try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vector import *


CANVAS_DIMS = (600, 600)
ITEMS = []
URL = "http://www.cs.rhul.ac.uk/courses/CS1830/sprites/explosion-spritesheet.png"


class Clock:
    def __init__(self):
        self.time = 0

    def tick(self):
        self.time += 1

    def transition(self, frame_duration):
        if self.time > frame_duration:
            self.time = 0
            return True
        return False


class Spritesheet:
    def __init__(self, url, columns, rows, num_frames, frame_duration, pos):
        self.url = url
        self.rows = rows
        self.columns = columns
        self.num_frames = num_frames
        self.speed = frame_duration #number of ticks before frame change
        self.pos = pos
        self.spritesheet = simplegui.load_image(self.url)
        self.total_dims = (self.spritesheet.get_width(), self.spritesheet.get_height())
        self.sprite_dims = (self.total_dims[0]/self.columns, self.total_dims[1]/self.rows)
        self.frame_centre = (self.sprite_dims[0]/2, self.sprite_dims[1]/2)
        self.frame_index = [0,0]    #x,y
        self.clock = Clock()
        self.current_frame = 0  #keep track of current frame

    def draw(self, canvas):
        centre_source = (self.sprite_dims[0]*self.frame_index[0]+self.frame_centre[0],
                         self.sprite_dims[1]*self.frame_index[1]+self.frame_centre[1])
        canvas.draw_image(self.spritesheet, centre_source, self.sprite_dims,
                          self.pos.get_p(), self.sprite_dims)
        if self.clock.transition(self.speed):
            self.next_frame()
        self.clock.tick()

    def next_frame(self):
        self.frame_index[0] += 1
        if self.frame_index[0] >= self.columns:
            self.frame_index[0] %= self.columns     #reset frame index to zero
        self.frame_index[1] += 1
        if self.frame_index[1] >= self.rows:
            self.frame_index[1] %= self.rows
        self.current_frame += 1
        if self.current_frame > self.num_frames:
            self.frame_index = [0,0]
            self.current_frame = 0

    def done(self):
        if self.current_frame == self.num_frames:
            return True
        else:
            return False

def draw(canvas):
    for item in ITEMS:
        item.draw(canvas)


explosion = Spritesheet(URL, 9, 9, 74, 3, Vector(CANVAS_DIMS[0]/2, CANVAS_DIMS[1]/2))
ITEMS.append(explosion)
frame = simplegui.create_frame("Milestone_4 Explosions", CANVAS_DIMS[0], CANVAS_DIMS[1])
frame.set_draw_handler(draw)

frame.start()