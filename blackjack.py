import click
from shoe import Shoe
from player import Player
from count import HiLoCount
from hand import Hand
from card import Card, CardValue
from dealer import Dealer, HouseRules
from strategies import BasicStrategy, GameActions
from typing import List
from collections import deque

@click.command()
@click.option('-s', '--shoesize', default=6, help='An integer representing the amount of decks to use in the shoe. Default is 6 decks.')
@click.option('-b', '--bankroll', default=1000, help='Determines the amount of dollars that each player begins the game with in their bankroll. Default is $1000.')
@click.option('-h', '--hands', default=1000, help='Determines the number of hands to deal. Default is 1000.')
@click.option('-t', '--tablemin', default=5, help='Determines the minimum table bet. Default is 5.')
@click.option('-p', '--penetration', default=0.84, help='Dictates the deck penetration by the dealer. Default is 0.84 which means that the dealer will penetrate 84 percent of the shoe before re-shuffling')
@click.option('-d', '--dealersettings', default=[17, True, True, True, True], help='Assigns the dealer rules.')
def main(shoesize, bankroll, hands, tablemin, penetration, dealersettings):
    print("Running blackjack simulation with variables:")
    print("Shoe size: ", shoesize, " | Bankroll: ", bankroll, " | Number of hands to simulate: ", hands, " | Minimum Table Bet: ", tablemin)
    houseRules = HouseRules(standValue=dealersettings[0], DASoffered=dealersettings[1], RSAoffered=dealersettings[2], LSoffered=dealersettings[3], doubleOnSoftTotal=dealersettings[4])
    game = BlackJackGame(shoesize, bankroll, hands, tablemin, penetration, houseRules)
    game.startGame()

