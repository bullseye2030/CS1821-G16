try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from vector import Vector

# Canvas Dimensions
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 400


class Keyboard:
    """Keyboard input class to check for user input on every update"""
    def __init__(self):
        self.w = False
        self.a = False
        self.s = False
        self.d = False
        self.left = False
        self.right = False
        self.space = False
        self.r = False

    def key_down(self, key):
        if key == simplegui.KEY_MAP['left']:
            self.left = True
        if key == simplegui.KEY_MAP['right']:
            self.right = True
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
        if key == simplegui.KEY_MAP['left']:
            self.left = False
        if key == simplegui.KEY_MAP['right']:
            self.right = False
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
        self.cannon_angle = 0.0  # Default angle from normal - starts cannon pointing left
        self.health = health  # Health value - default range 0-100 for normal tanks, potential for 2x health for others
        self.fire_rate = fire_rate  # Fire rate - default 1 (fires once a second) - can do draw_number % (60/fire_rate)
        self.speed = speed  # Speed value - Vector
        self.colour = colour  # Colour - load different tank image for different colour
        self.sprites = self.get_sprites()

    def get_sprites(self):
        """Method to get the right sprites (correct colour) for the tank, return as a list (tank body and cannon)"""
        return []


class PlayerTank(Tank):
    def __init__(self, x, y, health, fire_rate, speed, colour):
        super().__init__(x, y, health, fire_rate, speed, colour)

    def move(self):
        """Method called on every update which checks user input and moves the tank accordingly"""
        pass


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
    pass


frame = simplegui.create_frame("Tanks", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_draw_handler(draw_handler)

# Start the frame animation
frame.start()
