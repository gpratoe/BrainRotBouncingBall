from Box2D import b2ContactListener
from random import randint

class ContactListener(b2ContactListener):
    def __init__(self, ball):
        super().__init__()
        self.ball = ball

    def BeginContact(self, contact):
        bodyA = contact.fixtureA.body
        bodyB = contact.fixtureB.body

        if bodyA == self.ball.ball or bodyB == self.ball.ball:
            self.ball.color = (randint(0, 255), randint(0, 255), randint(0, 255))
            self.ball.inc_rad_flag = True
            
    def EndContact(self, contact):
        bodyA = contact.fixtureA.body
        bodyB = contact.fixtureB.body