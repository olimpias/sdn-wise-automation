import json
import os
import subprocess
import sys
import time
import re
import http.client


filePath = "executables/config.json"

topology_iteration_count = 10
label_num_topologies = ["10","13", "15", "18", "20"]
num_topologies = ["11","14", "16", "19", "21"]
rssi_weights = ["0.050","0.500", "1.000"]
battery_weights = ["0.95", "0.500","0"]

remoteIpAddress = ""
remoteFormatURL = "%s:9001"
remoteURL = ""


def executeController(numberOfNodes, numberOfMoteNotes, numberOfCommandedNodes, RSSIWeight, batteryWeight, topologyLabel):
    print("Ctrl will run for numberOfNodes:%s, numberOfCommandedNodes:%s, RSSIWeight:%s, batteryWeight:%s, topologyLabel:%d" %
          (numberOfNodes, numberOfCommandedNodes, RSSIWeight, batteryWeight, topologyLabel))
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
        data["controller"]["map"]["LABEL"] = topologyLabel
        f.seek(0)
        f.write(json.dumps(data))
        f.truncate()

    time.sleep(5)
    procForecast = subprocess.Popen(["./executables/forecast"])
    print("PID for forecast:", procForecast.pid)
    procCtrl = subprocess.Popen(['java', '-jar', 'executables/sdn-wise-ctrl-4.0.1-SNAPSHOT-jar-with-dependencies.jar', 'executables/config.json'])
    print("PID fore ctrl:", procCtrl.pid)
    time.sleep(5)
    if triggerVMAutomation(numberOfMoteNotes, topologyLabel - 1):
        exitCode = procCtrl.wait()
        if exitCode != 0:
            print("Problem occurred at CTRL")
        else:
            print("Ctrl is finished successfully")
    else:
        print("Starting VM automation is failed")
        procCtrl.kill()
    procForecast.kill()
    print("Forecast is killed.")

def triggerVMAutomation(topo, id):
    try:
        headerVal = "%s:%d" % (topo, id)
        headers = {"applypath": headerVal}
        conn = http.client.HTTPConnection(remoteURL)
        conn.request("GET", "", "", headers)
        print("Data will be sent to %s; applypath: %s" % (topo, id))
        response = conn.getresponse()
        return response.status == 200
    except:
        e = sys.exc_info()[0]
        print(e)
        return False

def is_time_value_acceptable(num_topology, weight,topologyLabel):
    path = str.format("%s/%s/" % (num_topology, weight))
    files = os.listdir(path)
    for file in files:
        if file.find("t%d" % (topologyLabel)) == 0:
            with open(path + file) as f:
                content = f.readlines()
                for line in content:
                    if line.startswith("Spend time: "):
                        val = int(re.search(r'\d+', line).group(0))
                        return val > 500
    return False

def remove_file(num_topology, weight,topology_label):
    path = str.format("%s/%s/" % (num_topology, weight))
    files = os.listdir(path)
    searchText = "t%d.data" % (topology_label)
    for file in files:
        if searchText in file:
            os.remove(path + file)
            print("File is removed -> ",path + file)

if len(sys.argv) < 2:
    print("remoteIpAddress")
    exit(2)

remoteIpAddress = sys.argv[1]

remoteURL = remoteFormatURL % (remoteIpAddress)

for index, weight in enumerate(rssi_weights):
    values = []
    for topo_index, topo in enumerate(num_topologies):
        counter = 0
        while counter != topology_iteration_count:
            while not is_time_value_acceptable(topo, weight, counter + 1):
                remove_file(topo, weight, counter + 1)
                executeController(topo, label_num_topologies[topo_index], 3, weight, battery_weights[index], counter + 1)
            counter += 1