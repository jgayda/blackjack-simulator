class Dealer:
    def __init__(self, standValue, DASoffered, RSAoffered, LSoffered, penetration):
        self.standValue = standValue
        self.DASoffered = DASoffered
        self.RSAoffered = RSAoffered
        self.LSoffered = LSoffered
        self.penetration = penetration
    
    def updateHand(self, upcard, hiddencard):
        self.hand = [upcard, hiddencard]