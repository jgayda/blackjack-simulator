class Player:
    def __init__(self, name, bankroll, strategy):
        print("Creating new player: ", name)
        self.bankroll = 1000
        self.bankrollSnapshots = [1000]
        self.strategy = strategy
    
    def updateBankroll(self, amount):
        self.bankroll = self.bankroll + amount
        self.bankrollSnapshots.append(self.bankroll)
    
    def updateHand(self, card1, card2):
        self.hand = [[card1, card2]]
    
    def computeAction(self, card1, card2):
        val1 = card1.getValue()
        val2 = card2.getValue()

    def clearHand(self):
        self.hand = []
