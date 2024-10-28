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



ball = Ball(screen,world, (width/2 , height/2), ballradius)

circle = Circle(screen, world, (width/2 , height/2), circle_radius, door_size=(ballradius*10), rotate=1)
circle2 = Circle(screen, world, (width/2 , height/2), circle_radius*0.80, door_size=(ballradius*5), rotate=-1)

triangle = Triangle(screen, world, (width/2 , height/2), height=circle_radius, door_size=ballradius*3,rotate=1)

shapes = [circle, circle2, triangle]
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