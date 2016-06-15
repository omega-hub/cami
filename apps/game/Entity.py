import math 
import gameBase
class Entity:

    def onCreate(self,x,y):
        print "Entity created"
        self.radius = 10
        self.x = x
        self.y = y
        self.velX = 0
        self.velY = 0
        self.accX = 0
        self.accY = 0
        self.angle = 0
        return False

    def setPosition(self,x,y):
        self.x = x
        self.y = y
        return False

    def setAngle(self,angle):
        self.angle = angle
        
    def setVelocity(self,x,y):
        self.velX = x
        self.velY = y
        return False

    def setMaxVel(self,maxX,maxY):
        self.maxVelX = maxX
        self.maxVelY = maxY
        return False

    def setAcceleration(self,x,y):
        self.accX = x
        self.accY = y
        return False

    def tick(self,dt):
        self.x = self.x + self.velX
        if (self.x > (screenWidth)):
            self.x = 0
        if (self.x < 0):
            self.x = screenWidth
        self.y = self.y + self.velY
        if (self.y > (screenHeight)):
            self.y = 0
        if (self.y < 0):
            self.y = screenHeight
        if abs(self.velX + self.accX) < self.maxVelX:
            self.velX = self.velX + self.accX
        if abs(self.velY + self.accY) < self.maxVelY:
            self.velY = self.velY + self.accY
        return False

    def draw(self):
        return False