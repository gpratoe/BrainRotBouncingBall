import pygame
from pygame import draw
from Box2D import (b2CircleShape, b2FixtureDef) 
from utils import utils

class Ball:
    def __init__(self, position, radius, hue = 0, animate_color=False):
        self.position = position
        self.color = (255,255,255)
        self.hue = hue
        self.animate_color = animate_color
        self.radius = radius
        self.prev_radius = radius
        self.ball = utils.world.CreateDynamicBody(
            fixtures=b2FixtureDef(
                shape=b2CircleShape(radius=utils.scale_to_world(self.radius)),
                density=0.5,
                restitution=1,
                friction=0.0),
            bullet=True,
            position=(utils.pixels_to_world(self.position)))
        
        self.ball.userData = self

        # pygame rect para optimizar animación
        self.rect = pygame.Rect(position[0] - radius, position[1] - radius, radius * 2, radius * 2)
    

    def update(self):
        if self.radius != self.prev_radius:
            self.ball.DestroyFixture(self.ball.fixtures[0])

            new_fixture = b2FixtureDef(
                shape=b2CircleShape(radius=utils.scale_to_world(self.radius)),
                density=0.5,
                restitution=1,
                friction=0
            )

            self.ball.CreateFixture(new_fixture)
            self.prev_radius = self.radius
            
        self.position = utils.world_to_pixels(self.ball.position)

        # Actualizamos el rect ya que cambia de posición 
        self.rect.topleft = (self.position[0] - self.radius, self.position[1] - self.radius)
        self.rect.size = (self.radius * 2, self.radius * 2)

    def draw_trail(self):
        if self.animate_color:
            self.hue = (self.hue + utils.delta_time/10) % 1
        self.color = utils.hue_to_RGB(self.hue)
        draw.circle(utils.trail_surface, self.color, self.position, self.radius)
        
    def draw(self):
        draw.circle(utils.screen, (255,255,255), self.position, self.radius*0.80)