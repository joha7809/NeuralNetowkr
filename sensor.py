import pygame
from pvector import PVector

class Sensor(PVector):
    def __init__(self, vector, car_pos, screen):
        #Sensor length and direction
        self.sens = vector

        #Add sens to origin to find coordinates where the sensor should be drawn
        self.pos = car_pos.add(self.sens)

        #pygame surface
        self.screen = screen

    def update_pos(self, acceleration, car_pos):
        #Add sensor vector to the car position, to find coordinates to draw sensor
        self.pos = car_pos.add(self.sens)

        #Add the accelaration to the position
        self.pos = self.pos.add(acceleration)

    def get_pixel(self):
        #Returns RGBA for the pixel at pos coordinates
        coordinates = list(map(round, self.pos.repr()))
        try: 
            color = self.screen.get_at(coordinates)
            if self.is_black(color):
                return (0,0,0,0)
            else:
                return (255,255,255,255)
        except Exception as e:
            return (0, 0, 0, 0)

    def is_black(self, color):
        r,g,b = color[:3]
        return r < 100 and g < 100 and b < 100