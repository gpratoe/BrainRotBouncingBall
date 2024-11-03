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
        utils.trail_surface = pg.Surface(self.screen.get_size(), pg.SRCALPHA)

        # simulation utils
        self.balls_distance_to_center = []
        self.balls_gone = []


    def update(self):       
        utils.world.Step(utils.delta_time, 6, 0)
        
        for shape in self.shapes:
            shape.update()
        
        for ball in self.balls:
            ball.update()

    def draw(self):
        self.screen.blit(self.background, (0, 0)) # clear screen
        
        for ball in self.balls:
            ball.draw_trail()
        utils.screen.blit(utils.trail_surface, (0,0))
        utils.trail_surface.fill((255,255,255,200), special_flags=pg.BLEND_RGBA_MULT) # pinto la nueva surface de blanco con alpha en 200 por cada cuadro
        for ball in self.balls:
            ball.draw()
        for shape in self.shapes:
            shape.draw()

        pg.display.flip()
        self.clock.tick(self.fps)

    def colission_handler(self):
        bodyA = utils.cl.bodyA
        bodyB = utils.cl.bodyB
        isBall_bodyA = isinstance(bodyA.userData, Ball)
        isBall_bodyB = isinstance(bodyB.userData, Ball)
        if isBall_bodyA or isBall_bodyB:
            utils.sounds.play_song()

        # for body in [bodyA, bodyB]:
        #     if isinstance(body.userData, Ball):
        #         utils.sounds.play_song()
        #         body.linearVelocity += (0, 1)
        #         break
        # if isBall_bodyA and isBall_bodyB:
        #     if bodyA.userData.radius > bodyB.userData.radius and bodyA.userData.radius > 10:
        #         bodyB.userData.radius -= bodyB.userData.radius*(randint(1, 15)/100)
        #         bodyB.userData.inc_rad_flag = True
        #     elif bodyB.userData.radius > bodyA.userData.radius and bodyB.userData.radius > 10:
        #         bodyA.userData.radius -= bodyA.userData.radius*(randint(1, 15)/100)
        #         bodyA.userData.inc_rad_flag = True
        # else:
        #     if isBall_bodyA and not isBall_bodyB and bodyA.userData.radius < 200:
        #         bodyA.userData.radius += bodyA.userData.radius*(randint(5, 8)/100)
        #         bodyA.userData.inc_rad_flag = True
        #     elif isBall_bodyB and not isBall_bodyA and bodyB.userData.radius < 200:
        #         bodyB.userData.radius += bodyB.userData.radius*(randint(5, 8)/100)
        #         bodyB.userData.inc_rad_flag = True
        
        bodyA.linearVelocity += (0.01, 1) if isBall_bodyA else (0, 0)
        bodyB.linearVelocity += (0.01, 1) if isBall_bodyB else (0, 0)

    def setup_level(self):
        utils.sounds.set_sound("sounds/fx/perfect-sf.wav")
        
        ballradius = 10
        hues=[315/355, 190/355]

        self.balls.append(Ball((self.width/2 - ballradius*2 , self.height/2 - 50), radius=ballradius, hue=hues[0]))
        self.balls.append(Ball((self.width/2 + ballradius*2, self.height/2 - 50), radius=ballradius, hue=hues[1]))
        circle = Circle(
                    (self.width/2 , self.height/2),
                    radius=200, 
                    rotate_speed=0.5,
                    hue=145/355, 
                    gap_angle=20,
                    segs=25,
                    thickness=2, 
                    animate_color=False
                )
        self.shapes.append(circle)


    def simulation_logic(self):
        
        for ball in self.balls:
            ball_pos = Vector2(utils.scale_to_pixels(ball.ball.position))
            if self.shapes and Vector2(self.center).distance_to(ball_pos) > self.shapes[0].radius and ball not in self.balls_gone:
                #self.balls.append(Ball((self.width/2 - ball.radius*2 , self.height/2 - 50), radius=ball.radius, hue=ball.hue))
                self.balls.append(Ball((self.width/2 + ball.radius*2, self.height/2 - 50), radius=ball.radius, hue=ball.hue))
                self.balls_gone.append(ball)
            if Vector2(self.center).distance_to(ball_pos) > self.shapes[0].radius + 200:
                utils.world.DestroyBody(ball.ball)
                self.balls.remove(ball)

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
                print(self.clock.get_fps())
                utils.calculate_dt()
                self.draw()
                self.update()
                self.simulation_logic()        