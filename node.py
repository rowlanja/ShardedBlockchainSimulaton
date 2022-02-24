from tkinter import E
from blspy import (PrivateKey, Util, AugSchemeMPL, PopSchemeMPL,
                   G1Element, G2Element)
import socket 
import time

class Node:
    def __init__(self, seed, isLeader, connections, port, message):
        self.sk = AugSchemeMPL.key_gen(seed)
        self.pk = self.sk.get_g1()
        self.message = message
        self.isLeader = isLeader
        self.connections = connections
        self.port = port

    def signMessage(self):
        return PopSchemeMPL.sign(self.sk1, self.message)

    def getProof(self):
        return PopSchemeMPL.pop_prove(self.sk1)

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

    def leaderListen(self):
        # put the socket into listening mode
        host = socket.gethostname()  # as both code is running on same pc
        port = 5074  # socket server port number

        client_socket = socket.socket()  # instantiate
        client_socket.connect((host, port))  # connect to the server

        message = input(" -> ")  # take input

        while message.lower().strip() != 'bye':
            client_socket.send(message.encode())  # send message
            data = client_socket.recv(1024).decode()  # receive response

            print('Received from server: ' + data)  # show in terminal

            message = input(" -> ")  # again take input

        client_socket.close()  # close the connection

    def memberListen(self):
        # put the socket into listening mode
            # get the hostname
        host = socket.gethostname()
        port = 5074  # initiate port no above 1024

        server_socket = socket.socket()  # get instance
        # look closely. The bind() function takes tuple as argument
        server_socket.bind((host, port))  # bind host address and port together

        # configure how many client the server can listen simultaneously
        server_socket.listen(2)
        conn, address = server_socket.accept()  # accept new connection
        print("Connection from: " + str(address))
        while True:
            # receive data stream. it won't accept data packet greater than 1024 bytes
            data = conn.recv(1024).decode()
            if not data:
                # if data is not received break
                break
            print("from connected user: " + str(data))
            data = input(' -> ')
            conn.send(data.encode())  # send data to the client

        conn.close()  # close the connection