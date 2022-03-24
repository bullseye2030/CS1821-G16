import math

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from vector import *
from random import randint
import numpy as np

np.set_printoptions(threshold=np.inf)

CANVAS_WIDTH = 768
CANVAS_HEIGHT = 576
GRID_START_COORDS = (50, 50)
GRID_DIMS = (516, 708)
BACKGROUND = 'gray'
BORDER_COLOUR = 'gray'
BORDER_THICKNESS = 50

EMPTY_GRID = [[], []]

ITEMS = []  # items to be drawn
walls = []


class Wall:
    def __init__(self, x, y, width, color, face):
        self.x = x
        self.y = y
        self.width = width * 2 + 1
        self.color = color
        self.face = face
        if self.face == 'l':
            self.normal = Vector(1, 0)
            self.edge = 0 + self.width
        elif self.face == 'r':
            self.edge = CANVAS_WIDTH - self.width
            self.normal = Vector(-1, 0)
        elif self.face == 't':
            self.normal = Vector(0, 1)
            self.edge = 0 + self.width
        elif self.face == 'b':
            self.normal = Vector(0, -1)
            self.edge = CANVAS_HEIGHT - self.width
        else:
            raise Exception("Invalid direction")

    def draw(self, canvas):
        start_xy = (0, 0)
        end_xy = (0, 0)
        if self.face == 'l':
            start_xy = (0, 0)
            end_xy = (0, CANVAS_HEIGHT)
        elif self.face == 'r':
            start_xy = (CANVAS_WIDTH, 0)
            end_xy = (CANVAS_WIDTH, CANVAS_HEIGHT)
        elif self.face == 't':
            start_xy = (0, 0)
            end_xy = (CANVAS_WIDTH, 0)
        elif self.face == 'b':
            start_xy = (0, CANVAS_HEIGHT)
            end_xy = (CANVAS_WIDTH, CANVAS_HEIGHT)
        canvas.draw_line(start_xy, end_xy, self.width, self.color)

    def check_collision(self, item) -> bool:
        if self.face == 'l':
            hit = (item.pos.x - item.radius <= self.edge)
        elif self.face == "r":
            hit = (item.pos.x + item.radius >= self.edge)
        elif self.face == 't':
            hit = (item.pos.y - item.radius <= self.edge)
        elif self.face == "b":
            hit = (item.pos.y + item.radius >= self.edge)
        else:
            raise Exception("Invalid direction")
        if hit:
            item.collide(self.normal)


class Obstacle:
    """
    This class simply stores all the variables required to draw
    the obstacles on the canvas
    """

    def __init__(self, image, image_centre, image_dims, obs_centre, obs_dims):
        self.image = image
        self.image_centre = image_centre
        self.image_dims = image_dims
        self.obs_centre = obs_centre
        self.obs_dims = obs_dims

    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_centre, self.image_dims, self.obs_centre, self.obs_dims)
        # canvas.draw_image(self.image, self.image_centre, self.image_dims, (200, 200), (50, 50))

    def check_collision(self, item):
        """
        checks if item position falls within a certain range
        :param item:
        :return None:
        """
        if abs(item.pos.x - self.obs_centre[0]) < self.obs_dims[0] and abs(item.pos.y - self.obs_centre[1]) < \
                self.obs_dims[1]:  # check by calculating if position of object is in obstacle
            normal = item.pos.copy().subtract(Vector(self.obs_centre[0], self.obs_centre[1]))
            item.collide(self)


class FloorTile:
    def __init__(self, image, image_centre, image_dims, tile_centre, tile_dims):
        self.image = image
        self.image_centre = image_centre
        self.image_dims = image_dims
        self.tile_centre = tile_centre
        self.tile_dims = tile_dims

    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_centre, self.image_dims, self.tile_centre, self.tile_dims)


def create_map(rows, columns):  # return array of 0's to represent map
    temp = [[0 for column in range(columns + 1)] for x in range(rows + 1)]
    return temp


