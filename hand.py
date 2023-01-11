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
    
    def __iter__(self):
        return HandIterator(self.cards)

    def insureHand(self):
        self.insuranceBet = self.betSize / 2
        self.isInsured = True
    
    def isBlackjack(self):
        if len(self.cards) is not 2:
            return False
        card1Value = self.cards[0].getValue()
        card2Value = self.cards[1].getValue()
        if (card1Value == 1 or card2Value == 1) and (card1Value == 10 or card2Value == 10):
            return True
        return False

    def isPair(self):
        if len(self.cards) is not 2: 
            return False
        card1Rank = self.cards[0].getRank()
        card2Rank = self.cards[1].getRank()
        return card1Rank == card2Rank
    
    def isSoftTotal(self):
        if len(self.cards) == 1:
            return False
        for card in self.cards:
            if card.getValue() == 1:
                return True
        return False
    
    def getInitialBet(self):
        return self.betSize

    def getSoftTotalOtherCard(self):
        for card in self.cards:
            if card.getValue() is not 1:
                return card.getValue()
    
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
    
    def splitHand(self):
        return self.cards.pop()