try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from vector import *

# Some constants
CANVAS_DIMS = (600, 400)

IMG = simplegui.load_image('http://www.cs.rhul.ac.uk/courses/CS1830/sprites/coach_wheel-512.png')

STEP = 0.05


class Keyboard:
    def __init__(self):
        self.left = False
        self.right = False

    def keyDown(self, key):
        if key == simplegui.KEY_MAP['left']:
            self.left = True
        elif key == simplegui.KEY_MAP['right']:
            self.right = True

    def keyUp(self, key):
        if key == simplegui.KEY_MAP['left']:
            self.left = False
        elif key == simplegui.KEY_MAP['right']:
            self.right = False


class Interaction:
    def __init__(self, wheel, keyboard):
        self.wheel = wheel
        self.keyboard = keyboard

    def update(self):
        if self.keyboard.right:
            self.wheel.vel.add(Vector(1, 0))
        if self.keyboard.left:
            self.wheel.vel.add(Vector(-1, 0))


class Wheel:
    def __init__(self, img, pos, radius = 0.1):
        self.pos = pos
        self.vel = Vector()
        self.img = img
        self.dims = (img.get_width(), img.get_height())
        self.radius = radius

    def draw(self, canvas):
        canvas.draw_image(self.img, (self.dims[0]/2, self.dims[1]/2),
                          self.dims, self.pos.get_p(),
                          (self.dims[0]*self.radius, self.dims[1]*self.radius))

    def update(self):
        self.pos.add(self.vel)


kbd = Keyboard()
wheel = Wheel(IMG, Vector(CANVAS_DIMS[0]/2, CANVAS_DIMS[1]/2)) ##
inter = Interaction(wheel, kbd)

ITEMS = [wheel, inter]


# Drawing handler
def draw(canvas):
    for item in ITEMS:
        try:
            item.update()
            item.draw(canvas)
        except AttributeError:
            pass


# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Milestone_3", CANVAS_DIMS[0], CANVAS_DIMS[1])
frame.set_canvas_background('#2C6A6A')
frame.set_draw_handler(draw)
frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)

# Start the frame animation
frame.start()

