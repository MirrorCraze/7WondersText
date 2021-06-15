from mainGameEnv.cardClass import Card
from mainGameEnv.PlayerClass import Player
import random


def filterPlayer(jsonCard, playerNum):
    jsonString = {}
    start = 3
    while start <= playerNum:
        name = str(start) + "players"
        # print(jsonCard[name])
        # print(jsonCard[name].keys())
        for color in jsonCard[name].keys():
            if color == "purple":
                random.shuffle(jsonCard[name][color])
                jsonCard[name][color] = jsonCard[name][color][0:playerNum + 2]
            if color not in jsonString:
                jsonString[color] = []
            jsonString[color] += (jsonCard[name][color])
        start += 1
    return jsonString
def buildCard(name, color, payResource, getResource):
    return Card(name, color, payResource, getResource)
def rotateHand(playerList):
    print(playerList)
    for i in range(1,len(playerList)+1):
        swapHand(playerList[i],playerList[(i)%len(playerList)+1])
def swapHand(player1,player2):
    hand = player1.hand
    player1.assignHand(player2.hand)
    player2.assignHand(hand)
