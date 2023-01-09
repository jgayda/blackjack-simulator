from hand import Hand
from typing import List
class Player:
    def __init__(self, name, initialBankroll, strategy):
        print("Creating new player: ", name)
        self.name = name
        self.bankroll = initialBankroll
        self.bankrollSnapshots = [initialBankroll]
        self.strategy = strategy
        self.hands: List[Hand] = []
    
    def updateBankroll(self, amount):
        self.bankroll = self.bankroll + amount
        self.bankrollSnapshots.append(self.bankroll)
    
    def updateHand(self, hand):
        self.hands.append(hand)
    
    def getHand(self):
        return self.hands[0]
    
    def canPlay(self):
        return len(self.hands) > 0

    def clearHand(self):
        self.hands.clear()
    
    def splitPair(self, tableMin, trueCount):
        self.updateHand(Hand([self.hands[0].splitHand()], self.calculateBetSize(tableMin, trueCount)))
        print(self.hands)
    
    def calculateBetSize(self, tableMin, trueCount):
        if self.strategy.isCounting:
            return tableMin * 2
        return tableMin
