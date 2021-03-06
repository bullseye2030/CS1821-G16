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
wait_frames = 60 * 3  # used for waiting at the start of a round

difficulty = 0
round_number = 0
enemies_left_this_round = 0
lives = 3


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
    def __init__(self, x, y, health, fire_rate, speed, radius=10):
        self.pos = Vector(x, y)
        self.vel = Vector()
        self.cannon_angle = 0.0  # Default angle from normal - starts cannon pointing left
        self.tank_angle = 0.0  # Default angle from normal - starts tank pointing left
        self.cannon_angle_speed = 0.05
        self.tank_angle_speed = 0.08
        self.health = health  # Health value - default range 3-0 for player tank (2 and 1 for damaged, 0 for destroyed)
        self.fire_rate = fire_rate  # Fire rate - default 1 (fires once a second) - can do draw_number % (60/fire_rate)
        self.speed = speed  # Speed value - default 1
        self.radius = radius
        self.destroyed = False
        self.in_collision = False
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
        limits position by checking if tanks velocity will carry it into the restricted region (hit box)
        returns velocity as a vector
        :param obs_pos: Vector position of obstacle
        :param obs_size:   size of obstacle
        :return: Velocity as a vector
        """
        x_lower_lim = obs_pos.x - obs_size  # calculates the start of the hit box region on the x axis
        x_upper_lim = obs_pos.x + obs_size  # calculates the end of the hit box region on the x axis
        y_lower_lim = obs_pos.y - obs_size
        y_upper_lim = obs_pos.y + obs_size
        next_pos_x = self.pos.x + self.vel.x
        next_pos_y = self.pos.y + self.vel.y
        if x_lower_lim < next_pos_x < x_upper_lim and y_lower_lim < next_pos_y < y_upper_lim:
            return Vector(0, 0)
        else:
            return self.vel

    def collide_obstacle(self, obstacle):
        self.vel = self.limit_pos(Vector(obstacle.obs_centre[0], obstacle.obs_centre[1]), obstacle.obs_dims[0])

    # noinspection PyMethodMayBeStatic
    def limit_input(self, minimum, maximum, num):
        if num < minimum:
            return minimum
        elif num > maximum:
            return maximum
        else:
            return num

    def collide_wall(self, wall):
        wall_size = wall.width / 2 + 1
        self.pos.x = self.limit_input(wall_size, CANVAS_WIDTH - wall_size, self.pos.x)
        self.pos.y = self.limit_input(wall_size, CANVAS_HEIGHT - wall_size, self.pos.y)

    def collide_projectile(self, projectile):
        self.damage()
        projectile.destroy()

    def check_collision(self, item):
        """
        function to check for collision with tanks and projectiles
        :param item:
        :return:
        """
        if item == self or not type(item) == Tank:
            return
        if item.pos.copy().subtract(self.pos).length() < self.radius:
            item.collide(self)

    def update(self):
        self.cannon_angle = self.cannon_angle % 2 * math.pi  # keep the tank angle between 0 and 2pi
        self.tank_angle = self.tank_angle % 2 * math.pi  # keep the tank angle between 0 and 2pi
        self.pos.add(self.vel)
        # code for checking collisions
        for item in ITEMS:  # first check for collisions with tanks and projectiles
            item.check_collision(self)
        game_map.check_collision(self)  # then check for collisions with walls and obstacles


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
                self.frames_til_next_fire = 120 * self.fire_rate

    def damage(self):  # reduce global lives by 1 as well as Tank's lives
        global lives
        lives -= 1
        super()

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
        game_map.check_collision(self)  # then check for collisions with walls and obstacles


def is_counter_clockwise(a, b, c):
    return (c.y - a.y) * (b.x - a.x) > (b.y - a.y) * (c.x - a.x)


# Return true if line segments AB and CD intersect
def intersect(a, b, c, d):
    return is_counter_clockwise(a, c, d) != is_counter_clockwise(b, c, d) and is_counter_clockwise(a, b,
                                                                                                   c) != is_counter_clockwise(
        a, b, d)


def calculate_lines(obs_centre, obs_size):
    top = Vector(obs_centre[0] - obs_size, obs_centre[1] - obs_size)
    right = Vector(obs_centre[0] + obs_size, obs_centre[1] - obs_size)
    bottom = Vector(obs_centre[0] + obs_size, obs_centre[1] + obs_size)
    left = Vector(obs_centre[0] - obs_size, obs_centre[1] + obs_size)
    return [(top, right), (right, bottom), (bottom, left), (left, top)]


class EnemyTank(Tank):
    def __init__(self, x, y, health, fire_rate, speed):
        global difficulty
        super().__init__(x, y, health, fire_rate, speed)
        self.movement = ""
        self.frames_left_for_move = 0
        self.difficulty = difficulty
        self.sprites[0] = self.sprites[2] = self.sprites[3] = simplegui.load_image(
            "https://github.com/bullseye2030/CS1821-G16/blob/main/sprites/tantank.png?raw=true")
        self.sprites[1] = simplegui.load_image(
            "https://github.com/bullseye2030/CS1821-G16/blob/main/sprites/tanturret.png?raw=true")

    def make_move(self):
        """Method called on every update which randomly decides if and when the tank wants to move"""
        # Need to check for line of sight
        # if no line of sight, move cannon left or right for x frames, and then decide next move
        # if line of sight from cannon crosses tank, try to fire at the tank and keep tracking the tank
        # decide if the tank also wants to move, for how many frames, and in which direction
        line_of_sight = True

        # check line of sight here
        for obstacle in game_map.obstacles:
            box_lines = calculate_lines(obstacle.obs_centre, obstacle.obs_dims[0])
            for line in box_lines:
                if intersect(line[0], line[1], self.pos, player.pos):
                    line_of_sight = False
                    print("No LOS")
                    break

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
                self.frames_left_for_move = random.randint(30, 120)  # all moves run for 0.5 - 2 seconds
        else:
            # Stop movements
            self.frames_left_for_move = 0
            self.movement = ""
            # See if cannon is pointing at player (if cannon angle is correct)
            angle_to_player = 0
            # If angle isn't correct, step towards the right angle for this frame
            if self.cannon_angle != angle_to_player:
                if angle_to_player > self.cannon_angle:
                    self.cannon_angle += 0.04
                if angle_to_player < self.cannon_angle:
                    self.cannon_angle -= 0.04
                # If the difference between the two is less than the standard step
                if -0.04 < self.cannon_angle - angle_to_player < 0.04:
                    self.cannon_angle = angle_to_player
            else:
                if self.frames_til_next_fire == 0:
                    spawn_point = self.pos.copy()
                    spawn_point.add(Vector(self.dims[1][1] / 2, 0).rotate_rad(self.cannon_angle + (math.pi / 2)))
                    proj_x, proj_y = spawn_point.get_p()
                    proj_vel = Vector(3, 0).rotate_rad(self.cannon_angle + (math.pi / 2)) \
                        .add(Vector(self.vel.length(), 0).rotate_rad(self.cannon_angle + (math.pi / 2)))
                    proj = Projectile(proj_x, proj_y, self, proj_vel)
                    # noinspection PyTypeChecker
                    ITEMS.append(proj)
                    self.frames_til_next_fire = 120 * self.fire_rate

    def update(self):
        global ITEMS, enemies_left_this_round
        self.make_move()
        for item in ITEMS:  # first check for collisions with tanks and projectiles
            if item == self:
                continue
            item.check_collision(self)
        game_map.check_collision(self)  # then check for collisions with walls and obstacles
        if self.destroyed:
            enemies_left_this_round -= 1
            ITEMS.remove(self)
            del self


class Projectile:
    def __init__(self, x, y, tank, vel, radius=2):
        self.tank = tank
        self.pos = Vector(x, y)
        self.vel = vel
        self.old_vel = Vector()
        self.radius = radius
        self.angle = self.tank.cannon_angle + math.pi
        self.bounces_left = 5
        self.sprite = simplegui.load_image(
            "https://github.com/bullseye2030/CS1821-G16/blob/main/sprites/projectile.png?raw=true")
        self.dims = (self.sprite.get_width(), self.sprite.get_height())
        self.in_collision = False

    def draw(self, canvas):
        canvas.draw_image(self.sprite,  # image,
                          (self.dims[0] / 2, self.dims[1] / 2),  # center_source,
                          (self.dims[0], self.dims[1]),  # width_height_source,
                          self.pos.get_p(),  # center_dest, (where it gets drawn on the canvas)
                          (self.dims[0], self.dims[1]),  # width_height_dest
                          self.angle  # rotation
                          )

    def collide_wall(self, wall):  # if hitting a wall then bounce
        self.bounces_left -= 1
        normal = wall.normal
        self.old_vel = self.vel.copy()
        self.vel.reflect(normal)
        if abs(self.vel.angle(normal)) > math.pi:
            self.vel = Vector(0, 0)
        self.angle = self.angle - self.vel.angle(self.old_vel)

    def exclude_input(self, start_range, end_range, input_num):
        if input_num > start_range:
            return start_range
        elif input_num < end_range:
            return end_range
        else:
            return input_num

    def check_vel(self, obs_pos, obs_size):
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
        if x_lower_lim < next_pos_x < x_upper_lim and y_lower_lim < next_pos_y < y_upper_lim:
            return False
        else:
            return True

    def collide(self, ball1, ball2):
        normal = ball1.pos.copy().subtract(ball2.pos).normalize()

        v1_x = ball1.vel.get_proj(normal)  # calculate velocity of ball 1 in x axis
        v1_y = ball1.vel.copy().subtract(v1_x)  # calculate velocity of ball 1 in y axis

        v2_x = ball2.vel.get_proj(normal)  # calculate velocity of ball 2 in x axis
        v2_y = ball2.vel.copy().subtract(v2_x)  # calculate velocity of ball 2 in y axis

        ball1.vel = v2_x + v1_y  # calculate new velocities
        ball2.vel = v1_x + v2_y

    def collide_obstacle(self, obstacle):
        self.bounces_left -= 1
        obstacle_pos = Vector(obstacle.obs_centre[0], obstacle.obs_centre[1])
        normal = self.pos.copy().subtract(obstacle_pos).normalize()
        self.old_vel = self.vel.copy()
        self.vel.reflect(normal)

        self.collide(obstacle, self)

        # self.angle = self.angle - self.vel.angle(self.old_vel)

    def collide_projectile(self, projectile):
        self.destroy()
        projectile.destroy()

    def destroy(self):
        ITEMS.remove(self)
        del self

    def update(self):
        self.pos.add(self.vel)
        # code for checking collisions
        for item in ITEMS:  # first check for collisions with tanks and projectiles
            item.check_collision(self)
            if self.bounces_left < 1:
                self.destroy()
        game_map.check_collision(self)  # then check for collisions with walls and obstacles
        if self.bounces_left < 1:
            self.destroy()

    def check_collision(self, item):
        if item == self or item == self.tank:
            return
        if item.pos.copy().subtract(self.pos).length() < self.radius + item.radius:
            item.collide_projectile(self)


def draw_handler(canvas):
    global frame_number, game_map, enemies_left_this_round, wait_frames
    frame_number += 1
    if frame_number > 600:
        frame_number = 1
    if menu.show or player.destroyed:
        menu.draw(canvas)
    else:
        if enemies_left_this_round == 0:
            game_map = new_round()
            wait_frames = 60 * 3
        game_map.draw(canvas)
        for item in ITEMS:
            try:
                if wait_frames == 0:
                    item.update()
                else:
                    wait_frames -= 1
                item.draw(canvas)
            except AttributeError as e:
                print(e)


def new_round():
    global round_number, difficulty, ITEMS, enemies_left_this_round, player
    if ITEMS:  # first round has no items yet
        ITEMS = []
    round_number += 1
    player_move_speed = {1: 1.0, 2: 1.15, 3: 1.3}.get(difficulty, 1)
    player_reload_time_multiplier = {1: 1.0, 2: 0.9, 3: 0.8}.get(difficulty, 1)
    enemy_move_speed = {1: 1.0, 2: 1.2, 3: 1.5}.get(difficulty, 1)
    enemy_reload_time_multiplier = {1: 1.0, 2: 0.8, 3: 0.6}.get(difficulty, 1)
    new_map = map.create_gamemap()
    enemies_left_this_round = min(max(1, (round_number // 2) + 1), 8)
    for _ in range(enemies_left_this_round):
        enemy_spawn = new_map.gen_spawn_t2()
        enemy = EnemyTank(enemy_spawn[0], enemy_spawn[1], 1, enemy_reload_time_multiplier, enemy_move_speed)
        ITEMS.append(enemy)
    player_spawn = new_map.gen_spawn_t1()
    player = PlayerTank(player_spawn[0], player_spawn[1], lives, player_reload_time_multiplier, player_move_speed, kbd)
    ITEMS.append(player)
    return new_map


ITEMS = []

kbd = Keyboard()
menu = Menu(kbd)
player = PlayerTank(0, 0, 1, 1, 1, kbd)  # initialising player (gets overwritten when first round is genned)
game_map = new_round()

frame = simplegui.create_frame("Tanks", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_draw_handler(draw_handler)
frame.set_keydown_handler(kbd.key_down)
frame.set_keyup_handler(kbd.key_up)

# Start the frame animation
frame.start()
