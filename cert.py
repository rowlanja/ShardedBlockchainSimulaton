# CERTIFICATE AUTHORITY

from tkinter import E
from blspy import (PrivateKey, Util, AugSchemeMPL, PopSchemeMPL,
                   G1Element, G2Element)
from _thread import *
import json
import numpy as np

class Cert:
    def __init__(self, name, pk, signature):
        self.name = name
        self.pk = pk
        self.signature = signature



 