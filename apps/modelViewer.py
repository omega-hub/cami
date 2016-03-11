from omega import *
from cyclops import *
import Manipulator
import os, glob,math
getDefaultCamera().setBackgroundColor(Color('black'))
camera = getDefaultCamera()
getSceneManager().getCompositingLayer().loadCompositor('cyclops/common/compositor/dof.xml')

ModelDict = {}
currentModelName = "noModel"
l1 = Light.create()
l1.setPosition(-0.1, 3, 0)
l1.setColor(Color(1, 1, 0.8, 1))
l1.setAmbient(Color(0,0,0.1,1))
sm = ShadowMap()
sm.setTextureSize(4096,4096)
sm.setSoft(True)
#sm.setSoftShadowParameters(0.005, 5)
l1.setShadow(sm)
l1.setLightType(LightType.Spot)
l1.setLightDirection(Vector3(0, 0, -1))

l2 = Light.create()
l2.setPosition(2.5, 3, 0)
l2.setColor(Color(0.8, 0.8, 1, 1))
sm2 = ShadowMap()
sm2.setTextureSize(4096,4096)
sm2.setSoft(True)
#sm2.setSoftShadowParameters(0.005, 5)
l2.setShadow(sm2)

ScrollSpeed = 0.1
obj = None
localDebug = True

# Utility function to send data to the web client
def calljs(methodname, data):
    mc = getMissionControlClient()
    if(mc != None):
        mc.postCommand('@server::calljs ' + methodname + ' ' + str(data))
    
# # example: send ModelDict to console.log to print it on the web client
# calljs('console.log', ModelDict)
# # example 2: set a variable on the web client to a list we pass here
# calljs('x=', [1, 2, 3, 4])
# # example 3: print a single value on the client
# calljs('console.log', 10)
def setLocalDebugging(debugMode):
    global localDebug
    localDebug = debugMode
    

def InitializeModelList():
    if (localDebug):
        os.chdir("../data")
    else:
        os.chdir("/fastdata/opt/data/fbx")
    fileList = []
    cwd = os.getcwd()
    numfolders = 0
    for (path, dirs, files) in os.walk(cwd):
        numfolders = numfolders + 1
        for file in glob.glob(path + "/*.fbx"):
            name = file[len(path)+1:]
            image = "../data/" + name[:len(name)-4] + ".jpg"

            if len(path[len(cwd)+1:]) > 1:
                newTuple = [path[len(cwd)+1:] + "/",name,image]
            else:
                newTuple = ["",file[len(path)+1:],image]

            print(newTuple)
            fileList.append(newTuple)

    print(fileList)
    #onModelSelect("ben.fbx=
    #onModelSelect("A_CueR_Exp.fbx")
    print(numfolders)
    calljs('createModelButtons', fileList)

def onModelSelect(modelName):
    print("Inside On Model Select")
    print(modelName)
    global currentModelName
    
    if modelName == currentModelName:
        print "Current model is same as selected model"
    elif modelName in ModelDict.keys(): 
        print "Model has already been loaded"
        #TODO: Make new model reappear
        toggleModelVisible(currentModelName,False)
        toggleModelVisible(modelName, True)
        currentModelName = modelName
    else:
        #TODO: Hide current Model
        if currentModelName != "noModel":
            toggleModelVisible(currentModelName,False)
        currentModelName = modelName
        LoadModel(modelName)
    
def LoadModel(modelName):
    if (localDebug):
        path = "../data/" + modelName
    else:
        path = "/fastdata/opt/data/fbx/" + modelName
    global currentModelName
    global ModelDict
    model = ModelInfo()
    model.name = "model"
    model.path = path
    model.generateNormals = True
    model.optimize = True
    model.size = 10
    getSceneManager().loadModelAsync(model, 'onModelLoaded()')
    
def toggleModelVisible(modelName, visible):
    parent = getScene()
    if visible:
        print "toggling to visible"
        ModelDict[modelName].setVisible(True)
        #parent.addChild(ModelDict[modelName])
    else:
        ModelDict[modelName].setVisible(False)
        #parent.removeChildByRef(ModelDict[modelName])
        print "toggling to invisible"

def onModelLoaded():
    global obj
    obj = StaticObject.create("model")
    obj.setPosition(0, 2, -10)
    mat = obj.getMaterial()
    mat.setProgram("colored")
    mat.setShininess(50)
    mat.setGloss(0.4)
    Manipulator.root = obj
    l1.lookAt(obj.getPosition(), Vector3(0, 1, 0))
    ModelDict[currentModelName] = obj

    
InitializeModelList()
print("initialized Model List")

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
    if currentModelName != "noModel":
        currentModel = ModelDict[currentModelName]
        currentModel.rotate(Vector3(0, 1, 0), math.radians(dx), Space.World)
        currentModel.rotate(Vector3(1, 0, 0), math.radians(dy), Space.World)
        currentModel.rotate(Vector3(0, 0, 1), math.radians(dz), Space.World)

def onZoom(delta):
    #print "inside On Zoom"
    #print delta
    camera.translate(0,0,delta,Space.World)
    if (camera.getPosition().z < -10):
        camera.translate(0,0,delta ,Space.World)
    elif (camera.getPosition().z > 15 ):
        camera.translate(0,0,-delta ,Space.World)

def pyresetOrientation(dummy):
    if currentModelName != "noModel":
        currentModel = ModelDict[currentModelName]
        currentModel.resetOrientation()
    print("in .py resetOrientation")
    
def logPan(dx,dy,dz,numTouch):
    print "Pan Gesture detected."
    print dx
    print dy
    print dz
    print numTouch