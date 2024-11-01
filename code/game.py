import pygame as pg
from pygame.math import Vector2
from utils import utils
from Box2D import b2World
from contactlistener import ContactListener
from ball import Ball
from circle import Circle
from triangle import Triangle

class Game:
    def __init__(self, width, height, fps):
        self.width = width
        self.height = height
        self.fps = fps
        self.screen = pg.display.set_mode((width, height),pg.HWSURFACE | pg.DOUBLEBUF)
        self.background = pg.Surface(self.screen.get_size())
        self.background.fill((0, 0, 0))
        self.current_screen = 0
        self.world = utils.world = b2World(gravity=(0, 60), doSleep=True)
        self.time_step = 1/fps
        self.clock = pg.time.Clock()
        self.running = False
        self.shapes = []
        self.balls = []

        # setup utils        
        utils.screen = self.screen
        utils.world = self.world
        utils.world.contactListener = ContactListener(self.colission_handler)
        utils.cl = utils.world.contactListener

    def update(self):       
        utils.world.Step(utils.delta_time, 6, 0)
        
        for shape in self.shapes:
            shape.update()
        
        for ball in self.balls:
            ball.update()
    
    def draw(self):
        self.screen.blit(self.background, (0, 0)) # clear screen
        
        for shape in self.shapes:
            shape.draw()
        for ball in self.balls:
            ball.draw()

        pg.display.flip()
        self.clock.tick(self.fps)

    def colission_handler(self):
        bodyA = utils.cl.bodyA
        bodyB = utils.cl.bodyB
        if bodyA.userData.__class__.__name__ == "Ball" or bodyB.userData.__class__.__name__ == "Ball":
            utils.sounds.play_composite()
            if bodyA.userData.__class__.__name__ == "Ball":
                bodyA.linearVelocity += (0, 1)
            else:
                bodyB.linearVelocity += (0, 1)
        
    def setup_level(self):
        utils.sounds.set_sound("sounds/basic1.wav")
        ballradius = 10
        circle_radius = 100

        self.balls.append(Ball((self.width/2 , self.height/2), radius=ballradius, hue=190/355))
        
        num_circles = 7
        rotate_speed = 0.5
        hue = 0
        inc = 1
        hue_boquita = [210/355, 60/355]
        for i in range (1,num_circles+1):
            circle = Circle((self.width/2 , self.height/2), radius=circle_radius,rotate_speed=rotate_speed, hue=hue_boquita[(i+1)%2], door_size=ballradius*2, segs=50, thickness=4)
            circle_radius += 15
            rotate_speed += 0.25
            hue += 1/num_circles
            inc += 2
            self.shapes.append(circle)

    def run(self):
        self.setup_level()
        while True:
            while not self.running:
                for event in pg.event.get():
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_p:
                            self.running = True
                    if event.type == pg.QUIT:
                        exit(0)

            while self.running:
                utils.calculate_dt()
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        exit(0)
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_p:
                            self.running = False

                self.draw()
                self.update()

                if len(self.shapes) > 0 and Vector2(self.width/2,self.height/2).distance_to(utils.scale_to_pixels(self.balls[0].ball.position)) > self.shapes[0].radius - (self.balls[0].radius-(self.balls[0].radius*0.1)):
                    self.shapes[0].polygon.DestroyFixture(self.shapes[0].polygon.fixtures[0])
                    utils.sounds.play_single_sound()
                    self.shapes.pop(0)