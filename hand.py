from card import Card
from typing import List

class HandIterator:
    def __init__(self, cards: List[Card]):
        self.index = 0
        self.cards = cards
    
    def __iter__(self):
        return self

    def __next__(self):
        self.index += 1
        try:
            return self.cards[self.index]
        except IndexError:
            self.index = 0
            raise StopIteration
class Hand:
    def __init__(self, cards: List[Card], betSize: int):
        self.cards = cards
        self.betSize = betSize
        self.insuranceBet = 0
        self.isInsured = False
        self.finalHandValue = 0
    
    def __iter__(self):
        return HandIterator(self.cards)
    
    def addCard(self, card: Card):
        self.cards.append(card)
    
    def doubleDown(self):
        self.betSize = self.betSize * 2

    def insureHand(self):
        self.insuranceBet = self.betSize / 2
        self.isInsured = True
    
    def isBlackjack(self):
        if len(self.cards) is not 2:
            return False
        card1Value = self.cards[0].getValue()
        card2Value = self.cards[1].getValue()
        if card1Value + card2Value == 21:
            return True
        return False
    
    def isBust(self):
        return self.getHandValue() > 21

    def isPair(self):
        if len(self.cards) is not 2: 
            return False
        card1Rank = self.cards[0].getRank()
        card2Rank = self.cards[1].getRank()
        return card1Rank == card2Rank
    
    def isSoftTotal(self, softTotalDeductionCount):
        if len(self.cards) == 1:
            return False
        numAces = self.getAcesCount()
        if (softTotalDeductionCount == numAces):
            return False
        # for card in self.cards:
        #     if card.getValue() == 11:
        #         return True
        return numAces != 0
    
    def getAcesCount(self):
        numAces = 0
        for card in self.cards:
            if card.getValue() == 11:
                numAces += 1
        return numAces
    
    def getInitialBet(self):
        return self.betSize

    def getSoftTotalAcelessValue(self, softAcesCount):
        total = 0
        for card in self.cards:
            if card.getValue() is not 11:
                total += card.getValue()
        return total + softAcesCount
    
    def printHand(self, playerName):
        print("Player: ", playerName, " has hand:")
        for card in self.cards:
            card.printCard()
    
    def getCards(self):
        return self.cards
    
    def getHandValue(self):
        sum = 0
        for card in self.cards:
            sum += card.getValue()
        return sum
    
    def setFinalHandValue(self, value):
        print("Hand has final value of:", value)
        self.finalHandValue = value

    def splitHand(self):
        return self.cards.pop()