# See https://www.blackjackapprenticeship.com/wp-content/uploads/2018/08/BJA_Basic_Strategy.jpg for charts
class BasicStrategy:
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
        self.pairSplitting.update(6, [True, True,  True,  True,  True,  False, False, False, False, False])
        self.pairSplitting.update(4, [False, False, False, True, True, False, False, False, False, False])
        self.pairSplitting.update(3, [True, True, True,  True,  True,  True,  False, False, False, False])
        self.pairSplitting.update(2, [True, True, True,  True,  True,  True,  False, False, False, False])
    
    def handlePairSplit(self, pairValue: int, dealerUpcard: int):
        assert 1 <= pairValue <= 10
        assert 2 <= dealerUpcard <= 11
        return self.pairSplitting.get(pairValue)[dealerUpcard - 2]

    
    def __init__(self, doubleAfterSplitOffered: boolean):
        self.doubleAfterSplitOffered = doubleAfterSplitOffered
        if doubleAfterSplitOffered:
            self.DASdeviations()