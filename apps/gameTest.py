from omega import *
from cyclops import *
import os, glob,math, time, random

print "Initializing Camera 2"
# camera = getDefaultCamera()
# camera.setPosition(0,0,0)
# camera.setBackgroundColor(Color('blue'))

# redColor = Color("red")
# whiteColor = Color("white")

l1 = Light.create()
l1.setPosition(0, 0, 0)
l1.setColor(Color(1, 1, 0.8, 1))
l1.setAmbient(Color(0,0,0.1,1))
l1.setLightType(LightType.Spot)
l1.setLightDirection(Vector3(0, 0, -1))
random.seed("pinata")
# testObj = BoxShape.create(100, 100, 100)
# testObj.getMaterial().setColor(redColor, whiteColor)
# testObj.setPosition(Vector3(0, 0, 4))

# box = BoxShape.create(0.8, 0.8, 0.8)
# box.setPosition(Vector3(0, 1, -20))

# Apply an emissive textured effect (no lighting)
#box.setEffect("textured -v emissive -d cyclops/test/omega-transparent.png")

screenWidth = 140
screenHeight = 100
lastFrameTime = 0
entities = []

#Adjustable Variables:
maxAsteroids = 4.0
numAsteroids = 0
asteroidSpawnRate = 5
asteroidSpeed = 0.5

maxSaucers = 2
numSaucers = 0
saucerSpawnRate = 1
saucerSpeed = 0.4

playerShotSpeed = 1
playerFireRate = 5
enemyShotFrequency = 0
enemyAccuracy = 1.0
currentPlayer = False
enemyMaxShots = 3
shotLifetime = 170
shotDamage = 10

def initGame():
    print "Initializing Game"
    screenWidth = 100
    screenHeight = 100
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
    global currentPlayer
    currentPlayer = Player()
    createObj(currentPlayer,screenWidth/2,screenHeight/2)
    return False

def gameLoop(t,dt):
    global lastFrameTime
    #currentTime = time.time()
    change = t - lastFrameTime
    if (change > (1.0/60.0)):
        lastFrameTime = t
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
    asteroid.setAsteroidSize(1.0)


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
    print "destroying Object"
    obj.onDestroy()
    print "done with onDestroy"
    entities.remove(obj)
    print "Removed Object?"


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
        #print "Entity created"
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

    def onDestroy(self):
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

    def draw(self):
        if (self.model):
            # print "X: " , (self.x- screenWidth/2)
            # print "Y: " , (self.y- screenHeight/2)
            self.model.setPosition(self.x - screenWidth/2 ,self.y - screenHeight/2 - 10,-50)
        return False

##########FIghter###########

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
        self.isFighter = True
        return False

    def tick(self,dt):
        Entity.tick(self,dt)
        if (self.thrusting):
            self.thurst()
        else:
            self.resetThrust()
        self.currFireRate = self.currFireRate - 1
        self.invincibleTime = self.invincibleTime - 1

    def thrust(self):
        self.accX = self.thrustVal * math.cos(self.angle)
        self.accY = self.thrustVal * math.sin(self.angle)

    def resetThrust(self):
        self.accX = 0
        self.accY = 0

    def fire(self,fireAng =False):

        if (self.currShots < self.maxShots and self.currFireRate <= 0):
            self.currShots = self.currShots + 1
            print "Successful Shot fired"
            self.currFireRate = self.fireRate
            newShot = Shot()
            # print "enemy firing shot"
            createObj(newShot,self.x,self.y,[self])
            if fireAng == False:
                fireAng = self.angle
            velX = math.cos(fireAng) * playerShotSpeed
            velY = math.sin(fireAng) * playerShotSpeed
            newShot.setVelocity(velX,velY)

    def onHit(self,damage):
        if self.invincibleTime <= 0:
            self.invincibleTime = 60
            self.health = self.health - damage
            if self.health < 0:
                destroyObj(self)

####################Player###################

class Player(Fighter):

    def __init__(self):
        print "Player Character initialized---------"

    def onCreate(self,x,y):
        Fighter.onCreate(self,x,y)
        self.model = BoxShape.create(1.0,1.0,1.0)
        self.radius = 0.2
        self.health = 100
        return False

    def onDestroy(self):
        gameOver()
        return False

##################Asteroid#############

class Asteroid(Fighter):
    def onCreate(self,x,y):
        Fighter.onCreate(self,x,y)
        print "Asteroid Created"
        self.health = 50
        self.damage = 50
        self.invincibleTime = 0
        self.size = 1.0
        self.model = False


        angle = random.random()*math.pi
        spd = random.uniform(asteroidSpeed/2,asteroidSpeed)
        newVelX = spd * math.cos(angle)
        newVelY = spd * math.cos(angle)
        self.setVelocity(newVelX,newVelY)

    def setAsteroidSize(self,size):
        self.size = size
        self.model = SphereShape.create(size * 6,4)
        self.radius = 6 * size



    def tick(self,dt):
        Fighter.tick(self,dt)
        hitList = calculateCollisions(self)
        for obj in hitList:
            if (obj.isFighter):
                obj.onHit(self.damage * self.size)
                self.onHit(obj.damage)
                break
        
    def onDestroy(self):
        Entity.onDestroy(self)
        print "Asteroid Destroyed"
        if self.size > 0.25:
            print "New Asteroids being created from debris"
            asteroid1 = Asteroid()
            createObj(asteroid1,self.x,self.y)
            asteroid1.setAsteroidSize(self.size/2)

            asteroid2 = Asteroid()
            createObj(asteroid2,self.x,self.y)
            asteroid2.setAsteroidSize(self.size/2)

########Shot######################

class Shot(Entity):

    def onCreate(self,x,y,shooter):
        Entity.onCreate(self,x,y)
        print "Shot Created"
        self.model = SphereShape.create(1,4)

        self.shooter = shooter
        self.radius = 1
        self.totalShotTime = shotLifetime
        self.shotTime = self.totalShotTime
        self.damage = shotDamage
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
            destroyObj(self)

    def onDestroy(self):
        print "Shot is being destroyed"
        Entity.onDestroy(self)
        self.shooter.currShots = self.shooter.currShots - 1

##############Fighter##############

class Saucer(Fighter):

    def __init__(self):
        print "Saucer Spawned"

    def onCreate(self,x,y):
        Fighter.onCreate(self,x,y)
        self.radius = 2.5
        self.model = BoxShape.create(5.0,5.0,5.0)
        self.health = 100
        angle = random.random()*math.pi
        spd = random.uniform(saucerSpeed/2,saucerSpeed)
        newVelX = spd * math.cos(angle)
        newVelY = spd * math.cos(angle)
        self.setVelocity(newVelX,newVelY)
        self.maxShots = enemyMaxShots

    def tick(self,dt):
        Fighter.tick(self,dt)
        # print "saucer tick"
        if ((random.random() * 1000) <= enemyShotFrequency):
            # print self.y
            # print currentPlayer.y
            # print currentPlayer.y - self.y
            # print currentPlayer.x - self.x
            # print math.atan2(currentPlayer.y - self.y, currentPlayer.x - self.x)
            # print enemyAccuracy
            # print (random.random()* (1.0 - enemyAccuracy) - ((1.0-enemyAccuracy)/2))
            targetAngle = math.atan2(currentPlayer.y - self.y, currentPlayer.x - self.x) + (random.random()* (1.0 - enemyAccuracy) - ((1.0-enemyAccuracy)/2))
            # print "Target ANgle: ", targetAngle
            self.fire(targetAngle)

initGame()

def onUpdate(frame, t, dt):
    gameLoop(t,dt)
setUpdateFunction(onUpdate)