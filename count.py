from card import Card

class HiLoCount:
    def __init__(self):
        self.runningCount = 0
    
    def updateRunningCount(self, cardValue: int):
        if 2 <= cardValue <= 6:
            self.runningCount = self.runningCount + 1
        elif (cardValue == 10 or cardValue == 11):
            self.runningCount = self.runningCount - 1
    
    def getTrueCount(self, decksRemaining: float) -> int:
        print("count.py -> Decks remaining:", decksRemaining, " | Running Count:", self.runningCount, " | True Count: ", round(self.runningCount / decksRemaining))
        return round(self.runningCount / decksRemaining)
    
    def resetCount(self):
        self.runningCount = 0