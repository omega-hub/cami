from omega import *
from cyclops import *
from omegaToolkit import *
import os, glob,math, time, random

ui = UiModule.createAndInitialize().getUi()
l = Label.create(ui)
l.setStyleValue('font','fonts/arial.ttf 120')
l.setPosition(Vector2(4, 26))
newNumber = 80
l2 = Label.create(ui)
l2.setStyleValue('font','fonts/arial.ttf 120')
l2.setPosition(Vector2(4, 140))

overText = Label.create(ui)
finalScore = Label.create(ui)

# camera = getDefaultCamera()
# camera.setPosition(0,0,0)
# camera.setBackgroundColor(Color('blue'))

redColor = Color("red")
greenColor = Color("green")

# whiteColor = Color("white")

l1 = Light.create()
l1.setPosition(0, 0, -0.5)
l1.setColor(Color(1, 1, 0.8, 1))
l1.setAmbient(Color(0.1,0.1,0.1,1))
l1.setLightType(LightType.Spot)
l1.setLightDirection(Vector3(0, 0, -1))
random.seed("randomseed")

skybox = Skybox()
skybox.loadCubeMap("../data/space", "png")
getSceneManager().setSkyBox(skybox)
# testObj = BoxShape.create(100, 100, 100)
# testObj.getMaterial().setColor(redColor, whiteColor)
# testObj.setPosition(Vector3(0, 0, 4))

# box = BoxShape.create(0.8, 0.8, 0.8)
# box.setPosition(Vector3(0, 1, -20))

# Apply an emissive textured effect (no lighting)
#box.setEffect("textured -v emissive -d cyclops/test/omega-transparent.png")

screenWidth = 70
screenHeight = 50
lastFrameTime = 0
entities = []
currentPlayer = False
score = 0
modelsLoaded = 0
#Adjustable Variables:
maxAsteroids = 4.0
numAsteroids = 0
asteroidSpawnRate = 20
asteroidCurrPeriod = 0
asteroidSpeed = 0.5

maxSaucers = 2.0
numSaucers = 0
saucerSpawnRate = 10
saucerCurrPeriod = 0

saucerSpeed = 0.2

enemyFireFrequency = 10
enemyAccuracy = 1.0
enemyMaxShots = 3
shotLifetime = 50
shotDamage = 10
playerShotDamage = 100

playerHealth = 100
playerMaxSpeed = 0.8
playerShotSpeed = 2.0
playerFireRate = 10
playerMaxShots = 20
playerThrustVal = 0.05
enemyShotSpeed = 0.35
deceleration = 0.975
gameOver = False

def calljs(methodname, data):
    mc = getMissionControlClient()
    if(mc != None):
        mc.postCommand('@server::calljs ' + methodname + ' ' + str(data))

def restartGame():
    global entities, gameOver
    if (gameOver == False):
        destroyObj(currentPlayer)
    for ent in entities:
        destroyObj(ent)
    initGame()

def initGame():
    global gameOver
    gameOver = False
    isGameOver = []
    isGameOver.append('started')
    calljs('isGameOver',isGameOver)
    screenWidth = 100
    screenHeight = 100
    lastFrameTime = 0
    global score
    score = 0
    entities = []

    #Adjustable Variables:
    maxAsteroids = 3.0
    numAsteroids = 0
    asteroidSpawnRate = 5
    asteroidSpeed = 4

    maxSaucers = 2.0
    numSaucers = 0
    saucerSpawnRate = 1
    saucerSpeed = 4
    global currentPlayer
    currentPlayer = Player()
    createObj(currentPlayer,screenWidth/4,screenHeight/4)
    setUpdateFunction(onUpdate)
    info = []
    info.append(score)
    calljs('onPythonInit', info)
    overText.setPosition(Vector2(-200, -800))
    finalScore.setPosition(Vector2(-200, -1000))

def gameLoop(t,dt):
    global lastFrameTime, gameOver
    #currentTime = time.time()
    change = t - lastFrameTime
    if (change > (1.0/60.0)):
        lastFrameTime = t
        if (gameOver):
            gameOverTick()
        else:
            gameTick(dt)

def gameTick(dt):
    for ent in entities:   
        ent.tick(dt)
    calculateSpawn()
    draw()
    global l2, l, currentPlayer,score
    newString = "Health: " + str(currentPlayer.health)
    l2.setText(newString)
    newString = "Score: " + str(score)
    l.setText(newString)
    info = []
    info.append(score)
    info.append(currentPlayer.health)
    calljs('updateHealthScore',info)


