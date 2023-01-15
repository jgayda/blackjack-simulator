from hand import Hand
from typing import List
from bet import spread1_50, spread1_6
class Player:
    def __init__(self, name, initialBankroll, strategy, betting):
        print("Creating new player: ", name)
        self.name = name
        self.bankroll = initialBankroll
        self.bankrollSnapshots = [initialBankroll]
        self.strategy = strategy
        self.betting = betting
        self.hands: List[Hand] = []
    
    def calculateBetSize(self, tableMin, trueCount):
        if self.strategy.isCounting:
            return self.betting.getBetSpreads(trueCount, tableMin)
        return tableMin
    
    def canPlay(self):
        return len(self.hands) > 0
    
    def clearHand(self, hand: Hand):
        self.hands.remove(hand)
        #self.hands.clear()
    
    def getStartingHand(self):
        return self.hands[0]
    
    def splitPair(self, hand: Hand):
        splitHand = Hand([hand.splitHand()], hand.getInitialBet())
        self.updateHand(splitHand)
        print(self.hands)
        return splitHand
    
    def takeBankrollSnapshot(self):
        self.bankrollSnapshots.append(self.bankroll)
    
    def updateBankroll(self, amount):
        self.bankroll = self.bankroll + amount
    
    def updateHand(self, hand):
        self.hands.append(hand)
