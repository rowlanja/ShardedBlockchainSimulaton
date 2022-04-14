# Simulation for sharded blockchain communication using BLS multisignatures

This simulation was written myself, James Rowland as a part of my final year project in Trinity College, University of Dublin. All code is free to use and extend once referenced to myself.

### Run Guide

1. Install python from https://www.python.org/downloads/. To verify python is installed use ``python -V ``
2. Install mandatory dependancies using pip as such: 
	a) ``pip install blspy time json threading secrets thread pickle numpy socket``
	b) there may be other packages I forgot about, install these when errors are shown during program execution
3. Run the python simulation file with ``python simulation.py``. This simulates a full block concensus round using PBFT with multisignatures with each Proof-of-Possession, Distinct Messages, Leader Excldued and Public key cert table. Some Advice : 
	a) Make sure you are in the correct directory
	b) if package errors are shown saying `unknown package X...` install is as such `pip install X`