import json
import random
from mainGameEnv.mainHelper import filterPlayer, buildCard,rotateHand
from mainGameEnv.PlayerClass import Player
from mainGameEnv.WonderClass import Wonder
from mainGameEnv.resourceClass import Resource
from mainGameEnv.Personality import Personality, StupidAI


def init(player):
    fileOper = open('../Card/card_list.json', 'rt')
    cardList = json.load(fileOper)
    cardAge = []
    for i in range(1, 4):
        cardAge.append(getCardAge("age_" + str(i), player, cardList))
    fileOper = open('../Card/wonders_list.json', 'rt')
    wonderList = json.load(fileOper)
    wonderList = wonderList["wonders"]
    wonderName= list(wonderList.keys())
    wonderSelected = wonderName[0:player]
    print(wonderSelected)
    print(wonderList['Rhodes'])
    playerList = {}
    for i in range(1,player+1):
        newPlayer = Player(i,player,StupidAI)
        side = "A" if random.randrange(2)%2 == 0 else "B"
        wonderCurName = wonderSelected[i-1]
        wonderCur = wonderList[wonderCurName]
        initialResource = Resource(wonderCur["initial"]["type"],wonderCur["initial"]["amount"])
        print(type(wonderList[wonderCurName][side]))
        newWonders = Wonder(wonderCurName, side, wonderCur["initial"]["type"],wonderCur["initial"]["amount"], **wonderList[wonderCurName][side])
        newPlayer.assignWonders(newWonders)
        playerList[i]=(newPlayer)
    return cardAge, playerList

def getCardAge(age, player, cardList):
    jsonAge = filterPlayer(cardList[age], player)
    cardAge = []
    for color in jsonAge:
        for card in jsonAge[color]:
            card = buildCard(card['name'], color, card['payResource'], card['getResource'])
            cardAge.append(card)
    return cardAge

if __name__ == "__main__":
    logger = open("loggers.txt","w+")
    player = input("How many players?")
    player = int(player)
    cardAge, playerList = init(player)
    for player in playerList.keys():
        playerList[player].printPlayer()
    for age in range(1,4):
        cardThisAge = cardAge[age-1]
        print(len(cardThisAge))
        random.shuffle(cardThisAge)
        cardShuffled = [cardThisAge[i:i + 7] for i in range(0, len(cardThisAge), 7)]
        for i in range(len(cardShuffled)):
            playerList[i+1].assignHand(cardShuffled[i])
        for i in range(0,6):
            for j in range(len(playerList)):
                playerList[j+1].playCard(playerList[playerList[j+1].left],playerList[playerList[j+1].right])
            rotateHand(playerList)
        print("AGE" + str(age))
        for j in range(len(playerList)):
            playerList[j+1].printPlayer()





