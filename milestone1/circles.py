from random import randint
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

frameCount = 0
colour1, colour2, colour3, colour4 = "", "", "", ""


def getRand():
    return str(hex(randint(0, 16777215))[2:])


def getColours():
    global colour1, colour2, colour3, colour4
    colour1 = "#{}".format(getRand())
    colour2 = "#{}".format(getRand())
    colour3 = "#{}".format(getRand())
    colour4 = "#{}".format(getRand())


def draw_handler(canvas):
    global frameCount, colour1, colour2, colour3, colour4
    if frameCount % 60 == 0:
        frameCount = 0
        getColours()
    frameCount += 1
    canvas.draw_circle((30, 50), 25, 5, colour1, colour2)
    canvas.draw_circle((70, 50), 25, 5, colour3, colour4)


# red one is on top because it is drawn after the green one is drawn
frame = simplegui.create_frame('Testing', 100, 100)
frame.set_draw_handler(draw_handler)
getColours()
frame.start()
