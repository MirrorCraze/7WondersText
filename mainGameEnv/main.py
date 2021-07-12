import json
import random
from operator import itemgetter

from mainGameEnv.mainHelper import filterPlayer, buildCard,rotateHand, battle
from mainGameEnv.PlayerClass import Player
from mainGameEnv.WonderClass import Wonder
from mainGameEnv.resourceClass import Resource
from mainGameEnv.Personality import Personality, StupidAI,Human
from mainGameEnv.stageClass import Stage
import sys
def init(player,human):
    fileOper = open('../Card/card_list.json', 'rt')
    cardList = json.load(fileOper)

    cardAge = []
    for i in range(1, 4):
        cardAge.append(getCardAge("age_" + str(i), player, cardList))
    fileOper = open('../Card/wonders_list.json', 'rt')
    wonderList = json.load(fileOper)
    wonderList = wonderList["wonders"]
    wonderName= list(wonderList.keys())
    random.shuffle(wonderName)
    wonderSelected = wonderName[0:player]
    #print(wonderSelected)
    #print(wonderList['Rhodes'])
    playerList = {}
    for i in range(1,player+1):
        newPlayer = None
        if i <=human:
            newPlayer = Player(i,player,Human)
        else:
            newPlayer = Player(i,player,StupidAI)
        side = "A" if random.randrange(2)%2 == 0 else "B"
        wonderCurName = wonderSelected[i-1]
        wonderCur = wonderList[wonderCurName]
        print(len(wonderCur[side]))
        initialResource = Resource(wonderCur["initial"]["type"],wonderCur["initial"]["amount"])
        #print(type(wonderList[wonderCurName][side]))
        newWonders = Wonder(wonderCurName, side, wonderCur["initial"]["type"],wonderCur["initial"]["amount"], **wonderList[wonderCurName][side])
        newPlayer.assignWonders(newWonders)
        playerList[i]=newPlayer
    for i in range(1,player+1):
        curPlayer = playerList[i]
        playerList[i].assignLeftRight(playerList[curPlayer.left],playerList[curPlayer.right])
    print("SETUP COMPLETE")
    return cardAge, playerList
def initActionSpace():
    counter = 0
    dictCard = {}
    fileOper = open('../Card/card_list.json', 'rt')
    cardList = json.load(fileOper)
    for age in cardList:
        print("AGE")
        for playerNum in cardList[age]:
            for color in cardList[age][playerNum]:
                for card in cardList[age][playerNum][color]:
                    if not card['name'] in dictCard.values():
                        dictCard[counter] = card['name']
                        counter +=1
    counter = 0
    dictPlay = {}
    fileOper.close()
    fileOper = open
    fileOper = open('../Card/wonders_list.json', 'rt')
    wonderList = json.load(fileOper)
    wonderList = wonderList["wonders"]
    wonderName = list(wonderList.keys())
    #[playStatus,wonder,side,stage] for each card.
    dictPlay[0] = [0,None,None,None] #playStatus 0 = play with paying cost
    dictPlay[1] = [1,None,None,None] #playStatus 1 = play with effect (= no cost)
    dictPlay[2] = [-1,None,None,None] #playStatus -1 = discard the card for 3 coins
    counter = 3
    sides = ["A","B"]
    for wonder in wonderName:
        for side in sides:
            for i in range(len(wonderList[wonder][side])):
                dictPlay[counter] = [2,wonder,side,i+1] #playStatus 2 = use card for wonder with side at stage i+1
                counter+=1
    print("dictCard")
    for keys,values in dictCard.items():
        print(keys,values)
    print("dictAction")
    for keys,values in dictPlay.items():
        print(keys,values)
def getCardAge(age, player, cardList):
    jsonAge = filterPlayer(cardList[age], player)
    cardAge = []
    for color in jsonAge:
        for card in jsonAge[color]:
            card = buildCard(card['name'], color, card['payResource'], card['getResource'])
            cardAge.append(card)
    return cardAge

if __name__ == "__main__":

    discarded = []
    logger = open("loggers.txt","w+")
    player = input("How many players?")
    player = int(player)
    human = int(input("How many human players?"))
    #path = '../gameLog.txt'
    #sys.stdout = open(path, 'w')
    initActionSpace()
    cardAge, playerList = init(player,human)
    for player in playerList.keys():
        print("Player {} with wonders {}".format(player,playerList[player].wonders.name))
    for age in range(1,4):
        cardThisAge = cardAge[age-1]
        random.shuffle(cardThisAge)
        cardShuffled = [cardThisAge[i:i + 7] for i in range(0, len(cardThisAge), 7)]
        for i in range(len(cardShuffled)):
            if any("freeStructure" in effect for effect in playerList[i+1].endAgeEffect):
                playerList[i+1].freeStructure = True
            playerList[i+1].assignHand(cardShuffled[i])
        for i in range(0,6):
            for j in range(len(playerList)):
                #print("j" + str(j))
                card,action = playerList[j+1].playCard(age)
                if action == -1:#card discarded
                    discarded.append(card)
                    print("PLAYER {} discard {}".format(j + 1, card.name))
                elif isinstance(card,Stage):
                    print("PLAYER {} play step {}".format(j + 1, card.stage))
                else:
                    print("PLAYER {} play {}".format(j+1,card.name))
            rotateHand(playerList,age)
            for j in range(len(playerList)):
                print("PLAYER {} resource".format(j+1), end = " ")
                for res in playerList[j+1].resource:
                    print(res,playerList[j+1].resource[res],end=" ")
                print()
            print("DISCARDED")
            print(discarded)
            for j in range(len(playerList)):
                player = playerList[j+1]
                if player.endTurnEffect == "buildDiscarded":
                    if not discarded:
                        continue
                    print("DISCARDED")
                    print(discarded)
                    card,action = player.playFromEffect(discarded,player.endTurnEffect,age)
                    discarded = [disCard for disCard in discarded if disCard.name!=card.name]
            endScore = []
            for i in range(len(playerList)):
                endScore.append((i + 1, playerList[i + 1].endGameCal()))
            endScore = sorted(endScore, key=itemgetter(1), reverse=True)
            print("SCOREBOARD")
            for i in endScore:
                print("Player {} with score {}".format(i[0], i[1]))
        print("REMAINING HANDS")
        for j in range(len(playerList)):
            discarded.append(playerList[j + 1].hand[0])
            print(playerList[j + 1].hand)
        print("AGE" + str(age))
        for j in range(len(playerList)):
            playerList[j+1].printPlayer()
        # military conflict
        for j in range(1, 1 + len(playerList)):
            battle(playerList[j], playerList[j % len(playerList) + 1], age)
    #end game period
    endScore = []
    for i in range(len(playerList)):
        endScore.append((i+1,playerList[i+1].endGameCal()))
    endScore = sorted(endScore,key = itemgetter(1),reverse=True)
    print("SCOREBOARD")
    for i in endScore:
        print("Player {} with score {}".format(i[0],i[1]))




