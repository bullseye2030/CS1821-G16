try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


CANVAS_DIMS = (600, 600)
ITEMS = []
URL = "http://www.cs.rhul.ac.uk/courses/CS1830/sprites/runnerSheet.png"


class Spritesheet:
    def __init__(self, url, rows, columns):
        self.url = url
        self.rows = rows
        self.columns = columns
        self.spritesheet = simplegui.load_image(self.url)
        self.total_dims = (self.spritesheet.get_width(), self.spritesheet.get_height())
        self.sprite_dims = (self.total_dims[0]/self.columns, self.total_dims[1]/self.rows)
        self.frame_centre = (self.sprite_dims[0]/2, self.sprite_dims[1]/2)
        self.frame_index = [0,0]    #x,y
        print(self.sprite_dims)

    def draw(self, canvas):
        centre_source = (self.sprite_dims[0]*self.frame_index[0]+self.frame_centre[0],
                         self.sprite_dims[1]*self.frame_index[1]+self.frame_centre[1])
        canvas.draw_image(self.spritesheet, centre_source, self.sprite_dims,
                          (CANVAS_DIMS[0]/2, CANVAS_DIMS[1]/2), self.sprite_dims)
        print("here")
        self.next_frame()

    def next_frame(self):
        #print("here")
        self.frame_index[0] += 1
        if self.frame_index[0] >= self.columns:
            self.frame_index[0] %= self.columns     #reset frame index to zero
        self.frame_index[1] += 1
        if self.frame_index[1] >= self.rows:
            self.frame_index[1] %= self.rows


def draw(canvas):
    for item in ITEMS:
        item.draw(canvas)


sprite = Spritesheet(URL, 5, 6)
ITEMS.append(sprite)
frame = simplegui.create_frame("Milestone_4", CANVAS_DIMS[0], CANVAS_DIMS[1])
frame.set_draw_handler(draw)

frame.start()
