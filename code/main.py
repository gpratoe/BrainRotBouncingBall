import pygame
from Box2D import b2World
from utils import utils
from contactlistener import ContactListener
from pygame import Vector2
from ball import Ball
from circle import Circle
from triangle import Triangle

factor = 1
width, height = 700/factor, 700/factor
ballradius = 10/factor
circle_radius = 40/factor


utils.sounds.set_sound("sounds/basic1.wav")
utils.screen = pygame.display.set_mode((width, height))
utils.world = b2World(gravity=(0, 60), doSleep=True)



ball = Ball((width/2 , height/2), ballradius)



shapes = []
num_circles = 20 
rotate_speed = 0.5
hue = 0

for i in range (1,num_circles+1):
    circle = Circle((width/2 , height/2), radius=circle_radius, door_size=ballradius*2*i, rotate_speed=rotate_speed, hue=hue, segs=50)

    circle_radius += 15
    rotate_speed += 0.25
    hue += 1/num_circles
    

    shapes.append(circle)

utils.world.contactListener = ContactListener(ball)

running = False
while True:
    while not running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    running = True
            if event.type == pygame.QUIT:
                exit(0)

    while running:
        print(utils.clock.get_fps())
        utils.calculate_dt()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    running = False
        
        ball.draw()
        
        for shape in shapes:
            shape.draw()

        pygame.display.update()
        utils.world.Step(utils.delta_time, 6, 0)

        for shape in shapes:
            shape.update()

        #ball.update()
        
        if len(shapes) > 0 and Vector2(width/2,height/2).distance_to(utils.scale_to_pixels(ball.ball.position)) > shapes[0].radius - (ball.radius-(ball.radius*0.1)):
            shapes[0].polygon.DestroyFixture(shapes[0].polygon.fixtures[0])
            utils.sounds.play_single_sound()
            shapes.pop(0)

        utils.screen.fill((0,0,0), (0, 0, width, height))
