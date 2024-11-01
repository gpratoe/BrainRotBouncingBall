import math
from polygon import Polygon

class Triangle(Polygon):
    def __init__(self, position, height, rotate_speed=0.1, thickness=3, door_size=0, hue=0, animate_color=False):
        self.door_size = door_size
        self.height = height
        super().__init__(num_segments=3, position=position,
                          open_segments=0, radius=height/2, rotate_speed=rotate_speed, thickness=thickness, hue=hue, animate_color=animate_color)



    def __setup_vertices__(self):
        for i in range(3):
            angle = i * (2 * math.pi / self.size) 
            x = self.radius * math.cos(angle) + self.position[0]
            y = self.radius * math.sin(angle) + self.position[1]
            self.vertices.append((x, y))


        subx = (self.vertices[2][0] - self.vertices[0][0])
        suby = (self.vertices[2][1] - self.vertices[0][1])
        base = math.sqrt(subx**2 + suby**2)
        
        length_door_wall = (base/2) - (self.door_size/2)  
        factor = (length_door_wall/base) # porporcion de un lado original que toma una de las paredes que forman la puerta

        # calculo los vertices que estan entre el vertice 0 y 2, para poder dividir ese lado y hacer la puerta
        door_vertex1_x = (factor) * self.vertices[0][0] + (1-factor) * self.vertices[2][0]
        door_vertex1_y = (factor) * self.vertices[0][1] + (1-factor) * self.vertices[2][1]
        
        self.vertices.append((door_vertex1_x, door_vertex1_y)) 

        # invierto el factor para calcular como si fuera desde el vertice 0 al 2, antes calculé como si fuera desde el 2 al 0,
        # de esta forma se mantiene la puerta al medio del triangulo 
        door_vertex2_x = (1-factor) * self.vertices[0][0] + factor * self.vertices[2][0]
        door_vertex2_y = (1-factor) * self.vertices[0][1] + factor * self.vertices[2][1]
        
        self.vertices.insert(0, (door_vertex2_x, door_vertex2_y))
