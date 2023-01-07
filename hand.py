from card import Card

class Hand:
    def __init__(self, card1: Card, card2?: Card):
        self.card1 = card1
        self.card2 = card2
        self.isPair = (card1.val == card2.val)