def requestStatusUpdate():
    global currentPlayer
    if currentPlayer:
        global score, currentPlayer
        info = []
        info.append(score)
        info.append(currentPlayer.health)
        calljs('updateHealthScore',info)

def draw():
    for ent in entities:   
        ent.draw()

def calculateSpawn():
    global asteroidCurrPeriod, saucerCurrPeriod
    asteroidCurrPeriod -= 1
    saucerCurrPeriod -= 1
    if (numAsteroids + 1.0 <= maxAsteroids):
        if (asteroidSpawnRate != 0 and asteroidCurrPeriod <= 0):
            spawnAsteroid()
    if (numSaucers + 1.0 <= maxSaucers):
        if (saucerSpawnRate != 0 and saucerCurrPeriod <= 0):
            spawnSaucer()

def spawnAsteroid():
    global numAsteroids, asteroidCurrPeriod, asteroidSpawnRate
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
    if asteroidSpawnRate != 0:
        asteroidCurrPeriod = (600 - (asteroidSpawnRate * 6))


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
    numSaucers = numSaucers + 1
    saucer = Saucer()
    createObj(saucer,x,y)
    if saucerSpawnRate != 0:
        saucerCurrPeriod = (600 - (saucerSpawnRate * 6))

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

def gameOverTick():
    overText.setStyleValue('font','fonts/arial.ttf 240')
    overText.setPosition(Vector2(800, 1200))
    overText.setText("Game Over: Restart button from Menu")
    finalScore.setStyleValue('font','fonts/arial.ttf 180')
    finalScore.setPosition(Vector2(1000, 1400))
    newString = "Score: " + str(score)
    finalScore.setText(newString)
    isGameOver = []
    isGameOver.append('over')
    calljs('isGameOver',isGameOver)

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
        self.maxVelX = 9000
        self.maxVelY = 9000
        self.damage = 30
        self.isFighter = False
        return False

    def onDestroy(self):
        self.model.getParent().removeChildByRef(self.model)
        return False

    def setPosition(self,x,y):
        self.x = x
        self.y = y
        return False

    def setAngle(self,angle):
        self.model.resetOrientation()
        self.model.pitch(1.57)
        self.model.yaw(angle)
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
        else:
            if self.velX > 0:
                self.velX = self.maxVelX
            else:
                self.velX = -self.maxVelX
        if abs(self.velY + self.accY) < self.maxVelY: 
            self.velY = self.velY + self.accY
        else:
            if self.velY > 0:
                self.velY = self.maxVelY
            else:
                self.velY = -self.maxVelY

    def draw(self):
        if (self.model):
            # print "X: " , (self.x- screenWidth/2)
            # print "Y: " , (self.y- screenHeight/2)
            self.model.setPosition(self.x - screenWidth/2  ,self.y - screenHeight/2 ,-25)
        return False

##########FIghter###########

class Fighter(Entity):

    def onCreate(self,x,y):
        Entity.onCreate(self,x,y)
        self.maxHealth = 100
        self.health = self.maxHealth
        self.numShots = 4
        self.currShots = 0
        self.currFirePeriod = 0
        self.thrustVal = playerThrustVal
        self.thrusting = False
        self.invincibleTime = 0
        self.isFighter = True
        return False

    def tick(self,dt):
        Entity.tick(self,dt)
        if (self.thrusting):
            self.thrust()
        else:
            self.resetThrust()
        self.currFirePeriod = self.currFirePeriod - 1
        self.invincibleTime = self.invincibleTime - 1
        self.thrusting = False

    def thrust(self):
        self.accX = self.thrustVal * math.cos(self.angle)
        self.accY = self.thrustVal * math.sin(self.angle)
        self.thrusting = True

    def resetThrust(self):
        self.accX = 0
        self.accY = 0

    def fire(self,fireAng =False):
        if (self.currShots < self.maxShots and self.currFirePeriod <= 0):
            self.currShots = self.currShots + 1

            global currentPlayer
            if self == currentPlayer:
                self.currFirePeriod = (22 - playerFireRate)
            else:
                self.currFirePeriod = 10
            newShot = Shot()

            createObj(newShot,(self.x *  1.0),(self.y * 1.0),[self])
            if fireAng == False:
                fireAng = self.angle
            if (self == currentPlayer):
                velX = math.cos(fireAng * 1.0) * (playerShotSpeed * 1.0)
                velY = math.sin(fireAng * 1.0) * (playerShotSpeed * 1.0)
            else:
                velX = math.cos(fireAng * 1.0) * (enemyShotSpeed * 1.0)
                velY = math.sin(fireAng * 1.0) * (enemyShotSpeed * 1.0)
            newShot.setVelocity(velX,velY)

    def onHit(self,damage):
        global currentPlayer
        if self.invincibleTime <= 0:
            if self == currentPlayer:
                self.invincibleTime = 60
            else:
                self.invincibleTime = 20
            self.health = self.health - damage
            if self.health <= 0:
                destroyObj(self)

