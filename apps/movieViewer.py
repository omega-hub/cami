if(isMaster()):
    from oav import *

    uim = UiModule.createAndInitialize()

    v = VideoStream()

    v.open('/opt/data/Videos/4ktest.mp4')

    img = Image.create(uim.getUi())
    img.setData(v.getPixels())
    img.setAutosize(False)
    img.setSize(uim.getUi().getSize())
    #img.setStereo(True)
    v.play()

    def setLooping(loop):
        v.setLooping(loop)

    def setPlaying(loop):
        v.setPlaying(loop)

    def seekToTime(time):
        v.seekToTime(time)

    def restart():
        v.seekToTime(0)