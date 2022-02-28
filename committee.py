from node import Node
import threading
import secrets


class Committee:
    def __init__(self, protocol, committeeSize):
        self.announce = False
        self.prepare = False
        self.commit = False
        self.nodes = []
        self.protocol = protocol
        self.committeeSize = committeeSize
        self.leaderToNodeMsgSize = 0
        self.nodeToLeaderMsgSize = 0

    def cleanUp(self):
        for x in self.nodes:
            x.pks=[]

    def runRound(self, phase):
        threads = []
        for index in range(len(self.nodes)):
            node = self.nodes[index]
            x = threading.Thread(target=self.threadFunction, args=(node,))
            threads.append(x)
            x.start()

        for thread in threads:
            thread.join()

        print('FINISHED : ', phase)

    def PBFT(self):
        self.runRound('Announce')
        self.runRound('Prepare')
        self.runRound('Commit')
        self.nodeToLeaderMsgSize = (self.nodes[2].nodeToLeaderMsgSize)
        self.leaderToNodeMsgSize = (self.nodes[2].leaderToNodeMsgSize)

    def threadFunction(self, node):
        node.runSignature()

    def main(self):
        for x in range(self.committeeSize):
            if x == 0:self.nodes.append(Node(secrets.token_bytes(32), True, 5074, bytes([1, 2, 3, 4, 5]), self.protocol,self.committeeSize,x))
            else :self.nodes.append(Node(secrets.token_bytes(32), False, 5074, bytes([1, 2, 3, 4, 5]), self.protocol,self.committeeSize,x))
        self.PBFT()

