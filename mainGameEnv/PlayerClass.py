from mainGameEnv.WonderClass import Wonder
from mainGameEnv.Personality import Personality
from mainGameEnv.resourceClass import Resource
import operator
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
        self.left = (playerNumber-2)%totalPlayer+1
        self.right = playerNumber%totalPlayer+1
        self.wonders = None
        self.hand = []
        self.personality = person
    def assignWonders(self,wonder):
        self.wonders = wonder
        beginRes = wonder.beginResource
        print(beginRes.resource)
        self.resource[beginRes.resource] += beginRes.amount
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
    def checkLeftRight(self,amount,type,left,right):
        leftPrice = self.westTradePrices[type]
        rightPrice = self.eastTradePrices[type]
        if self.coin >= leftPrice*amount and left.resource[type] > 0:
            return True
        elif self.coin >=rightPrice*amount and right.resource[type] > 0:
            return True
        else:
            return False

    def playable(self,card,left,right):
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
            dictAll = {}
            for card in self.choosecard:
                mixRes = card.getResource['resource']
                for res in mixRes:
                    if res['type'] not in dictAll:
                        dictAll[res['type']] = 1
                    else:
                        dictAll[res['type']]+=1
            print("dictAll")
            print(dictAll)
            missResource = {key : missResource[key] - dictAll.get(key,0) for key in missResource if missResource[key] - dictAll.get(key,0) > 0}
            print("missResource---------------")
            print(missResource)
            if len(missResource.keys()) == 0:
                return True
            else:
                return False
        else:
            if self.resource[payRes['type']] >= payRes['amount']:
                return True
            else:
                extendAmount = payRes['amount'] - self.resource[payRes['type']]
                return self.checkLeftRight(extendAmount,payRes['type'],left,right)
    def activateEffect(self,effect):
        return 0
    def deleteCardFromHand(self,card):
        self.hand.remove(card)
    def playCard(self,left,right):
        choices = []
        for card in self.hand:
            if self.playable(card,left,right):
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







