import pygame
from pygame import draw
from Box2D import (b2CircleShape, b2FixtureDef) 
from utils import utils

class Ball:
    def __init__(self, position, radius):
        self.bloom_ratio = 1.5
        self.bloom_surface = pygame.Surface((radius*2*self.bloom_ratio, radius*2*self.bloom_ratio), pygame.SRCALPHA)
        self.bloom_surface.set_alpha(128)
        self.position = position
        self.color = (255,255,255)
        self.radius = radius
        self.inc_rad_flag = False
        self.ball = utils.world.CreateDynamicBody(
            fixtures=b2FixtureDef(
                shape=b2CircleShape(radius=utils.scale_to_world(self.radius)),
                density=0.5,
                restitution=1,
                friction=0.0),
            bullet=True,
            position=(utils.pixels_to_world(self.position)))
        
        self.ball.userData = self
    

    def update(self):
        if self.inc_rad_flag:
            self.radius += (self.radius*0.03)

            self.ball.DestroyFixture(self.ball.fixtures[0])

            new_fixture = b2FixtureDef(
                shape=b2CircleShape(radius=utils.scale_to_world(self.radius)),
                density=0.5,
                restitution=1,
                friction=0
            )

            self.ball.CreateFixture(new_fixture)

            self.inc_rad_flag = False
    
    def draw(self):
        new_position = utils.world_to_pixels(self.ball.position)
        bloom_radius = self.radius*self.bloom_ratio
        center_bloom_surface = (bloom_radius, bloom_radius)

        #draw.circle(self.bloom_surface, self.color, center_bloom_surface, bloom_radius)
        #utils.screen.blit(self.bloom_surface, new_position - center_bloom_surface)
        draw.circle(utils.screen, self.color, new_position, self.radius)
