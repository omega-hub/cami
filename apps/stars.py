from cyclops import *
from pointCloud import *
import Manipulator
from math import *
import sys
from PointSet import *
import csv
# from moving import *

print "initializing Star Scene"
scene = getSceneManager()
galaxy = [
    PointSet('/fastdata/software/omegalib/apps/stars/data.xyzb', Color(0.1, 0.5, 0.8, 1), 0.2),
    PointSet('/fastdata/software/omegalib/apps/stars/data_1.xyzb', Color(0.5, 0.5, 0.0, 1), 0.15),
    PointSet('/fastdata/software/omegalib/apps/stars/data_2.xyzb', Color(0.5, 0.5, 0.0, 1), 2),
    PointSet('/fastdata/software/omegalib/apps/stars/data_4.xyzb', Color(1, 0.1, 0.1, 1), 0.7)
]

pivot = SceneNode.create('pivot')
for ps in galaxy:
    pivot.addChild(ps.object)
Manipulator.root = pivot

camera = getDefaultCamera()
camera.setBackgroundColor(Color('black'))
camera.getController().setSpeed(50)
camera.setPosition(0,-5,0)
isRotating = False
initialized = False
yaw = 0
pitch = 0
rotSpeed = 1

def calljs(methodname, data):
    mc = getMissionControlClient()
    if(mc != None):
        mc.postCommand('@server::calljs ' + methodname + ' ' + str(data))

def center():
    for ps in galaxy:
        ps.object.setPosition(-470, -190, -640)

center()
    
def rs():
    scene.reloadAndRecompileShaders()
    
s = 0
k = 0

# def onUpdate(frame, time, dt):
#     global s
#     pivot.yaw(s * dt)
#     pivot.pitch(k * dt)
    
# setUpdateFunction(onUpdate)
    
def onSliderChanged(id, i, clientId):
    galaxy[id].pointScale.setFloat(float(i) / 10)
    # Update slider state on all connected clients.
    #porthole.getService().broadcastjs('updateSliders({0})'.format(i), clientId)

def toggle(id):
    galaxy[id].object.setVisible(not galaxy[id].object.isVisible())
    print(galaxy[id].object.isVisible())

#Model Manipulation Functions:
def setZoom(z):
    oldX = camera.getPosition().x
    oldY = camera.getPosition().y
    camera.setPosition(oldX,oldY,z)

def setPan(x,y):
    #print "inside on Pan!!!!!!!!!!!!!!!"
    oldZ = camera.getPosition().z
    camera.setPosition(x,y ,oldZ)

def onRotate(dx,dy,dz):
    #print "inside on Rotate!"
    pivot.rotate(Vector3(0, 1, 0), math.radians(dx), Space.World)
    pivot.rotate(Vector3(1, 0, 0), math.radians(dy), Space.World)
    pivot.rotate(Vector3(0, 0, 1), math.radians(dz), Space.World)

def onZoom(delta):
    #print "inside On Zoom"
    #print delta
    camera.translate(0,0,delta,Space.World)
    if (camera.getPosition().z < -10):
        camera.translate(0,0,delta ,Space.World)
    elif (camera.getPosition().z > 15 ):
        camera.translate(0,0,-delta ,Space.World)

def pyresetOrientation(dummy):
    pivot.resetOrientation()
    print("in .py resetOrientation")
    
def logPan(dx,dy,dz,numTouch):
    # print "Message from HTML"
    return 0
    #print "Pan Gesture detected."
    #print dx
    #print dy
    #print dz
    #print numTouch

def printMessage():
    print "Message from HTML:"
    print message
    return

def onReload():
    print "on reload"
    global reader, data, file, reader
    file = open('moving_data.tsv','rU')
    skip = True
    reader = csv.reader(file, delimiter='\t')
    calljs('resetImage', 0)
    for row in reader:
        if skip: skip = False
        else: 
            print row[3]
            print row[4]
            print row[5]
            q = quaternionFromEulerDeg(float(row[3]),float(row[4]),float(row[5]))
            v = [float(row[0]),float(row[1]),float(row[2]),q,float(row[6]),float(row[7]),float(row[8]),float(row[9])]
            data.append(v)
            calljs('addViewButton', 0)

    #print(fileList)
    #onModelSelect("ben.fbx=
    #onModelSelect("A_CueR_Exp.fbx")
    #print "number of folders: " ,numfolders
    #calljs('createModelButtons', fileList)

