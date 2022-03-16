try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import math
from vector import Vector

# Canvas Dimensions
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 400

items = []


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
        self.space = False
        self.r = False

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
        if key == simplegui.KEY_MAP['r']:
            self.r = True
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
            self.a = True
        if key == simplegui.KEY_MAP['w']:
            self.w = False
        if key == simplegui.KEY_MAP['s']:
            self.s = False
        if key == simplegui.KEY_MAP['r']:
            self.r = False
        if key == simplegui.KEY_MAP['space']:
            self.space = False


class Tank:
    def __init__(self, x, y, health, fire_rate, speed, colour):
        self.pos = Vector(x, y)
        self.vel = Vector()
        self.cannon_angle = 0.0  # Default angle from normal - starts cannon pointing left
        self.tank_angle = 0.0  # Default angle from normal - starts tank pointing left
        self.health = health  # Health value - default range 0-100 for normal tanks, potential for 2x health for others
        self.fire_rate = fire_rate  # Fire rate - default 1 (fires once a second) - can do draw_number % (60/fire_rate)
        self.speed = speed  # Speed value - Vector - default 1
        self.colour = colour  # Colour - load different tank image for different colour
        self.sprites = self.get_sprites()
        self.dims = []
        for sprite in self.sprites:
            self.dims.append([sprite.get_width(), sprite.get_height()])

    def get_sprites(self):
        """Method to get the right sprites (correct colour) for the tank, return as a list (tank body and cannon)"""
        tank = simplegui.load_image("https://github.com/bullseye2030/CS1821-G16/blob/main/sprites/bluetank.png?raw=true")
        cannon = simplegui.load_image("https://github.com/bullseye2030/CS1821-G16/blob/main/sprites/blueturret.png?raw=true")
        return [tank, cannon]

    def draw(self, canvas):
        """Method to draw the tank on the canvas - tank body then cannon"""
        canvas.draw_image(self.sprites[0], (self.dims[0][0] / 2, self.dims[0][1] / 2),
                          self.dims[0], self.pos.get_p(),
                          (self.dims[0][0], self.dims[0][1]),
                          self.tank_angle)
        canvas.draw_image(self.sprites[1], (self.dims[1][0] / 2, self.dims[1][1] / 2),
                          self.dims[1], self.pos.get_p(),
                          (self.dims[1][0], self.dims[1][1]),
                          self.cannon_angle)


class PlayerTank(Tank):
    def __init__(self, x, y, health, fire_rate, speed, colour, keyboard):
        super().__init__(x, y, health, fire_rate, speed, colour)
        self.keyboard = keyboard

    def move(self):
        """Method called on every update which checks user input and moves the tank accordingly"""
        if self.keyboard.d:
            self.vel.add(Vector(self.speed/10, 0))
            self.tank_angle = 270*(math.pi/180)
        if self.keyboard.a:
            self.vel.add(Vector(-self.speed/10, 0))
            self.tank_angle = 90*(math.pi/180)
        if self.keyboard.w:
            self.vel.add(Vector(0, -self.speed/10))
            self.tank_angle = 180*(math.pi/180)
        if self.keyboard.s:
            self.vel.add(Vector(0, self.speed/10))
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
    def __init__(self, x, y, health, fire_rate, speed, colour, ammo_type, difficulty):
        super().__init__(x, y, health, fire_rate, speed, colour)
        self.ammo_type = ammo_type
        self.difficulty = difficulty

    def make_move(self):
        """Method called on every update which randomly decides if and when the tank wants to move"""
        pass


class Projectile:
    def __init__(self, x, y, speed, trail_colour, damage):
        self.pos = Vector(x, y)
        self.speed = speed
        self.trail_colour = trail_colour
        self.damage = damage
        self.sprites = self.get_sprites()

    def get_sprites(self):
        """Method called by constructor to get the correct sprites, return as a list (trail image and projectile)"""
        return []


class FastProjectile(Projectile):
    def __init__(self, x, y, speed, trail_colour, damage):
        super().__init__(x, y, speed, trail_colour, damage)


def draw_handler(canvas):
    for item in ITEMS:
        try:
            item.update()
            item.draw(canvas)
        except AttributeError:
            pass


ITEMS = []

kbd = Keyboard()
player = PlayerTank(30, 30, 100, 1, 1, "blue", kbd)
ITEMS.append(player)

frame = simplegui.create_frame("Tanks", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_draw_handler(draw_handler)
frame.set_keydown_handler(kbd.key_down)
frame.set_keyup_handler(kbd.key_up)

# Start the frame animation
frame.start()
