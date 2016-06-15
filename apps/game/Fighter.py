import math
class Fighter(Entity):

	def onCreate(x,y):
		self.maxHealth = 100
		self.health = self.maxHealth
		self.numShots = 4
		self.currShots = 0
		self.fireRate = 10
		self.currFireRate = 0
		self.x = x
		self.y = y
		self.velX = 0
		self.velY = 0
		self.accX = 0
		self.accY = 0
		self.angle = 0
		self.thrustVal = 1.0
		self.maxVelX = 10
		self.maxVelY = 10
		self.thrusting = False
		return False

	def tick():
		if (self.thrusting):
			thurst()
		else:
			resetThrust()
		self.currFireRate = self.currFireRate - 1
		if self.
		return False

	def thrust():
		self.accX = self.thrustVal * math.cos(self.angle)
		self.accY = self.thrustVal * math.sin(self.angle)

	def resetThrust():
		self.accX = 0
		self.accY = 0

	def fire():
		if (self.currShots > self.numShots && self.currFireRate <= 0):
			self.currShots = self.currShots + 1
			self.currFireRate = self.fireRate
			newShot = Shot()
			Game.createObj(newShot,self.x,self.y)
		return False

	def onHit(damage):
		self.health = self.health - damage
		if self.health < 0:
			onDeath()
			
	def onDeath():
		return False