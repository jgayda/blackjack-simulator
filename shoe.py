from card import Card, Suit

class Shoe:

    def __init__(self, numDecks):
        assert numDecks >= 1
        self.discard = []
        self.drawPile = []
        for deck in range(0, numDecks):
            for suit in Suit.Clubs, Suit.Diamonds, Suit.Hearts, Suit.Spades:
                for rank in range (1, 14):
                    self.drawPile.append(Card(rank, suit))

    def printDeck(self):
        for card in self.drawPile:
            card.printCard()
