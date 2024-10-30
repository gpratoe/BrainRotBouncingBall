import pygame
from pygame import draw
from Box2D import (b2CircleShape, b2FixtureDef) 
from utils import utils

class Ball:
    def __init__(self, position, radius):
        self.trail_surface = pygame.Surface(utils.screen.get_size(), pygame.SRCALPHA)
        self.position = position
        self.color = (255,255,255)
        self.hue = 0
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

        self.hue = (self.hue + utils.delta_time/10) % 1
        self.color = utils.hue_to_RGB(self.hue)
        draw.circle(self.trail_surface, self.color, new_position, self.radius,)

        utils.screen.blit(self.trail_surface, (0,0))
        self.trail_surface.fill((255,255,255,200), special_flags=pygame.BLEND_RGBA_MULT) # pinto la nueva surface de blanco con alpha en 200 por cada cuadro
        
        
        draw.circle(utils.screen, (255,255,255), new_position, self.radius-self.radius*0.2)