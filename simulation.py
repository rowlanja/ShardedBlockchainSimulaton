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
    msgSizes[protocol+str(committeeSize)] = {
        "protocol":protocol,
        "committeeSize":str(committeeSize),
        "nodeToLeader" : committee.nodeToLeaderMsgSize, 
        "leaderToNode" : committee.leaderToNodeMsgSize
    }
    
def writeResult(filename, dict):
    with open(filename,'w') as file:
        json.dump(dict, file)


def simulation():        
    maxCommitteeSize = 12
    minCommitteeSize = 3
    sizes = range(maxCommitteeSize)[minCommitteeSize:]
    for size in sizes:
        basicTimeTaken, basicCommittee = runPBFT('basic',size)
        popTimeTaken, popCommittee = runPBFT('pop', size)
        saveResult('pop', size, popTimeTaken, basicCommittee)
        saveResult('basic', size, basicTimeTaken, popCommittee)
    writeResult("data.json", dataset)
    writeResult("msgSizes.json", msgSizes)



simulation()
analysis = Analyse()
analysis.displaySpeed()
analysis.displayMsgSize()