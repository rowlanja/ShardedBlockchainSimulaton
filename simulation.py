from committee import Committee
import json
import time
from analyse import Analyse
dataset = {}
msgSizes = {}
def runPBFT(protocol, committeeSize):
    start = time.process_time()
    committee = Committee(protocol, committeeSize)
    committee.main()
    difference = time.process_time()-start
    print(protocol, ' time Took : ', difference)
    return difference, committee


def saveResult(protocol, committeeSize, timeTaken, committee):
    title = protocol+str(committeeSize) 
    dataset[title] = {
        "protocol":protocol,
        "committeeSize":str(committeeSize),
        "timeTaken":str(timeTaken)
    }
    msgSizes[title] = {
        "protocol":protocol,
        "committeeSize":str(committeeSize),
        "nodeToLeader" : committee.nodeToLeaderMsgSize, 
        "leaderToNode" : committee.leaderToNodeMsgSize
    }
    
def writeResult(filename, dict):
    with open(filename,'w') as file:
        json.dump(dict, file)

def checkValidRound(committee):
    if committee.validated == False:
        return False

# creates a simulation for hardcoded sizes
def simulationV2():
    sizes = [40,50,60,70]
    for size in sizes:
        validPKI = False
        validBasic = False
        validPop = False
        validLe = False
        # re run any failed consensus round. Round can fail for weird reasons
        while validPKI is False or validBasic is False or validPop is False or validLe is False :
            if validPKI is False : 
                pkiTimeTaken, pkiCommittee = runPBFT('pki',size)
                validPKI = checkValidRound(pkiCommittee)
            if validBasic is False : 
                basicTimeTaken, basicCommittee = runPBFT('basic',size)
                validBasic = checkValidRound(basicCommittee)
            if validPop is False : 
                popTimeTaken, popCommittee = runPBFT('pop', size)
                validPop = checkValidRound(popCommittee)
            if validLe is False : 
                leTimeTaken, leCommittee = runPBFT('le', size)
                validLe = checkValidRound(leCommittee)
        saveResult('pki', size, pkiTimeTaken, pkiCommittee)
        saveResult('pop', size, popTimeTaken, popCommittee)
        saveResult('basic', size, basicTimeTaken, basicCommittee)
        saveResult('le', size, leTimeTaken, leCommittee)
    writeResult("data/timeTaken.json", dataset)
    writeResult("data/msgSizes.json", msgSizes)

# creates a simulation for range of sizes
def simulation():        
    maxCommitteeSize = 30
    minCommitteeSize = 3
    sizes = range(maxCommitteeSize)[minCommitteeSize:]
    for size in sizes:
        validPKI = False
        validBasic = False
        validPop = False
        validLe = False
        # re run any failed consensus round. Round can fail for weird reasons
        while validPKI is False or validBasic is False or validPop is False or validLe is False :
            if validPKI is False : 
                pkiTimeTaken, pkiCommittee = runPBFT('pki',size)
                validPKI = checkValidRound(pkiCommittee)
            if validBasic is False : 
                basicTimeTaken, basicCommittee = runPBFT('basic',size)
                validBasic = checkValidRound(basicCommittee)
            if validPop is False : 
                popTimeTaken, popCommittee = runPBFT('pop', size)
                validPop = checkValidRound(popCommittee)
            if validLe is False : 
                leTimeTaken, leCommittee = runPBFT('le', size)
                validLe = checkValidRound(leCommittee)
        saveResult('pki', size, pkiTimeTaken, pkiCommittee)
        saveResult('pop', size, popTimeTaken, popCommittee)
        saveResult('basic', size, basicTimeTaken, basicCommittee)
        saveResult('le', size, leTimeTaken, leCommittee)
    writeResult("data/timeTaken.json", dataset)
    writeResult("data/msgSizes.json", msgSizes)



simulationV2()
analysis = Analyse()
analysis.displaySpeed()
analysis.displayMsgSize()