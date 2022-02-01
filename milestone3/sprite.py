try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from milestone2.vector import *

# Some constants
CANVAS_DIMS = (600, 400)
IMG = simplegui.load_image('http://www.cs.rhul.ac.uk/courses/CS1830/sprites/coach_wheel-512.png')
PI = 3.14
MAX_HEIGHT = 1.0

class Keyboard:
    def __init__(self):
        self.left = False
        self.right = False
        self.space = False

    def keyDown(self, key):
        if key == simplegui.KEY_MAP['left']:
            self.left = True
        elif key == simplegui.KEY_MAP['right']:
            self.right = True
        elif key == simplegui.KEY_MAP['space']:
            self.space = False

    def keyUp(self, key):
        if key == simplegui.KEY_MAP['left']:
            self.left = False
        elif key == simplegui.KEY_MAP['right']:
            self.right = False
        elif key == simplegui.KEY_MAP['space']:
            self.space = False


class Interaction:
    def __init__(self, wheel, keyboard):
        self.wheel = wheel
        self.keyboard = keyboard

    def update(self):
        global MAX_HEIGHT
        if self.keyboard.right:
            self.wheel.vel.add(Vector(1, 0))
        if self.keyboard.left:
            self.wheel.vel.add(Vector(-1, 0))
        if self.keyboard.space:
            self.wheel.vel.add(Vector(0, MAX_HEIGHT))
            if MAX_HEIGHT > 0:
                MAX_HEIGHT -= 0.1
        if not self.keyboard.space:
            MAX_HEIGHT = 1.0

class Wheel:
    def __init__(self, img, pos, radius = 0.1):
        self.pos = pos
        self.vel = Vector()
        self.img = img
        self.dims = (img.get_width(), img.get_height())
        self.radius = radius
        self.rot = 0    #rotation
        self.ang_velo = 0   #angular velocity

    def draw(self, canvas):
        canvas.draw_image(self.img, (self.dims[0]/2, self.dims[1]/2),
                          self.dims, self.pos.get_p(),
                          (self.dims[0]*self.radius, self.dims[1]*self.radius),
                          self.rot)

    def update(self):
        self.pos.add(self.vel)
        self.ang_velo = (self.vel.get_p()[0] * self.radius) / PI
        self.rot += self.ang_velo

kbd = Keyboard()
wheel = Wheel(IMG, Vector(CANVAS_DIMS[0]/2, CANVAS_DIMS[1]/2))
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

