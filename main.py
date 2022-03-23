try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import math
import map
from vector import Vector

# Canvas Dimensions
CANVAS_WIDTH = 768  # 48*16
CANVAS_HEIGHT = 576  # 48*12

items = []
difficulty = 0
round_number = 0


class Menu:
    def __init__(self, keyboard):
        self.start_image = simplegui.load_image(
            "https://github.com/bullseye2030/CS1821-G16/blob/main/sprites/menu.png?raw=true")
        self.end_image = simplegui.load_image(
            "https://github.com/bullseye2030/CS1821-G16/blob/main/sprites/gameover.png?raw=true")
        self.dims = (self.start_image.get_width(), self.start_image.get_height())  # Same for menu and game over images
        self.keyboard = keyboard
        self.show = True

    def draw(self, canvas):
        global difficulty, player
        if self.show:
            if not player.destroyed:
                canvas.draw_image(self.start_image,                       # image,
                                  (self.dims[0] / 2, self.dims[1] / 2),   # center_source,
                                  (self.dims[0], self.dims[1]),           # width_height_source,
                                  (self.dims[0] / 2, self.dims[1] / 2),   # center_dest,
                                  (self.dims[0], self.dims[1])            # width_height_dest
                                  )
            else:
                canvas.draw_image(self.end_image,                         # image,
                                  (self.dims[0] / 2, self.dims[1] / 2),   # center_source,
                                  (self.dims[0], self.dims[1]),           # width_height_source,
                                  (self.dims[0] / 2, self.dims[1] / 2),   # center_dest,
                                  (self.dims[0], self.dims[1])            # width_height_dest
                                  )
                canvas.draw_text(str(round_number), (460, 312), 22, "white")
                if self.keyboard.space:
                    exit()
        if self.keyboard.one:
            difficulty = 1
            self.show = False
        if self.keyboard.two:
            difficulty = 2
            self.show = False
        if self.keyboard.three:
            difficulty = 3
            self.show = False


class Keyboard:
    """Keyboard input class to check for user input on every update"""

    def __init__(self):
        self.key_released = ""
        self.w = False
        self.a = False
        self.s = False
        self.d = False
        self.q = False
        self.e = False
        self.one = False
        self.two = False
        self.three = False
        self.space = False

    def key_down(self, key):
        if key == simplegui.KEY_MAP['q']:
            self.q = True
        if key == simplegui.KEY_MAP['e']:
            self.e = True
        if key == simplegui.KEY_MAP['d']:
            self.d = True
        if key == simplegui.KEY_MAP['a']:
            self.a = True
        if key == simplegui.KEY_MAP['w']:
            self.w = True
        if key == simplegui.KEY_MAP['s']:
            self.s = True
        if key == simplegui.KEY_MAP['1']:
            self.one = True
        if key == simplegui.KEY_MAP['2']:
            self.two = True
        if key == simplegui.KEY_MAP['3']:
            self.three = True
        if key == simplegui.KEY_MAP['space']:
            self.space = True

    def key_up(self, key):
        if key == simplegui.KEY_MAP['q']:
            self.q = False
        if key == simplegui.KEY_MAP['e']:
            self.e = False
        if key == simplegui.KEY_MAP['d']:
            self.d = False
        if key == simplegui.KEY_MAP['a']:
            self.a = False
        if key == simplegui.KEY_MAP['w']:
            self.w = False
        if key == simplegui.KEY_MAP['s']:
            self.s = False
        if key == simplegui.KEY_MAP['1']:
            self.one = False
        if key == simplegui.KEY_MAP['2']:
            self.two = False
        if key == simplegui.KEY_MAP['3']:
            self.three = False
        if key == simplegui.KEY_MAP['space']:
            self.space = False


