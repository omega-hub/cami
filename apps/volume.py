import volrend

vr = volrend.initialize()
vr.loadTiff('volrend/rabbit.tif')

# move camera back a bit
getDefaultCamera().translate(Vector3(0, 0, 20), Space.Local)
getDefaultCamera().getController().setSpeed(10)