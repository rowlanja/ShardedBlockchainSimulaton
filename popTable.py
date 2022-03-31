#   blockchain

class PopTable:
    def __init__(self):
        self.pops = {}
        

    def addPop(self, pk, pop):
        self.pops[pk] = pop

    def addPops(self, pkpops):
        for key, value in pkpops.items():
            self.pops[key] = value

    def getPops(self):
        pops = self.pops
        return pops
