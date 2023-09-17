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
    global ac, appWindow, trackNameLabel, carNameLabel, driverNameLabel, currentLapLabel, previousLapLabel, speedLabel, lastLapTime, currentSpeedInKPH, timerData, simInfo, previousLapValue, lapCountLabel, prevLapCount

    appWindow = ac.newApp(appName)
    ac.setTitle(appWindow, appName)
    ac.drawBorder(appWindow, 0)
    ac.setIconPosition(appWindow, 0, -10000)
    ac.setSize(appWindow, 704 * posScale, 240 * posScale)

    # Initialize font
    ac.initFont(0, "Consolas", 1, 1)

    # Track name
    trackNameLabel = ac.addLabel(appWindow, "Track: ")
    ac.setPosition(trackNameLabel, 40 * posScale, 40 * posScale)
    ac.setFontSize(trackNameLabel, 24 * fontScale)
    ac.setCustomFont(trackNameLabel, "Consolas", 0, 1)
    ac.setText(trackNameLabel, "Track: " + ac.getTrackName(0))

    # Car name
    carNameLabel = ac.addLabel(appWindow, "Car: ")
    ac.setPosition(carNameLabel, 40 * posScale, 52 * posScale)
    ac.setFontSize(carNameLabel, 24 * fontScale)
    ac.setCustomFont(carNameLabel, "Consolas", 0, 1)
    ac.setText(carNameLabel, "Car: " + ac.getCarName(0))

    # Driver name
    driverNameLabel = ac.addLabel(appWindow, "Driver: ")
    ac.setPosition(driverNameLabel, 40 * posScale, 64 * posScale)
    ac.setFontSize(driverNameLabel, 24 * fontScale)
    ac.setCustomFont(driverNameLabel, "Consolas", 0, 1)
    ac.setText(driverNameLabel, "Driver: " + ac.getDriverName(0))

    # Previous lap
    previousLapLabel = ac.addLabel(appWindow, "Previous lap: ")
    ac.setPosition(previousLapLabel, 40 * posScale, 12 * posScale)
    ac.setFontSize(previousLapLabel, 24 * fontScale)
    ac.setCustomFont(previousLapLabel, "Consolas", 0, 1)

    # Current lap
    currentLapLabel = ac.addLabel(appWindow, "Current lap:")
    ac.setPosition(currentLapLabel, 40 * posScale, 25 * posScale)
    ac.setFontSize(currentLapLabel, 24 * fontScale)
    ac.setCustomFont(currentLapLabel, "Consolas", 0, 1)

    # Speed
    speedLabel = ac.addLabel(appWindow, "---")
    ac.setPosition(speedLabel, 40 * posScale, 79 * posScale)
    ac.setFontSize(speedLabel, 12 * fontScale)
    ac.setCustomFont(speedLabel, "Consolas", 0, 1)
    ac.setFontAlignment(speedLabel, "center")

    # Lapcount
    lapCountLabel = ac.addLabel(appWindow, "Lapcount: ")
    ac.setPosition(lapCountLabel, 40 * posScale, 91 * posScale)
    ac.setFontSize(lapCountLabel, 24 * fontScale)
    ac.setCustomFont(lapCountLabel, "Consolas", 0, 1)
    ac.setText(lapCountLabel, "Lapcount: " + str(ac.getCarState(0, acsys.CS.LapCount)))

    ac.addRenderCallback(appWindow, acUpdate)

    return appName

def acUpdate(deltaT):
    global ac, appWindow, currentLapLabel, previousLapLabel, speedLabel, lastLapTime, timerData, simInfo, previousLapValue, lapCount, prevLapCount
    global ticks
    ticks += 1
    
    lastLapTime = simInfo.graphics.iLastTime
    lapCount = ac.getCarState(0, acsys.CS.LapCount)

    if prevLapCount != lapCount:
        prevLapCount = lapCount
        if ticks >= 16:
            laptime_data = {
                "laptime": lastLapTime,
                "circuit": ac.getTrackName(0),
                "car": ac.getCarName(0),
                "driver": ac.getDriverName(0)
            }
            t = threading.Thread(target=sendInfo(laptime_data))
            t.start()
            ac.log("Thread started, sending data...")
            ticks = 0

    # Display current laptime in the app window
    ac.setText(currentLapLabel, str(lastLapTime))
    ac.setText(lapCountLabel, str(lapCount))

def sendInfo(data):
    headers = {'Content-Type': 'application/json'}
    params = json.dumps(data).encode('utf8')
    ac.log("Sending data: " + str(params))
    try:
        requests.post(url, data=params, headers=headers, verify=False)
    except:
        pass
