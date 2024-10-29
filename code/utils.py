import colorsys
import pygame
from Box2D import b2Vec2
from sounds import Sounds

class Utils:
    def __init__(self):
        self.world = None
        self.screen = None
        self.PPM = 10

        self.delta_time = 0
        self.clock = pygame.time.Clock()

        self.sounds = Sounds()

    def world_to_pixels(self, world_coords):
        return b2Vec2(int(world_coords[0] * self.PPM), int(world_coords[1] * self.PPM))

    def pixels_to_world(self, pixel_coords):
        return b2Vec2(pixel_coords[0] / self.PPM, pixel_coords[1] / self.PPM)

    def scale_to_world(self, value):
        return value / self.PPM

    def scale_to_pixels(self, value):
        return value * self.PPM

    def list_to_world(self, list):
        return [self.pixels_to_world(x) for x in list]

    def list_to_pixels(self,list):
        return [self.world_to_pixels(x) for x in list]

    def vertices_to_world(self, vertices, position):
        return self.list_to_world([(b2Vec2(vertice) - position) for vertice in vertices])

    def hue_to_RGB(self, hue):
        return tuple(int(i * 255) for i in colorsys.hsv_to_rgb(hue, 1, 1))

    def calculate_dt(self):
        self.delta_time = self.clock.tick(60) / 1000

utils = Utils()