####################Player###################

class Player(Fighter):

    def __init__(self):
        print "Player Character initialized---------"

    def onCreate(self,x,y):
        Fighter.onCreate(self,x,y)
        #self.model = BoxShape.create(2.0,1.0,1.0)
        self.radius = 2
        self.maxHealth = playerHealth
        self.health = self.maxHealth
        self.maxShots = playerMaxShots
        self.invincibleTime = 100
        self.prepareModel()
        self.setAngle(0)
        self.maxVelX = playerMaxSpeed
        self.maxVelY = playerMaxSpeed

    def prepareModel(self):
        self.model = StaticObject.create("ship.fbx")
        self.model.setScale(0.4,0.4,0.4)
        mat = self.model.getMaterial()
        mat.setProgram("textured")
        print "Finished player model"

    def tick(self,dt):
        Fighter.tick(self,dt)
        self.velX = self.velX * deceleration
        self.velY = self.velY * deceleration
        # self.thrust()or
        # self.fire()

    def onDestroy(self):
        Entity.onDestroy(self)
        global gameOver
        gameOver = True

##################Asteroid#############

class Asteroid(Fighter):
    def onCreate(self,x,y):
        Fighter.onCreate(self,x,y)
        self.health = 50
        self.damage = 50
        self.invincibleTime = 20
        self.size = 1.0
        self.model = False

        angle = random.random()*math.pi
        spd = random.uniform(asteroidSpeed/2.0,asteroidSpeed)
        newVelX = spd * math.cos(angle)
        newVelY = spd * math.cos(angle)
        self.setVelocity(newVelX,newVelY)

    def setAsteroidSize(self,size):
        self.size = size
        self.model = StaticObject.create("asteroid2.fbx")
        scale = size * 1.2
        self.model.setScale(scale,scale,scale)
        mat = self.model.getMaterial()
        mat.setProgram("textured")
        self.radius = 6 * size

    def tick(self,dt):
        Fighter.tick(self,dt)
        hitList = calculateCollisions(self)
        # self.model.roll(0.02)
        # self.model.yaw(0.02)
        for obj in hitList:
            if (obj.isFighter):
                obj.onHit(self.damage * self.size)
                self.onHit(obj.damage)
                break
        
    def onDestroy(self):
        global numAsteroids,score
        Entity.onDestroy(self)
        if self.size > 0.25:
            if self.size > 0.75:
                score = score + 20
            else:
                score = score + 50
            asteroid1 = Asteroid()
            createObj(asteroid1,self.x,self.y)
            asteroid1.setAsteroidSize(self.size/2)

            asteroid2 = Asteroid()
            createObj(asteroid2,self.x,self.y)
            asteroid2.setAsteroidSize(self.size/2)
        else:
            score = score + 200
            numAsteroids = numAsteroids - 0.25

########Shot######################

class Shot(Entity):

    def onCreate(self,x,y,shooter):
        global currentPlayer
        Entity.onCreate(self,x,y)
        self.model = SphereShape.create(0.5,4)
        mat = self.model.getMaterial()
        if (shooter == currentPlayer):
            mat.setColor(greenColor,greenColor)
        else:
            mat.setColor(redColor,redColor)
        mat.setProgram("colored")
        self.shooter = shooter
        self.radius = 0.5
        self.totalShotTime = shotLifetime
        self.shotTime = self.totalShotTime
        if self.shooter == currentPlayer:
            self.damage = playerShotDamage
        else:
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
            if (obj != self.shooter and obj.isFighter):
                self.shotTime = 0
                obj.onHit(self.damage)
                break
        self.shotTime = self.shotTime - 1
        if self.shotTime < 0:
            destroyObj(self)

    def onDestroy(self):
        Entity.onDestroy(self)
        self.shooter.currShots = self.shooter.currShots - 1

##############Fighter##############

