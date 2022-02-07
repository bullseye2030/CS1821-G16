from user304_rsf8mD0BOQ_1 import Vector
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

WIDTH = 500
HEIGHT = 500
                
class Wheel:
    def __init__(self, pos, radius=10):
        self.pos = pos
        self.vel = Vector()
        self.radius = max(radius, 10)
        self.colour = 'White'

    def draw(self, canvas):
        canvas.draw_circle(self.pos.get_p(), self.radius, 1, self.colour, self.colour)
        
    def update(self):
        self.pos.add(self.vel)
        self.vel.multiply(0.85)
    
class Keyboard:
    def __init__(self): 
        self.right = False
        self.left = False
        self.up = False 
        self.down = False 

    def keyDown(self, key): #When the key is pressed it shows it by saying 'down' 
        if key == simplegui.KEY_MAP['right']:
            self.right = True
        if key == simplegui.KEY_MAP['left']:
            self.left = True 
        if key == simplegui.KEY_MAP['up']:
            self.up = True 
        if key == simplegui.KEY_MAP['down']:
            self.down = True 

    def keyUp(self, key): #This is so that when the key is not pressed it shows 'up' to show that it is not pressed. 
        if key == simplegui.KEY_MAP['right']:
            self.right = False
        if key == simplegui.KEY_MAP['left']:
            self.left = False 
        if key == simplegui.KEY_MAP['up']:
            self.up = False 
        if key == simplegui.KEY_MAP['down']:
            self.down = False 

class Interaction:
    def __init__(self, wheel, keyboard):
        self.wheel = wheel
        self.keyboard = keyboard

    def update(self):
        if self.keyboard.right:
            self.wheel.vel.add(Vector(1, 0))
        if self.keyboard.left:
            self.wheel.vel.add(Vector(-1, 0)) #This is to for the direction of the ball to go on. 
        if self.keyboard.up:
            self.wheel.vel.add(Vector(0, -1))
        if self.keyboard.down:
            self.wheel.vel.add(Vector(0, 1))

kbd = Keyboard()
wheel = Wheel(Vector(WIDTH/2, HEIGHT-40), 40)
inter = Interaction(wheel, kbd)

def draw(canvas):
    inter.update()
    wheel.update()
    wheel.draw(canvas)

frame = simplegui.create_frame('Interactions', WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)
frame.start()
