from tkinter import E
from blspy import (PrivateKey, Util, AugSchemeMPL, PopSchemeMPL,
                   G1Element, G2Element)
import socket 
import time
from _thread import *
import threading
import numpy as np

class Node:
    def __init__(self, seed, isLeader, connections, port, message):
        self.sk = AugSchemeMPL.key_gen(seed)
        self.pk = self.sk.get_g1()
        self.message = message
        self.isLeader = isLeader
        self.connections = connections
        self.port = port
        self.aggregatedSignature = []
        self.pks = []
        self.msgs = []
        self.pk0 = []

    def signMessage(self):
        return PopSchemeMPL.sign(self.sk, self.message)

    def getProof(self):
        return PopSchemeMPL.pop_prove(self.sk)

    def verify(self, other_pk, other_pop):
        return PopSchemeMPL.pop_verify(other_pk, other_pop)

    def aggregate(self, pks):
        return PopSchemeMPL.aggregate(pks)
        
    def popAggregateVerify(self, pks, message, pop_sig_agg):
        return PopSchemeMPL.fast_aggregate_verify(pks, message, pop_sig_agg)

    def listen(self):
        if self.isLeader is True:
            self.leaderListen()
        else:
            self.memberListen()

    def parse(self, data):
        pk = data[0:48]
        proof = data[48:144]
        msg0 = data[144:]

        pk = G1Element.from_bytes(pk)
        msg = G2Element.from_bytes(msg0)
        proof = G2Element.from_bytes(proof)
        return pk, msg, proof, msg0

    def compose(self,arr):
        byteObj = b''
        for element in arr:
            byteObj += bytes(element)
        return byteObj

    def threaded(self, c, aggregatedSignature, pks, msgs, pk0s):
        while True:
    
            data = c.recv(1024)
            if not data:
                # if data is not received break
                break

            pk, msg, proof, msg0 = self.parse(data)
            valid = self.verify(pk, proof)
            print('Pop proof : ', valid)
            # Collect pks, msgs, and aggregated signature to send to each member to validate the aggregated signature
            if valid : 

                aggregatedSignature.append(msg)
                pks.append(pk)
                msgs.append(msg)
                pk0s.append(msg0)
            # Wait for all threads to be finished processing message
            time.sleep(2)
            agg_sig = bytes(PopSchemeMPL.aggregate(aggregatedSignature))
            agg_pks = self.compose(pks)
            agg_msgs = self.compose(msgs)
            print('OK : ', PopSchemeMPL.fast_aggregate_verify(pks, self.message, G2Element.from_bytes(agg_sig)))
            c.send(agg_sig+agg_pks+agg_msgs)  # send data to the client

        c.close()  # close the connection

    def leaderListen(self):
        # put the socket into listening mode
        # get the hostname
        host = socket.gethostname()
        port = 5074  # initiate port no above 1024

        server_socket = socket.socket()  # get instance
        # look closely. The bind() function takes tuple as argument
        server_socket.bind((host, port))  # bind host address and port together

        # configure how many client the server can listen simultaneously
        server_socket.listen(20)
        while True:
            conn, address = server_socket.accept()  # accept new connection
            print("Starting new thread for : " + str(address))
            start_new_thread(self.threaded, (conn,self.aggregatedSignature, self.pks, self.msgs, self.pk0))
            # receive data stream. it won't accept data packet greater than 1024 bytes
        

    def parseMsg(self, payload):
        pks=[]
        msgs=[]
        while(len(payload)!= 0):
            pk = payload[:48]
            msg = payload[len(payload)-96:]
            pks.append(G1Element.from_bytes(pk))
            msgs.append(msg)
            payload = payload[48:len(payload)-96]

        return pks, msgs[::-1]

    def memberListen(self):
      # put the socket into listening mode
        host = socket.gethostname()  # as both code is running on same pc
        port = 5074  # socket server port number

        client_socket = socket.socket()  # instantiate
        client_socket.connect((host, port))  # connect to the server

        pubKey = bytes(self.pk)
        proof = bytes(self.getProof())
        signedMessage = bytes(self.signMessage())
        
        message = pubKey+proof+signedMessage

        while message.lower().strip() != 'bye':
            client_socket.send(message)  # send message
            data = client_socket.recv(4096)  # receive response
            sig = data[:96]
            pks,msgs=self.parseMsg(data[96:])
            print('pks : ', len(pks))
            print('msgs : ', len(msgs))
            print('sig : ', len(sig))
            ok = PopSchemeMPL.aggregate_verify(pks, msgs, G2Element.from_bytes(sig))
            print(ok)

        client_socket.close()  # close the connection
