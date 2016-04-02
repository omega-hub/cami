from omega import *
import porthole
import subprocess
from time import sleep
import sys

serverName = "gozer.at.northwestern.edu"

# update settings    
updateInterval = 1   
lastUpdateTime = 0

# This var stores data from the nodes
data = {}

#-------------------------------------------------------------------------------
# slave functions
def getcputime():
    cpu_infos = {} 
    with open('/proc/stat') as f:
        for l in f:
            if(l.startswith('cpu')):
                cpu_line = l.split()
                cpu_line = [cpu_line[0]]+[float(i) for i in cpu_line[1:]]#type casting
                #print cpu_line
                cpu_id,user,nice,system,idle,iowait,irq,softrig,steal,guest = cpu_line

                Idle=idle+iowait
                NonIdle=user+nice+system+irq+softrig+steal

                Total=Idle+NonIdle
                cpu_infos.update({cpu_id:{'total':Total,'idle':Idle}})
    return cpu_infos

def poll_cpus():
    start = getcputime()
    sleep(0.02)
    stop = getcputime()

    cpu_load = []

    for cpu in start:
        Total = stop[cpu]['total']
        PrevTotal = start[cpu]['total']

        Idle = stop[cpu]['idle']
        PrevIdle = start[cpu]['idle']
        CPU_Percentage=((Total-PrevTotal)-(Idle-PrevIdle))/(Total-PrevTotal)*100
        cpu_load.append((cpu, CPU_Percentage))
    return cpu_load

def poll_gpus():
    out = subprocess.check_output(['nvidia-smi', '--query-gpu=utilization.gpu', '--format=csv'])
    res = []
    for l in out.splitlines():
        if(not l.startswith('utilization')):
            vals = l.split()
            res.append(int(vals[0]))
    return res

#-------------------------------------------------------------------------------
# update functions
def requestUpdate(clientId):
    porthole.getService().sendjs("data = {0}; update()".format(data), clientId)

# slave update function: poll usage data and send it back to baster
def update_slave(frame, time, dt):
    global lastUpdateTime
    #print [time, lastUpdateTime]
    if(time - lastUpdateTime > 2):
        print ('asasa ' + str(time))
        lastUpdateTime = time 
        cpuUsage = poll_cpus()  
        gpuUsage = poll_gpus()
        #print hostname + " " + str(cpuUsage)
        mcc.postCommand('@server: monitor.data["{0}"] = [{1}, {2}]'.format(getHostname(), cpuUsage, gpuUsage))
        
if(not isMaster()):
    mcc = MissionControlClient.create()
    mcc.setName(getHostname())
    mcc.connect(serverName, 22500)
    setUpdateFunction(update_slave)