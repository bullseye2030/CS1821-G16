try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

WIDTH = 400
HEIGHT = 300
x = 1


def draw_handler(canvas):
    global x
    canvas.draw_line((1, 1), (WIDTH-1, HEIGHT-1), 10, 'Red')
    canvas.draw_line((WIDTH-1, 1), (1, HEIGHT-1), 10, 'Red')
    canvas.draw_line((x, 5), (x, 10), 1, 'Blue')
    x += 1
    if x > 60:
        x = x % WIDTH


frame = simplegui.create_frame('Testing', WIDTH, HEIGHT)
frame.set_draw_handler(draw_handler)
frame.start()
