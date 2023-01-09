from shoe import Shoe
from card import Card
from hand import Hand
from typing import List
class Dealer:
    def __init__(self, standValue, DASoffered, RSAoffered, LSoffered, penetration, shoeSize):
        self.standValue = standValue
        self.DASoffered = DASoffered
        self.RSAoffered = RSAoffered
        self.LSoffered = LSoffered
        self.penetration = penetration
        self.shoe = Shoe(shoeSize)
        self.hand: Hand = None
    
    def updateHand(self, hand: Hand):
        self.hand = hand
    
    # def clearHand(self):
    #     self.discardCards(self.hand)
    #     self.hand = None
    
    def dealCard(self):
        return self.shoe.drawCard()

    def discardCards(self, hand: Hand):
        print(hand.cards)
        for card in hand.cards:
            print("discarding card...")
            card.printCard()
            self.shoe.discardCard(card)
    
    def deckPenetrationTooHigh(self):
        return self.shoe.getPenetration() >= self.penetration
    
    def ensureDeckCompleteness(self, isVerbose):
        if isVerbose:
            print("Length of discard and draw piles: ", len(self.shoe.discard), " + ", len(self.shoe.drawPile), " = ", len(self.shoe.discard)+len(self.shoe.drawPile))
            print("Should be equal to: ", self.shoe.numDecks * 52)
        return (len(self.shoe.discard) + len(self.shoe.drawPile) == self.shoe.numDecks * 52)
    
    def shuffle(self):
        self.shoe.resetShoe()

    # def discardCards(self, cards: List[Card]):
    #     print("Discarding: ", type(cards))
    #     for card in cards:
    #         self.shoe.discardCard(card)