import os, glob
localDebug = True
if (localDebug):
    os.chdir("../data")
else:
    os.chdir("/fastdata/opt/data/fbx")
fileList = []
cwd = os.getcwd()
for (path, dirs, files) in os.walk(cwd):
    for file in glob.glob(path + "/*.fbx"):
        newTuple = [path[len(cwd)+1:],file[len(path)+1:]]
        print(newTuple)
        fileList.append(newTuple)
print(fileList)
#onModelSelect("ben.fbx=
#onModelSelect("A_CueR_Exp.fbx")
#calljs('createModelButtons', fileList)