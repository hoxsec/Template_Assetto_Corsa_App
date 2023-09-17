import ac, acsys
import os, sys, json

sysdir = os.path.dirname(__file__) + '/third_party/'
sys.path.insert(0, sysdir)
os.environ['PATH'] = os.environ['PATH'] + ";."

from third_party.sim_info import *
from third_party import requests
import threading

url = "http://dev.shanonithoer.nl/api/stats/update"
appName = "Boosted Timer"
width, height = 800, 800  # width and height of the app's window
posScale = 1.3
fontScale = 1.0
simInfo = SimInfo()

timerData = 0
ticks = 0

trackName = "Unknown"
carName = "Unknown"
driverName = "Unknown"

lastLapTime = 0
previousLapValue = 0
lapCount = 0
prevLapCount = 0

def acMain(ac_version):
    global ac, appWindow, lastLapTime, timerData, simInfo, previousLapValue, prevLapCount

    appWindow = ac.newApp(appName)
    ac.setTitle(appWindow, appName)
    ac.drawBorder(appWindow, 1)
    ac.setIconPosition(appWindow, 0, -10000)
    ac.setSize(appWindow, 50 * posScale, 50 * posScale)

    ac.addRenderCallback(appWindow, acUpdate)

    return appName

def acUpdate(deltaT):
    global ac, appWindow, lastLapTime, timerData, simInfo, previousLapValue, lapCount, prevLapCount
    global ticks
    ticks += 1
    
    lastLapTime = simInfo.graphics.iLastTime
    lapCount = ac.getCarState(0, acsys.CS.LapCount)

    if ticks >= 200:
        t = threading.Thread(target=sendInfo)
        t.start()
        ticks = 0

def sendInfo():
    global ac, appWindow, lastLapTime, timerData, simInfo, previousLapValue, lapCount, prevLapCount
    if prevLapCount != lapCount:
        prevLapCount = lapCount
        laptime_data = {
            "laptime": lastLapTime,
            "circuit": ac.getTrackName(0),
            "car": ac.getCarName(0),
            "driver": ac.getDriverName(0)
        }
        headers = {'Content-Type': 'application/json'}
        params = json.dumps(laptime_data).encode('utf8')
        ac.log("---------")
        ac.log("BoostedTimer - Sending data: " + str(params))
        ac.log("---------")
        try:
            requests.post(url, data=params, headers=headers, verify=False)
        except:
            pass
