# CERTIFICATE AUTHORITY

from tkinter import E
from blspy import (PrivateKey, Util, AugSchemeMPL, PopSchemeMPL,
                   G1Element, G2Element)
from cert import Cert
from _thread import *
import json
import numpy as np
import secrets

class CA:
    def __init__(self):
        self.sk = AugSchemeMPL.key_gen(secrets.token_bytes(32))
        self.pk = self.sk.get_g1()

    def createCert(self, credentials):
        validity = self.validateCredentials(credentials)
        if validity != True : return       
        signature = self.sign(credentials)
        cert = Cert(credentials['name'],credentials['pk'],signature)
        return cert

    def sign(self, credentials):
        credString = bytes(credentials['name'])+bytes(credentials['pk'])
        signature = PopSchemeMPL.sign(self.sk, credString)
        return signature

    def validateCredentials(self, credentials):
        validName = credentials['name'] != ''
        validPK = credentials['pk'] != ''
        if validName and validPK :
            return True
        return PopSchemeMPL.sign(self.sk, self.message)

 