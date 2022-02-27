from node import Node
import logging
import threading
import time
import secrets


    # for index, thread in enumerate(threads):
    #     logging.info("Main    : before joining thread %d.", index)
    #     thread.join()
    #     logging.info("Main    : thread %d done", index)

class Committee:
    def __init__(self, protocol, committeeSize):
        self.announce = False
        self.prepare = False
        self.commit = False
        self.nodes = []
        self.protocol = protocol
        self.committeeSize = committeeSize

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

    def threadFunction(self, node):
        node.runSignature()

    def main(self):
        for x in range(self.committeeSize):
            if x == 0:self.nodes.append(Node(secrets.token_bytes(32), True, 5074, bytes([1, 2, 3, 4, 5]), self.protocol,self.committeeSize,x))
            else :self.nodes.append(Node(secrets.token_bytes(32), False, 5074, bytes([1, 2, 3, 4, 5]), self.protocol,self.committeeSize,x))
        format = "%(asctime)s: %(message)s"
        logging.basicConfig(format=format, level=logging.INFO,
                            datefmt="%H:%M:%S")
        self.PBFT()

