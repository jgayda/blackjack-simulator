class Suit:
    Clubs = u"\N{BLACK CLUB SUIT}"
    Diamonds = u"\N{WHITE DIAMOND SUIT}"
    Hearts = u"\N{WHITE HEART SUIT}"
    Spades = u"\N{BLACK SPADE SUIT}"

class Card:

    def __init__(self, rank, suit):
        assert suit in (Suit.Clubs, Suit.Diamonds, Suit.Hearts, Suit.Spades)
        assert 1 <= rank < 14
        self.rank = rank
        self.suit = suit
    
    @property
    def getValue(self):
        return self.rank

    @property
    def hardValue(self):
        return self.rank

    @property
    def softValue(self):
        return self.rank
    
    def printCard(self):
        suit_symbols = {Suit.Clubs: '''♣''', Suit.Diamonds: '''♦''', Suit.Hearts: '''♥''', Suit.Spades: '''♠'''}
        face_values = {11: "J", 12: "Q", 13: "K", 1: "A"}
        if face_values.__contains__(self.rank):
            print(str(self.suit), face_values.get(self.rank))
        else:
            print(str(self.suit), self.rank)