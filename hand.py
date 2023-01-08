from card import Card
class Hand:
    def __init__(self, card1: Card = None, card2: Card = None, betSize: int = None):
        if card1 is not None:
            self.card1 = card1
        if card2 is not None:
            self.card2 = card2
        if betSize is not None:
            self.betSize = betSize

    def isPair(self):
        card1Value = self.card1.getValue()
        card2Value = self.card2.getValue()
        print("1: ", card1Value, " 2: ", card2Value)
        return card1Value == card2Value
    
    def printHand(self):
        print("Player has hand:")
        self.card1.printCard()
        self.card2.printCard()