from card import Card

class HiLoCount:
    def __init__(self):
        self.runningCount = 0
        self.trueCount = 0
    
    def updateRunningCount(self, card: Card):
        if 2 <= card.getValue() <= 6:
            self.runningCount = self.runningCount + 1
        elif (10 <= card.getValue() <= 13 | card.getValue() == 1):
            self.runningCount = self.runningCount - 1
    
    def resetCount(self):
        self.runningCount = 0
        self.trueCount = 0