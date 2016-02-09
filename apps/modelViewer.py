from omega import *
from cyclops import *
import Manipulator

getDefaultCamera().setBackgroundColor(Color('black'))

model = ModelInfo()
model.name = "model"
model.path = "../data/R_CueR_Exp.fbx"
model.size = 10

getSceneManager().loadModel(model)

obj = StaticObject.create("model")
obj.setPosition(0, 2, -10)
mat = obj.getMaterial()
mat.setProgram("colored")
mat.setShininess(50)
mat.setGloss(0.8)
Manipulator.root = obj

l1 = Light.create()
l1.setPosition(-0.1, 3, 0)
l1.setColor(Color(1, 1, 0.8, 1))
l1.setAmbient(Color(0,0,0.1,1))
sm = ShadowMap()
sm.setSoft(True)
l1.setShadow(sm)
l1.setLightType(LightType.Directional)
l1.setLightDirection(Vector3(0, 0, -1))
l1.lookAt(obj.getPosition(), Vector3(0, 1, 0))

l2 = Light.create()
l2.setPosition(0.5, 2, 0)
l2.setColor(Color(0.8, 0.8, 1, 1))
sm2 = ShadowMap()
sm2.setSoft(True)
l2.setShadow(sm2)