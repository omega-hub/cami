# if(isMaster()):
#     from oav import *
#     print "Reached MovieViewer.py 2"
#     uim = UiModule.createAndInitialize()

#     v = VideoStream()

#     v.open('/opt/data/Videos/4ktest.mp4')

#     img = Image.create(uim.getUi())
#     img.setData(v.getPixels())
#     #img.setAutosize(False) # Inserting these resulted in it not working
#     #img.setSize(uim.getUi().getSize())
#     #img.setStereo(True)
#     v.play()

    # def setLooping(loop):
    #     v.setLooping(loop)

    # def setPlaying(loop):
    #     v.setPlaying(loop)

    # def seekToTime(time):
    #     place = v.getVideoLength()
    #     place = place - place*(100-time)/100
    #     v.seekToTime(place)

    # def restart():
    #     v.seekToTime(0)
from oav import *
import os, glob,math, time

# Utility function to send data to the web client
def calljs(methodname, data):
    mc = getMissionControlClient()
    if(mc != None):
        mc.postCommand('@server::calljs ' + methodname + ' ' + str(data))
localDebug = False
currentMovieName = "noMovie"
uim = UiModule.createAndInitialize()
img = Image.create(uim.getUi())
v = False
#if (not isMaster()):
    # v.open('/software/omegalib/release/modules/oav/example/small.mp4')
    # #v.open('/opt/data/Videos/4ktest.mp4')
    # img.setData(v.getPixels())
    # img.setAutosize(False) # Inserting these resulted in it not working
    # img.setSize(uim.getUi().getSize())
    # v.play()

def setLooping(loop):
    global v
    if (v != False):
        # print "Accepted Command:"
        # print loop
        # print "Before:"
        # print v.isLooping()
        v.setLooping(loop)
        # print "After:"
        # print v.isLooping()

def setPlaying(play):
    global v
    if (v != False):
        # print "Accepted Command:"
        # print play
        # print "Before:"
        # print v.isPlaying()
        v.setPlaying(play)
        # print "After:"
        # print v.isPlaying()

def seekToTime(time):
    global v
    print v
    if (v != False):
        # print "AttemptingSeek to time:"
        # print time
        timeBef = v.getCurrentTime()
        # print "Time before:"
        # print timeBef
        v.seekToTime(time)
        timeBef = v.getCurrentTime()
        # print "Time after:"
        # print timeBef

def requestUpdate():
    global v
    if (v != False):
        time = v.getCurrentTime()
        #print time
        calljs('updateTime', time)
    else:
        return 0

def requestDuration():
    global v
    if (v != False):
        duration = v.getDuration()
        #print duration
        calljs('updateDuration', duration)
    else:
        return 0

def InitializeMovieList():

    print "initializing movie list with localDebug set to: " + str(localDebug)
    if (localDebug):
        os.chdir("../data")
    else:
        os.chdir("/fastdata/opt/data/Videos/")
    fileList = []
    cwd = os.getcwd()
    numfolders = 0
    for (path, dirs, files) in os.walk(cwd):
        numfolders = numfolders + 1
        extra = ""
        for file in glob.glob(path + "/*.mov"):
            name = file[len(path)+1:]
            # image = "../data/" + name[:len(name)-4] + ".mov"

            if len(path[len(cwd)+1:]) > 1:
                newTuple = [path[len(cwd)+1:] + "/",name,extra]
            else:
                newTuple = ["",file[len(path)+1:],extra]

            # print(newTuple)
            fileList.append(newTuple)
        for file in glob.glob(path + "/*.mpg"):
            name = file[len(path)+1:]
            # image = "../data/" + name[:len(name)-4] + ".mov"

            if len(path[len(cwd)+1:]) > 1:
                newTuple = [path[len(cwd)+1:] + "/",name,extra]
            else:
                newTuple = ["",file[len(path)+1:],extra]

            # print(newTuple)
            fileList.append(newTuple)
        for file in glob.glob(path + "/*.mkv"):
            name = file[len(path)+1:]
            # image = "../data/" + name[:len(name)-4] + ".mov"

            if len(path[len(cwd)+1:]) > 1:
                newTuple = [path[len(cwd)+1:] + "/",name,extra]
            else:
                newTuple = ["",file[len(path)+1:],extra]

            # print(newTuple)
            fileList.append(newTuple)

        for file in glob.glob(path + "/*.mp4"):
            name = file[len(path)+1:]
            # image = "../data/" + name[:len(name)-4] + ".mov"

            if len(path[len(cwd)+1:]) > 1:
                newTuple = [path[len(cwd)+1:] + "/",name,extra]
            else:
                newTuple = ["",file[len(path)+1:],extra]

            # print(newTuple)
            fileList.append(newTuple)

    print(fileList)
    #onMovieSelect("ben.fbx=
    #onMovieSelect("A_CueR_Exp.fbx")
    print(numfolders)
    calljs('createMovieButtons', fileList)
print "Preparing to initialize Movie List"
InitializeMovieList()

def onMovieSelect(MovieName):
    print("Inside OnMovieSelect")
    print(MovieName)
    global currentMovieName
    
    if MovieName == currentMovieName:
        #print "Current Movie is same as selected Movie"
        calljs('noloading', 0)
    else:
        #TODO: Hide current Movie
        #if currentMovieName != "noMovie":
            #Unload current movie
        currentMovieName = MovieName
        LoadMovie(MovieName)
        
    
def LoadMovie(MovieName):
    global v, img
    if (localDebug):
        path = "../data/" + MovieName
    else:
        path = "/fastdata/opt/data/Videos/" + MovieName
    if (v):
        print "Video Module detected, to delete module"
        v.close()
    v = VideoStream()
    v.open(path)
    #v.open('/opt/data/Videos/4ktest.mp4')
    #img = Image.create(uim.getUi())
    # print "Getting width: " + str(v.getPixels().getWidth())
    # print "Getting height: " + str(v.getPixels().getHeight())
    # print "ratio = " + str(v.getPixels().getWidth()/v.getPixels().getHeight())
    ratio = (v.getPixels().getWidth()/v.getPixels().getHeight())
    # print "ratio found to be: " + str(ratio)
    # print (ratio > (16/9))
    if (ratio > (16/9)):
        img.setStereo(True)
    else:
        img.setStereo(False)
    img.setData(v.getPixels())
    img.setAutosize(False) # Inserting these resulted in it not working
    img.setSize(uim.getUi().getSize())
    v.play()
    duration = v.getDuration()
    print "Sending discovered duration: "
    print duration
    calljs('updateDuration',duration)

def closeMovie():
    if (v):
        print "Video Module detected, to delete module"
        v.close()

def onReload():
    print "Returning to Movie Viewer"
    InitializeMovieList()

# setTilesEnabled(0, 0, 5, 5, False)
