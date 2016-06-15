import math 
class Entity:

	def onCreate():
		self.radius = 10
		return False

	def setPosition(x,y):
		self.x = x
		self.y = y
		return False

	def setAngle(angle):
		self.angle = angle
		
	def setVelocity(x,y):
		self.velX = x
		self.velY = y
		return False

	def setMaxVel(maxX,maxY)
		self.maxVelX = maxX
		self.maxVelY = maxY
		return False

	def setAcceleration(x,y):
		self.accX = x
		self.accY = y
		return False

	def tick():
		self.x = self.x + self.velX
		if (self.x > (Game.screenWidth)):
			self.x = 0
		if (self.x < 0):
			self.x = Game.screenWidth
		self.y = self.y + self.velY
		if (self.y > (Game.screenHeight)):
			self.y = 0
		if (self.y < 0):
			self.y = Game.screenHeight
		if abs(self.velX + self.accX) < self.maxVelX:
			self.velX = self.velX + self.accX
		if abs(self.velY + self.accY) < self.maxVelY:
			self.velY = self.velY + self.accY
		return False

	def draw():
		return False