class Tank:
    def __init__(self, x, y, health, fire_rate, speed):
        self.pos = Vector(x, y)
        self.vel = Vector()
        self.cannon_angle = 0.0  # Default angle from normal - starts cannon pointing left
        self.tank_angle = 0.0  # Default angle from normal - starts tank pointing left
        self.health = health  # Health value - default range 3-0 for player tank (2 and 1 for damaged, 0 for destroyed)
        self.fire_rate = fire_rate  # Fire rate - default 1 (fires once a second) - can do draw_number % (60/fire_rate)
        self.speed = speed  # Speed value - Vector - default 1
        self.destroyed = False
        self.sprites = self.get_sprites()
        self.dims = []
        self.frame_number = 0
        for sprite in self.sprites:
            self.dims.append([sprite.get_width(), sprite.get_height()])

    def get_sprites(self):
        """Method to get the right sprites (correct colour) for the tank, return as a list (tank body and cannon)"""
        tank = simplegui.load_image(
            "https://github.com/bullseye2030/CS1821-G16/blob/main/sprites/bluetank.png?raw=true")
        cannon = simplegui.load_image(
            "https://github.com/bullseye2030/CS1821-G16/blob/main/sprites/blueturret.png?raw=true")
        tankdamaged = simplegui.load_image(
            "https://github.com/bullseye2030/CS1821-G16/blob/main/sprites/bluetankdamaged.png?raw=true")
        tankdamaged2 = simplegui.load_image(
            "https://github.com/bullseye2030/CS1821-G16/blob/main/sprites/bluetankdamaged2.png?raw=true")
        exp1 = simplegui.load_image(
            "https://github.com/bullseye2030/CS1821-G16/blob/main/sprites/explosion2.png?raw=true")
        exp2 = simplegui.load_image(
            "https://github.com/bullseye2030/CS1821-G16/blob/main/sprites/explosion1.png?raw=true")
        exp3 = simplegui.load_image(
            "https://github.com/bullseye2030/CS1821-G16/blob/main/sprites/explosion3.png?raw=true")
        return [tank, cannon, tankdamaged, tankdamaged2, exp1, exp2, exp3]

    def draw(self, canvas):
        """Method to draw the tank on the canvas - tank body then cannon"""
        if not self.destroyed:
            if self.health == 3:
                canvas.draw_image(self.sprites[0], (self.dims[0][0] / 2, self.dims[0][1] / 2),
                                  self.dims[0], self.pos.get_p(),
                                  (self.dims[0][0], self.dims[0][1]),
                                  self.tank_angle)
            if self.health == 2:
                canvas.draw_image(self.sprites[2], (self.dims[2][0] / 2, self.dims[2][1] / 2),
                                  self.dims[2], self.pos.get_p(),
                                  (self.dims[2][0], self.dims[2][1]),
                                  self.tank_angle)
            if self.health == 1:
                canvas.draw_image(self.sprites[3], (self.dims[3][0] / 2, self.dims[3][1] / 2),
                                  self.dims[3], self.pos.get_p(),
                                  (self.dims[3][0], self.dims[3][1]),
                                  self.tank_angle)
            # Draw tank cannon
            canvas.draw_image(self.sprites[1], (self.dims[1][0] / 2, self.dims[1][1] / 2),
                              self.dims[1], self.pos.get_p(),
                              (self.dims[1][0], self.dims[1][1]),
                              self.cannon_angle)
        else:
            if len(self.sprites) > 4:
                canvas.draw_image(self.sprites[0], (self.dims[0][0] / 2, self.dims[0][1] / 2),
                                  self.dims[0], self.pos.get_p(),
                                  (self.dims[0][0], self.dims[0][1]),
                                  self.tank_angle)
                canvas.draw_image(self.sprites[1], (self.dims[1][0] / 2, self.dims[1][1] / 2),
                                  self.dims[1], self.pos.get_p(),
                                  (self.dims[1][0], self.dims[1][1]),
                                  self.cannon_angle)
                canvas.draw_image(self.sprites[4], (self.dims[4][0] / 2, self.dims[4][1] / 2),
                                  self.dims[4], self.pos.get_p(),
                                  (self.dims[4][0], self.dims[4][1]))
                if self.frame_number % 10 == 0:
                    self.sprites.remove(self.sprites[4])
                    self.dims.remove(self.dims[4])
                self.frame_number += 1
            else:
                self.destroyed = True


class PlayerTank(Tank):
    def __init__(self, x, y, health, fire_rate, speed, keyboard):
        super().__init__(x, y, health, fire_rate, speed)
        self.keyboard = keyboard

    def move(self):
        """Method called on every update which checks user input and moves the tank accordingly"""
        if self.keyboard.d:
            self.vel.add(Vector(self.speed / 10, 0))
            self.tank_angle = 270 * (math.pi / 180)
        if self.keyboard.a:
            self.vel.add(Vector(-self.speed / 10, 0))
            self.tank_angle = 90 * (math.pi / 180)
        if self.keyboard.w:
            self.vel.add(Vector(0, -self.speed / 10))
            self.tank_angle = 180 * (math.pi / 180)
        if self.keyboard.s:
            self.vel.add(Vector(0, self.speed / 10))
            self.tank_angle = 0
        if not self.keyboard.d and not self.keyboard.a and not self.keyboard.w and not self.keyboard.s:
            self.vel = Vector(0, 0)
        if self.keyboard.q:
            self.cannon_angle += 0.03
        if self.keyboard.e:
            self.cannon_angle -= 0.03

    def update(self):
        self.pos.add(self.vel)
        self.move()


class EnemyTank(Tank):
    def __init__(self, x, y, health, fire_rate, speed):
        global difficulty
        super().__init__(x, y, health, fire_rate, speed)
        self.difficulty = difficulty
        self.sprites[0] = simplegui.load_image(
            "https://github.com/bullseye2030/CS1821-G16/blob/main/sprites/tantank.png?raw=true")
        self.sprites[1] = simplegui.load_image(
            "https://github.com/bullseye2030/CS1821-G16/blob/main/sprites/tanturret.png?raw=true")

    def make_move(self):
        """Method called on every update which randomly decides if and when the tank wants to move"""
        pass


class Projectile:
    def __init__(self, x, y, speed):
        self.pos = Vector(x, y)
        self.vel = Vector()
        self.speed = speed
        self.bounces_left = 3
        self.sprites = self.get_sprites()

    def get_sprites(self):
        """Method called by constructor to get the correct sprites, return as a list (trail image and projectile)"""
        projectile = simplegui.load_image(
            "https://github.com/bullseye2030/CS1821-G16/blob/main/sprites/projectile.png?raw=true")
        return [projectile]

    def spawn(self, tank):
        """Spawn the projectile at the given tank"""
        pass


def draw_handler(canvas):
    if menu.show or player.destroyed:
        menu.draw(canvas)
    else:
        for item in ITEMS:
            try:
                item.update()
                item.draw(canvas)
            except AttributeError:
                pass


ITEMS = []

kbd = Keyboard()
menu = Menu(kbd)
player = PlayerTank(30, 30, 3, 1, 1, kbd)
map = map.create_map()


ITEMS.append(player)

frame = simplegui.create_frame("Tanks", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_draw_handler(draw_handler)
frame.set_keydown_handler(kbd.key_down)
frame.set_keyup_handler(kbd.key_up)

# Start the frame animation
frame.start()
