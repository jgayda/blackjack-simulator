class Dealer:
    def __init__(self, standValue, DASoffered, RSAoffered, LSoffered):
        self.standValue = standValue
        self.DASoffered = DASoffered
        self.RSAoffered = RSAoffered
        self.LSoffered = LSoffered
    
    def updateHand(self, upcard, hiddencard):
        self.hand = [upcard, hiddencard]