import math
import pygame
from shapes import *
from Box2D import b2World
from utils import *
from contactlistener import ContactListener

width, height = 700, 700
ballradius = 10
circle_radius = 200

clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
screen.fill((0, 0, 0), (0, 0, width, height))

world = b2World(gravity=(0, 60), doSleep=True)



ball = Ball(screen,world, pixels_to_world((width/2 - 1 , height/2-circle_radius+ballradius*2)), ballradius / PPM)

circle = Circle(screen, world, pixels_to_world((width/2 , height/2)), circle_radius / PPM, open_segments=40)

cl = ContactListener(ball)
world.contactListener = cl

running = False

while not running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                running = True
        if event.type == pygame.QUIT:
            exit(0)

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
    
    ball.draw()
    circle.draw()
    pygame.display.flip()
    world.Step(1/60, 6, 0)
    circle.update()

    screen.fill((0, 0, 0), (0, 0, width, height))