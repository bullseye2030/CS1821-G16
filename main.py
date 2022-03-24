try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import math
import random
from vector import Vector
import map

# Canvas Dimensions
CANVAS_WIDTH = 768  # 48*16
CANVAS_HEIGHT = 576  # 48*12

frame_number = 0

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
                canvas.draw_image(self.start_image,  # image,
                                  (self.dims[0] / 2, self.dims[1] / 2),  # center_source,
                                  (self.dims[0], self.dims[1]),  # width_height_source,
                                  (self.dims[0] / 2, self.dims[1] / 2),  # center_dest,
                                  (self.dims[0], self.dims[1])  # width_height_dest
                                  )
            else:
                canvas.draw_image(self.end_image,  # image,
                                  (self.dims[0] / 2, self.dims[1] / 2),  # center_source,
                                  (self.dims[0], self.dims[1]),  # width_height_source,
                                  (self.dims[0] / 2, self.dims[1] / 2),  # center_dest,
                                  (self.dims[0], self.dims[1])  # width_height_dest
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
        self.cannon_angle_speed = 0.05
        self.tank_angle_speed = 0.08
        self.health = health  # Health value - default range 3-0 for player tank (2 and 1 for damaged, 0 for destroyed)
        self.fire_rate = fire_rate  # Fire rate - default 1 (fires once a second) - can do draw_number % (60/fire_rate)
        self.speed = speed  # Speed value - default 1
        self.destroyed = False
        self.sprites = self.get_sprites()
        self.dims = []
        self.frames_til_next_fire = 0
        for sprite in self.sprites:
            self.dims.append([sprite.get_width(), sprite.get_height()])

    # noinspection PyMethodMayBeStatic
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
        global frame_number
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
                if frame_number % 10 == 0:
                    self.sprites.remove(self.sprites[4])
                    self.dims.remove(self.dims[4])
            else:
                self.destroyed = True

    def damage(self):
        self.health -= 1
        if self.health <= 0:
            self.destroyed = True

    def limit_pos(self, obs_pos, obs_size):
        """
        limits position by checking if tanks velocity will carry it into the restricted region (hitbox)
        returns velocity as a vector
        :param obs_pos: Vector position of obstacle
        :param obs_size:   size of obstacle
        :return: Velocity as a vector
        """
        x_lower_lim = obs_pos.x - obs_size  # calculates the start of the hitbox region on the x axis
        x_upper_lim = obs_pos.x + obs_size  # calculates the end of the hitbox region on the x axis
        y_lower_lim = obs_pos.y - obs_size
        y_upper_lim = obs_pos.y + obs_size
        next_pos_x = self.pos.x + self.vel.x
        next_pos_y = self.pos.y + self.vel.y
        temp_vel_x = 0
        temp_vel_y = 0
        if next_pos_x > x_lower_lim and next_pos_x < x_upper_lim and next_pos_y > y_lower_lim and next_pos_y < y_upper_lim:
            return Vector(0, 0)
        else:
            return self.vel

    def collide(self, obstacle):
        self.vel = self.limit_pos(Vector(obstacle.obs_centre[0], obstacle.obs_centre[1]), obstacle.obs_dims[0])

    def update(self):
        self.cannon_angle = self.cannon_angle % 2 * math.pi  # keep the tank angle between 0 and 2pi
        self.tank_angle = self.tank_angle % 2 * math.pi  # keep the tank angle between 0 and 2pi
        self.pos.add(self.vel)
        self.move()
        # code for checking collisions
        for item in ITEMS:  # first check for collisions with tanks and projectiles
            item.check_collision(self)
        gamemap.check_collision(self)  # then check for collisions with walls and obstacles


class PlayerTank(Tank):
    def __init__(self, x, y, health, fire_rate, speed, keyboard):
        super().__init__(x, y, health, fire_rate, speed)
        self.keyboard = keyboard

    def move(self):
        """Method called on every update which checks user input and moves the tank accordingly"""
        if self.keyboard.d:
            self.tank_angle = self.tank_angle + self.tank_angle_speed
            self.cannon_angle = self.cannon_angle + self.tank_angle_speed
        if self.keyboard.a:
            self.tank_angle = self.tank_angle - self.tank_angle_speed
            self.cannon_angle = self.cannon_angle - self.tank_angle_speed
        if self.keyboard.w:
            new_vel = Vector(self.speed * 1.5, 0).rotate_rad(self.tank_angle + (math.pi / 2))
            self.vel.add(new_vel)  # add vector with magnitude speed in direction tank_angle
        if self.keyboard.s:
            new_vel = Vector(self.speed * 1.5, 0).rotate_rad(self.tank_angle + (math.pi / 2) + math.pi)
            self.vel.add(new_vel)  # add vector with magnitude speed in direction tank_angle + 180deg
        if not self.keyboard.d and not self.keyboard.a and not self.keyboard.w and not self.keyboard.s:
            self.vel = Vector(0, 0)
        if self.keyboard.q:
            self.cannon_angle += self.cannon_angle_speed
        if self.keyboard.e:
            self.cannon_angle -= self.cannon_angle_speed

        # set max speed
        if self.vel.length() > self.speed:
            self.vel = self.vel.normalize().multiply(self.speed * 1.5)
        if self.vel.length() < -self.speed:
            self.vel = self.vel.normalize().multiply(-self.speed * 1.5)

    def fire(self):
        global ITEMS
        if self.keyboard.space:
            if self.frames_til_next_fire == 0:
                spawn_point = self.pos.copy()
                spawn_point.add(Vector(self.dims[1][1] / 2, 0).rotate_rad(self.cannon_angle + (math.pi / 2)))
                proj_x, proj_y = spawn_point.get_p()
                proj_vel = Vector(3, 0).rotate_rad(self.cannon_angle + (math.pi / 2)) \
                    .add(Vector(self.vel.length(), 0).rotate_rad(self.cannon_angle + (math.pi / 2)))
                proj = Projectile(proj_x, proj_y, self, proj_vel)
                # noinspection PyTypeChecker
                ITEMS.append(proj)
                self.frames_til_next_fire = 120

    def update(self):
        self.pos.add(self.vel)
        if self.frames_til_next_fire > 0:
            self.frames_til_next_fire -= 1
        self.fire()
        self.move()
        # code for checking collisions
        for item in ITEMS:  # first check for collisions with tanks and projectiles
            if item == self:
                continue
            item.check_collision(self)
        gamemap.check_collision(self)  # then check for collisions with walls and obstacles


class EnemyTank(Tank):
    def __init__(self, x, y, health, fire_rate, speed):
        global difficulty
        super().__init__(x, y, health, fire_rate, speed)
        self.movement = ""
        self.frames_left_for_move = 0
        self.difficulty = difficulty
        self.sprites[0], self.sprites[2], self.sprites[3] = simplegui.load_image(
            "https://github.com/bullseye2030/CS1821-G16/blob/main/sprites/tantank.png?raw=true")
        self.sprites[1] = simplegui.load_image(
            "https://github.com/bullseye2030/CS1821-G16/blob/main/sprites/tanturret.png?raw=true")

    def make_move(self):
        """Method called on every update which randomly decides if and when the tank wants to move"""
        # Need to check for line of sight
        # if no line of sight, move cannon left or right for x frames, and then decide next move
        # if line of sight from cannon crosses tank, try to fire at the tank and keep tracking the tank
        # decide if the tank also wants to move, for how many frames, and in which direction
        line_of_sight = False

        # check line of sight here

        if not line_of_sight:
            if self.movement and self.frames_left_for_move > 0:
                if self.movement.find("rotate_cannon") != -1:
                    if self.movement == "rotate_cannon_left":
                        self.cannon_angle -= self.cannon_angle_speed
                    if self.movement == "rotate_cannon_right":
                        self.cannon_angle += self.cannon_angle_speed
                elif self.movement.find("move_tank") != -1:
                    if self.movement == "move_tank_right":
                        self.tank_angle = self.tank_angle + self.tank_angle_speed
                        self.cannon_angle = self.cannon_angle + self.tank_angle_speed
                    if self.movement == "move_tank_left":
                        self.tank_angle = self.tank_angle - self.tank_angle_speed
                        self.cannon_angle = self.cannon_angle - self.tank_angle_speed
                    if self.movement == "move_tank_forward":
                        new_vel = Vector(self.speed * 1.5, 0).rotate_rad(self.tank_angle + (math.pi / 2))
                        self.vel.add(new_vel)  # add vector with magnitude speed in direction tank_angle
                    if self.movement == "move_tank_backward":
                        new_vel = Vector(self.speed * 1.5, 0).rotate_rad(self.tank_angle + (math.pi / 2) + math.pi)
                        self.vel.add(new_vel)  # add vector with magnitude speed in direction tank_angle + 180deg
                    if self.frames_left_for_move == 1:  # stop on the last frame
                        self.vel = Vector(0, 0)
                    # set max speed
                    if self.vel.length() > self.speed:
                        self.vel = self.vel.normalize().multiply(self.speed * 1.5)
                    if self.vel.length() < -self.speed:
                        self.vel = self.vel.normalize().multiply(-self.speed * 1.5)
                elif self.movement == "do_nothing":
                    pass
                self.frames_left_for_move -= 1
            else:
                self.movement = ""
            if not self.movement:
                choice = random.randint(0, 12)  # 50% of the time - nothing happens for a x frames
                self.movement = {
                    0: "rotate_cannon_left",
                    1: "rotate_cannon_right",
                    2: "move_tank_right",
                    3: "move_tank_left",
                    4: "move_tank_forward",
                    5: "move_tank_backward",
                    **dict.fromkeys([6, 7, 8, 9, 10, 11], "do_nothing")  # 6 to 11 are "do_nothing"
                }.get(choice)
                self.frames_left_for_move = random.randint(30, 300)  # all moves run for 0.5 - 5 seconds
        else:
            # Stop movements
            self.frames_left_for_move = 0
            self.movement = ""
            # See if cannon is pointing at player (if cannon angle is correct)
            # if not:
            #   Move cannon towards player
            # else:
            #   if enemy can fire:
            #       Fire at player

    def update(self):
        self.make_move()

class Projectile:
    def __init__(self, x, y, tank, vel):
        self.tank = tank
        self.pos = Vector(x, y)
        self.vel = vel
        self.angle = self.tank.cannon_angle + math.pi
        self.bounces_left = 3
        self.sprite = simplegui.load_image(
            "https://github.com/bullseye2030/CS1821-G16/blob/main/sprites/projectile.png?raw=true")
        self.dims = (self.sprite.get_width(), self.sprite.get_height())

    def draw(self, canvas):
        canvas.draw_image(self.sprite,  # image,
                          (self.dims[0] / 2, self.dims[1] / 2),  # center_source,
                          (self.dims[0], self.dims[1]),  # width_height_source,
                          self.pos.get_p(),  # center_dest, (where it gets drawn on the canvas)
                          (self.dims[0], self.dims[1]),  # width_height_dest
                          self.angle  # rotation
                          )

    def collide(self, normal):  # if hitting a wall then bounce
        self.vel.reflect(normal)
        print(self.vel.angle(normal))
        if abs(self.vel.angle(normal)) > math.pi:
            self.vel = Vector(0, 0)
            print(self.vel.angle(normal))

    def hit(self, tank):  # if hitting a tank then damage it
        tank.damage()

    def update(self):
        self.pos.add(self.vel)
        # code for checking collisions
        for item in ITEMS:  # first check for collisions with tanks and projectiles
            item.check_collision(self)
        gamemap.check_collision(self)  # then check for collisions with walls and obstacles


def draw_handler(canvas):
    global frame_number
    frame_number += 1
    if frame_number > 600:
        frame_number = 1
    if menu.show or player.destroyed:
        menu.draw(canvas)
    else:
        gamemap.draw(canvas)
        for item in ITEMS:
            try:
                item.update()
                item.draw(canvas)
            except AttributeError as e:
                print(e)


def new_round():
    global round_number, difficulty
    enemies = []
    gamemap = map.create_gamemap()
    no_tanks_to_spawn = min(max(1, (round_number // 2)), 8)
    for i in range(no_tanks_to_spawn):
        # find a location that is valid to spawn
        x, y = 0, 0
        enemies.append(EnemyTank(x, y, 1, 1, 1))
    return gamemap, enemies


ITEMS = []

kbd = Keyboard()
gamemap, enemies = new_round()
menu = Menu(kbd)
player = PlayerTank(30, 30, 3, 1, 1, kbd)
for enemy in enemies:
    ITEMS.append(enemy)
ITEMS.append(player)

frame = simplegui.create_frame("Tanks", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_draw_handler(draw_handler)
frame.set_keydown_handler(kbd.key_down)
frame.set_keyup_handler(kbd.key_up)

# Start the frame animation
frame.start()
