import matplotlib.pyplot as plt
import os
import re
import sys

label_num_topologies = ["10","13", "15", "18", "20","22","25","28","30"]
num_topologies = ["11","14", "16", "19", "21","23", "26", "29", "31"]
rssi_weights = ["0.050","0.500", "1.000"]
label_weights = ["RSSI W:0.05","RSSI W:0.5", "RSSI W:1.000"]
colors = ["orange","blue","purple"]

def get_spendtime_duration(num_topology, weight):
    path = str.format("%s/%s/" % (num_topology, weight))
    files = os.listdir(path)
    print("files ",files)
    values = []
    min_value = sys.maxsize
    max_value = 1 - sys.maxsize
    for file in files:
        with open(path + file) as f:
            content = f.readlines()
            for line in content:
                if line.startswith("Spend time: "):
                    values.append(int(re.search(r'\d+', line).group(0)))
                    break
    result = 0
    for value in values:
        if min_value > value:
            min_value = value
        if max_value < value:
            max_value = value
        result += value
    return result / len(values), max_value, min_value
for index, weight in enumerate(rssi_weights):
    values = []
    for topoIndex, topo in enumerate(num_topologies):
        value, max_value, min_value = get_spendtime_duration(topo, weight)
        values.append(value)
    plt.plot(label_num_topologies, values, color=colors[index], label=label_weights[index])

plt.xlabel("number of nodes")
plt.ylabel("life time(s)")
#plt.legend(loc='upper left')
plt.savefig("results.png")