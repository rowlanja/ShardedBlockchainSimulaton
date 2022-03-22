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
            pktableTimes = []
            popComitteeSize = []
            basicComitteeSize = []
            pktableComitteeSize = []
            
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
                elif value['protocol'] == 'pki':
                    pktableTimes.append(time)
                    pktableComitteeSize.append(size)
                

            plt.plot(popComitteeSize, popTimes, label='Using POP security')
            plt.plot(basicComitteeSize, basicTimes, label='Using Basic security')
            plt.plot(pktableComitteeSize, pktableTimes, label='Using PK Cert Table security')

            plt.xlabel('comittee size')
            plt.ylabel('PBFT time execution')
            plt.legend()
            path = 'results/'+'timeComparison'+str(datetime.now().strftime("%Y%m%d%H%M%S"))+'.png'
            plt.savefig(path)
            plt.show()

    def displayMsgSize(self):
        with open('msgSizes.json', 'r') as f:
            data = json.load(f)

            popNodeToLeaderMsgSizes = []
            popLeaderToNodeMsgSizes = []
            popComitteeSize = []            
            
            basicNodeToLeaderMsgSizes = []
            basicLeaderToNodeMsgSizes = []
            basicComitteeSize = []

            PKTNodeToLeaderMsgSizes = []
            PKTLeaderToNodeMsgSizes = []
            PKTComitteeSize = []

            LENodeToLeaderMsgSizes = []
            LELeaderToNodeMsgSizes = []
            LEComitteeSize = []

            for key in data:
                value = data[key]
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
                elif value['protocol'] == 'pki':
                    PKTNodeToLeaderMsgSizes.append(nodeToLeader-1)
                    PKTLeaderToNodeMsgSizes.append(leaderToNode-1)
                    PKTComitteeSize.append(comSize)
                elif value['protocol'] == 'le':
                    LENodeToLeaderMsgSizes.append(nodeToLeader-1)
                    LELeaderToNodeMsgSizes.append(leaderToNode-1)
                    LEComitteeSize.append(comSize)
                

            plt.plot(popComitteeSize, popNodeToLeaderMsgSizes, label='Node to Leader msg size ( PoP )')
            plt.plot(popComitteeSize, popLeaderToNodeMsgSizes, label='Leader to Node msg size ( Pop )')

            plt.plot(basicComitteeSize, basicNodeToLeaderMsgSizes, label='Node to Leader msg size ( DM ) ')
            plt.plot(basicComitteeSize, basicLeaderToNodeMsgSizes, label='Leader to Node msg size ( DM )')

            plt.plot(PKTComitteeSize, PKTNodeToLeaderMsgSizes, label='Node to Leader msg size ( PKCert Table )')
            plt.plot(PKTComitteeSize, PKTLeaderToNodeMsgSizes, label='Leader to Node msg size ( PKCert Table )')
  
            plt.xlabel('comittee size')
            plt.ylabel('Msg size (bytes)')
            plt.legend()
            path = 'results/'+'msgSizeComparison'+str(datetime.now().strftime("%Y%m%d%H%M%S"))+'.png'
            plt.savefig(path)
            plt.show()
    
    def saveGraphs(self):
        time = datetime.now()