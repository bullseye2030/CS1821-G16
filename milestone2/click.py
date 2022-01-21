from tkinter import *
from turtle import update

root = Tk()
myCanvas = Canvas(root, width=400, height=400, background='white')


class Ball:
    x = None
    y = None
    r = 30
    v = 0

    def __init__(self, x, y):
        Ball.x = x
        Ball.y = y

    def create_circle(self, x, y, canvasName):  # center coordinates, radius
        x0 = x - Ball.r
        y0 = y - Ball.r
        x1 = x + Ball.r
        y1 = y + Ball.r
        return canvasName.create_oval(x0, y0, x1, y1, fill='yellow')


class Mouse:
    x = 0
    y = 0

    def mouseHandler(self, x, y):
        Mouse.x = x
        Mouse.y = y


class Interaction:
    ball = None
    mouse = None

    def __init__(self, ball, mouse):
        Interaction.ball = ball
        Interaction.mouse = mouse

    def update_txt(txt, x, y):
        myCanvas.create_text(
            x, y,
            fill="darkblue",
            font="Times 20 italic bold",
            text=txt, tags='velovity')

    def interact(self, event):
        myCanvas.delete('all')
        if mouse.x == 0 and mouse.y == 0:
            ball.create_circle(event.x, event.y, myCanvas)
            print("test")
            Ball.v = 0
            Interaction.update_txt("v:" + str(Ball.v), event.x, event.y)
            mouse.mouseHandler(event.x, event.y)
        else:
            x_good = event.x in range(mouse.x - ball.r, mouse.x + ball.r)
            y_good = event.y in range(mouse.y - ball.r, mouse.y + ball.r)
            ball.create_circle(mouse.x, mouse.y, myCanvas)
            if x_good == True and y_good == True:
                Ball.v = Ball.v + 1
                Interaction.update_txt("v:" + str(Ball.v), mouse.x, mouse.y)
            else:
                myCanvas.delete('all')
                Ball.v = 0
                mouse.mouseHandler(event.x, event.y)
                ball.create_circle(event.x, event.y, myCanvas)
                Interaction.update_txt("v:" + str(Ball.v), event.x, event.y)


ball = Ball(0, 0)
mouse = Mouse()
interaction = Interaction(mouse, ball)

# def get_cordinates(event):
# mouse.mouseHandler(event.x,event)

myCanvas.bind('<Button-1>', interaction.interact)
myCanvas.grid(row=0, column=0)
myCanvas.grid(row=1, column=0)
root.mainloop()