from card import Card, Suit
import random
class Shoe:
    def __init__(self, numDecks):
        assert numDecks >= 1
        self.numDecks = numDecks
        self.discard = []
        self.drawPile = []
        for deck in range(0, numDecks):
            for suit in Suit.Clubs, Suit.Diamonds, Suit.Hearts, Suit.Spades:
                for rank in range (1, 14):
                    self.drawPile.append(Card(rank, suit))
    
    def discardCard(self, card):
        self.discard.append(card)

    def drawCard(self):
        return self.drawPile.pop(0)
    
    def getDecksRemaining(self):
        decksDiscarded = len(self.discard) % 52
        return self.numDecks - decksDiscarded
    
    def getPenetration(self):
        print("Discard pile: ", len(self.discard))
        print("Draw Pile: ", len(self.drawPile))
        print("Deck penetration: ", len(self.discard) / (self.numDecks * 52))
        return len(self.discard) / (self.numDecks * 52)

    def printDeck(self):
        for card in self.drawPile:
            card.printCard()
    
    def resetShoe(self):
        print("Resetting shoe...")
        for card in self.discard:
            self.drawPile.append(card)
        self.discard = []
        random.shuffle(self.drawPile)
