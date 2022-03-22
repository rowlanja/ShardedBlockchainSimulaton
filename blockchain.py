#   blockchain

class Blockchain:
    def __init__(self):
        self.blockchain = []
        

    def addCert(self, cert):
        self.blockchain.append(cert)

    def addCerts(self, certs):
        self.blockchain = self.blockchain + certs

    def getCerts(self):
        certs = self.blockchain
        return certs
