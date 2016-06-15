class Shot(Entity):

	def onCreate(shtr):
		self.shooter = shtr
		self.totalShotTime = 100
		self.shotTime = self.totalShotTime
		self.damage = 10
		return False

	def setDamage(dmg):
		self.damage = dmg
		
	def setPosition(x,y):
		return False

	def tick():
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

	def dissispateShot():

		return False

	def testCollide():

	def draw():
		return False