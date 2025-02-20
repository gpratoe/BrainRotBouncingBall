import pygame as pg
from pygame.math import Vector2
from utils import utils
from Box2D import b2World
from contactlistener import ContactListener
from ball import Ball
from circle import Circle
from triangle import Triangle
from random import randint

class Game:
    def __init__(self, width, height, fps):
        self.width = width
        self.height = height
        self.center = Vector2(width/2, height/2)
        self.fps = fps
        self.screen = pg.display.set_mode((width, height),pg.HWSURFACE | pg.DOUBLEBUF   )
        self.background = pg.Surface(self.screen.get_size())
        self.background.fill((0, 0, 0))
        self.current_screen = 0
        self.world = utils.world = b2World(gravity=(0, 60), doSleep=True)
        self.time_step = 1/fps
        self.clock = pg.time.Clock()
        self.running = False
        self.shapes = []
        self.balls = []
        self.update_rect = pg.Rect(0, 0, width/2, height/2)

        # setup utils        
        utils.screen = self.screen
        utils.world = self.world
        utils.world.contactListener = ContactListener(self.colission_handler)
        utils.cl = utils.world.contactListener
        utils.trail_surface = pg.Surface(self.screen.get_size(), pg.SRCALPHA)
        self.fade_surface = pg.Surface(self.screen.get_size(), pg.SRCALPHA)
        self.fade_surface.fill((0,0,0,10))

        # simulation utils
        self.balls_distance_to_center = []
        self.balls_gone = []
        self.rects = []

    def update(self):       
        utils.world.Step(utils.delta_time, 4, 2)
        
        for shape in self.shapes:
            shape.update()
        
        for ball in self.balls:
            ball.update()

    def draw(self):
        self.screen.blit(self.background, (0, 0)) # clear screen
        
        for ball in self.balls:
            ball.draw_trail()
        utils.screen.blit(utils.trail_surface, (0,0))
        utils.trail_surface.blit(self.fade_surface, (0,0), special_flags=pg.BLEND_RGBA_SUB)
        for ball in self.balls:
            ball.draw()
        for shape in self.shapes:
            shape.draw()

        pg.display.update(self.rects)
        self.clock.tick(self.fps)

    def colission_handler(self):
        bodyA = utils.cl.bodyA
        bodyB = utils.cl.bodyB
        isBall_bodyA = isinstance(bodyA.userData, Ball)
        isBall_bodyB = isinstance(bodyB.userData, Ball)
        if isBall_bodyA:
            utils.sounds.play_composite()
            bodyA.userData.ball.linearVelocity += (0.01, 1)
            bodyA.userData.radius = bodyA.userData.radius * 1.1
        if isBall_bodyB:
            utils.sounds.play_composite()
            bodyB.userData.ball.linearVelocity += (0.01, 1)
            bodyB.userData.radius = bodyB.userData.radius * 1.01

    def setup_level(self):
        utils.sounds.set_sound("sounds/fx/perfect-sf.wav")
        
        ballradius = 10
        hues=[315/355, 190/355]
        circle_radius = 80

        self.balls.append(Ball((self.width/2 - ballradius*2 , self.height/2 - 50), radius=ballradius, hue=hues[0]))
        #self.balls.append(Ball((self.width/2 + ballradius*2, self.height/2 - 50), radius=ballradius, hue=hues[1]))
        for i in range (1,9):
            circle = Circle(
                        (self.width/2 , self.height/2),
                        radius=circle_radius, 
                        rotate_speed=0,
                        hue=hues[i%2], 
                        gap_angle=40,
                        segs=360,
                        thickness=2, 
                        animate_color=False,
                        angle_start = 90 - 20
                    )
            circle_radius += 20
            self.shapes.append(circle)
            self.shapes[0].rotate_speed = 0.5
        
        self.rects = [ball.rect for ball in self.balls] + [shape.rect for shape in self.shapes]

    def simulation_logic(self):
        
        for ball in self.balls:
            ball_pos = Vector2(utils.scale_to_pixels(ball.ball.position))
            if self.shapes and Vector2(self.center).distance_to(ball_pos) > self.shapes[0].radius - ball.radius*0.8:
                self.shapes[0].cleanup()
                self.shapes.pop(0)
                if self.shapes:
                    self.shapes[0].rotate_speed = 0.5
                utils.sounds.play_single_sound()

    def run(self):
        self.setup_level()
        pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.KEYUP])
        while True:            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit(0)
                elif event.type == pg.KEYDOWN and event.key == pg.K_p:
                    self.running = not self.running

            if self.running:

                utils.calculate_dt(self.fps)
                self.update()
                self.simulation_logic()        
                self.draw()