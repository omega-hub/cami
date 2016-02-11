testDict = {}
testString = "test"
testDict[testString] = "Hello"
print(testDict[testString])
if testString in testDict.keys():
  print "found key"
else:
  print "no Key"
if "TEST" == "TEST":
	print "succesful comparison"
else:
	print "can't do that"

testBool = True
testBool2 = False
if testBool:
	print "testBool is true"
if testBool2:
	print "Oh nO! you shouldn't be here"

import os, glob
os.chdir("/fastdata/opt/data/fbx")
fileList = []
cwd = os.getcwd()
for (path, dirs, files) in os.walk(cwd):
	for file in glob.glob("*.fbx"):
		newTuple = (path[len(cwd):],file)
		print(newTuple)
		fileList.append(file)