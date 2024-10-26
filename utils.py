from Box2D import b2Vec2

PPM = 10 # factor de escala para box2d

def world_to_pixels(world_coords):
    return b2Vec2(int(world_coords[0] * PPM), int(world_coords[1] * PPM))

def pixels_to_world(pixel_coords):
    return b2Vec2(pixel_coords[0] / PPM, pixel_coords[1] / PPM)