from tkinter import E
from blspy import (PrivateKey, Util, AugSchemeMPL, PopSchemeMPL,
                   G1Element, G2Element)
import socket 
import time
from _thread import *
import threading
import numpy as np

class Node:
    def __init__(self, seed, isLeader, leaderPort, message, protocol, committeeSize, nodeID):
        self.sk = AugSchemeMPL.key_gen(seed)
        self.pk = self.sk.get_g1()
        self.message = message
        self.isLeader = isLeader
        self.aggregatedSignature = []
        self.pks = []
        self.msgs = []
        self.protocol = protocol
        self.validated = False
        self.committeeSize = committeeSize
        self.nodeID = nodeID
        self.sentMsgSize = 0
        self.recvMsgSize = 0
        self.blockhash = ''

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

    def runSignature(self, state):
        if self.isLeader is True:
            self.leaderListen(state)
        else:
            self.memberListen(state)
        return

    def parsePop(self, data):
        pk = data[0:48]
        proof = data[48:144]
        msg = data[144:]

        pk = G1Element.from_bytes(pk)
        msg = G2Element.from_bytes(msg)
        proof = G2Element.from_bytes(proof)
        return pk, msg, proof

    def parseBasic(self, data):
        pk = data[0:48]
        msg = data[48:53]
        sig = data[53:]

        pk = G1Element.from_bytes(pk)
        sig = G2Element.from_bytes(sig)
        return pk, msg, sig

    def compose(self,arr):
        byteObj = b''
        for element in arr:
            byteObj += bytes(element)
        return byteObj

    def broadcast(self, c):
        while True:
            c.send('BLOCKHASH'.encode())
            c.close() 
            break


    def formMultiSig(self, c, aggregatedSignature, pks, msgs, recvMsgSize, sentMsgSize):
        while True:
    
            data = c.recv(4096)
            if not data:
                # if data is not received break
                break
            
            if self.protocol == 'pop': 
                pk, msg, proof = self.parsePop(data)
                if self.verify(pk, proof):
                    aggregatedSignature.append(msg)
                    pks.append(pk)
                    msgs.append(msg)
            elif self.protocol == 'basic' : 
                pk, msg, sig = self.parseBasic(data)
                aggregatedSignature.append(sig)
                pks.append(pk)
                msgs.append(msg)

            # if len(pks) == (self.committeeSize-1):
            time.sleep(0.1)
            # Wait for all threads to be finished processing message

            if self.protocol == 'pop': 
                agg_sig = bytes(PopSchemeMPL.aggregate(aggregatedSignature))
                agg_pks = self.compose(pks)
                msg = agg_sig+agg_pks
                c.send(msg)  # send data to the client
            elif self.protocol == 'basic': 
                agg_sig = bytes(AugSchemeMPL.aggregate(aggregatedSignature))
                agg_pks = self.compose(pks)
                agg_msgs = self.compose(msgs)
                msg = agg_sig+agg_pks+agg_msgs
                c.send(msg)  # send data to the client
            # print(' Before sent OK : ', PopSchemeMPL.fast_aggregate_verify(pks, self.message, G2Element.from_bytes(agg_sig)))
            c.close()  # close the connection
            break

    def leaderListen(self, state):
        print('leader state : ', state)
        host = socket.gethostname()
        port = 5074  # initiate port no above 1024
        server_socket = socket.socket()  # get instance
        server_socket.bind((host, port))  # bind host address and port together
        server_socket.listen(20)
        if state == 'pre-prepare':
            connections = 0
            while connections != (self.committeeSize-1):
                conn, address = server_socket.accept()  # accept new connection
                start_new_thread(self.broadcast, (conn,))
                connections+=1
        elif state == 'prepare' or state == 'commit':
            connections = 0
            while connections != (self.committeeSize-1):
                conn, address = server_socket.accept()  # accept new connection
                start_new_thread(self.formMultiSig, (conn,self.aggregatedSignature, self.pks, self.msgs, self.recvMsgSize, self.sentMsgSize))
                connections+=1
        self.pks = []
        self.msgs = []
        self.aggregatedSignature = []

    def basicParse(self, payload):
        pks=[]
        msgs=[]
        while(len(payload)!= 0):
            pk = payload[:48]
            msg = payload[len(payload)-5:]
            pks.append(G1Element.from_bytes(pk))
            msgs.append(msg)
            payload = payload[48:len(payload)-5]

        return pks, msgs[::-1]

    def popParse(self, payload):
        pks=[]
        msgs=[]
        while(len(payload)!= 0):
            pk = payload[:48]
            pks.append(G1Element.from_bytes(pk))
            payload = payload[48:]

        return pks

    def memberListen(self, state):
        # put the socket into listening mode
        host = socket.gethostname()  # as both code is running on same pc
        port = 5074  # socket server port number

        client_socket = socket.socket()  # instantiate
        client_socket.connect((host, port))  # connect to the server

        # INFORMATION SENDING PHASE
        pubKey = bytes(self.pk)
        if self.protocol == 'pop' : 
            popSig = bytes(self.popSig())
            proof = bytes(self.getProof())
            message = pubKey+proof+popSig
        elif self.protocol == 'basic' : 
            #need to send pubKey, msg, sig
            msg = self.message
            basicSig = bytes(AugSchemeMPL.sign(self.sk, msg))
            message = pubKey+msg+basicSig
        if state != 'pre-prepare':
            client_socket.send(message)  # send message

        # INFORMATION RECEIVING PHASE
        data = client_socket.recv(4096)  # receive response
        if state == 'pre-prepare':
            self.blockhash = data.decode()
            client_socket.close()  # close the connection
            return

        sig = data[:96]
        self.nodeToLeaderMsgSize = len(message)
        self.leaderToNodeMsgSize = len(data)
        # print('recieved from leader during : ', self.protocol, " is ", len(data))
        if self.protocol == 'pop' : 
            pks=self.popParse(data[96:])
            ok = PopSchemeMPL.fast_aggregate_verify(pks, self.message, G2Element.from_bytes(sig))
        elif self.protocol == 'basic' : 
            pks,msgs=self.basicParse(data[96:])        
            ok = AugSchemeMPL.aggregate_verify(pks, msgs, G2Element.from_bytes(sig))
        client_socket.close()  # close the connection
        # if ok : self.validated = True
        
 