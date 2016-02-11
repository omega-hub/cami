from omega import *
from cyclops import *
import Manipulator
import os, glob
print("THis is inside my version of modelView.py")
getDefaultCamera().setBackgroundColor(Color('black'))

getSceneManager().getCompositingLayer().loadCompositor('cyclops/common/compositor/dof.xml')

ModelDict = {}
currentModel = "noModel!"
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

obj = None

def InitializeModelList():

	os.chdir("/fastdata/opt/data/fbx")
	fileList = []
	cwd = os.getcwd()
	for (path, dirs, files) in os.walk(cwd):
		for file in glob.glob("*.fbx"):
			newTuple = (path[len(cwd):],file)
			print(newTuple)
			fileList.append(file)
	onModelSelect("ben.fbx")

def onModelSelect(modelName):
	global currentModel
	path = "/fastdata/opt/data/fbx/" + modelName
	if modelName == currentModel:
		print "Current model is same as selected model"
	elif modelName in ModelDict.keys(): 
		print "Model has already been loaded"
		#TODO: Make new model reappear
		toggleModelVisible(currentModel,False)
		toggleModelVisible(modelName, True)
		currentModel = modelName
	else:
		#TODO: Hide current Model
		toggleModelVisible(currentModel,False)
		LoadModel(path)
	
def LoadModel(modelPath):
	global currentModel
	global ModelDict
	model = ModelInfo()
	model.name = "model"
	model.path = modelPath
	model.generateNormals = True
	model.optimize = True
	model.size = 10
	getSceneManager().loadModelAsync(model, 'onModelLoaded()')
	currentModel = model
	ModelDict[modelPath] = model
	
def toggleModelVisible(modelName, visible):
	if visible:
		print "toggling to visible"
	else:
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

	
InitializeModelList()
print("initialized Model List")