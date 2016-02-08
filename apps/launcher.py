from omegaToolkit import *
from cyclops import *
import porthole

uim = UiModule.createAndInitialize()
label = Label.create(uim.getUi())

label.setText('Hello Launcher')
label.setFont('fonts/arial.ttf 40')

# stores the id of the last web client connected. This is
# the client in charge of controlling the running application.
appControllerClient = ""

mc = getMissionControlClient()

# Setup web server
porthole.initialize()
ps = porthole.getService()
ps.setConnectedCommand('onClientConnected("%id%")')
ps.setDisconnectedCommand('onClientDisconnected("%id%")')

def startApplication(clientId, appName):
    global appControllerClient
    appControllerClient = clientId
    # 'app' is the application identifier, we can use it to send mission controlling
    # messages to the app using it.
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