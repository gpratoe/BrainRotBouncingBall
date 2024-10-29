import pygame
import time
from pygame import draw
from Box2D import (b2CircleShape, b2FixtureDef, b2LoopShape, b2PolygonShape, b2Vec2, b2ChainShape, b2Mul, Box2D) 
from utils import *
import random
import math

class Ball:
    def __init__(self, screen, world, position, radius):
        self.bloom_ratio = 1.5
        self.bloom_surface = pygame.Surface((radius*2*self.bloom_ratio, radius*2*self.bloom_ratio), pygame.SRCALPHA)
        self.bloom_surface.set_alpha(128)
        self.screen = screen
        self.world = world
        self.position = position
        self.color = (255,0,10)
        self.radius = radius
        self.inc_rad_flag = False
        self.ball = self.world.CreateDynamicBody(
            fixtures=b2FixtureDef(
                shape=b2CircleShape(radius=scale_to_world(self.radius)),
                density=0.5,
                restitution=1,
                friction=0.0),
            bullet=True,
            position=(pixels_to_world(self.position)))
        
        self.ball.userData = self
    

    def update(self):
        if self.inc_rad_flag:
            self.radius += 0.1

            self.ball.DestroyFixture(self.ball.fixtures[0])

            new_fixture = b2FixtureDef(
                shape=b2CircleShape(radius=scale_to_world(self.radius)),
                density=0.5,
                restitution=1,
                friction=0
            )

            self.ball.CreateFixture(new_fixture)

            self.inc_rad_flag = False
    
    def draw(self):
        new_position = world_to_pixels(self.ball.position)
        bloom_radius = self.radius*self.bloom_ratio
        center_bloom_surface = (bloom_radius, bloom_radius)

        draw.circle(self.bloom_surface, self.color, center_bloom_surface, bloom_radius)
        self.screen.blit(self.bloom_surface, new_position - center_bloom_surface)
        draw.circle(self.screen, self.color, new_position, self.radius)



class Polygon:
    def __init__(self, screen,world,position,radius, num_segments=3, thickness=3, open_segments=0, rotate_speed=0.01, hue=0):
        self.screen = screen
        self.world = world
        self.position = b2Vec2(position)
        self.radius = radius
        self.color = (255,255,255)
        self.hue = hue
        self.thickness = thickness
        self.rotate_speed = rotate_speed
        self.size = num_segments
        self.open_segments = open_segments
        self.vertices = []
        self.__setup_vertices__()

        self.polygon = self.world.CreateStaticBody(position=pixels_to_world(position),
                                                    fixtures=b2FixtureDef(
                                                        shape=b2ChainShape(vertices_chain=vertices_to_world(self.vertices, self.position)),
                                                        density=1.0,
                                                        friction=0.0,
                                                        restitution=1.0),
                                                    bullet=True)
        self.polygon.userData = self

    def __setup_vertices__(self):
        total_segments = (self.size - self.open_segments)
        for i in range(total_segments + 1):
            angle = i * (2 * math.pi / self.size)
            x = self.radius * math.cos(angle) + self.position[0]
            y = self.radius * math.sin(angle) + self.position[1]
            self.vertices.append((x, y))

    def draw(self):
        self.hue = (self.hue + 0.001) % 1
        self.color = hue_to_RGB(self.hue)
        draw.lines(self.screen, self.color,False, self.vertices, self.thickness)

    def update(self):
        self.polygon.angle += self.rotate_speed
        world_vertices = self.polygon.fixtures[0].shape.vertices
        self.vertices = [world_to_pixels(b2Mul(self.polygon.transform, point)) for point in world_vertices]
        
class Circle(Polygon):
    def __init__(self, screen, world, position, radius, rotate_speed=0.1, thickness=3,  door_size=0, hue=0):
        SEGMENTS = 360
        circumference = 2 * math.pi * radius
        # explicacion: armo una "bola" tomando el tamaño de la puerta como su diámetro, de esa nueva bola quiero saber cuantos segmentos
        # se necesitan para armar la mitad de su circumferencia. Estos segmentes son los que voy a cortar de la circumferencia original,
        # lo cual me asegura que la puerta tenga el tamaño deseado y no lo arruine la curvatura del circulo.
        # Si calculara la cantidad de segmentos basandome solo en el tamaño de la puerta, al proyectarla sobre el circulo, la curvatura
        # de este haría que la puerta sea mas chica de lo que se espera.
        # 
        # **El tamaño final de la puerta es un poquito mas grande que el especificado pero funciona bien para lo que se necesita.**

        door_to_ball_circumference = math.pi * door_size
        door_to_ball_interest_section = door_to_ball_circumference / 2

        segments_to_cut = math.ceil(door_to_ball_interest_section / circumference * SEGMENTS)

        open_segs = segments_to_cut if segments_to_cut < SEGMENTS/2 else SEGMENTS - segments_to_cut # no se puede cortar mas que la mitad
        
        super().__init__(num_segments=SEGMENTS, screen=screen, world=world, position=position,
                          radius=radius, thickness=thickness, open_segments=open_segs, rotate_speed=rotate_speed, hue=hue)

class Triangle(Polygon):
    def __init__(self, screen, world, position, height, rotate_speed=0.1, thickness=3, door_size=0, hue=0):
        self.door_size = door_size
        self.height = height
        super().__init__(num_segments=3, screen=screen, world=world, position=position,
                          open_segments=0, radius=height/2, rotate_speed=rotate_speed, thickness=thickness, hue=hue)



    def __setup_vertices__(self):
        for i in range(3):
            angle = i * (2 * math.pi / self.size) 
            x = self.radius * math.cos(angle) + self.position[0]
            y = self.radius * math.sin(angle) + self.position[1]
            self.vertices.append((x, y))


        subx = (self.vertices[2][0] - self.vertices[0][0])
        suby = (self.vertices[2][1] - self.vertices[0][1])
        base = math.sqrt(subx**2 + suby**2)
        
        length_door_wall = (base/2) - (self.door_size/2)  
        factor = (length_door_wall/base) # porporcion de un lado original que toma una de las paredes que forman la puerta

        # calculo los vertices que estan entre el vertice 0 y 2, para poder dividir ese lado y hacer la puerta
        door_vertex1_x = (factor) * self.vertices[0][0] + (1-factor) * self.vertices[2][0]
        door_vertex1_y = (factor) * self.vertices[0][1] + (1-factor) * self.vertices[2][1]
        
        self.vertices.append((door_vertex1_x, door_vertex1_y)) 

        # invierto el factor para calcular como si fuera desde el vertice 0 al 2, antes calculé como si fuera desde el 2 al 0,
        # de esta forma se mantiene la puerta al medio del triangulo 
        door_vertex2_x = (1-factor) * self.vertices[0][0] + factor * self.vertices[2][0]
        door_vertex2_y = (1-factor) * self.vertices[0][1] + factor * self.vertices[2][1]
        
        self.vertices.insert(0, (door_vertex2_x, door_vertex2_y))


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