# print("initialized Model List")


###########Code Imported from moving.py##############

c = getDefaultCamera()

file = False
reader = False

data = []

onReload()

file.close()

current = [0,0,0,Quaternion(),0,0,0,0]
target = [0,0,0,Quaternion(),0,0,0,0]

animationTime = 1
currentTime = animationTime

def loadView(id):
    global target
    global current
    global currentTime
    target = data[id]
    current = []
    cpos = c.getPosition()
    for x in cpos: current.append(x)
    q = pivot.getOrientation()
    current.append(q)
    currIndex = 0
    for x in galaxy: 
        scale = []
        scale.append(currIndex)
        scale.append(x.pointScale.getFloat())
        current.append(scale[1])
        calljs('updateStarBrightness', scale)
        currIndex = currIndex + 1
    currentTime = 0
    
def saveView(id):
    global data
    global file
    row = []
    cpos = c.getPosition()
    for x in cpos: row.append(x)
    row.append(pivot.getOrientation())
    for x in galaxy: row.append(x.pointScale.getFloat())
    if (id > (len(data)-1)):
        data.append(row)
    else:
        data[id] = row
    file = open('moving_data.tsv','w')
    writer = csv.writer(file, delimiter='\t')
    s = ['x','y','z','pitch','yaw','roll','intensity 1','intensity 2','intensity 3','intensity 4']
    writer.writerow(s)
    for row in data:
        v = quaternionToEulerDeg(row[3])
        r = [row[0],row[1],row[2],v[0],v[1],v[2],row[4],row[5],row[6],row[7]]
        writer.writerow(r)
    file.close()
    
def onEvent():
    e = getEvent()
    if(e.isKeyDown(ord("u"))): 
        if(e.isFlagSet(EventFlags.Shift)): saveView(0)
        else: loadView(0)
    if(e.isKeyDown(ord("i"))): 
        if(e.isFlagSet(EventFlags.Shift)): saveView(1)
        else: loadView(1)
    if(e.isKeyDown(ord("o"))): 
        if(e.isFlagSet(EventFlags.Shift)): saveView(2)
        else: loadView(2)
    if(e.isKeyDown(ord("p"))): 
        if(e.isFlagSet(EventFlags.Shift)): saveView(3)
        else: loadView(3)
                
setEventFunction(onEvent)

def mix(x1,x2,w):
    return x1+(x2-x1)*w

def onUpdate(frame, time, dt):
    global current
    global target
    global currentTime

    if(currentTime <= animationTime):
        w = currentTime/animationTime
        v = []
        p = []
        
        currentTime = currentTime + dt
        for i in range(0,3): v.append(mix(current[i],target[i],w))
        c.setPosition(v[0],v[1],v[2])
        for j in range(4,8): p.append(mix(current[j],target[j],w))
        k = 0 
        for x in galaxy: 
            x.pointScale.setFloat(p[k])
            k = k+1
        q = Quaternion.new_interpolate(current[3],target[3],w)
        pivot.setOrientation(q)
    global isRotating, yaw, pitch
    if isRotating:
        pivot.rotate(Vector3(0, 1, 0), math.radians(yaw * dt), Space.World)
        pivot.rotate(Vector3(1, 0, 0), math.radians(pitch * dt), Space.World)
        pivot.rotate(Vector3(0, 0, 1), math.radians(0), Space.World)
        # pivot.yaw(yaw * dt)
        # pivot.pitch(pitch * dt)
    global initialized
    if not initialized:
        calljs('onLoaded',0)
        initialized = True

#################################################

def setYawPitchSpeed(dx,dy):
    global yaw, pitch, rotSpeed
    totalSpeed = abs(dx) + abs(dy)
    if totalSpeed > 0:
        yaw = (-(dx*1.0)/totalSpeed) * rotSpeed
        pitch = (-(dy*1.0)/totalSpeed) * rotSpeed
        # print "Yaw set to: ", yaw

def setRotationSpeed(spd):
    global rotSpeed, yaw, pitch
    oldRotSpeed = rotSpeed
    rotSpeed = spd
    yaw = yaw * (rotSpeed/oldRotSpeed)
    pitch = pitch * (rotSpeed/oldRotSpeed)

def toggleAutoRotate(rotate):
    global isRotating
    isRotating = rotate

setUpdateFunction(onUpdate) 