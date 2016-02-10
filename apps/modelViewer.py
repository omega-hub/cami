from omega import *
from cyclops import *
import Manipulator

getDefaultCamera().setBackgroundColor(Color('black'))

model = ModelInfo()
model.name = "model"
#model.path = "../data/R_CueR_Exp.fbx"
model.path = "/fastdata/opt/data/fbx/estrogenDNA.fbx"
#model.path = "/fastdata/opt/data/fbx/pMMO.fbx"
model.generateNormals = True
model.optimize = True
model.size = 10

getSceneManager().loadModelAsync(model, 'onModelLoaded()')
getSceneManager().getCompositingLayer().loadCompositor('cyclops/common/compositor/dof.xml')

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
