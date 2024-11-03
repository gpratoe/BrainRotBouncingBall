import math
from utils import utils
from polygon import Polygon
from pygame import draw

class Circle(Polygon):
    def __init__(self, position, radius, rotate_speed=0.1, thickness=3,  gap_angle=30, hue=0, segs = 200, animate_color=False):
        self.gap_angle = gap_angle
        self.start_angle = self.gap_angle
        self.end_angle = 0
        SEGMENTS = segs

        segments_to_cut = int((gap_angle * SEGMENTS) / 360)
        super().__init__(num_segments=SEGMENTS, position=position,radius=radius, thickness=thickness,
                          open_segments=segments_to_cut, rotate_speed=rotate_speed, hue=hue, animate_color=animate_color)
        
    
    def draw(self):
        if self.animate_color:
            self.hue = (self.hue + utils.delta_time / 10) % 1
        self.color = utils.hue_to_RGB(self.hue)

        if self.gap_angle == 0:
            draw.circle(utils.screen, self.color, self.position, self.radius, self.thickness)
        else:
            draw.arc(
                utils.screen,
                self.color,
                (self.position[0] - self.radius, self.position[1] - self.radius, self.radius * 2, self.radius * 2),
                math.radians(self.start_angle),
                math.radians(self.end_angle),
                self.thickness
            )

    def update(self):
        self.polygon.angle += self.rotate_speed * utils.delta_time

        angle_increment = self.rotate_speed * utils.delta_time * (180 / math.pi)  

        self.start_angle = (self.start_angle - angle_increment) % 360
        self.end_angle = (self.end_angle - angle_increment) % 360
