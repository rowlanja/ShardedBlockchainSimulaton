from committee import Committee
import json
import time
from analyse import Analyse
dataset = {}

def runPBFT(protocol, committeeSize):
    start = time.process_time()
    committee = Committee(protocol, committeeSize)
    committee.main()
    difference = time.process_time()-start
    print(protocol, ' time Took : ', difference)
    return difference


def saveResult(protocol, committeeSize, timeTaken):
    title = protocol+str(committeeSize) 
    dataset[title] = {
        "protocol":protocol,
        "committeeSize":str(committeeSize),
        "timeTaken":str(timeTaken)
    }

def writeResult(dict):
    with open('data.json','w') as file:
        json.dump(dict, file)


def simulation():        
    maxCommitteeSize = 15
    minCommitteeSize = 3
    sizes = range(maxCommitteeSize)[minCommitteeSize:]
    for size in sizes:
        basicTimeTaken = runPBFT('basic',size)
        popTimeTaken = runPBFT('pop', size)
        saveResult('pop', size, popTimeTaken)
        saveResult('basic', size, basicTimeTaken)
        break
    writeResult(dataset)



simulation()
analysis = Analyse()
analysis.displayDatabase()