# AC App Template by Hunter Vaners
# ------------------------------
#
# Don't forget to rename assettocorsa\apps\python\Template_Assetto_Corsa_App
#           by assettocorsa\apps\python\[Your_App_Name_Without_Spaces]
#  and
# the file Template_Assetto_Corsa_App.py
#           by Your_App_Name_Without_Spaces.py
#
# ------------------------------

import ac, acsys
import platform, os, sys, json
from third_party.sim_info import *
from third_party import requests
import threading, datetime

if platform.architecture()[0] == "64bit":
    sysdir = os.path.dirname(__file__) + '/third_party/'

sys.path.insert(0, sysdir)
os.environ['PATH'] = os.environ['PATH'] + ";."

url = "http://141.148.244.131:1120/record-laptime"
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
    ac.setSize(appWindow, 25 * posScale, 25 * posScale)

    ac.addRenderCallback(appWindow, acUpdate)

    return appName

def acUpdate(deltaT):
    global ac, appWindow, lastLapTime, timerData, simInfo, previousLapValue, lapCount, prevLapCount
    global ticks
    ticks += 1
    
    lastLapTime = simInfo.graphics.iLastTime
    lapCount = ac.getCarState(0, acsys.CS.LapCount)

    if ticks >= 32:
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
        ac.log("Sending data: " + str(params))
        try:
            requests.post(url, data=params, headers=headers, verify=False)
        except:
            pass
