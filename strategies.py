from hand import Hand
from enum import Enum
import random
class GameActions(Enum):
    HIT = "H"
    STAND = "S"
    DOUBLE = "D"
class StrategyInterface:
    def __init__(self, doubleAfterSplitOffered, isCounting):
        pass
    
    def shouldSplitPair(self, pairValue: int, dealerUpcard: int) -> bool:
        pass

    def softTotalOptimalDecision(self, hand: Hand, dealerUpcard: int) -> GameActions:
        pass
    
    def willTakeInsurance(self) -> None:
        pass

# RandomStrategy represents the strategy of a player who will leave every single game decision up to chance.
# This goes without saying, do not attempt this strategy in a real life casino.
class RandomStrategy(StrategyInterface):
    def __init__(self, doubleAfterSplitOffered, isCounting):
        self.doubleAfterSplitOffered = doubleAfterSplitOffered
        self.isCounting = isCounting
        self.name = "random"
    
    def shouldSplitPair(self, pairValue: int, dealerUpcard: int) -> bool:
        return bool(random.getrandbits(1))
    
    def softTotalOptimalDecision(self, hand: Hand, dealerUpcard: int) -> GameActions:
        return random.choice([GameActions.HIT, GameActions.STAND, GameActions.DOUBLE])
    
    def willTakeInsurance(self):
        return bool(random.getrandbits(1))

# CasinoStrategy represents the strategy of a player who will play exactly how the casino plays. In other words,
# if the dealer was an actual player at the table this is who they'd be. 
class CasinoStrategy(StrategyInterface):
    def __init__(self, doubleAfterSplitOffered, isCounting):
        self.name = "casino"
        self.doubleAfterSplitOffered = doubleAfterSplitOffered
        self.isCounting = isCounting
    
    def shouldSplitPair(self, pairValue: int, dealerUpcard: int):
        # Casinos never split pairs! 
        return False
    
    def softTotalOptimalDecision(self, hand: Hand, dealerUpcard: int) -> GameActions:
        return super().softTotalOptimalDecision(hand, dealerUpcard)

# See https://www.blackjackapprenticeship.com/wp-content/uploads/2018/08/BJA_Basic_Strategy.jpg for charts
class BasicStrategy(StrategyInterface):
    def __init__(self, doubleAfterSplitOffered, isCounting):
        self.doubleAfterSplitOffered = doubleAfterSplitOffered
        self.isCounting = isCounting
        if doubleAfterSplitOffered:
            self.DASdeviations()
    
    # Contains the optimal pair splitting strategy given the rank of the player's pair and the
    # dealer's upcard according to Basic Strategy principles. 
        #     2      3      4      5      6      7      8      9      10      A
    pairSplitting = {
        1:  [True,  True,  True,  True,  True,  True,  True,  True,  True,  True],
        10: [False, False, False, False, False, False, False, False, False, False],
        9:  [True,  True,  True,  True,  True,  False, True,  True,  False, False],
        8:  [True,  True,  True,  True,  True,  True,  True,  True,  True,  True],
        7:  [True,  True,  True,  True,  True,  True,  False, False, False, False],
        6:  [False, True,  True,  True,  True,  False, False, False, False, False],
        5:  [False, False, False, False, False, False, False, False, False, False],
        4:  [False, False, False, False, False, False, False, False, False, False],
        3:  [False, False, True,  True,  True,  True,  False, False, False, False],
        2:  [False, False, True,  True,  True,  True,  False, False, False, False]
    }

    # Contains the optimal hit/stand/double strategy given that the player has one ace and another card
    # of a certain value and the dealer's upcard according to Basic Strategy principles. 
        #    2     3     4     5     6     7    8    9   10    A
    softTotals = {
        9: ["S",  "S",  "S",  "S",  "S",  "S", "S", "S", "S", "S"],
        8: ["S",  "S",  "S",  "S",  "Ds", "S", "S", "S", "S", "S"],
        7: ["Ds", "Ds", "Ds", "Ds", "Ds", "S", "S", "H", "H", "H"],
        6: ["H",  "D",  "D",  "D",  "D",  "H", "H", "H", "H", "H"],
        5: ["H",  "H",  "D",  "D",  "D",  "H", "H", "H", "H", "H"],
        4: ["H",  "H",  "D",  "D",  "D",  "H", "H", "H", "H", "H"],
        3: ["H",  "H",  "H",  "D",  "D",  "H", "H", "H", "H", "H"],
        2: ["H",  "H",  "H",  "D",  "D",  "H", "H", "H", "H", "H"]
    }

    # Contains the optimal hit/stand/double strategy for the player's cards against the dealer's upcard
    # according to Basic Strategy principles.
        #     2    3    4    5    6    7    8    9   10    A
    hardTotals = {
        17: ["S", "S", "S", "S", "S", "S", "S", "S", "S", "S"],
        16: ["S", "S", "S", "S", "S", "H", "H", "H", "H", "H"],
        15: ["S", "S", "S", "S", "S", "H", "H", "H", "H", "H"],
        14: ["S", "S", "S", "S", "S", "H", "H", "H", "H", "H"],
        13: ["S", "S", "S", "S", "S", "H", "H", "H", "H", "H"],
        12: ["H", "H", "S", "S", "S", "H", "H", "H", "H", "H"],
        11: ["D", "D", "D", "D", "D", "D", "D", "D", "D", "D"],
        10: ["D", "D", "D", "D", "D", "D", "D", "D", "H", "H"],
        9:  ["H", "D", "D", "D", "D", "H", "H", "H", "H", "H"],
        8:  ["H", "H", "H", "H", "H", "H", "H", "H", "H", "H"],
    }
    # Handles pair splitting deviations in the event that double-after-split (DAS) is offered.
    def DASdeviations(self):
        self.pairSplitting.update({6: [True, True,  True,  True,  True,  False, False, False, False, False]})
        self.pairSplitting.update({4: [False, False, False, True, True, False, False, False, False, False]})
        self.pairSplitting.update({3: [True, True, True,  True,  True,  True,  False, False, False, False]})
        self.pairSplitting.update({2: [True, True, True,  True,  True,  True,  False, False, False, False]})

    def shouldSplitPair(self, pairValue: int, dealerUpcard: int):
        return self.pairSplitting.get(pairValue)[dealerUpcard - 2]
    
    def softTotalOptimalDecision(self, hand: Hand, dealerUpcard: int):
        chartVal: GameActions = self.softTotals.get(hand.getSoftTotalOtherCard())[dealerUpcard - 2]
        return chartVal
    
    def willTakeInsurance(self, runningCount):
        # Perfect basic strategy never takes insurance unless running count is exceptionally high
        return runningCount >= 8