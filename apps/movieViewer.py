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

# Utility function to send data to the web client
def calljs(methodname, data):
    mc = getMissionControlClient()
    if(mc != None):
        mc.postCommand('@server::calljs ' + methodname + ' ' + str(data))

uim = UiModule.createAndInitialize()

v = VideoStream()

v.open('/software/omegalib/release/modules/oav/example/small.mp4')
#v.open('/opt/data/Videos/4ktest.mp4')
img = Image.create(uim.getUi())
img.setData(v.getPixels())
looping = False
v.play()

def setLooping(loop):
    # print "Accepted Command:"
    # print loop
    # print "Before:"
    # print v.isLooping()
    v.setLooping(loop)
    # print "After:"
    # print v.isLooping()

def setPlaying(loop):
    # print "Accepted Command:"
    # print loop
    # print "Before:"
    # print v.isPlaying()
    v.setPlaying(loop)
    # print "After:"
    # print v.isPlaying()

def seekToTime(time):
    print "AttemptingSeek to time:"
    print time
    timeBef = v.getCurrentTime()
    print "Time before:"
    print timeBef
    v.seekToTime(time)
    timeBef = v.getCurrentTime()
    print "Time after:"
    print timeBef

def restart():
    v.seekToTime(0)

def requestUpdate():
    time = v.getCurrentTime()
    calljs('updateTime', time)

def requestDuration():
    duration = v.getDuration()
    calljs('updateDuration', duration)