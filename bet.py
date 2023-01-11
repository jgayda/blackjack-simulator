class BetSpreadInterface:
    def getBetSpreads(trueCount: int, tableMin: int) -> int:
        pass
class spread1_6(BetSpreadInterface):
    def __init__(self):
        print("Initializing 1-6 Bet Spread")
    
    # 1-6 Bet Spread
    def getBetSpreads(trueCount, tableMin):
        if trueCount < 0: return 100
        if trueCount > 5: return 600
        betSpread = {
            0: 100,
            1: 200,
            2: 300,
            3: 400,
            4: 500,
            5: 600
        }

        return betSpread.get(trueCount)

class spread1_50(BetSpreadInterface):
    def __init__(self):
        print("Initializing 1-50 Bet Spread")
    
    def getBetSpreads(trueCount: int, tableMin: int):
        if trueCount <= 0: return tableMin
        if trueCount >= 5: return 500
        betSpread = {
            1: 100,
            2: 200,
            3: 300,
            4: 400,
        }
        return betSpread.get(trueCount)