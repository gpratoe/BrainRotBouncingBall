from Box2D import b2Vec2

PPM = 10 # factor de escala para box2d

def world_to_pixels(world_coords):
    return b2Vec2(int(world_coords[0] * PPM), int(world_coords[1] * PPM))

def pixels_to_world(pixel_coords):
    return b2Vec2(pixel_coords[0] / PPM, pixel_coords[1] / PPM)

def scale_to_world(value):
    return value / PPM

def scale_to_pixels(value):
    return value * PPM

def list_to_world(list):
    return [pixels_to_world(x) for x in list]

def list_to_pixels(list):
    return [world_to_pixels(x) for x in list]

def vertices_to_world(vertices, position):
    return list_to_world([(b2Vec2(vertice) - position) for vertice in vertices])