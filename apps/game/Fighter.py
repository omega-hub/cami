print "Fighter.py file Reached"
import math

from Entity import Entity
class Fighter(Entity):

    def onCreate(self,x,y):
        Entity.onCreate(self,x,y)
        self.maxHealth = 100
        self.health = self.maxHealth
        self.numShots = 4
        self.currShots = 0
        self.fireRate = 10
        self.currFireRate = 0
        self.thrustVal = 1.0
        self.maxVelX = 10
        self.maxVelY = 10
        self.thrusting = False
        return False

    def tick(self,dt):
        Entity.tick(self,dt)
        if (self.thrusting):
            thurst()
        else:
            resetThrust()
        self.currFireRate = self.currFireRate - 1
        return False

    def thrust(self):
        self.accX = self.thrustVal * math.cos(self.angle)
        self.accY = self.thrustVal * math.sin(self.angle)

    def resetThrust(self):
        self.accX = 0
        self.accY = 0

    def fire(self):
        if (self.currShots > self.numShots and self.currFireRate <= 0):
            self.currShots = self.currShots + 1
            self.currFireRate = self.fireRate
            newShot = Shot()
            Game.createObj(newShot,self.x,self.y)
        return False

    def onHit(self,damage):
        self.health = self.health - damage
        if self.health < 0:
            onDeath()
            
    def onDeath(self):
        return False