class Saucer(Fighter):

    # def __init__(self):
        # print "Saucer Spawned"

    def onCreate(self,x,y):
        Fighter.onCreate(self,x,y)
        self.radius = 2.5
        self.model = StaticObject.create("ufo.fbx")
        self.model.setScale(0.7,0.7,0.7)
        mat = self.model.getMaterial()
        mat.setProgram("textured")

        self.health = 50
        angle = random.random()*math.pi
        spd = random.uniform(saucerSpeed/2,saucerSpeed)
        newVelX = spd * math.cos(angle)
        newVelY = spd * math.cos(angle)
        self.setVelocity(newVelX,newVelY)
        self.maxShots = enemyMaxShots

    def tick(self,dt):
        Fighter.tick(self,dt)
        global currentPlayer
        # print "saucer tick"
        if ((random.random() * 1000) <= enemyFireFrequency):
            # print self.y
            # print currentPlayer.y
            # print currentPlayer.y - self.y
            # print currentPlayer.x - self.x
            # print math.atan2(currentPlayer.y - self.y, currentPlayer.x - self.x)
            # print enemyAccuracy
            # print (random.random()* (1.0 - enemyAccuracy) - ((1.0-enemyAccuracy)/2))
            targetAngle = math.atan2(currentPlayer.y - self.y, currentPlayer.x - self.x)
            randomVal = random.random()
            targetAngle += (randomVal* (1.0 - enemyAccuracy) - ((1.0-enemyAccuracy)/2))
            # print "Target ANgle: ", targetAngle
            self.fire(targetAngle)

    def onDestroy(self):
        global numSaucers,score
        Entity.onDestroy(self)
        score = score + 200
        numSaucers = numSaucers - 1.0

###############Game Settings###############

def setMaxAsteroids(num):
    global maxAsteroids
    print "setting max asteroids to " , num
    maxAsteroids  = num

def setAsteroidSpawnRate(num):
    global asteroidSpawnRate
    print "setting asteroid Spawn Rate to " , num
    asteroidSpawnRate = num

def setAsteroidSpeed(num):
    global asteroidSpeed
    print "setting asteroid speed to " , num
    asteroidSpeed = (num/6.0)

def setMaxSaucers(num):
    global maxSaucers
    print "setting max Saucers to " , num
    maxSaucers  = num

def setSaucerSpawnRate(num):
    global saucerSpawnRate
    print "setting saucer spawn rate to " , num
    saucerSpawnRate = num

def setSaucerShotFrequency(num):
    global enemyFireFrequency
    print "setting enemy shot Frequency to " , num
    enemyFireFrequency = num

def setEnemyAccuracy(num):
    global enemyAccuracy
    print "setting enemy accuracy to " , num
    enemyAccuracy = num

def setEnemyShotSpeed(num):
    global enemyShotSpeed
    print "setting enemy shot Speed to " , num
    enemyShotSpeed = num

def setPlayerShotSpeed(num):
    global playerShotSpeed
    print "setting player shot Speed to " , num
    playerShotSpeed = (num/100.0)

def setPlayerMaxHealth(num):
    global playerHealth, currentPlayer
    print "setting player max health to " , num
    playerHealth = num
    currentPlayer.health = playerHealth

def setPlayerSpeed(num):
    global playerMaxSpeed,currentPlayer
    print "setting player max speed to " , num
    playerMaxSpeed = (num/6.0)
    currentPlayer.maxVelX = playerMaxSpeed
    currentPlayer.maxVelY = playerMaxSpeed

def setPlayerThrustVal(num):
    global playerThrustVal,currentPlayer
    print "setting player thrust val to " , num
    playerThrustVal = (num/4.0)
    currentPlayer.thrustVal = playerThrustVal

def setPlayerFireRate(num):
    global playerFireRate
    print "setting player firerate to " , num
    playerFireRate = num

def setShotLifeTime(num):
    global shotLifetime
    print "setting shot life time to " , num
    shotLifetime = num

def onReload():
    return True

##################### Model Loading ###################

def LoadModel(modelName):
    print "Loading Model: " , modelName
    path = "../data/" + modelName
    model = ModelInfo()
    model.name = modelName
    model.path = path
    model.generateNormals = False
    model.optimize = False
    model.size = 10
    getSceneManager().loadModel(model)
    onModelLoaded()

def onModelLoaded():
    print "Finished loading model"
    global modelsLoaded
    modelsLoaded = modelsLoaded + 1
    if modelsLoaded >= 3:
        initGame()

################Game Initialization ################

def loadModels():
    LoadModel("ship.fbx")
    LoadModel("asteroid2.fbx")
    LoadModel("ufo.fbx")

def onUpdate(frame, t, dt):
    gameLoop(t,dt)
loadModels()
