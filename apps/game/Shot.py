class Shot(Entity):

	def onCreate(self,shtr):
		self.shooter = shtr
		self.totalShotTime = 100
		self.shotTime = self.totalShotTime
		self.damage = 10
		return False

	def setDamage(self,dmg):
		self.damage = dmg

	def setPosition(self,x,y):
		return False

	def tick(self):
		Entity.tick(self)
		hitList = calculateCollision()
		for obj in hitList:
			if (obj != self.shooter && obj.type == Fighter )
				self.shotTime == 0
				obj.onHit(self.damage)
				break
		self.shotTime = self.shotTime - 1
		if self.shotTime < 0:
			onDestroy()
		return False

	def draw(self):
		return False