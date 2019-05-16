import json
import os
import subprocess
import sys
import time

filePath = "executables/config.json"

if len(sys.argv) < 5:
    print("number of argument must be bigger than 5.")
    exit(2)

numberOfNodes = sys.argv[1]
numberOfCommandedNodes = sys.argv[2]
RSSIWeight = sys.argv[3]
batteryWeight = sys.argv[4]

exists = os.path.isfile(filePath)
if not exists:
    print(filePath, " is not founds")
    exit(2)

with open(filePath,'r+') as f:
    data = json.load(f)
    data["controller"]["map"]["N_OF_NODES"] = numberOfNodes
    data["controller"]["map"]["N_OF_COMMANDED_NODES"] = numberOfCommandedNodes
    data["controller"]["map"]["RSSI_WEIGHT"] = RSSIWeight
    data["controller"]["map"]["BATTERY_WEIGHT"] = batteryWeight
    f.seek(0)
    f.write(json.dumps(data))
    f.truncate()

time.sleep(5)
procForecast = subprocess.Popen(["./executables/forecast"])
print("PID for forecast:", procForecast.pid)
procCtrl = subprocess.Popen(['java', '-jar', 'executables/sdn-wise-ctrl-4.0.1-SNAPSHOT-jar-with-dependencies.jar', 'executables/config.json'])
print("PID fore ctrl:", procCtrl.pid)
exitCode = procCtrl.wait()
if exitCode != 0:
    print("Problem occurred at CTRL")
else:
    print("Ctrl is finished successfully")
procForecast.kill()
print("Forecast is killed.")
