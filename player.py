from hand import Hand
from typing import List
from bet import spread1_50, spread1_6
class Player:
    def __init__(self, name, initialBankroll, strategy, betting, isVerbose):
        if isVerbose: print("Creating new player: ", name)
        self.name = name
        self.bankroll = initialBankroll
        self.bankrollSnapshots = [initialBankroll]
        self.strategy = strategy
        self.betting = betting
        self.isVerbose = isVerbose
        self.hands: List[Hand] = []
        self.winData = [0, 0, 0] # [Wins, Losses, Draws]
    
    def calculateBetSize(self, tableMin, trueCount):
        if self.strategy.isCounting:
            return self.betting.getBetSpreads(trueCount, tableMin)
        return tableMin
    
    def canPlay(self):
        return len(self.hands) > 0
    
    def clearHand(self, hand: Hand):
        self.hands.remove(hand)
    
    def clearAllHands(self):
        self.hands.clear()
    
    def getStartingHand(self):
        return self.hands[0]
    
    def splitPair(self, hand: Hand):
        splitHand = Hand([hand.splitHand()], hand.getInitialBet())
        self.updateHand(splitHand)
        return splitHand
    
    def takeBankrollSnapshot(self):
        self.bankrollSnapshots.append(self.bankroll)
    
    def updateBankroll(self, amount):
        self.bankroll = self.bankroll + amount
    
    def updateHand(self, hand):
        self.hands.append(hand)
