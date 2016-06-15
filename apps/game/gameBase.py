import math
class Game:
	def initGame():
		self.screenWidth = 800
		self.screenHeight = 800
		self.entities = []
		return False

	def tick():
		for ent in self.entities:	
			ent.tick()
		return False

	def draw():
		for ent in self.entities:	
			ent.draw()

	def createObj(obj, x, y):
		self.entitites.append(obj)
		obj.setPosition(x,y)

	def destroyObj(obj):
		self.entities.remove(obj)

	def calculateCollision(obj):
		collideList = []
		for ent in self.entities:
			if (ent != obj && calculateDistance(obj,ent) < (obj.radius + ent.radius)):
				collideList.append(ent)

	def calculateDistance(obj1,obj2):
		dist = 0.0
		dist = math.sqrt(math.pow(obj1.y-obj2.y,2) + math.pow(obj1.x-obj2.x,2))
		return dist