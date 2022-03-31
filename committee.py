from node import Node
import threading
import secrets
from ca import CA 
from blockchain import Blockchain
from popTable import PopTable
import time

class Committee:
    def __init__(self, protocol, committeeSize):
        self.announce = False
        self.prepare = False
        self.commit = False
        self.validated = True
        self.nodes = []
        self.protocol = protocol
        self.committeeSize = committeeSize
        self.leaderToNodeMsgSize = 0
        self.nodeToLeaderMsgSize = 0
        self.TimeA = 0
        self.TimeB = 0
        self.TimeC = 0
        
    def cleanUp(self):
        for x in self.nodes:
            x.pks=[]

    def runState(self, state):
        threads = []
        for index in range(len(self.nodes)):
            node = self.nodes[index]
            x = threading.Thread(target=self.threadFunction, args=(node,state,))
            threads.append(x)
            x.start()
        for thread in threads:
            thread.join()
        print('FINISHED : ', state)

    def checkValidRound(self):
        for node in self.nodes:
            if node.validated == False : 
                self.validated = False

    def PBFT(self):
        self.runState('pre-prepare')
        self.checkValidRound()
        self.runState('prepare')
        self.checkValidRound()
        self.runState('commit')
        self.checkValidRound()
        self.nodeToLeaderMsgSize = (self.nodes[2].nodeToLeaderMsgSize)
        self.leaderToNodeMsgSize = (self.nodes[2].leaderToNodeMsgSize)


    def threadFunction(self, node, state):
        node.runSignature(state)

    def main(self):
        CAReference = CA()
        BlockchainReference = Blockchain()
        popTable = PopTable()
        certificates = []
        pops = {}
        pks = []
        for x in range(self.committeeSize):
            if x == 0:self.nodes.append(Node(secrets.token_bytes(32), True, 5074, bytes([1, 2, 3, 4, 5]), self.protocol,self.committeeSize,x, CAReference, BlockchainReference, popTable))
            else :self.nodes.append(Node(secrets.token_bytes(32), False, 5074, bytes([1, 2, 3, 4, 5]), self.protocol,self.committeeSize,x, CAReference, BlockchainReference, popTable))
            certificates.append(self.nodes[len(self.nodes)-1].cert)
            pops[bytes(self.nodes[len(self.nodes)-1].pk)] = self.nodes[len(self.nodes)-1].pop
            
        BlockchainReference.addCerts(certificates)
        popTable.addPops(pops)
        self.PBFT()
        # print('cert count : ', len(certificates))
        # for cert in certificates:
        #     print('cert pk : ', cert.pk)
        # print('node pk : ', self.nodes[0].pk)

