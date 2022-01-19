try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import random
import vector

#constants
WIDTH = 200
HEIGHT = 200

#global variables
draw_objs = []  #list of items to animate
timer = 1   #acts as a timer for animation

def randCol():
    r = random.randrange(0, 256)
    g = random.randrange(0, 256)
    b = random.randrange(0, 256)
    return 'rgb(' + str(r) + ',' + str(g) + ',' + str(b) + ')'


def createBall():
    pos = vector.Vector(WIDTH // 2, HEIGHT // 2)  # position is centre of the screen
    velo = vector.Vector(random.randint(-5, 5), random.randint(-5, 5))  # initialise velocity to random
    radius = random.randint(10,50)
    colour = randCol()
    ball = Ball(pos,velo, radius, colour)
    return ball

class Ball:
    def __init__(self, pos, velo, radius, colour):
        self.pos = pos
        self.velo = velo
        self.radius = radius
        self.colour = colour

    def draw(self, canvas):
        canvas.draw_circle(self.pos.get_p(), self.radius, 3, self.colour)

    def update(self):
        self.pos.add(self.velo)
        self.radius = self.radius - 1 if self.radius > 1 else self.radius   #decrement radius if its positive


def draw(canvas):
    global draw_objs
    global timer
    if timer % 6 == 0:      #every 1/10 of a second...
        new_ball = createBall()     #create a new ball
        draw_objs.append(new_ball)      #and add it to the list of items to be animated

    if timer > 60 == 0:         #if the timer is at 61 then a second has passed
        timer = 1           #so reset the timer

    for item in draw_objs:  # list of items to animate
        try:  # wrap in try block just in case any item doesn't have either function
            item.draw(canvas)
            item.update()
        except:  # continue to next item if either method failed
            pass
    timer += 1      #increment the timer

frame = simplegui.create_frame("Points", WIDTH, HEIGHT)
frame.set_draw_handler(draw)

# Start the frame animation
frame.start()
