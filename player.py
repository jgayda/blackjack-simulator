from hand import Hand
class Player:
    def __init__(self, name, bankroll, strategy):
        print("Creating new player: ", name)
        self.name = name
        self.bankroll = 1000
        self.bankrollSnapshots = [1000]
        self.strategy = strategy
        self.hands = []
    
    def updateBankroll(self, amount):
        self.bankroll = self.bankroll + amount
        self.bankrollSnapshots.append(self.bankroll)
    
    def updateHand(self, hand):
        self.hands.append(hand)
    
    def getHand(self):
        return self.hands[0]
    
    def canPlay(self):
        return len(self.hands) > 0

    def clearHand(self):
        self.hands.clear()
    
    def splitPair(self):
        print(self.hands)
        currentHand = self.hands.pop()
        hand1 = Hand(currentHand.card1)
        hand2 = Hand(currentHand.card2)
        self.updateHand(hand1)
        self.updateHand(hand2)
    
    def calculateBetSize(self):
        return 5
