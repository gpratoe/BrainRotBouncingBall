import pygame
from pygame import draw
from Box2D import (b2CircleShape, b2FixtureDef, b2LoopShape, b2PolygonShape, b2Vec2)
from utils import *
import math

class Ball:
    def __init__(self, screen, world, position, radius):
        self.screen = screen
        self.world = world
        self.position = position
        self.color = (255,0,10)
        self.radius = radius
        self.inc_rad_flag = False
        self.ball = self.world.CreateDynamicBody(
            fixtures=b2FixtureDef(
                shape=b2CircleShape(radius=self.radius),
                density=0.5,
                restitution=1,
                friction=0),
            bullet=True,
            position=(self.position))
        
        self.ball.userData = self
    

    def update(self):
        if self.inc_rad_flag:
            self.radius += 0.1

            self.ball.DestroyFixture(self.ball.fixtures[0])

            new_fixture = b2FixtureDef(
                shape=b2CircleShape(radius=self.radius),
                density=0.5,
                restitution=1,
                friction=0
            )

            self.ball.CreateFixture(new_fixture)

            self.inc_rad_flag = False
    
    def draw(self):
        draw.circle(self.screen, self.color, world_to_pixels(self.ball.position), self.radius * PPM)


class Circle:
    def __init__(self, screen,world,position,radius, num_segments=360, thickness=3):
        self.screen = screen
        self.world = world
        self.position = position
        self.radius = radius
        self.color = (255,255,200)
        self.thickness = thickness

        self.size = num_segments
        self.vertices = []
        
        for i in range(self.size):
            angle = i * (2 * math.pi / self.size)
            x = radius * math.cos(angle) #+ position[0]
            y = radius * math.sin(angle) #+ position[1]
            self.vertices.append((x, y))

        self.circle = self.world.CreateStaticBody(position=position,
                                                    fixtures=b2FixtureDef(
                                                        shape=b2LoopShape(vertices=self.vertices),
                                                        density=1.0,
                                                        friction=0.0,
                                                        restitution=1.0),
                                                    bullet=True)
        self.circle.userData = self

    def draw(self):
        draw.circle(self.screen, self.color, world_to_pixels(self.circle.position), self.radius * PPM, width=self.thickness)

class Rect:
    def __init__(self, screen, world, position, width, height):
        self.screen = screen
        self.world = world
        self.position = b2Vec2(position[0], position[1]) 
        self.width = width 
        self.height = height
        self.color = (255, 255, 255)
        
        self.rect = self.world.CreateStaticBody(
            position=self.position,
            fixtures=b2FixtureDef(
                shape=b2PolygonShape(box=(self.width/2, self.height/2)), 
                density=1.0
            ),
            bullet=True
        )
        self.rect.userData = self

    def draw(self):
        position_in_pixels = world_to_pixels(self.rect.position)
        
        rect_width = int(self.width * PPM )
        rect_height = int(self.height * PPM)
        
        pygame.draw.rect(
            self.screen,
            self.color,
            pygame.Rect(
                position_in_pixels[0] - rect_width/2,  # Centrar el rectángulo
                position_in_pixels[1] - rect_height/2,
                rect_width,
                rect_height
            )
        )