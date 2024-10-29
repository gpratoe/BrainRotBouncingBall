from Box2D import b2ContactListener
from utils import utils

class ContactListener(b2ContactListener):
    def __init__(self, ball):
        super().__init__()
        self.ball = ball

    def BeginContact(self, contact):
        bodyA = contact.fixtureA.body
        bodyB = contact.fixtureB.body

        if bodyA == self.ball.ball or bodyB == self.ball.ball: # esto capaz va mejor en el shapes, y aca seteo nomas una flag y despues llamo a update para todo lo que quiera que haga la bola
            utils.sounds.play_pong()
            
            self.ball.ball.linearVelocity += (0, 0.7) # aumenta la velocidad de la bola
            self.ball.inc_rad_flag = True
            
            
    def EndContact(self, contact):
        bodyA = contact.fixtureA.body
        bodyB = contact.fixtureB.body