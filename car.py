import random
import pygame
from pvector import PVector
from sensor import Sensor
from math import pi
from brain import Brain

class Car:
    
    def __init__(self, screen, size: int, startx: int, starty: int, heading:int = 0, track_img = None):
        self.track_img = track_img
        self.BLACK = (0, 0, 0, 0)
        heading = heading*pi/180
        self.screen = screen
        self.size = size
        self.pos = PVector(startx, starty)
        self.velocity = PVector(0, -3).rotate(heading)
        self.accelaration = PVector(0.0, -0.02).rotate(heading) #Constant accelaration
        sensor_len = (0, -20)
        self.color = [random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)]
        self.sensors = [
            Sensor(PVector(*sensor_len).rotate(heading), self.pos, self.screen),
            Sensor(PVector(0, -100).rotate(heading), self.pos, self.screen),
            Sensor(PVector(*sensor_len).rotate(heading), self.pos, self.screen),
            Sensor(PVector(*sensor_len).rotate(heading+1/3*pi), self.pos, self.screen),
            Sensor(PVector(*sensor_len).rotate(heading+2/3*pi), self.pos, self.screen),
            Sensor(PVector(*sensor_len).rotate(heading+3/3*pi), self.pos, self.screen),
            Sensor(PVector(*sensor_len).rotate(heading+4/3*pi), self.pos, self.screen),
            Sensor(PVector(*sensor_len).rotate(heading+5/3*pi), self.pos, self.screen)
        ]
        #random.shuffle(self.color)
        self.color = tuple(self.color)

        #Determine if a car hasnt moved in a while
        self.num_of_zero_vel = 0

        #Has the car passed red and green checkpoint?
        self.has_passed_red = False
        self.has_passed_green = False
        
        # Init brain
        self.brain = Brain(len(self.sensors) + 1, 8, 4)
    
    def drive(self):
        "Adds the velocity to the cars position and updates the position of its sensors"
        self.pos = self.pos.add(self.velocity)
        
        # Update sensors position and get new pixel val
        pixel_vals = []
        for i in self.sensors:
            i.update_pos(self.velocity, self.pos)
            pixel_vals.append(i.get_pixel())

        # Neural network
        inputs = self.brain.input_processing(inputs=pixel_vals, velocity=self.velocity.length())
        outputs = self.brain.neuralnet(inputs)

        if outputs[0]: # Meaning accelerate
            self.accelarate()
        if outputs[1]: # Meaning brake
            self.brake()
        if outputs[2]: # Meaning accelerate
            self.turn(-.1) # TUrn left
        if outputs[3]: # Meaning brake
            self.turn(.1) # TUrn right
        
        self.has_passed_checkpoint()
        
    def accelarate(self):
        "Adds the accelaration to the velocity"
        self.velocity = self.velocity.add(self.accelaration)

    def brake(self):
        "Subtracts the accelaration from the velocity"
        if self.velocity.length() > self.accelaration.length():
            self.velocity = self.velocity.sub(self.accelaration)
        else:
            self.velocity.x = 0
            self.velocity.y = 0

    def turn(self, angle: float):
        """
        Rotates the velocity and the sensors of the car \n
        Takes one parameter, angle in radians.
        """
        if self.velocity.length() > 0:
            self.accelaration.rotate(angle)
            self.velocity.rotate(angle)
            for i in self.sensors:
                i.sens.rotate(angle)

            
    def draw(self):
        "Draws the car and its sensors in Pygame"
        pygame.draw.circle(self.screen, self.color, self.pos.repr(), self.size)
        #print(self.sensors[0].get_pixel())
        # for i in self.sensors:    
        #     pygame.draw.line(self.screen, self.color, self.pos.repr(), i.pos.repr(), 2)
    
    def is_dead(self):
        #Returns true if the car pos is outside the track
        try:
            coordinates = list(map(round, self.pos.repr()))
            color = self.track_img.get_at(coordinates)
        except:
            return True

        if self.velocity.length() == 0:
            #Count number of times the velocity is equal to zero
            self.num_of_zero_vel += 1

        if self.num_of_zero_vel > 60: return True #The car is dead, if the velocity has been 0 for 1 second

        if self.is_green(color[:3]) and not self.has_passed_red: #Has the car passed the green checkpoint without passing the red? (Drive the wrong way)
            return True

        try:
            return color == self.BLACK
        except:
            return False

        
        

    def has_passed_checkpoint(self):
        coordinates = list(map(round, self.pos.repr()))
        try:
            color_at_pos = self.track_img.get_at(coordinates)[:3]
        except:
            color_at_pos = (0,0,0)
        #print(color_at_pos, coordinates)
        if self.is_red(color_at_pos) and not self.has_passed_red:
            self.has_passed_red = True
        if self.is_green(color_at_pos) and self.has_passed_red:
            self.has_passed_green = True
        if self.is_white(color_at_pos) and self.has_passed_red and self.has_passed_green:
            self.has_passed_red, self.has_passed_green = False, False
            print('CHECKPOINT PAAAAASSED')
            return True
        return False
    
    def is_red(self, color):
        r, g, b = color
        if r > 200 and g < 100 and b < 100:
            return True
        return False
        

    def is_green(self, color):
        r, g, b = color
        if g > 200 and r < 100 and b < 100:
            return True
        return False
    
    def is_white(self, color):
        r, g, b = color
        return r > 200 and g > 200 and b > 200