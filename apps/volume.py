#import volrend

#vr = volrend.initialize()
#vr.loadTiff('volrend/rabbit.tif')

# move camera back a bit
#getDefaultCamera().translate(Vector3(0, 0, 20), Space.Local)
#getDefaultCamera().getController().setSpeed(10)

from omega import *
from cyclops import *
import volrend
import os, glob,math, time

vr = volrend.initialize()
vr.loadTiff('volrend/rabbit.tif')
vr.node.setPosition(0,0,-14)

# move camera back a bit
getDefaultCamera().translate(Vector3(0, 0, 0), Space.Local)
getDefaultCamera().getController().setSpeed(10)
getDefaultCamera().setBackgroundColor(Color('black'))

camera = getDefaultCamera()
#getSceneManager().getCompositingLayer().loadCompositor('cyclops/common/compositor/dof.xml')

#ModelDict = {}
currentModelName = "rabbit"
l1 = Light.create()
l1.setPosition(-0.1, 3, 0)
l1.setColor(Color(1, 1, 0.8, 1))
l1.setAmbient(Color(0,0,0.1,1))
# sm = ShadowMap()
# sm.setTextureSize(1024,1024)
# sm.setSoft(True)
# #sm.setSoftShadowParameters(0.005, 5)
# l1.setShadow(sm)
l1.setLightType(LightType.Spot)
l1.setLightDirection(Vector3(0, 0, -1))

l2 = Light.create()
l2.setPosition(2.5, 3, 0)
l2.setColor(Color(0.8, 0.8, 1, 1))
# sm2 = ShadowMap()
# sm2.setTextureSize(1024,1024)
# sm2.setSoft(True)
# #sm2.setSoftShadowParameters(0.005, 5)
# l2.setShadow(sm2)

ScrollSpeed = 0.1
obj = None
#localDebug = True
# Utility function to send data to the web client
def calljs(methodname, data):
    mc = getMissionControlClient()
    if(mc != None):
        mc.postCommand('@server::calljs ' + methodname + ' ' + str(data))    

def InitializeModelList():
    return False
    # if (localDebug):
    #     os.chdir("../data")
    # else:
    #     os.chdir("/fastdata/opt/data/fbx")
    # fileList = []
    # cwd = os.getcwd()
    # numfolders = 0
    # for (path, dirs, files) in os.walk(cwd):
    #     numfolders = numfolders + 1
    #     for file in glob.glob(path + "/*.fbx"):
    #         name = file[len(path)+1:]
    #         image = "../data/" + name[:len(name)-4] + ".jpg"

    #         if len(path[len(cwd)+1:]) > 1:
    #             newTuple = [path[len(cwd)+1:] + "/",name,image]
    #         else:
    #             newTuple = ["",file[len(path)+1:],image]

    #         print(newTuple)
    #         fileList.append(newTuple)

    # print(fileList)
    # #onModelSelect("ben.fbx=
    # #onModelSelect("A_CueR_Exp.fbx")
    # print(numfolders)
    # calljs('createModelButtons', fileList)

def onModelSelect(modelName):
    return False
#     print("Inside On Model Select")
#     print(modelName)
#     global currentModelName
    
#     if modelName == currentModelName:
#         print "Current model is same as selected model"
#         calljs('noloading', ScrollSpeed)
#     elif modelName in ModelDict.keys(): 
#         print "Model has already been loaded"
#         #TODO: Make new model reappear
#         toggleModelVisible(currentModelName,False)
#         toggleModelVisible(modelName, True)
#         currentModelName = modelName
#         calljs('noloading', ScrollSpeed)
#     else:
#         #TODO: Hide current Model
#         if currentModelName != "noModel":
#             toggleModelVisible(currentModelName,False)
#         currentModelName = modelName
#         LoadModel(modelName)
        
    
def LoadModel(modelName):
    return False
    # if (localDebug):
    #     path = "../data/" + modelName
    # else:
    #     path = "/fastdata/opt/data/fbx/" + modelName
    # global currentModelName
    # global ModelDict
    # model = ModelInfo()
    # model.name = "model"
    # model.path = path
    # model.generateNormals = False
    # model.optimize = False
    # model.size = 10
    # getSceneManager().loadModelAsync(model, 'onModelLoaded()')
    
    
def toggleModelVisible(modelName, visible):
    return False
    # parent = getScene()
    # if visible:
    #     print "toggling to visible"
    #     ModelDict[modelName].setVisible(True)
    #     #parent.addChild(ModelDict[modelName])
    # else:
    #     ModelDict[modelName].setVisible(False)
    #     #parent.removeChildByRef(ModelDict[modelName])
    #     print "toggling to invisible"

def onModelLoaded():
    return False
    # global obj
    # obj = StaticObject.create("model")
    # obj.setPosition(0, 2, -8)
    # mat = obj.getMaterial()
    # mat.setProgram("colored")
    # mat.setShininess(50)
    # mat.setGloss(0.4)
    # Manipulator.root = obj
    # l1.lookAt(obj.getPosition(), Vector3(0, 1, 0))
    # ModelDict[currentModelName] = obj
    # time.sleep(5)
    # calljs('noloading', ScrollSpeed)
    
#InitializeModelList()
print("initialized Model List")

#Model Manipulation Functions:
def setZoom(z):
    oldX = camera.getPosition().x
    oldY = camera.getPosition().y
    print camera.getPosition().z
    print z
    camera.setPosition(oldX,oldY,z)

def setPan(x,y):
    #print "inside on Pan!!!!!!!!!!!!!!!"
    oldX = camera.getPosition().x
    oldY = camera.getPosition().y
    # print oldX
    # print oldY
    # print "oldX = " + str(x)
    # print "oldY = " + str(y)
    oldZ = camera.getPosition().z
    camera.setPosition(x,y ,oldZ)

def onRotate(dx,dy,dz):
    #print "inside on Rotate!"
    if currentModelName != "noModel":
        currentModel = vr.node #ModelDict[currentModelName]
        currentModel.rotate(Vector3(0, 1, 0), math.radians(dx), Space.World)
        currentModel.rotate(Vector3(1, 0, 0), math.radians(dy), Space.World)
        currentModel.rotate(Vector3(0, 0, 1), math.radians(dz), Space.World)

def onZoom(delta):
    #print "inside On Zoom"
    #print delta
    print camera.getPosition.z()
    print delta
    camera.translate(0,0,delta,Space.World)
    if (camera.getPosition().z < -10):
        camera.translate(0,0,delta ,Space.World)
    elif (camera.getPosition().z > 20 ):
        camera.translate(0,0,-delta ,Space.World)

def pyresetOrientation(dummy):
    if currentModelName != "noModel":
        currentModel = vr.node #ModelDict[currentModelName]
        print camera.getPosition().x
        print camera.getPosition().y
        print camera.getPosition().z
        camera.setPosition(0,0,-4)
        # print currentModel.getPosition().x
        # print currentModel.getPosition().y
        # print currentModel.getPosition().z
        currentModel.resetOrientation()
    print("in .py resetOrientation")

pyresetOrientation(0)

def logPan(dx,dy,dz,numTouch):
    return 0
    #print "Pan Gesture detected."
    #print dx
    #print dy
    #print dz
    #print numTouch

def changeSlice(axis, start,end):
	if (axis == 1):
		vr.setSliceBoundX(start,end)
	elif (axis == 2):
		vr.setSliceBoundY(start,end)
	elif (axis == 3):
		vr.setSliceBoundZ(start,end)

def onReload():
    calljs('resetImage', False)

# setTilesEnabled(0, 0, 5, 5, False)