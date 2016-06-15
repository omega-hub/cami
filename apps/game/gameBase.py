import math, time,random;


def initGame():
    print "Initializing Game"
    from Player import Player
    global screenWidth,screenHeight,lastFrameTime,entities,maxAsteroids,numAsteroids
    global asteroidSpeed,asteroidSpawnRate,maxSaucers,numSaucers,saucerSpawnRate,saucerSpeed
    global currentPlayer
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
            tick(dt)

def tick(dt):
    for ent in entities:   
        ent.tick(dt)
    calculateSpawn()
    draw()
    return False

def draw():
    for ent in entities:   
        ent.draw()

def calculateSpawn():
    import Asteroid
    if (numAsteroids + 1.0 <= maxAsteroids):
        if ((random.random() * 1000) >= asteroidSpawnRate):
            spaw
            nAsteroid()
    if (numSaucers + 1.0 <= maxSaucers):
        if ((random.random() * 1000) >= saucerSpawnRate):
            spawnSaucer()

def spawnAsteroid():
    import Saucer
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
    create(asteroid,x,y)

def spawnSaucer():
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
    asteroid = Saucer()
    create(asteroid,x,y)

def createObj(obj, x, y,args=[]):
    entities.append(obj)
    obj.onCreate(x,y,*args)
    obj.setPosition(x,y)

def destroyObj(obj):
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