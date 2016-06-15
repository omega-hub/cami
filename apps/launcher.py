from omegaToolkit import *
from cyclops import *
from oav import *
import porthole

uim = UiModule.createAndInitialize()
AppDict = {}
numApps = 0
currApp = False
#label = Label.create(uim.getUi())

#label.setText('Hello Launcher')
#label.setFont('fonts/arial.ttf 40')

# cam = getDefaultCamera()
# cam.setBackgroundColor(Color('red'))
# cam.setControllerEnabled(False)

# print("Test print, this is in my launcher")
# p = SceneNode.create('pivot')
# tls = []
# for x in range(0, 6):
#     for y in range(0, 6):
#         pl = PlaneShape.create(0.53, 0.3)
#         pl.getMaterial().setProgram('colored')
#         pl.getMaterial().setAdditive(True)
#         pl.getMaterial().setTransparent(True)
#         pl.getMaterial().setDepthTestEnabled(False)
#         pl.getMaterial().setColor(Color('black'), Color(float(x) / 5, 1 - float(y) / 5, 1, 1))
#         pl.setPosition(- 3.18 + x * 1.06, 1.55 -1.8 + y * 0.6, -2)
#         p.addChild(pl)
#         tls.append(pl)

# def onUpdate(frame, time, dt):
#     sp = 0.1 * dt
    
#     i = 1
#     for t in tls:
#         t.yaw(sp * i)
#         t.pitch(sp * i)
#         i += 0.2

# setUpdateFunction(onUpdate)
#toggleStereo()
v = None
#getSceneManager().getCompositingLayer().loadCompositor('cyclops/common/compositor/motionblur.xml')
if( not isMaster()):
    uim = UiModule.createAndInitialize()
    global v
    v = VideoStream()

    v.open('/opt/data/Videos/Screensaver.mov')
    #v.open('/opt/data/Videos/4ktest.mp4')
    img = Image.create(uim.getUi())
    img.setData(v.getPixels())
    img.setAutosize(False) # Inserting these resulted in it not working
    img.setSize(uim.getUi().getSize())
    img.setStereo(True)
    v.play()


# stores the id of the last web client connected. This is
# the client in charge of controlling the running application.
appControllerClient = ""

mc = getMissionControlClient()

# Setup web server
if(isMaster()):
    porthole.initialize(4080, 'index.html')
    ps = porthole.getService()
    ps.setConnectedCommand('onClientConnected("%id%")')
    ps.setDisconnectedCommand('onClientDisconnected("%id%")')


# This quick command is used to easily forward js commands to clients from
# launched apps
addQuickCommand('calljs', "ps.sendjs(\"%1%({0})\".format(%2%), appControllerClient)", 2, 'call js on porthole clients')

def startApplication(clientId, appName):
    global appControllerClient, numApps, AppDict, currApp
    print "Preparing to Launch " + appName
    appControllerClient = clientId
    # 'app' is the application identifier, we can use it to send mission controlling
    # messages to the app using it.
    if currApp:
        hideApplication(currApp)
    broadcastCommand('hideLauncher()')
    currApp = appName
    if appName in AppDict:
        print "Application already loaded, showing application"
        showApplication(appName)
    else:
        numApps = numApps + 1
        print "Spawning new instance of " + appName
        mc.spawn(appName, numApps, appName + '.py', 'default.cfg')
        AppDict[appName] = True
    

def onClientConnected(clientId):
    print "client connected: " + clientId
    
def onClientDisconnected(clientId):
    global appControllerClient
    #print "Client for the following App disconnected: " + str(appName)
    # web client disconnected: stop application and go back to launcher.
    print appControllerClient
    print clientId
    if(clientId == appControllerClient):
        print "hiding app: " + clientId
        #hideApplication(appName)
        # mc.postCommand('@app: :q')
        broadcastCommand('showLauncher()')



    # Always force a refresh of the html/js files, so we can quickly test
    # code changes by refreshing an app web page.
    #ps.clearCache()    
        
        
def hideLauncher():
    setTilesEnabled(0, 0, 5, 5, False)
    if(not isMaster()): v.setPlaying(False)
    
def showLauncher():
    setTilesEnabled(0, 0, 5, 5, True)
    if(not isMaster()): v.setPlaying(True)

def showApplication(appName):
    print "Showing application: " + str(appName)
    if appName in AppDict:
        mc.postCommand('@' + appName + ': setTilesEnabled(0, 0, 5, 5, True)')
        mc.postCommand('@' + appName + ': onReload()')
    else:
        print "App: " + str(appName) + " not currently running. Starting New instance of app"
    
def hideApplication(appName):
    print "Hiding application: " + str(appName)
    if appName in AppDict:
        mc.postCommand('@' + appName + ': setTilesEnabled(0, 0, 5, 5, False)')
    else:
        print "App: " + str(appName) + " not currently running."

# Event function: forward event to connected mission control clients
def onEvent():
    e = getEvent()
    mcs = getMissionControlServer()
    appConnection = mcs.findConnection('app')
    if(appConnection != None):
        mcs.sendEventTo(e, appConnection)
setEventFunction(onEvent)


# Start the cluster CPU/GPU monitor service (comment this when testing on laptop)
#import monitor
