from cyclops import *
from pointCloud import *
from math import *
import sys


scene = getSceneManager()
scene.addLoader(BinaryPointsLoader())

pointProgram = ProgramAsset()
pointProgram.name = "points"
pointProgram.vertexShaderName = "pointCloud/shaders/Sphere.vert"
pointProgram.fragmentShaderName = "/fastdata/software/omegalib/apps/stars/star.frag"
pointProgram.geometryShaderName = "/fastdata/software/omegalib/apps/stars/star.geom"
pointProgram.geometryOutVertices = 4
pointProgram.geometryInput = PrimitiveType.Points
pointProgram.geometryOutput = PrimitiveType.TriangleStrip
scene.addProgram(pointProgram)


class PointSet:
    def __init__(self, file, color, pointScale):
        self.pointScale = Uniform.create('pointScale', UniformType.Float, 1)
        self.pointScale.setFloat(pointScale)
        
        self.color = Uniform.create('color', UniformType.Color, 1)
        self.color.setColor(color)
        
        self.model = ModelInfo()
        self.model.name = file
        self.model.path = file
        self.model.options = "200000 100:1000000:50 20:101:10 0:21:4"
        #pointCloudModel.options = "10000 1000:1000000:10 100:1000:4 10:100:2 0:10:1"
        #pointCloudModel.options = "200000 0:1000000:10"
        scene.loadModel(self.model)

        self.object = StaticObject.create(self.model.name)
        # attach shader uniforms
        self.material = self.object.getMaterial()
        self.material.setProgram(pointProgram.name)
        self.material.attachUniform(self.pointScale)
        self.material.attachUniform(self.color)
        self.material.setTransparent(True)
        self.material.setAdditive(True)
        self.material.setDepthTestEnabled(False)