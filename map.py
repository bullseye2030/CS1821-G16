try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from vector import *
from random import randint
import numpy as np
np.set_printoptions(threshold=np.inf)

CANVAS_HEIGHT = 600
CANVAS_WIDTH = 600
GRID_START_COORDS = (100, 100)
GRID_DIMS = (400, 400)
BACKGROUND = 'gray'
BORDER_COLOUR = 'black'
BORDER_THICKNESS = 15

EMPTY_GRID = [[], []]

ITEMS = []  #items to be drawn

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

    def hit(self, ball) -> bool:
        if self.face == 'l':
            hit = (ball.pos.x - ball.radius <= self.edge)
        elif self.face == "r":
            hit = (ball.pos.x + ball.radius >= self.edge)
        elif self.face == 't':
            hit = (ball.pos.y - ball.radius <= self.edge)
        elif self.face == "b":
            hit = (ball.pos.y + ball.radius >= self.edge)
        else:
            raise Exception("Invalid direction")
        return hit

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
        #canvas.draw_image(self.image, self.image_centre, self.image_dims, (200, 200), (50, 50))


def create_map(rows, columns): #return array of 0's to represent map
    temp = [[0 for column in range(columns+1)] for x in range(rows+1)]
    return temp


class Map:

    def __init__(self, items, grid_start_coords,  grid_dims, rows, columns, obstacle_rate, obstacle_min_size = 2, obstacle_max_size = 4, debug = False):
        self.items = items  #should be changed to just instantiate walls here
        self.grid_start_coords = grid_start_coords  #pixel coordinates of the top left corner of the grid, where 0, 0 would be
        self.grid_dims = grid_dims  #dimensions of grid in pixels, format y, x
        self.rows = rows
        self.columns = columns
        self.obstacle_rate = obstacle_rate
        self.obstacle_min_size = obstacle_min_size  #minimum size of obstacles
        self.obstacle_max_size = obstacle_max_size  #maximum size of obstacles
        self.debug = debug #if true then lines will be drawn to show the grid

        #self.image = simplegui._load_local_image("map_sprites/block_sprite.png")
        self.image = simplegui.load_image('https://lh3.googleusercontent.com/X8MWUElYqJ5DFjHbuOF2diN9ARFFPVqp3CHJNx8XCItvgxNKeNMIOn_iEmv2Bkqk88Qx9hw1bQmFSWDF1BOX=s400')
        self.img_dims = (self.image.get_width(), self.image.get_height())
        self.img_centre = (self.img_dims[0]/2, self.img_dims[1]/2)
        self.obs_dims = (self.grid_dims[0]/columns, self.grid_dims[1]/rows)
        print(self.img_dims)
        print(self.img_centre)
        print(self.obs_dims)


        heatmap = self.generate_heat_map()
        obstacles = self.heatmap_to_obstacles(heatmap)
        for i in obstacles:
            items.append(i)

        print(obstacles[5].obs_centre)


    def draw(self, canvas): #callback function to draw entire map, called in update function
        for item in self.items:
            item.draw(canvas)


    def check_overlap(self, map1, map2):    #map1 should be existing map to build on, map2 should be temp map with 1 object on it
        for x in range(self.rows):
            for y in range(self.columns):
                if map1[y][x] == 1 and map2[y][x] == 1:
                    return True
        return False


    def build_corner(self, gamemap):
        for y in range(self.rows):  # y because go down columns first then pick a row number
            for x in range(self.columns):
                if gamemap[y][x] != 0:  #check if map already has an obstacle there; if it is 1 then ignore
                    #pick direction of growth
                    direction_x = -1 if randint(0, 1) % 0 == 0 else 1    #pick whether one arm of the obstacle will go left or right
                    direction_y = -1 if randint(0, 1) % 0 == 0 else 1
                    #pick size
                    obstacle_size = randint(self.obstacle_min_size, self.obstacle_max_size)
                    #build temp map
                    create_map(self.rows, self.columns)
                    start_coords = (y, x)   #
                    #do checks here
                    self.check_overlap()
                    gamemap[y][x] = 1  #change gamemap after everything else is done

    def build_block(self, main_map, start_coords, size):
        #main map is 2d array with all the other obstacles on it
        #start is coordinates (indexes) of starting points
        #size is how big the obstacle will be
        tmap = create_map(self.rows, self.columns)
        for x in range(start_coords[0], start_coords[0] + size):
            for y in range(start_coords[1], start_coords[1] + size):
                y = y % self.columns
                x = x % self.rows
                tmap[y][x] = 1
        if not self.check_overlap(main_map, tmap):  #checks if the obstacle will overlap with existing obstacles
            for x in range(start_coords[0], start_coords[0] + size):
                for y in range(start_coords[1], start_coords[1] + size):
                    y = y % self.columns
                    x = x % self.rows
                    if tmap[y][x] == 1:
                        main_map[y][x] = 1
        return main_map



    def generate_heat_map(self):    #return 2d array of numbers
        temp_map = create_map(self.rows, self.columns)
        for x in range(self.rows):  #y because go down columns first then pick a row number
            for y in range(self.columns):
                if randint(1, self.obstacle_rate) == 1:     #a 1/obstacle rate chance of creating an obstacles
                    obstacle = randint(1, 4)
                    obstacle = 2    #for debug
                    start_coords = (x, y)
                    size = randint(self.obstacle_min_size, self.obstacle_max_size)
                    if obstacle == 1:
                        self.build_corner(temp_map)
                    elif obstacle == 2:
                        temp_map = self.build_block(temp_map, start_coords, size)   #size of generatted obstacles

                    elif obstacle == 3:
                        #build_line(temp_map)
                        x = 1
                    elif obstacle == 4:
                        #build_plus(temp_map)
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
        for x in range(0, self.rows):
            for y in range(0, self.columns):
                if heatmap[y][x] == 1:
                    new_y = self.obs_dims[0] * y + self.grid_start_coords[0]
                    new_x = self.obs_dims[1] * x + self.grid_start_coords[1]
                    new_coords = (new_x, new_y)
                    new_block = Obstacle(self.image, self.img_centre, self.img_dims, new_coords, self.obs_dims)
                    blocks.append(new_block)
                    print("coords: ", new_coords)
                    print("obs_centre", new_block.obs_centre)
        print(np.matrix(heatmap))
        return blocks

l = Wall(0, 0, BORDER_THICKNESS, BORDER_COLOUR, 'l')
r = Wall(0, CANVAS_WIDTH, BORDER_THICKNESS, BORDER_COLOUR, 'r')
t = Wall(0, 0, BORDER_THICKNESS, BORDER_COLOUR, 't')
b = Wall(0, CANVAS_HEIGHT, BORDER_THICKNESS, BORDER_COLOUR, 'b')
ITEMS = [l, r, t, b]


gamemap = Map(ITEMS, GRID_START_COORDS, GRID_DIMS, 20, 20, 30)
frame = simplegui.create_frame("TANKS!", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_draw_handler(gamemap.draw)

frame.set_canvas_background(BACKGROUND)

frame.start()
