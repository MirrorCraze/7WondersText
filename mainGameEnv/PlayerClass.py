from mainGameEnv.WonderClass import Wonder
from mainGameEnv.Personality import Personality
from mainGameEnv.resourceClass import Resource
from mainGameEnv import mainHelper
import operator

class ResourceBFS:
    def __init__(self,accuArr,remainArr):
        self.accuArr = accuArr
        self.remainArr = remainArr
class Player:
    def __init__(self, playerNumber,totalPlayer,person):
        self.player = playerNumber
        self.card = []
        self.choosecard = []
        self.coin = 3
        self.warVP = 0
        self.warLoseVP = 0
        self.color = dict.fromkeys(["brown","grey","blue","yellow","red","green","purple"],0)
        self.eastTradePrices = dict.fromkeys(["wood", "clay", "ore", "stone","papyrus","glass","loom"],2)
        self.westTradePrices = self.eastTradePrices.copy()
        self.resource = dict.fromkeys(["wood", "clay", "ore", "stone","papyrus","glass","loom","compass", "wheel", "tablet","shield"],0)
        self.VP = 0
        self.wonders = None
        self.left = (playerNumber-2)%totalPlayer+1
        self.right = playerNumber%totalPlayer+1
        self.hand = []
        self.personality = person
    def assignWonders(self,wonder):
        self.wonders = wonder
        beginRes = wonder.beginResource
        print(beginRes.resource)
        self.resource[beginRes.resource] += beginRes.amount
    def assignLeftRight(self, leftPlayer, rightPlayer):
        self.left = leftPlayer
        self.right = rightPlayer
    def printPlayer(self):
        print(self.__dict__)
        self.wonders.printWonder()
        for card in self.card:
            card.printCard()
    def assignHand(self,hand):
        self.hand = hand
    def cardExist(self,name):
        for singleCard in self.card:
            if singleCard.name == name:
                return True
        return False
    def checkLeftRight(self,amount,type):
        leftPrice = self.westTradePrices[type]
        rightPrice = self.eastTradePrices[type]
        minPrice = 10000000
        side = "M"
        if self.coin >= leftPrice*amount and self.left.resource[type] > 0:
            minPrice = leftPrice*amount
            side = "L"
        if self.coin >=rightPrice*amount and self.right.resource[type] > 0:
            if minPrice > rightPrice*amount:
                minPrice = rightPrice*amount
                side = "R"
        if side == "M":
            return -1,side
        else:
            return minPrice,side


    def addiResComp(self,targetArr,curResArr):
        print("BEFORE")
        for i in targetArr:
            i.printResource()
        for res in curResArr:
            name = res.resource
            print("Name" + name)
            for tar in targetArr:
                if name == tar.resource:
                    tar.amount -= res.amount
        targetArr = [i for i in targetArr if i.amount>0]
        print("AFTER")
        for i in targetArr:
            i.printResource()
        return targetArr
    def BFS(self,targetArray,resourceArray):
        layerBefore = []
        queue = []
        minLeft = 10000000
        minRight = 10000000
        queue.append(ResourceBFS([],resourceArray))
        while queue:
            left = 0
            right = 0
            price = -1
            side = "M"
            print(queue[0])
            qFront = queue[0]
            curRes = qFront.accuArr
            remainRes = qFront.remainArr
            print("REMAINRES")
            print(remainRes)
            remainArr = self.addiResComp(targetArray.copy(), curRes.copy())
            for remain in remainArr:
                price,side = self.checkLeftRight(remain.amount,remain.resource)
                if price == -1:
                    break
                elif side == "L":
                    left += price
                elif side == "R":
                    right += price
            if price != -1 and left + right < minLeft + minRight
                minLeft = left
                minRight = right
            queue.pop(0)
            if remainRes:
                resChooseCard = remainRes[0]
                for res in resChooseCard.getResource['resource']:
                    queue.append(curRes.append(mainHelper.resBuild(res)),remainRes[1:])

        return 0
    def playable(self,card):
        print(card.payResource)
        #print("--------------")
        #print(card.payResource)
        payRes = card.payResource
        if payRes['type'] == 'choose':
            if self.cardExist(payRes['resource'][0]['name']):
                return True
            else:
                payRes = payRes['resource'][1]
                #print("NEW PAYRES-----")
                #print(payRes)
        if payRes['type'] == 'none':
            return True
        elif payRes['type'] == 'coin':
            if self.coin >= payRes['amount']:
                return True
            else:
                return False
        elif payRes['type'] == 'mixed': #left it be
            missResource = {}
            for res in payRes['resource']:
                if self.resource[res['type']] < res['amount']:
                    missResource[res['type']] = res['amount'] - self.resource[res['type']]
            if len(missResource) == 0:
                return True
            missResource = dict(sorted(missResource.items(), key = operator.itemgetter(1), reverse = True))
            print("oldMissResource")
            print(missResource)
            missArr = []
            for name,amount in missResource.items():
                missArr.append(Resource(name,amount))
            amount = self.BFS(missArr,self.choosecard)
            dictAll = {}

    def activateEffect(self,effect):
        return 0
    def deleteCardFromHand(self,card):
        self.hand.remove(card)
    def playCard(self):
        choices = []
        for card in self.hand:
            if self.playable(card):
                choices.append(card)
        #print("CHOICE-----------CHOICE")

        #print(len(choices))
        if len(choices) == 0:
            self.coin +=3
        else:
            #print(choices[0].printCard())
            persona = self.personality
            selectedCard = choices[self.personality.make_choice(persona,options=choices)]
            self.deleteCardFromHand(selectedCard)
            self.card.append(selectedCard)
            self.color[selectedCard.color]+=1
            if selectedCard.getResource["type"] == "choose":
                self.choosecard.append(selectedCard)
            elif selectedCard.getResource["type"] == "VP":
                self.VP +=selectedCard.getResource["amount"]
            elif selectedCard.getResource["type"] == "coin":
                self.coin +=selectedCard.getResource["amount"]
            elif selectedCard.getResource["type"] != "effect":
                self.resource[selectedCard.getResource["type"]]+=selectedCard.getResource["amount"]
            else:
                self.activateEffect(selectedCard.getResource["effect"])









