from pickle import FALSE, TRUE
from blspy import (
    PrivateKey, 
    Util,
    AugSchemeMPL, 
    PopSchemeMPL,
    G1Element, 
    G2Element)
import socket 
import time
from _thread import *
import threading
import numpy as np
from ca import CA 
class Node:
    def __init__(self, seed, isLeader, leaderPort, message, protocol, committeeSize, nodeID, CAReference, BlockchainReference, PopTable):
        self.sk = AugSchemeMPL.key_gen(seed)
        self.pk = self.sk.get_g1()
        self.message = message
        self.isLeader = isLeader
        self.protocol = protocol
        self.validated = True
        self.committeeSize = committeeSize
        self.nodeID = nodeID
        self.sentMsgSize = 0
        self.recvMsgSize = 0
        self.blockhash = ''
        self.certtable = []
        self.pks = []
        self.msgs = []
        self.pops = []
        self.aggregatedSignature = []
        self.popTable = PopTable
        self.cert = CAReference.createCert({'name':self.nodeID,'pk':self.pk})
        self.blockchain = BlockchainReference
        self.pop = self.getProof()
        self.nodeSize = 0

    def size(self, metadata):
        size = 0
        for data in metadata : 
            for entry in data :
                size += len(bytes(entry))

        for entry in self.certtable: size+=entry.size()
        size += self.cert.size()
        
        size += self.popTable.size() 
        size += len(bytes(self.pop))

        size += len(bytes(self.pks))
        size += len(bytes(self.msgs)) 
        return size

    def popSig(self):
        return PopSchemeMPL.sign(self.sk, self.message)

    def getProof(self):
        return PopSchemeMPL.pop_prove(self.sk)

    def verify(self, other_pk, other_pop):
        return PopSchemeMPL.pop_verify(other_pk, other_pop)

    def aggregate(self, pks):
        return PopSchemeMPL.aggregate(pks)
        
    def popAggregateVerify(self, pks, message, pop_sig_agg):
        return PopSchemeMPL.fast_aggregate_verify(pks, message, pop_sig_agg)

    def checkPopsTable(self, pks):
        for pk in pks: 
            if bytes(pk) not in self.popTable.getPops().keys() : 
                return False
        return True 

    def runSignature(self, state):
        if self.protocol == 'pki' : self.certtable = self.blockchain.getCerts()
        else : self.certtable = []

        if self.isLeader is True: self.leaderListen(state)
        else: self.memberListen(state)
        return


    def parseMemberPop(self, data):
        pk = data[0:48]
        sig = data[48:]

        pk = G1Element.from_bytes(pk)
        sig = G2Element.from_bytes(sig)
        return pk, sig

    def parseMemberBasic(self, data):
        pk = data[0:48]
        msg = data[48:53]
        sig = data[53:]

        pk = G1Element.from_bytes(pk)
        sig = G2Element.from_bytes(sig)
        return pk, msg, sig

    def parseMemberLE(self, data):
        pk = data[0:48]
        sig = data[48:]

        pk = G1Element.from_bytes(pk)
        sig = G2Element.from_bytes(sig)
        return pk, sig

    def parseMemberPKI(self, data):
        pk = data[0:48]
        sig = data[48:]

        pk = G1Element.from_bytes(pk)
        sig = G2Element.from_bytes(sig)
        return pk, sig

    def composeBitstring(self, arr):
        bitstring = bin(0)
        for index in range(len(self.certtable)):
            if self.certtable[index].pk == self.pk: bitstring += '0'
            elif self.certtable[index].pk in arr : bitstring += '1'
            else : bitstring += '0'
        return bitstring.encode()

    def compose(self,arr):
        byteObj = b''
        for element in arr: byteObj += bytes(element)
        return byteObj

    def broadcast(self, c, address):
        while True:
            c.send('BLOCKHASH'.encode())
            c.close() 
            break

    def multiSig(self, c, aggregatedSignature, pks, msgs, pops):
        while True:
            data = c.recv(4096)
            if not data:
                # if data is not received break
                break
            
            if self.protocol == 'pop': 
                pk, msg = self.parseMemberPop(data)
                aggregatedSignature.append(msg)
                pks.append(pk)
                msgs.append(msg)
                # pops.append(proof)
            elif self.protocol == 'basic' : 
                pk, msg, sig = self.parseMemberBasic(data)
                aggregatedSignature.append(sig)
                pks.append(pk)
                msgs.append(msg)
            elif self.protocol == 'pki' :
                pk, sig = self.parseMemberPKI(data)
                aggregatedSignature.append(sig)
                pks.append(pk)
            elif self.protocol == 'le': 
                pk, sig = self.parseMemberLE(data)
                aggregatedSignature.append(sig)
                pks.append(pk)

            time.sleep(0.6)
            # time.sleep(0.1*self.committeeSize)
            # Wait for all threads to be finished processing message
            # This could be refactored. 

            if self.protocol == 'pop': 
                agg_sig = bytes(PopSchemeMPL.aggregate(aggregatedSignature))
                agg_pks = self.compose(pks)
                agg_pops = self.compose(pops)
                validPkPops = self.checkPopsTable(pks)
                assert(validPkPops)
                msg = agg_sig+agg_pks
                c.send(msg)  # send data to the client

            elif self.protocol == 'basic': 
                agg_sig = bytes(AugSchemeMPL.aggregate(aggregatedSignature))
                agg_pks = self.compose(pks)
                agg_msgs = self.compose(msgs)
                msg = agg_sig+agg_pks+agg_msgs
                c.send(msg)  # send data to the client

            elif self.protocol == 'pki': 
                agg_sig = bytes(PopSchemeMPL.aggregate(aggregatedSignature))
                bitstring = self.composeBitstring(pks)
                msg = agg_sig+bitstring
                c.send(msg)  # send data to the client

            elif self.protocol == 'le':
                self_sig = AugSchemeMPL.sign(self.sk, self.message)
                agg_sig = bytes(PopSchemeMPL.aggregate(aggregatedSignature))
                agg_pks = self.compose(pks)
                msg = agg_sig+bytes(self_sig)+bytes(self.pk)+agg_pks
                c.send(msg)  # send data to the client

            c.close()  # close the connection
            break

    def leaderListen(self, state):
        host = socket.gethostname()
        port = 5074  # initiate port no above 1024
        server_socket = socket.socket()  # get instance
        server_socket.bind((host, port))  # bind host address and port together
        server_socket.listen(20)
        threads = []
        if state == 'pre-prepare':
            while len(threads) < (self.committeeSize-1):
                conn, address = server_socket.accept()  # accept new connection
                x = threading.Thread(target=self.broadcast, args=(conn, address))
                threads.append(x)
                x.start()
                

        elif state == 'prepare' or state == 'commit':
            while len(threads) != (self.committeeSize-1):
                conn, address = server_socket.accept()  # accept new connection
                x = threading.Thread(target=self.multiSig, args=(conn,self.aggregatedSignature, self.pks, self.msgs, self.pops))
                threads.append(x)
                x.start()
        
        for thread in threads:
            thread.join()

        self.pks = []
        self.msgs = []
        self.aggregatedSignature = []

    def parseLeaderLE(self, payload):
        pks = []
        while(len(payload)!= 0):
            pk = payload[:48]
            pks.append(G1Element.from_bytes(pk))
            payload = payload[48:]
        return pks

    def parseLeaderBasic(self, payload):
        pks=[]
        msgs=[]
        while(len(payload)!= 0):
            pk = payload[:48]
            msg = payload[len(payload)-5:]
            pks.append(G1Element.from_bytes(pk))
            msgs.append(msg)
            payload = payload[48:len(payload)-5]

        return pks, msgs[::-1]

    def parseLeaderPopV1(self, payload):
        pks=[]
        pops=[]
        while(len(payload)!= 0):
            pk = payload[:48]
            pks.append(G1Element.from_bytes(pk))
            pop = payload[len(payload)-96:]
            pops.append(G2Element.from_bytes(pop))
            payload = payload[48:len(payload)-96]
            payload = payload[48:]
        pops.reverse()
        for index in range(len(pks)):
            pop = pops[index]
            pk = pks[index]
            PopSchemeMPL.pop_verify(pk, pop)
        return pks


    def parseLeaderPop(self, payload):
        pks=[]
        pops=[]
        while(len(payload)!= 0):
            pk = payload[:48]
            pks.append(G1Element.from_bytes(pk))
            payload = payload[48:]
        return pks

    def parseLeaderPKI(self, payload):
        pks=[]
        payload = payload.decode()[3:]

        for cert in self.certtable:
            isParticipant = payload[0:1]
            if isParticipant == '1':
                pks.append(G1Element.from_bytes(bytes(cert.pk)))
            payload = payload[1:]
        return pks

    def initPop(self):
        pk = bytes(self.pk)
        popSig = bytes(self.popSig())
        proof = bytes(self.getProof())
        message = pk+popSig
        return message 

    def initBasic(self):
        pk = bytes(self.pk)
        msg = self.message
        basicSig = bytes(AugSchemeMPL.sign(self.sk, msg))
        message = pk+msg+basicSig
        return message 

    def initPKI(self):
        pk = bytes(self.pk)
        msg = self.message
        sig = bytes(self.popSig())
        message = pk+sig
        return message 

    def initLE(self):
        pk = bytes(self.pk)
        msg = self.message
        sig = bytes(self.popSig())
        message = pk+sig  
        return message 

    def handlePreprepare(self, client_socket, data):
        self.blockhash = data.decode()
        client_socket.close() 
        quit()

    def handlePopResponse(self, data, sig):
        pks=self.parseLeaderPop(data[96:])
        validPkPops = self.checkPopsTable(pks)
        verifyMultiSignature = PopSchemeMPL.fast_aggregate_verify(pks, self.message, G2Element.from_bytes(sig))
        self.validated = verifyMultiSignature
        self.nodeSize = self.size([pks])       
        assert(validPkPops)
        assert(verifyMultiSignature)

    def handleBasicResponse(self, data, sig):
        pks,msgs=self.parseLeaderBasic(data[96:])     
        verifyMultiSignature = AugSchemeMPL.aggregate_verify(pks, msgs, G2Element.from_bytes(sig))
        self.validated = verifyMultiSignature       
        self.nodeSize = self.size([pks, msgs])
        assert(verifyMultiSignature)

    def handlePKIResponse(self, data, sig):
        bitstring = data[96:]
        pks=self.parseLeaderPKI(bitstring)   
        verifyMultiSignature = PopSchemeMPL.fast_aggregate_verify(pks, self.message, G2Element.from_bytes(sig))
        self.validated = verifyMultiSignature  
        self.nodeSize = self.size([pks])     
        assert(verifyMultiSignature)

    def handleLEResponse(self, data, sig):
        leaderSig = G2Element.from_bytes(data[96:192])
        leaderPk = G1Element.from_bytes(data[192:240])
        pks =self.parseLeaderLE(data[240:])
        verifyLeader = AugSchemeMPL.verify(leaderPk, self.message, leaderSig)
        verifyMultiSignature = PopSchemeMPL.fast_aggregate_verify(pks, self.message, G2Element.from_bytes(sig))
        self.validated = verifyMultiSignature
        self.nodeSize = self.size([pks, [leaderSig, leaderPk]])
        assert(verifyLeader)
        assert(verifyMultiSignature)

    def memberListen(self, state):
        host = socket.gethostname()  
        client_socket = socket.socket()  
        port = 5074  
        client_socket.connect((host, port))

        # INFORMATION SENDING PHASE
        if self.protocol == 'pop' : message = self.initPop()
        elif self.protocol == 'basic' :  message = self.initBasic()
        elif self.protocol == 'pki':  message = self.initPKI()
        elif self.protocol == 'le': message = self.initLE()         
        if state != 'pre-prepare': client_socket.send(message) 
        
        # INFORMATION RECEIVING PHASE
        data = client_socket.recv(16000)  # receive response
        if state == 'pre-prepare': self.handlePreprepare(client_socket, data)

        sig = data[:96]
        if self.protocol == 'pop' : self.handlePopResponse(data,sig)
        elif self.protocol == 'basic' : self.handleBasicResponse(data,sig)
        elif self.protocol == 'pki' : self.handlePKIResponse(data,sig)
        elif self.protocol == 'le' : self.handleLEResponse(data,sig)
        
        # assert(verifyMultiSignature)
        # initialize various analytics 
        self.nodeToLeaderMsgSize = len(message)
        self.leaderToNodeMsgSize = len(data)
        client_socket.close()  # close the connection