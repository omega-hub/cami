import os, glob,math, time
from omegaToolkit import *

# Utility function to send data to the web client
def calljs(methodname, data):
    mc = getMissionControlClient()
    if(mc != None):
        mc.postCommand('@server::calljs ' + methodname + ' ' + str(data))

localDebug = True
currentPictureName = 'defaultImage.jpg'

getDefaultCamera().setBackgroundColor(Color('black'))
ui = UiModule.createAndInitialize().getUi()

background = Image.create(ui)

def setScale(scale):
    background.setScale(-scale)
    pass

def resetScale():
    background.setScale(10)
    pass

def setCenter(posX,posY):
    background.setCenter(Vector2(posX * 100,posY * 100))
    pass

def resetPosition():
    background.setCenter(Vector2(2800, 3000))
    pass

def InitializePictureList():
    print "initializing Picture list with localDebug set to: " + str(localDebug)
    if (localDebug):
        os.chdir("../data")
    else:
        os.chdir("/fastdata/opt/data/Pictures/")
    fileList = []
    cwd = os.getcwd()
    numfolders = 0
    for (path, dirs, files) in os.walk(cwd):
        numfolders = numfolders + 1
        for file in glob.glob(path + "/*.png"):
            name = file[len(path)+1:]
            image = "../data/" + name[:len(name)-4] + ".png"

            if len(path[len(cwd)+1:]) > 1:
                newTuple = [path[len(cwd)+1:] + "/",name,image]
            else:
                newTuple = ["",file[len(path)+1:],image]

            print(newTuple)
            fileList.append(newTuple)
        for file in glob.glob(path + "/*.jpg"):
            name = file[len(path)+1:]
            image = "../data/" + name[:len(name)-4] + ".jpg"

            if len(path[len(cwd)+1:]) > 1:
                newTuple = [path[len(cwd)+1:] + "/",name,image]
            else:
                newTuple = ["",file[len(path)+1:],image]

            print(newTuple)
            fileList.append(newTuple)
        for file in glob.glob(path + "/*.tif"):
            name = file[len(path)+1:]
            image = "../data/" + name[:len(name)-4] + ".tif"

            if len(path[len(cwd)+1:]) > 1:
                newTuple = [path[len(cwd)+1:] + "/",name,image]
            else:
                newTuple = ["",file[len(path)+1:],image]

            print(newTuple)
            fileList.append(newTuple)

        for file in glob.glob(path + "/*.gif"):
            name = file[len(path)+1:]
            image = "../data/" + name[:len(name)-4] + ".gif"

            if len(path[len(cwd)+1:]) > 1:
                newTuple = [path[len(cwd)+1:] + "/",name,image]
            else:
                newTuple = ["",file[len(path)+1:],image]

            print(newTuple)
            fileList.append(newTuple)

    print(fileList)
    #onPictureSelect("ben.fbx=
    #onPictureSelect("A_CueR_Exp.fbx")
    print(numfolders)
    calljs('createPictureButtons', fileList)

print "Preparing to initialize Picture List"
InitializePictureList()

def onPictureSelect(PictureName):
    print("Inside OnPictureSelect")
    print(PictureName)
    global currentPictureName
    
    if PictureName == currentPictureName:
        #print "Current Picture is same as selected Picture"
        calljs('noloading', 0)
    else:
        #TODO: Hide current Picture
        #if currentPictureName != "noPicture":
            #Unload current Picture
        currentPictureName = PictureName
        LoadPicture(PictureName)
        
    
def LoadPicture(PictureName):
    global background
    if (localDebug):
        path = "../data/" + PictureName
    else:
        path = "/fastdata/opt/data/Videos/" + PictureName
    background.setData(loadImage(currentPictureName))
    background.setLayer(WidgetLayer.Back)

def closePicture():
    pass

def onReload():
    print "Returning to Picture Viewer"
    InitializePictureList()

# setTilesEnabled(0, 0, 5, 5, False)