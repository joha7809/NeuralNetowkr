import math

class PVector:
    def __init__(self, x,y):
        self.x = x
        self.y = y

    def rotate(self, radians: float):
        x = self.x * math.cos(radians) - self.y * math.sin(radians)
        y = self.x * math.sin(radians) + self.y * math.cos(radians)
        self.x = x
        self.y = y
        return PVector(x,y)
    
    def add(self, pvector):
        x = self.x + pvector.x
        y = self.y + pvector.y
        return PVector(x, y)
    
    def sub(self, pvector):
        x = self.x - pvector.x
        y = self.y - pvector.y
        return PVector(x, y)

    def mul(self, i: float):
        x = self.x * i
        y = self.y * i
        return PVector(x,y)
   
    def length(self):
        length = (self.x**2 + self.y**2)**0.5
        return length
    
    def normalize(self):
        l = self.length()
        x = self.x/l
        y = self.y/l
        return PVector(x,y)
        
    def repr(self):
        return (self.x, self.y)
