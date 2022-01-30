from random import randint
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

frameCount = 0
radius = 50
shrinking = True


def draw_handler(canvas):
    global frameCount, radius, shrinking
    if radius == 10:
        shrinking = False
    elif radius == 50:
        shrinking = True
    if shrinking:
        radius -= 1
    else:
        radius += 1
    frameCount += 1
    canvas.draw_circle((50, 50), radius, 1, "Red", "Red")


# red one is on top because it is drawn after the green one is drawn
frame = simplegui.create_frame('Testing', 100, 100)
frame.set_draw_handler(draw_handler)
frame.start()
