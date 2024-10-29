import math
from utils import utils
from polygon import Polygon

class Circle(Polygon):
    def __init__(self, position, radius, rotate_speed=0.1, thickness=3,  door_size=0, hue=0):
        SEGMENTS = 360
        circumference = 2 * math.pi * radius
        # explicacion: armo una "bola" tomando el tamaño de la puerta como su diámetro, de esa nueva bola quiero saber cuantos segmentos
        # se necesitan para armar la mitad de su circumferencia. Estos segmentes son los que voy a cortar de la circumferencia original,
        # lo cual me asegura que la puerta tenga el tamaño deseado y no lo arruine la curvatura del circulo.
        # Si calculara la cantidad de segmentos basandome solo en el tamaño de la puerta, al proyectarla sobre el circulo, la curvatura
        # de este haría que la puerta sea mas chica de lo que se espera.
        # 
        # **El tamaño final de la puerta es un poquito mas grande que el especificado pero funciona bien para lo que se necesita.**

        door_to_ball_circumference = math.pi * door_size
        door_to_ball_interest_section = door_to_ball_circumference / 2

        segments_to_cut = math.ceil(door_to_ball_interest_section / circumference * SEGMENTS)

        open_segs = segments_to_cut if segments_to_cut < SEGMENTS/2 else SEGMENTS - segments_to_cut # no se puede cortar mas que la mitad
        
        super().__init__(num_segments=SEGMENTS, position=position,radius=radius, thickness=thickness,
                          open_segments=open_segs, rotate_speed=rotate_speed, hue=hue)