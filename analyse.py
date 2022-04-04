import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os
class Analyse():
    def displaySpeed(self):
        print('displaying speed')
        with open('data/timeTaken.json', 'r') as f:
            data = json.load(f)

            popTimes = []
            basicTimes = []
            pktableTimes = []
            leaderExcludedTimes = []
            popComitteeSize = []
            basicComitteeSize = []
            pktableComitteeSize = []
            leaderExcludedComitteeSize = []

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
                elif value['protocol'] == 'le':
                    leaderExcludedTimes.append(time)
                    leaderExcludedComitteeSize.append(size)                

            plt.plot(popComitteeSize, popTimes, label='Existing : Proof-of-Possession')
            plt.plot(basicComitteeSize, basicTimes, label='Existing : Distinct Messages')
            plt.plot(pktableComitteeSize, pktableTimes, label='Proposed : Public Key Cert Table ')
            plt.plot(leaderExcludedComitteeSize, leaderExcludedTimes, label='Proposed : Leader Excluded')

            plt.xlabel('comittee size')
            plt.ylabel('Time taken to reach consensus (seconds)')
            plt.legend()
            plt.title('Time Taken to Reach Consensus')
            path = 'results/'+'timeComparison'+'.png'
            plt.savefig(path)
            plt.show()

    def displayMsgSize(self):
        with open('data/msgSizes.json', 'r') as f:
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
                    popNodeToLeaderMsgSizes.append(nodeToLeader-1)
                    popLeaderToNodeMsgSizes.append(leaderToNode-1)
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
                
            
            plt.plot(popComitteeSize, popLeaderToNodeMsgSizes, label='Existing : Proof-of-Possession')
            plt.plot(basicComitteeSize, basicLeaderToNodeMsgSizes, label='Existing : Distinct Messages')
            plt.plot(PKTComitteeSize, PKTLeaderToNodeMsgSizes, label='Proposed : Public Key Cert Table')
            plt.plot(LEComitteeSize, LELeaderToNodeMsgSizes, label='Proposed : Leader Excluded')
            plt.xlabel('comittee size')
            plt.ylabel('Msg Size (bytes)')
            plt.legend()
            plt.title('Message Size from Leader to Member')
            path = 'results/'+'msgSizeLeadertoMemberComparison'+'.png'
            plt.savefig(path)
            plt.show()
            plt.clf()

            barYs = [popNodeToLeaderMsgSizes[0], basicNodeToLeaderMsgSizes[0], PKTNodeToLeaderMsgSizes[0], LENodeToLeaderMsgSizes[0]]
            barXs = ['PoP', 'DM', 'PKT', 'LE']
            # plt.plot(popComitteeSize, popNodeToLeaderMsgSizes, label='Existing : Proof-of-Possession')
            # plt.plot(basicComitteeSize, basicNodeToLeaderMsgSizes, label='Existing : Distinct Messages')
            # plt.plot(PKTComitteeSize, PKTNodeToLeaderMsgSizes, label='Proposed : Public Key Cert Table')
            # plt.plot(LEComitteeSize, LENodeToLeaderMsgSizes, label='Proposed : Leader Excluded')
            plt.bar(barXs, barYs)
            plt.xlabel('Defence Mechanism')
            plt.ylabel('Msg Size (bytes)')
            plt.legend()
            plt.title('Message Size from Member to Leader')
            path = 'results/'+'msgSizeMembertoLeaderComparison'+'.png'
            plt.savefig(path)
            plt.show()
            plt.clf()

    def displayNodeSize(self):
        with open('data/nodeSizes.json', 'r') as f:
            data = json.load(f)

            popNodeSizes = []
            popComitteeSize = []            
            
            basicNodeSizes = []
            basicComitteeSize = []

            PKTNodeSizes = []
            PKTComitteeSize = []

            LENodeSizes = []
            LEComitteeSize = []

            for key in data:
                value = data[key]
                nodeSize = float(value['nodeSize'])
                comSize =  int(value['committeeSize'])
                if value['protocol'] == 'pop':
                    popNodeSizes.append(nodeSize)
                    popComitteeSize.append(comSize)
                elif value['protocol'] == 'basic':
                    basicNodeSizes.append(nodeSize)
                    basicComitteeSize.append(comSize)
                elif value['protocol'] == 'pki':
                    PKTNodeSizes.append(nodeSize)
                    PKTComitteeSize.append(comSize)
                elif value['protocol'] == 'le':
                    LENodeSizes.append(nodeSize)
                    LEComitteeSize.append(comSize)
                
            
            plt.plot(popComitteeSize, popNodeSizes, label='Existing : Proof-of-Possession')
            plt.plot(basicComitteeSize, basicNodeSizes, label='Existing : Distinct Messages')
            plt.plot(PKTComitteeSize, PKTNodeSizes, label='Proposed : Public Key Cert Table')
            plt.plot(LEComitteeSize, LENodeSizes, label='Proposed : Leader Excluded')
            plt.xlabel('Comittee size')
            plt.ylabel('Node Size (bytes)')
            plt.legend()
            plt.title('Node Size')
            path = 'results/'+'nodeSizeComparison'+'.png'
            plt.savefig(path)
            plt.show()
            plt.clf()

 

    
    def saveGraphs(self):
        time = datetime.now()


# analysis = Analyse()
# analysis.displayNodeSize()