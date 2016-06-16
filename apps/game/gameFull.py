import math, time,random;

screenWidth = 500
screenHeight = 500
lastFrameTime = 0
entities = []

#Adjustable Variables:
maxAsteroids = 3.0
numAsteroids = 0
asteroidSpawnRate = 5
asteroidSpeed = 4

maxSaucers = 2
numSaucers = 0
saucerSpawnRate = 1
saucerSpeed = 4

playerShotSpeed = 20

def initGame():
    print "Initializing Game"
    screenWidth = 500
    screenHeight = 500
    lastFrameTime = 0
    entities = []

    #Adjustable Variables:
    maxAsteroids = 3.0
    numAsteroids = 0
    asteroidSpawnRate = 5
    asteroidSpeed = 4

    maxSaucers = 2
    numSaucers = 0
    saucerSpawnRate = 1
    saucerSpeed = 4

    currentPlayer = Player()
    createObj(currentPlayer,200,200)
    return False

def gameLoop():
    global lastFrameTime
    while True:
        currentTime = time.time()
        dt = currentTime - lastFrameTime
        if (dt > (1.0/60.0)):
            lastFrameTime = currentTime
            gameTick(dt)

def gameTick(dt):
    for ent in entities:   
        ent.tick(dt)
    calculateSpawn()
    draw()
    return False

def draw():
    for ent in entities:   
        ent.draw()

def calculateSpawn():
    if (numAsteroids + 1.0 <= maxAsteroids):
        if ((random.random() * 1000) >= asteroidSpawnRate):
            spawnAsteroid()
    if (numSaucers + 1.0 <= maxSaucers):
        if ((random.random() * 1000) >= saucerSpawnRate):
            spawnSaucer()

def spawnAsteroid():
    global numAsteroids
    x = 0
    y = 0
    wallSide = random.random()
    if wallSide < 0.25:
        x = 0
        y = random.randint(0,screenHeight)
    elif wallSide > 0.25 and wallSide < 0.5:
        x = screenWidth
        y = random.randint(0,screenHeight)
    elif wallSide > 0.5 and wallSide < 0.75:
        y = 0
        x = random.randint(0,screenWidth)
    elif wallSide > 0.75:
        y = screenHeight
        x = random.randint(0,screenWidth)
    asteroid = Asteroid()
    numAsteroids = numAsteroids + 1
    createObj(asteroid,x,y)


def spawnSaucer():
    global numSaucers
    x = 0
    y = 0
    wallSide = random.random()
    if wallSide < 0.25:
        x = 0
        y = random.randint(0,screenHeight)
    elif wallSide > 0.25 and wallSide < 0.5:
        x = screenWidth
        y = random.randint(0,screenHeight)
    elif wallSide > 0.5 and wallSide < 0.75:
        y = 0
        x = random.randint(0,screenWidth)
    elif wallSide > 0.75:
        y = screenHeight
        x = random.randint(0,screenWidth)
    numSaucers = numAsteroids + 1
    saucer = Saucer()
    createObj(saucer,x,y)

def createObj(obj, x, y,args=[]):
    entities.append(obj)
    obj.onCreate(x,y,*args)
    obj.setPosition(x,y)

def destroyObj(obj):
    obj.onDestroy()
    entities.remove(obj)

def calculateCollisions(obj):
    collideList = []
    for ent in entities:
        if (ent != obj and calculateDistance(obj,ent) < (obj.radius + ent.radius)):
            collideList.append(ent)
    return collideList

def calculateDistance(obj1,obj2):
    dist = 0.0
    dist = math.sqrt(math.pow(obj1.y-obj2.y,2) + math.pow(obj1.x-obj2.x,2))
    return dist
def gameOver():
    print "GameOver"

################

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
        self.maxVelX = 10
        self.maxVelY = 10
        self.damage = 30
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

##########FIghter###########

print "Fighter.py file Reached"
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
        self.thrusting = False
        self.invincibleTime = 100
        return False

    def tick(self,dt):
        Entity.tick(self,dt)
        if (self.thrusting):
            self.thurst()
        else:
            self.resetThrust()
        self.currFireRate = self.currFireRate - 1
        self.invincibleTime = self.invincibleTime - 1
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
            Game.createObj(newShot,self.x,self.y,[self])
            velX = math.cos(self.angle) * playerShotSpeed
            velX = math.cos(self.angle) * playerShotSpeed
            newShot.setVelocity(velX,velY)

        return False

    def onHit(self,damage):
        if self.invincibleTime <= 0:
            self.invincibleTime = 60
            self.health = self.health - damage
            if self.health < 0:
                onDeath()
            
    def onDeath(self):
        print "Object has died"
        game.onDestroy(self)
        return False

####################Player###################

print "Player.py file Reached"
class Player(Fighter):

    def __init__(self):
        print "Player Character initialized---------"

    def onCreate(self,x,y):
        Fighter.onCreate(self,x,y)
        self.health = 100
        return False

    def onDeath(self):
        gameOver()
        return False

##################Asteroid#############

class Asteroid(Fighter):
    def onCreate(self,x,y):
        Fighter.onCreate(self,x,y)
        self.health = 50
        self.damage = 50
        self.size = 1.0

        angle = random.random()*math.pi
        spd = random.uniform(asteroidSpeed/2,asteroidSpeed)
        newVelX = spd * math.cos(angle)
        newVelY = spd * math.cos(angle)
        self.setVelocity(newVelX,newVelY)

    def setSize(size):
        self.size = size


    def tick(self,dt):
        Entity.tick(self,dt)
        hitList = calculateCollisions(self)
        for obj in hitList:
            if (type(obj) is Fighter):
                obj.onHit(self.damage * self.size)
                self.onHit(obj.damage)
                break
        
    def onDeath():
        print "Asteroid Destroyed"
        if self.size > 0.25:
            print "New Asteroids being created from debris"
            asteroid1 = Asteroid()
            createObj(asteroid1,self.x,self.y)
            asteroid1.setSize(self.size/2)

            asteroid2 = Asteroid()
            createObj(asteroid2,self.x,self.y)
            asteroid2.setSize(self.size/2)
        return False

########Shot######################

class Shot(Entity):

    def onCreate(self,x,y,shooter):
        Entity.onCreate(self,x,y)
        self.shooter = shtr
        self.totalShotTime = 100
        self.shotTime = self.totalShotTime
        self.damage = 10
        return False

    def setDamage(self,dmg):
        self.damage = dmg

    def setPosition(self,x,y):
        return False

    def tick(self,dt):
        Entity.tick(self,dt)
        hitList = calculateCollisions(self)
        for obj in hitList:
            if (obj != self.shooter and type(obj) is Fighter):
                self.shotTime = 0
                obj.onHit(self.damage)
                break
        self.shotTime = self.shotTime - 1
        if self.shotTime < 0:
            onDestroy()
        return False

    def onDestroy(self):
        Entity.onDestroy(self)
        self.shooter.currShots = self.shooter.currShots - 1


    def draw(self):
        return False

##############Fighter##############

print "Player.py file Reached"
class Saucer(Fighter):

    def __init__(self):
        print "Saucer Spawned"

    def onCreate(self,x,y):
        Fighter.onCreate(self,x,y)
        self.health = 100

        angle = random.random()*math.pi
        spd = random.uniform(saucerSpeed/2,saucerSpeed)
        newVelX = spd * math.cos(angle)
        newVelY = spd * math.cos(angle)
        self.setVelocity(newVelX,newVelY)