class BlackJackGame:
    def __init__(self, shoeSize, bankroll, hands, tableMin, penetration, houseRules):
        print("Initializing game...")
        self.shoeSize = shoeSize
        self.hands = hands
        self.tableMin = tableMin

        print("Dealer has rules: ")
        print("Deck Penetration %: ", penetration, " | Minimum table bet: $", tableMin)
        self.dealer = Dealer(penetration, shoeSize, houseRules)

        self.players = [Player("Optimal", bankroll, BasicStrategy(self.dealer.houseRules, isCounting=True)), 
                        Player("Sub-Optimal I", bankroll, BasicStrategy(self.dealer.houseRules, isCounting=False)),
                        Player("Random", bankroll, BasicStrategy(self.dealer.houseRules, isCounting=True)),]
        print("There are ", len(self.players), " players in the game.")
    
    def clearAllCards(self, players: List[Player]):
        # Collect the cards from each player before moving onto the next round and put the cards in the
        # discard pile
        for player in players:
            allHands = player.hands
            for hand in allHands:
                self.dealer.discardPlayersCards(hand, player.name)
            player.clearHand()
        
        # Discard the dealer's cards and move them to the discard pile
        self.dealer.discardDealersCards()

    def dealDealersHand(self, count):
        # Deal out the dealers cards
        upcard = self.dealer.dealCard()
        self.dealer.setUpCard(upcard)
        count.updateRunningCount(upcard.getValue())
        # The hidden card is not added to the count yet as only the dealer knows this information
        hiddenCard = self.dealer.dealCard()
        dealerHand = Hand([upcard, hiddenCard], 0)
        self.dealer.updateHand(dealerHand)
        print("Dealer shows:")
        upcard.printCard()
        print("Dealer hides:")
        hiddenCard.printCard()

    def dealPlayersHands(self, players, count):
        print("Dealing hands...")
        for player in players:
            betSize = player.calculateBetSize(self.tableMin, count.trueCount)

            card1: Card = self.dealer.dealCard()
            card2: Card = self.dealer.dealCard()

            count.updateRunningCount(card1.getValue())
            count.updateRunningCount(card2.getValue())

            player.updateBankroll(-1 * betSize)
            player.updateHand(Hand([card1, card2], betSize))
            player.getStartingHand().printHand(player.name)
    
    def doubleDown(self, player: Player, hand: Hand, count: HiLoCount):
        print("Doubling down!")
        player.updateBankroll(-1 * hand.getInitialBet())
        hand.doubleDown()
        self.hit(player, hand, count)
    
    def handleBustHand(self, player: Player, hand: Hand):
        print("Hand went bust.")

    def handleDealerBlackjack(self, players: List[Player], count: HiLoCount):
        # Need to update the count as the dealer reveals the hidden card to show blackjack
        # Guaranteed to have a count value of -1
        count.updateRunningCount(10)

        for player in players:
            for hand in player.hands:
                if hand.isBlackjack():
                    print("Player ", player.name, " pushes with another blackjack.")
                    player.updateBankroll(hand.betSize)
                elif hand.isInsured:
                    print("Player ", player.name, "'s hand is insured!")
                    player.updateBankroll(hand.betSize + hand.insuranceBet)
                else:
                    self.dealer.updateGains(hand.betSize)

    def handlePlayerBlackjack(self, player: Player, hand: Hand):
        payout = self.dealer.handlePayout(hand.betSize, isBlackjack=True)
        print("Blackjack! Initial bet: $", hand.getInitialBet(), " Payout: $", payout)
        player.updateBankroll(hand.betSize + payout)
        self.dealer.discardPlayersCards(hand, player.name)
        player.clearHand()

    def handleInsurance(self, players: List[Player], trueCount):
        print("Dealer shows ace - Insurance offered")
        for player in players:
            for hand in player.hands:
                if player.strategy.willTakeInsurance(trueCount) and not hand.isBlackjack():
                    player.updateBankroll(-1 * hand.betSize / 2)
                    hand.insureHand()
                    print("Player ", player.name, " has insured their hand.")
        print("Insurance closed.")

    def handleSplitPair(self, player: Player, hand: Hand, dealerUpcard: Card, trueCount):
        print("Determining whether or not to split pair based on player's strategy...")
        if player.strategy.shouldSplitPair(hand.getHandValue() / 2, dealerUpcard.getValue()) and player.calculateBetSize(self.tableMin, trueCount) <= player.bankroll:
            print("Splitting pair!")
            splitHand = player.splitPair(hand)
            return splitHand
        print("Player decided not to split pair.")
        return None

    
    def hit(self, player: Player, hand: Hand, count: HiLoCount):
        hitCard = self.dealer.dealCard()
        count.updateRunningCount(hitCard.getValue())
        hand.addCard(hitCard)
        print(player.name, " has new hand: ")
        hand.printHand(player.name)

    def playRound(self, player: Player, dealerUpcard: Card, handNumber, count):
        dealtHand = player.getStartingHand()
        print(player.name, " is playing their hand...")

        # Check if the dealt hand is a blackjack and payout immediately if it is
        if dealtHand.isBlackjack():
            self.handlePlayerBlackjack(player, dealtHand)
        else:
            # First, determine if we have a pair and if we should split:
            if dealtHand.isPair():
                self.handleSplitPair(player, dealtHand, dealerUpcard, count.trueCount)
            
            # It's now possible that we have two hands that we need to simulate as the player could have split the pair.
            # Instatiate a new dealtHands object:
            handQueue = deque()
            for hand in player.hands:
                handQueue.append(hand)

            while len(handQueue) > 0:
                hand = handQueue.pop()
                action: GameActions = None
                softTotalDeductionCount = 0

                while (action != GameActions.STAND.value):
                    if hand.isBust():
                        if softTotalDeductionCount < hand.getAcesCount():
                            print("BUST! Ace now becomes 1. Old hand value: ", hand.getHandValue(), " New value: ", hand.getHandValue() - 10)
                            softTotalDeductionCount += 1
                        else:
                            print("BUST! Value is: ", hand.getHandValue() - softTotalDeductionCount * 10)
                            self.handleBustHand(player, hand)
                            break
                    if hand.isSoftTotal() and softTotalDeductionCount < hand.getAcesCount():
                        print("We have a soft total...")
                        action = player.strategy.softTotalOptimalDecision(hand, dealerUpcard.getValue())
                    elif hand.isPair():
                        print("We have a pair...")
                        splitHand = self.handleSplitPair(player, hand, dealerUpcard, count.trueCount)
                        if splitHand is not None:
                            handQueue.append(splitHand)
                            handQueue.append(hand)
                        break
                    else:
                        # Get hard total value
                        print("We have a hard total of ", hand.getHandValue()- softTotalDeductionCount * 10)
                        action = player.strategy.hardTotalOptimalDecision(hand, dealerUpcard.getValue(), softTotalDeductionCount)
                    if (action == GameActions.HIT.value):
                        print("Player is gonna hit!")
                        self.hit(player, hand, count)
                    elif (action == GameActions.STAND.value):
                        print("Player will stand")
                    elif (action == GameActions.DOUBLE.value):
                        print("Double down!")
                        self.doubleDown(player, hand, count)
                    
        print(player.name, " has played all of their hands!")

    def startGame(self):
        self.dealer.shuffle()
        print("Starting new blackjack game:")

        handCount = 1
        playersInGame: List[Player] = []

        for player in self.players:
            playersInGame.append(player)
            print("Player: ", player.name, " has joined the round.")

        count = HiLoCount()

        # Play the game! 
        while (handCount <= self.hands and len(playersInGame) > 0):
            print("Round: ", handCount, " Count: ", count.runningCount)
            # Deal out the players' and dealer's cards
            self.dealPlayersHands(playersInGame, count)
            self.dealDealersHand(count)

            # If the dealer shows an ace, dealer will offer insurance to all players.
            if self.dealer.insuranceIsOffered():
                self.handleInsurance(playersInGame, count.runningCount)
            
            # If the dealer was dealt a blackjack, all players automatically lose UNLESS they too have a blackjack
            if self.dealer.hand.isBlackjack():
                self.handleDealerBlackjack(playersInGame, count)
            else:
                # Allow players to play out each round
                for player in playersInGame:
                    self.playRound(player, self.dealer.upcard, handCount, count)
        
            handCount = handCount + 1

            self.clearAllCards(playersInGame)

            # Used to debug deck sizes to ensure that no cards are being lost:
            self.dealer.ensureDeckCompleteness(isVerbose=True)

            # If we have exceeded or reached optimal shoe penetration, reset the shoe and the running count
            if self.dealer.deckPenetrationTooHigh():
                self.dealer.shuffle()
                count.resetCount()




if __name__ == '__main__':
    main()