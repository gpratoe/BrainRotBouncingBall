from Box2D import b2ContactListener
from random import randint
from sounds import Sounds

class ContactListener(b2ContactListener):
    def __init__(self, ball):
        super().__init__()
        self.ball = ball
        self.sounds = Sounds()

    def BeginContact(self, contact):
        bodyA = contact.fixtureA.body
        bodyB = contact.fixtureB.body

        if bodyA == self.ball.ball or bodyB == self.ball.ball: # esto capaz va mejor en el shapes, y aca seteo nomas una flag y despues llamo a update para todo lo que quiera que haga la bola
            self.sounds.play()
            
            self.ball.ball.linearVelocity += (0, 0.7) # aumenta la velocidad de la bola

            self.ball.color = (randint(0, 255), randint(0, 255), randint(0, 255))
            self.ball.inc_rad_flag = True
            
            
    def EndContact(self, contact):
        bodyA = contact.fixtureA.body
        bodyB = contact.fixtureB.body