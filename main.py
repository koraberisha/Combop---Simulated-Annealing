import math
import random
import copy
import time
import sys
import os

def returnPath(fileName):
    print(fileName[len(fileName)-4:len(fileName)])
    if (fileName[len(fileName)-4:len(fileName)] == ".wmg"):
        path = os.path.abspath(os.getcwd())+"/"+fileName
    else:
        path = os.path.abspath(os.getcwd())+"/"+fileName+".wmg"

    return path

def returnAllNeighbors(driverDict,matchups,currentItems = 0):

    currentRanking = random.randint(0,46)
    nextRanking = random.randint(0,46)
    while nextRanking==currentRanking or (abs(nextRanking-currentRanking) == 1 and random.randint(0,10) < 5):
        nextRanking = (currentRanking+random.randint(1,46))%46
    val = currentItems[nextRanking]
    currentItems[nextRanking] = currentItems[currentRanking]
    currentItems[currentRanking] = val

    kemenyScoreNeigh = returnScoresKemeny(currentRanking,nextRanking,currentItems,returnKemenyRanking( currentItems, matchups),matchups)

    return kemenyScoreNeigh,currentItems

def returnKemenyRankingArray(currentRank, neighborhood, tourneyData):
    kemeny_score_value = 0
    for i in range(len(neighborhood) - currentRank):kemeny_score_value += tourneyData[neighborhood[currentRank] - 1][neighborhood[i + currentRank] - 1]
    return kemeny_score_value

def returnKemenyRanking(neighborhood, tourneyData):
    scoreBuffer = []
    for i in range(len(neighborhood)): scoreBuffer.append(returnKemenyRankingArray(i, neighborhood, tourneyData))
    return scoreBuffer

def returnScoresKemeny(currentRank, nextRank, neighborhood, scoreBuffer, tourneyData):
    if currentRank > len(neighborhood) - 1:currentRank = 0
    elif currentRank < 0:currentRank = len(neighborhood) - 1
    if nextRank > len(neighborhood) - 1:nextRank = 0
    elif nextRank < 0:nextRank = 0
    new_scoreBuffer = []
    if currentRank < nextRank:
        for i in range(currentRank, nextRank + 1):  new_scoreBuffer.append(returnKemenyRankingArray(i, neighborhood, tourneyData))
        return scoreBuffer[0:currentRank] + new_scoreBuffer + scoreBuffer[nextRank + 1::]
    else:
        for i in range(nextRank, currentRank + 1):new_scoreBuffer.append(returnKemenyRankingArray(i, neighborhood, tourneyData))
        return scoreBuffer[0:nextRank] + new_scoreBuffer + scoreBuffer[currentRank + 1::]

def simulateAnealing(driverDict,tourneyData,temperature,length,value,ratio):
    count = 0
    count2 = 0

    """Initially the program first inputs the values of the initialisation matrix,e.g. [0,1,3... 45,46],
        the ranking for this is returned and used in the first comparison in order to determine if, the kemeny score has

        values are extracted in the same manner for both the initialisation of the intial kemeny score, and the repeated neighborhood
        score retrieval

        at the while statement, this is the beggining of the outer loop and also the stopping criterion, in this case this is the num of not improved scores.

        The for loop is the beggining of the inner loop, which is also the beggining of the cooling schedule(annealing process analagous)

        The random neighbor and the resultant ranking array and kemeny ranking are returned at the beggining of each itteration

        the cost function is calculated by subtracting the inital orderings ranking score by the newly generated neighbor. If this value is less than 0 then it
        can be said that a new local minimum has been found.

        after this the check is made to see if the currentKemeny value is more than the newly suggested value, if this does not occur then it can be said
        there has been no improvement in kemeny score, this value is related to the stopping criterion.

        in the case that the kemeny score is not higher, the system will use a calculation incroperating the cost, the current temperature(calculated as
        a function f(t) = t*tempRatio). the function E^(-cost/temperature) gives the probability of allowing the current score to be accepted as a minimum even
        if it isnt the current, in order to take uphill climbs.


    """

    tempRanking = [i for i in range(47)]
    currentTotal,ranksRed = returnAllNeighbors(driverDict,tourneyData,tempRanking)
    nextKemeny = currentTotal[:]
    nextKemeny = nextKemeny[:]
    nextKemeny = max(nextKemeny[:])
    currentTotal = nextKemeny
    bestKemeny = 0
    currentDriverRanks = tempRanking
    newDriverRanks = tempRanking
    while count<value:
        for n in range(length):
            potentialKemeny,potentialRanks = returnAllNeighbors(driverDict,tourneyData,newDriverRanks)
            potentialTotal = potentialKemeny[:]
            potentialTotal = (potentialTotal[:])
            potentialTotal = max(potentialTotal)
            deltaCost = potentialTotal-currentTotal
            if deltaCost<=0:
                currentDriverRanks = copy.copy(potentialRanks)

                if (potentialTotal<nextKemeny):

                    newDriverRanks = copy.copy(currentDriverRanks)
                    nextKemeny = copy.copy(potentialTotal)

                else:
                    count+=1
            else:
                probabilityValue = math.pow(math.e,(-deltaCost/temperature))
                if probabilityValue > random.random():
                    currentDriverRanks = copy.copy(potentialRanks)

                    count2 += 1


                count+=1
        temperature = temperature*ratio


    return nextKemeny,newDriverRanks

def returnArrayFromWMG(data):
    readData = open(data, "r")
    totalPlayers = int(readData.readline())
    newArray = ["" for n in range(totalPlayers)]
    for i in range(totalPlayers):
        line = readData.readline()
        if line:

            arrTemp = line.split(",")
            currentIndex = int(arrTemp[0])
            driverName = arrTemp[1]
            newArray[currentIndex-1] = driverName[0:len(driverName)-2]

    initialiser = readData.readline().split(",")
    totalMatchups = int(initialiser[2])
    matchups = [[0 for i in range(47)] for n in range(47)]
    pairings = {}
    for j in range(totalMatchups):
        line = readData.readline()
        if line:

            arrTemp = line.split(",")

            matchups[int(arrTemp[2])-1][int(arrTemp[1])-1] = int(arrTemp[0])

            driverOne,driverTwo = int(arrTemp[2])-1,int(arrTemp[1])-1
            value = int(arrTemp[0])
            tempTup = (driverOne,driverTwo)
            pairings[tempTup] = value;

    return newArray,pairings,matchups

name = (sys.argv)
print(name[1])
data = returnPath(name[1])
drivers,driverDict,matchups = returnArrayFromWMG(data)
newDriverRanks = ["" for n in range(47)]
milliseconds1 = int(time.time() * 1000)
bestRank,ranking = simulateAnealing(driverDict,matchups,1.0,18,1400,0.875)
milliseconds2 = int(time.time() * 1000)
print("")
print("Kemeny score of: " +str(bestRank))
print("")
print("-------------------------")
print("")
print("Time taken in ms: " + str(milliseconds2-milliseconds1) +"ms")
print("")
print("-------------------------")
print("")
m =0
for n in ranking:
    print(str(m) +" - "+ str(drivers[int(n)-1]))
    m+=1
