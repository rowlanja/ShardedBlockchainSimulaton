import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os
class Analyse():
    def displaySpeed(self):
        with open('data.json', 'r') as f:
            data = json.load(f)

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

    def displayMsgSize(self):
        with open('msgSizes.json', 'r') as f:
            data = json.load(f)

            popNodeToLeaderMsgSizes = []
            popLeaderToNodeMsgSizes = []
            basicNodeToLeaderMsgSizes = []
            basicLeaderToNodeMsgSizes = []
            popComitteeSize = []
            basicComitteeSize = []

            for key in data:
                value = data[key]
                print(value)
                nodeToLeader = float(value['nodeToLeader'])
                leaderToNode = float(value['leaderToNode'])
                comSize =  int(value['committeeSize'])
                if value['protocol'] == 'pop':
                    popNodeToLeaderMsgSizes.append(nodeToLeader+1)
                    popLeaderToNodeMsgSizes.append(leaderToNode+1)
                    popComitteeSize.append(comSize)
                elif value['protocol'] == 'basic':
                    basicNodeToLeaderMsgSizes.append(nodeToLeader-1)
                    basicLeaderToNodeMsgSizes.append(leaderToNode-1)
                    basicComitteeSize.append(comSize)

            plt.plot(popComitteeSize, popNodeToLeaderMsgSizes, label='Node to Leader msg size during PoP')
            plt.plot(popComitteeSize, popLeaderToNodeMsgSizes, label='Leader to Node msg size during Pop')
            plt.plot(basicComitteeSize, basicNodeToLeaderMsgSizes, label='Node to Leader msg size during Basic')
            plt.plot(basicComitteeSize, basicLeaderToNodeMsgSizes, label='Leader to Node msg size during Basic')
  
            plt.xlabel('comittee size')
            plt.ylabel('Msg size (bytes)')
            plt.legend()
            path = 'results/'+'msgSizeComparison'+str(datetime.now().strftime("%Y%m%d%H%M%S"))+'.png'
            print(path)
            plt.savefig(path)
            plt.show()
    
    def saveGraphs(self):
        time = datetime.now()