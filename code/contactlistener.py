from Box2D import b2ContactListener

class ContactListener(b2ContactListener, ):
    def __init__(self, colission_handler: callable):
        super().__init__()
        self.bodyA = None
        self.bodyB = None
        self.collision_handler = colission_handler

    def BeginContact(self, contact):
        self.bodyA = contact.fixtureA.body
        self.bodyB = contact.fixtureB.body

        self.collision_handler()

            
    def EndContact(self, contact):
        bodyA = contact.fixtureA.body
        bodyB = contact.fixtureB.body