import matplotlib.pyplot as plt
import os
import re

label_num_topologies = ["10","13", "15", "18", "20"]
num_topologies = ["11","14", "16", "19", "21"]
rssi_weights = ["0.050","0.500", "1.000"]
label_weights = ["RSSI W:0.05","RSSI W:0.5", "RSSI W:1.000"]
colors = ["orange","blue","purple"]

def get_spendtime_duration(num_topology, weight):
    path = str.format("%s/%s/" % (num_topology, weight))
    files = os.listdir(path)
    print("files ",files)
    values = []
    for file in files:
        with open(path + file) as f:
            content = f.readlines()
            for line in content:
                if line.startswith("Spend time: "):
                    values.append(int(re.search(r'\d+', line).group(0)))
                    break
    result = 0
    for value in values:
        result += value
    return result / len(values)
for index, weight in enumerate(rssi_weights):
    values = []
    for topo in num_topologies:
        value = get_spendtime_duration(topo, weight)
        values.append(value)
    plt.plot(label_num_topologies, values, color=colors[index], label=label_weights[index])

plt.xlabel("number of nodes")
plt.ylabel("life time(s)")
plt.legend(loc='upper left')
plt.savefig("results.png")