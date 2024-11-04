import math
from pygame import draw
from Box2D import (b2FixtureDef, b2Vec2, b2ChainShape, b2Mul) 
from utils import utils

class Polygon:
    def __init__(self, position, radius, num_segments=3, thickness=3, open_segments=0, rotate_speed=0.01, hue=0, animate_color=False, angle_start=0):
        self.position = b2Vec2(position)
        self.radius = radius
        self.color = (255,255,255)
        self.animate_color = animate_color
        self.hue = hue
        self.thickness = thickness
        self.rotate_speed = rotate_speed
        self.size = num_segments
        self.open_segments = open_segments
        self.vertices = []
        self.angle_start = math.radians(angle_start) 
        self.__setup_vertices__()

        self.polygon = utils.world.CreateStaticBody(position=utils.pixels_to_world(position),
                                                    fixtures=b2FixtureDef(
                                                        shape=b2ChainShape(vertices_chain=utils.vertices_to_world(self.vertices, self.position)),
                                                        density=1.0,
                                                        friction=0.0,
                                                        restitution=1.0),
                                                    bullet=True)
        self.polygon.userData = self

    def __setup_vertices__(self):
        total_segments = (self.size - self.open_segments)
        for i in range(total_segments + 1):
            angle = (i * (2 * math.pi / self.size)) - self.angle_start
            x = self.radius * math.cos(angle) + self.position[0]
            y = self.radius * math.sin(angle) + self.position[1]
            self.vertices.append((x, y))

    def draw(self):
        if self.animate_color:
            self.hue = (self.hue + utils.delta_time/10) % 1
        self.color = utils.hue_to_RGB(self.hue)
        draw.lines(utils.screen, self.color,False, self.vertices, self.thickness)

    def update(self):
        self.polygon.angle += self.rotate_speed * utils.delta_time
        world_vertices = self.polygon.fixtures[0].shape.vertices
        self.vertices = [utils.world_to_pixels(b2Mul(self.polygon.transform, point)) for point in world_vertices]
    
    def cleanup(self):
        if self.polygon:
            utils.world.DestroyBody(self.polygon)  
            self.polygon = None  