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
        self.center = Vector2(width/2, height/2)
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
        self.update_rect = pg.Rect(0, 0, width/2, height/2)

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
        
        for ball in self.balls:
            ball.draw()
        for shape in self.shapes:
            shape.draw()

        pg.display.flip()
        self.clock.tick(self.fps)

    def colission_handler(self):
        bodyA = utils.cl.bodyA
        bodyB = utils.cl.bodyB
        for body in [bodyA, bodyB]:
            if isinstance(body.userData, Ball):
                utils.sounds.play_composite()
                body.linearVelocity += (0, 1)
                break
    
    def setup_level(self):
        utils.sounds.set_sound("sounds/basic1.wav")
        ballradius = 10
        
        circle_radius = 100
        num_circles = 7
        rotate_speed = 0.5
        hue = 0

        self.balls.append(Ball((self.width/2 , self.height/2), radius=ballradius, hue=190/355))
        
        for i in range (1,num_circles+1):
            circle = Circle(
                (self.width/2 , self.height/2),
                 radius=circle_radius, 
                 rotate_speed=rotate_speed,
                 hue=hue, 
                 door_size=ballradius*2*i,
                 segs=50,
                 thickness=4, 
                 animate_color=True
            )
            self.shapes.append(circle)
            
            circle_radius += 15
            rotate_speed += 0.25
            hue += 1/num_circles

    def simulation_logic(self):
        ball_pos = Vector2(utils.scale_to_pixels(self.balls[0].ball.position))

        if self.shapes and Vector2(self.center).distance_to(ball_pos) > self.shapes[0].radius - (self.balls[0].radius-(self.balls[0].radius*0.1)):
            self.shapes[0].polygon.DestroyFixture(self.shapes[0].polygon.fixtures[0])
            utils.sounds.play_single_sound()

            self.shapes[0].cleanup()
            self.shapes.pop(0)

    def run(self):
        self.setup_level()
        while True:            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit(0)
                elif event.type == pg.KEYDOWN and event.key == pg.K_p:
                    self.running = not self.running

            if self.running:
                print(self.clock.get_fps())
                utils.calculate_dt()
                self.draw()
                self.update()
                self.simulation_logic()
        