from omegaToolkit import *
from cyclops import *
import porthole

uim = UiModule.createAndInitialize()
#label = Label.create(uim.getUi())

#label.setText('Hello Launcher')
#label.setFont('fonts/arial.ttf 40')

cam = getDefaultCamera()
cam.setBackgroundColor(Color('red'))
cam.setControllerEnabled(False)

print("Test print, this is in my launcher")
p = SceneNode.create('pivot')
tls = []
for x in range(0, 6):
    for y in range(0, 6):
        pl = PlaneShape.create(0.53, 0.3)
        pl.getMaterial().setProgram('colored')
        pl.getMaterial().setAdditive(True)
        pl.getMaterial().setTransparent(True)
        pl.getMaterial().setDepthTestEnabled(False)
        pl.getMaterial().setColor(Color('black'), Color(float(x) / 5, 1 - float(y) / 5, 1, 1))
        pl.setPosition(- 3.18 + x * 1.06, 1.55 -1.8 + y * 0.6, -2)
        p.addChild(pl)
        tls.append(pl)

def onUpdate(frame, time, dt):
    sp = 0.1 * dt
    
    i = 1
    for t in tls:
        t.yaw(sp * i)
        t.pitch(sp * i)
        i += 0.2

setUpdateFunction(onUpdate)
toggleStereo()

getSceneManager().getCompositingLayer().loadCompositor('cyclops/common/compositor/motionblur.xml')


# stores the id of the last web client connected. This is
# the client in charge of controlling the running application.
appControllerClient = ""

mc = getMissionControlClient()

# Setup web server
porthole.initialize()
ps = porthole.getService()
ps.setConnectedCommand('onClientConnected("%id%")')
ps.setDisconnectedCommand('onClientDisconnected("%id%")')


# This quick command is used to easily forward js commands to clients from
# launched apps
addQuickCommand('calljs', "ps.sendjs(\"%1%({0})\".format(%2%), appControllerClient)", 2, 'call js on porthole clients')

def startApplication(clientId, appName):
    global appControllerClient
    print "Preparing to Launch" + appName
    appControllerClient = clientId
    # 'app' is the application identifier, we can use it to send mission controlling
    # messages to the app using it.
    print("this is Inside my version of the function")
    mc.spawn('app', 1, appName + '.py', 'default.cfg')
    hideLauncher()

def onClientConnected(clientId):
    print "client connected: " + clientId
    
def onClientDisconnected(clientId):
    global appControllerClient
    # web client disconnected: stop application and go back to launcher.
    print appControllerClient
    print clientId
    if(clientId == appControllerClient):
        print "stopping app: " + clientId
        mc.postCommand('@app: :q')
        showLauncher()
        
        
        
def hideLauncher():
    setTilesEnabled(0, 0, 1, 1, False)
    
def showLauncher():
    setTilesEnabled(0, 0, 1, 1, True)
    
# Event function: forward event to connected mission control clients
def onEvent():
    e = getEvent()
    mcs = getMissionControlServer()
    appConnection = mcs.findConnection('app')
    if(appConnection != None):
        mcs.sendEventTo(e, appConnection)
setEventFunction(onEvent)