import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import random
import numpy as np
import copy
from collections import defaultdict

'''get two arrays and return the winner name'''
def getWinner (winnerVotes,typeOfVotes):
    winners2 =""
    maxVotes =0
    for i in range (len(winnerVotes)):
        if(maxVotes<winnerVotes[i]):
            maxVotes = winnerVotes[i]
    for i2 in range (len(winnerVotes)):
        if( winnerVotes[i2] == maxVotes):
            winners2=winners2 + typeOfVotes[i2]
    return  winners2

'''get a friend and remove him from set'''
def getValue(a):
    for b in a:
        x=b
        a.remove(b)
        return x

def probMatrix(numberOfCom,probs,MinFriendsIn,MaxFriendsIn):
    for a in range (numberOfCom):
        for b in range(numberOfCom):
            if ( probs[a][b] == 0):
                if(a == b):
                    probs[a][b]= round(random.uniform(MinFriendsIn,MaxFriendsIn),2)
                else:
                    probs[a][b] = round(random.uniform(MinFriendsOut, MaxFriendsOut),2)
                    probs[b][a] = probs[a][b]

def creatOpinions(BlockGraph, typeOfVotes, Opinions2, winnerVotes):
    for x in range(len(BlockGraph)):
        Opinions2[x] = random.choice(typeOfVotes)
        Countvotes(typeOfVotes, winnerVotes, Opinions2,x)
    Opinions = copy.deepcopy(Opinions2)
    return Opinions

def Countvotes(typeOfVotes, winnerVotes, Opinions2,x):
    for i3 in range(len(typeOfVotes)):
        if (Opinions2[x] == typeOfVotes[i3]):
            winnerVotes[i3] = (winnerVotes[i3] + 1)

def setFridends(edges, friends):
    '''pair=(1,2),friend[1]={2}'''
    for d in range(len(edges)):
        pair = list(edges.keys())[d]
        friends[pair[0]].add(pair[1])
        friends[pair[1]].add(pair[0])
    for e in range(len(friends)):
        friends[e].remove(-1)

def runInit(friends, votes, votes2,numOfIteration,change):
    friends2 = copy.deepcopy(friends)
    CleanDouble(votes)
    CleanDouble(votes2)
    print("iteration number:", numOfIteration)
    numOfIteration = numOfIteration + 1
    change = False
    return friends2

def countMyOpinion(typeOfVotes, Opinions, votes, counter,f):

    for h1 in range(len(typeOfVotes)):
        print(h1, f)
        if (Opinions[f] == typeOfVotes[h1]):
            votes[f][h1] = (votes[f][h1] + 2)
            counter = counter + 2

def countFriendsOpinion(typeOfVotes, Opinions, votes, counter,f):
    set = friends2[f]
    for g in range(len(set)):
        friendOpi = Opinions[getValue(set)]
        for h in range(len(typeOfVotes)):
            if (friendOpi == typeOfVotes[h]):
                votes[f][h] = (votes[f][h] + 1)
                counter = counter + 1

def percentOfVotes(counter,typeOfVotes,votes2,threshold,Opinions,f,change):
    if (counter>0):
        for h2 in range(len(typeOfVotes)):
            allVote=votes[f][h2]
            votes2[f][h2]=round(allVote/counter,2)
            changeOpinion(votes2, threshold, typeOfVotes, Opinions, f, h2, change)

def changeOpinion(votes2,threshold,typeOfVotes,Opinions,f,h2,change):
    if (votes2[f][h2]>= threshold and typeOfVotes[h2]!=Opinions[f] ):
       change = True
       print("new opinion:", typeOfVotes[h2],"   old opinion:", Opinions[f], "  friend:",f, "   precent:",votes2[f][h2] )
       Opinions[f]= typeOfVotes[h2]

def CleanDouble(array):
    for i in range (len(array)):
        for j in range(len(array[0])):
            array[i][j]=0

def Clean(array):
    for i in range (len(array)):
        array[i] = 0

