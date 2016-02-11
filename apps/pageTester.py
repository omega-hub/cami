import porthole

# Setup web server
porthole.initialize()
ps = porthole.getService()
ps.setDisconnectedCommand('onClientDisconnected()')

def onClientDisconnected():
    print('reload')