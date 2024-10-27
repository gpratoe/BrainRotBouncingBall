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



ball = Ball(screen,world, pixels_to_world((width/2 , height/2)), ballradius / PPM)

circle = Circle(screen, world, pixels_to_world((width/2 , height/2)), circle_radius / PPM, door_size=(ballradius*2)/PPM, rotate=1)
#circle2 = Circle(screen, world, pixels_to_world((width/2 , height/2)), circle_radius/2 / PPM, door_size=(ballradius*2)/PPM, rotate=-1)

triangle = Triangle(screen, world, pixels_to_world((width/2 , height/2)), height=circle_radius / PPM, door_size=(ballradius*2+1)/PPM,rotate=0)

shapes = [circle, triangle]
world.contactListener = ContactListener(ball)

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
    
    for shape in shapes:
        shape.draw()

    pygame.display.flip()
    world.Step(1/60, 6, 0)

    for shape in shapes:
        shape.update()

    screen.fill((0, 0, 0), (0, 0, width, height))