import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os
class Analyse():
    def displayDatabase(self):
        with open('data.json', 'r') as f:
            data = json.load(f)

            # Output: {'name': 'Bob', 'languages': ['English', 'French']}
            committeeSizes = []
            popTimes = []
            basicTimes = []
            popComitteeSize = []
            basicComitteeSize = []

            for key in data:
                value = data[key]
                time = float(value['timeTaken'])
                size = float(value['committeeSize'])
                if value['protocol'] == 'pop':
                    popTimes.append(time)
                    popComitteeSize.append(size)
                elif value['protocol'] == 'basic':
                    basicTimes.append(time)
                    basicComitteeSize.append(size)

            plt.plot(popComitteeSize, popTimes, label='Using POP security')
            plt.plot(basicComitteeSize, basicTimes, label='Using Basic security')
            plt.xlabel('comittee size')
            plt.ylabel('PBFT time execution')
            plt.legend()
            path = 'results/'+'timeComparison'+str(datetime.now().strftime("%Y%m%d%H%M%S"))+'.png'
            print(path)
            plt.savefig(path)
            plt.show()
    
    def saveGraphs(self):
        time = datetime.now()

analysis = Analyse()
analysis.displayDatabase()
