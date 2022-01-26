try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random


def randCol():
    r = random.randrange(0, 256)
    g = random.randrange(0, 256)
    b = random.randrange(0, 256)
    return 'rgb('+str(r) + ','+str(g) + ','+str(b) + ')'


# Drawing handler :
frameCount = 1


# this function is called 60 times per second
def draw(canvas):
    global frameCount
    if frameCount % 60 == 0:
        frame.set_canvas_background(randCol())
        frameCount = 1
    frameCount += 1


# Create a frame and assign the callback to the event handler
frame = simplegui.create_frame(" Colours ", 400, 200)
frame.set_draw_handler(draw)

# Start the frame animation
frame.start()