def mirror_list(input_list):
    list_length = len(input_list)
    temp = reversed(input_list[:list_length // 2])
    i = list_length // 2 if list_length % 2 == 0 else list_length // 2 + 1
    for num in temp:
        input_list[i] = num
        i += 1
    return input_list


class Map:

    def __init__(self, items, grid_start_coords, grid_dims, rows, columns, obstacle_rate, obstacle_min_size=2,
                 obstacle_max_size=4, mirror_map=True, debug=False):
        self.items = items  # should be changed to just instantiate walls here
        self.grid_start_coords = grid_start_coords  # pixel coordinates of the top left corner of the grid, where 0, 0 would be
        self.grid_dims = grid_dims  # dimensions of grid in pixels, format y, x
        self.rows = rows
        self.columns = columns
        self.obstacle_rate = obstacle_rate
        self.obstacle_min_size = obstacle_min_size  # minimum size of obstacles
        self.obstacle_max_size = obstacle_max_size  # maximum size of obstacles
        self.mirror_map = mirror_map  # if true then map will be symmetrical
        self.debug = debug  # if true then lines will be drawn to show the grid

        # self.image = simplegui.load_image(
        #    'https://i.pinimg.com/originals/43/6a/bb/436abb31c4c2bad27e9bc22b5ca318cf.jpg')
        self.image = simplegui.load_image("https://github.com/bullseye2030/CS1821-G16/blob/main/sprites/walltile.png"
                                          "?raw=true")
        self.img_dims = (self.image.get_width(), self.image.get_height())
        self.img_centre = (self.img_dims[0] / 2, self.img_dims[1] / 2)
        self.floor_tile_image = simplegui.load_image(
            "https://github.com/bullseye2030/CS1821-G16/blob/main/sprites/floortile.png?raw=true")
        self.floor_tile_image_dims = (self.floor_tile_image.get_width(), self.floor_tile_image.get_height())
        self.floor_tile_image_centre = (self.floor_tile_image_dims[0] / 2, self.floor_tile_image_dims[1] / 2)
        self.obs_dims = (self.grid_dims[0] / columns, self.grid_dims[0] / columns)
        self.floor_tile_dims = (self.obs_dims[0]/1, self.obs_dims[1]/1)
        print(self.img_dims)
        print(self.img_centre)
        print(self.obs_dims)

        heatmap = self.generate_heat_map()
        if self.mirror_map:
            heatmap = [mirror_list(row) for row in heatmap]
        self.obstacles, self.floor_tiles = self.heatmap_to_obstacles(heatmap)
        for i in self.floor_tiles:
            items.append(i)
        for i in self.obstacles:
            items.append(i)

        self.t1_spawns = []
        self.t2_spawns = []

    def draw(self, canvas):  # callback function to draw entire map, called in update function
        for item in self.items:
            item.draw(canvas)

    def check_overlap(self, map1,
                      map2):  # map1 should be existing map to build on, map2 should be temp map with 1 object on it
        for x in range(self.rows):
            for y in range(self.columns):
                if map1[x][y] == 1 and map2[x][y] == 1:
                    return True
        return False

    def build_corner(self, gamemap):
        for y in range(self.rows):  # y because go down columns first then pick a row number
            for x in range(self.columns):
                if gamemap[y][x] != 0:  # check if map already has an obstacle there; if it is 1 then ignore
                    # pick direction of growth
                    direction_x = -1 if randint(0,
                                                1) % 0 == 0 else 1  # pick whether one arm of the obstacle will go left or right
                    direction_y = -1 if randint(0, 1) % 0 == 0 else 1
                    # pick size
                    obstacle_size = randint(self.obstacle_min_size, self.obstacle_max_size)
                    # build temp map
                    create_map(self.rows, self.columns)
                    start_coords = (y, x)  #
                    # do checks here
                    self.check_overlap()
                    gamemap[y][x] = 1  # change gamemap after everything else is done

    def build_block(self, main_map, start_coords, size):
        # main map is 2d array with all the other obstacles on it
        # start is coordinates (indexes) of starting points
        # size is how big the obstacle will be
        tmap = create_map(self.rows, self.columns)
        for x in range(start_coords[0], start_coords[0] + size):
            for y in range(start_coords[1], start_coords[1] + size):
                y = y % self.columns
                x = x % self.rows
                tmap[x][y] = 1
        if not self.check_overlap(main_map, tmap):  # checks if the obstacle will overlap with existing obstacles
            for x in range(start_coords[0], start_coords[0] + size):
                for y in range(start_coords[1], start_coords[1] + size):
                    y = y % self.columns
                    x = x % self.rows
                    if tmap[x][y] == 1:
                        main_map[x][y] = 1
        return main_map

    def generate_heat_map(self):  # return 2d array of numbers
        temp_map = create_map(self.rows, self.columns)
        for x in range(self.rows):  # y because go down columns first then pick a row number
            for y in range(self.columns):
                if randint(1, self.obstacle_rate) == 1:  # a 1/obstacle rate chance of creating an obstacles
                    obstacle = randint(1, 4)
                    obstacle = 2  # for debug
                    start_coords = (x, y)
                    size = randint(self.obstacle_min_size, self.obstacle_max_size)
                    if obstacle == 1:
                        self.build_corner(temp_map)
                    elif obstacle == 2:
                        temp_map = self.build_block(temp_map, start_coords, size)  # size of generatted obstacles

                    elif obstacle == 3:
                        # build_line(temp_map)
                        x = 1
                    elif obstacle == 4:
                        # build_plus(temp_map)
                        x = 1
        return temp_map

    def heatmap_to_obstacles(self, heatmap):
        """
        Translates 2d array of 1's and 0's into a list of obstacles

        it calculates the coordinates of the obstacle using the formula below:
        2d_centre_of_image * index_in_heatmap + top_left_corner_of

        :return:
        """
        blocks = []
        floor_tiles = []
        for x in range(0, self.rows):
            for y in range(0, self.columns):
                if heatmap[x][y] == 1:
                    new_y = self.obs_dims[0] * y + self.grid_start_coords[0]
                    new_x = self.obs_dims[1] * x + self.grid_start_coords[1]
                    new_coords = (new_x, new_y)
                    new_block = Obstacle(self.image, self.img_centre, self.img_dims, new_coords, self.obs_dims)
                    blocks.append(new_block)
                    print("coords: ", new_coords)
                    print("obs_centre", new_block.obs_centre)
                else:
                    # create a floor tile object
                    new_y = self.obs_dims[0] * y + self.grid_start_coords[0]
                    new_x = self.obs_dims[1] * x + self.grid_start_coords[1]
                    new_coords = (new_x, new_y)
                    new_tile = FloorTile(self.floor_tile_image, self.floor_tile_image_centre,
                                         self.floor_tile_image_dims, new_coords, self.floor_tile_dims)
                    floor_tiles.append(new_tile)
        print(np.matrix(heatmap))
        return blocks, floor_tiles

    def check_collision(self, item):
        for obs in self.obstacles:
            obs.check_collision(item)
        for wall in walls:
            wall.check_collision(item)

    def check_spawn_dist(self, spawn_1, spawn_2, minimum_dist):
        dist = math.sqrt((spawn_1[0]-spawn_2[0])**2 +(spawn_1[1]-spawn_2[1])**2)
        if dist < minimum_dist:
            return False
        else:
            return True

    def gen_spawn_t1(self):
        valid_spawn = False
        friendly_min_distance = 5
        enemy_min_distance = 10
        spawn_x = 1
        spawn_y = 1
        while not valid_spawn:
            spawn_x = randint(2, self.rows / 2 - 5)  # spawn on left side of the map
            spawn_y = randint(2, self.columns - 5)
            if self.heatmap[spawn_x][spawn_y] == 1: #if there is an obstacle there
                continue    #dont use this spawn and try again
            for tank_spawn in self.t1_spawns:
                if not self.check_spawn_dist((spawn_x, spawn_y), tank_spawn, friendly_min_distance): #if the tank spawns to close to a friendly tank
                    continue    #dont use this spawn and try again
            for tank_spawn in self.t2_spawns:
                if not self.check_spawn_dist((spawn_x, spawn_y), tank_spawn, enemy_min_distance):
                    continue
            valid_spawn = True
        new_spawn = (spawn_x, spawn_y)
        self.t1_spawns.append(new_spawn)
        return new_spawn

    def update(self):
        return 1


def create_gamemap():
    l = Wall(0, 0, BORDER_THICKNESS, BORDER_COLOUR, 'l')  # define walls and pass as initial items to draw
    r = Wall(0, CANVAS_WIDTH, BORDER_THICKNESS, BORDER_COLOUR, 'r')
    t = Wall(0, 0, BORDER_THICKNESS, BORDER_COLOUR, 't')
    b = Wall(0, CANVAS_HEIGHT, BORDER_THICKNESS, BORDER_COLOUR, 'b')
    ITEMS = [l, r, t, b]
    gamemap = Map(ITEMS, GRID_START_COORDS, GRID_DIMS, 32, 24, 50)
    return gamemap

# frame = simplegui.create_frame("TANKS!", CANVAS_WIDTH, CANVAS_HEIGHT)
# frame.set_draw_handler(gamemap.draw)

# frame.set_canvas_background(BACKGROUND)

# frame.start()
