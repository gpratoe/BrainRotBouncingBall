import pygame
from pygame import draw
from Box2D import (b2CircleShape, b2FixtureDef, b2LoopShape, b2PolygonShape, b2Vec2, b2ChainShape, b2Mul)
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
                friction=0.0),
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
    def __init__(self, screen,world,position,radius, num_segments=1000, thickness=3, open_segments=0):
        self.screen = screen
        self.world = world
        self.position = position
        self.radius = radius
        self.color = (255,255,255)
        self.thickness = thickness

        self.size = num_segments
        self.vertices = []
        
        for i in range((self.size+1) - open_segments):
            angle = i * (2 * math.pi / self.size)
            x = radius * math.cos(angle) #+ position[0]
            y = radius * math.sin(angle) #+ position[1]
            self.vertices.append((x, y))

        self.pixel_vertices = [world_to_pixels((x + self.position[0], y + self.position[1])) for x,y in self.vertices]

        self.circle = self.world.CreateStaticBody(position=position,
                                                    fixtures=b2FixtureDef(
                                                        shape=b2ChainShape(vertices_chain=self.vertices),
                                                        density=1.0,
                                                        friction=0.0,
                                                        restitution=1.0),
                                                    bullet=True)
        self.circle.userData = self

    def draw(self):
        draw.lines(self.screen, self.color,False, self.pixel_vertices, self.thickness)

    def update(self):
        self.circle.angle += 0.01
        self.pixel_vertices = [world_to_pixels(b2Mul(self.circle.transform, point)) for point in self.vertices]
         
        

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