MinFriendsIn = 0.4
MaxFriendsIn = 0.6
MinFriendsOut = 0.01
MaxFriendsOut = 0.1
threshold = 0.6
typeOfVotes=["A","B", "C"]
winnerStart=''
winnerFinal=''
xLengthGraph=3
Xlegend = "Number of friends"
TotalIter = [0 for a3 in range (xLengthGraph)]
changeVar = [0 for a4 in range (xLengthGraph)]
numberOfCom = 10
WinnerGraph = [ "" for j in range(xLengthGraph)]
Opinions2={}
winnerVotes = [0 for i2 in range(len(typeOfVotes))]

'''checking on different size of communities'''
for a1 in range (xLengthGraph):
    change = True
    numOfIteration=0
    MinPeople = (a1*10)
    MaxPeople = (a1*10)+10
    print("The Round : " , a1 , "the" , Xlegend , " min  : " , MinPeople,  " max  : " , MaxPeople )
    sizes = [ 0 for i in range(numberOfCom) ]
    probs = [[0 for i in range(numberOfCom)] for j in range(numberOfCom)]

    '''creats random communities '''
    for i in range(numberOfCom):
        sizes[i] = random.randint(MinPeople, MaxPeople)
    changeVar[a1] = sum(sizes)

    probMatrix(numberOfCom,probs,MinFriendsIn,MaxFriendsIn)

    print("size of Coum :")
    print(sizes)

    print("probs :")
    print(np.matrix(probs))

    BlockGraph = nx.stochastic_block_model(sizes, probs, seed=364)
    edges = nx.edges(BlockGraph)
    friends = [{-1} for j in range(len(BlockGraph))]
    Opinions=creatOpinions(BlockGraph, typeOfVotes, Opinions2, winnerVotes)
    votes = [[0 for i in range(len(typeOfVotes))] for j in range(len(friends))]
    votes2 = [[0 for i in range(len(typeOfVotes))] for j in range(len(friends))]
    winnerStart=getWinner (winnerVotes,typeOfVotes)

    print("Start votes")
    print(np.matrix(typeOfVotes))
    print(np.matrix(winnerVotes))
    print("Start winner is:",winnerStart)
    print(" opinions:")
    print (Opinions2 )
    print("edges :")
    print(edges)

    setFridends(edges, friends)

    print("friends :")
    print(friends)

    while(change ):

        friends2=runInit(friends,votes, votes2,numOfIteration,change)
        print("change",change)
        for f in range(len(friends)):
            counter=0
            if(len(friends2[f])==0 and (len(friends2))!=f):
                f=f+1
            countMyOpinion(typeOfVotes, Opinions, votes, counter,f)
            countFriendsOpinion(typeOfVotes, Opinions, votes, counter,f)
            percentOfVotes(counter, typeOfVotes, votes2, threshold, Opinions, f, change)


        '''print(np.matrix(votes2))'''
        Clean(winnerVotes)


        winnerVotes= [0 for i7 in range(len(typeOfVotes))]
        for y2 in range(len(BlockGraph)):
            Countvotes(typeOfVotes, winnerVotes, Opinions2, y2)



    print("final votes")
    print(np.matrix(typeOfVotes))
    print(np.matrix(winnerVotes))
    WinnerGraph[a1] = getWinner(winnerVotes,typeOfVotes)
    print("Final winner is:",WinnerGraph[a1])


    '''print(np.matrix(votes))
    print()
    print(np.matrix(votes2))
    print("num of iteration")
    print(numOfIteration)'''
    TotalIter[a1] = numOfIteration

    '''plt.show(nx.draw(BlockGraph , pos = nx.spring_layout(BlockGraph)))'''

print()
print("End  : ")
print(np.matrix(changeVar))
print(np.matrix(TotalIter))

# Threshold plot
dataPlot = plt.plot(changeVar, TotalIter, label='linear')
plt.xlabel(Xlegend)
plt.ylabel("number of iterations")
plt.legend()
plt.show()


# Winner Plot
print(np.matrix(WinnerGraph))

plt.scatter(changeVar,WinnerGraph)
plt.xlabel(Xlegend )
plt.ylabel(" Final Winner is :")
plt.legend()
plt.show()
