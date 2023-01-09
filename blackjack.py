import click
from shoe import Shoe
from player import Player
from count import HiLoCount
from hand import Hand
from card import Card, CardValue
from dealer import Dealer
from strategies import BasicStrategy, GameActions
from typing import List

@click.command()
@click.option('-s', '--shoesize', default=6, help='An integer representing the amount of decks to use in the shoe. Default is 6 decks.')
@click.option('-b', '--bankroll', default=1000, help='Determines the amount of dollars that each player begins the game with in their bankroll. Default is $1000.')
@click.option('-h', '--hands', default=1000, help='Determines the number of hands to deal. Default is 1000.')
@click.option('-t', '--tablemin', default=5, help='Determines the minimum table bet. Default is 5.')
@click.option('-p', '--penetration', default=0.84, help='Dictates the deck penetration by the dealer. Default is 0.84 which means that the dealer will penetrate 84 percent of the shoe before re-shuffling')
@click.option('-d', '--dealersettings', default=[17, True, True, True], help='Assigns the dealer rules.')
def main(shoesize, bankroll, hands, tablemin, penetration, dealersettings):
    print("Running blackjack simulation with variables:")
    print("Shoe size: ", shoesize, " | Bankroll: ", bankroll, " | Number of hands to simulate: ", hands, " | Minimum Table Bet: ", tablemin)
    game = BlackJackGame(shoesize, bankroll, hands, tablemin, penetration, dealersettings)
    game.startGame()

class BlackJackGame:
    def __init__(self, shoeSize, bankroll, hands, tableMin, penetration, dealerSettings):
        print("Initializing game...")
        self.shoeSize = shoeSize
        self.hands = hands
        self.tableMin = tableMin

        print("Dealer has rules: ")
        print("Deck Penetration %: ", penetration, " | Dealer stands on ", dealerSettings[0], " | Double after split offered? ", dealerSettings[1], " | Players can re-split aces? ", dealerSettings[2], " Surrender offered? ", dealerSettings[3])
        dealerStandValue = dealerSettings[0]
        doubleAfterSplitOffered = dealerSettings[1]
        resplitAcesOffered = dealerSettings[2]
        surrenderOffered = dealerSettings[3]
        self.dealer = Dealer(dealerStandValue, doubleAfterSplitOffered, resplitAcesOffered, surrenderOffered, penetration, shoeSize)

        self.players = [Player("Optimal", bankroll, BasicStrategy(doubleAfterSplitOffered, isCounting=True)), 
                        Player("Sub-Optimal I", bankroll, BasicStrategy(doubleAfterSplitOffered, isCounting=False)),
                        Player("Sub-Optimal II", bankroll, BasicStrategy(doubleAfterSplitOffered, isCounting=True)),]
        print("There are ", len(self.players), " players in the game.")
    
    def playRound(self, player: Player, dealerUpcard: Card, handNumber, count):
        # First, determine if we have a pair and if we should split:
        dealtHand = player.getHand()

        if dealtHand.isBlackjack():
            # Todo pay out player 3:2
            print("Blackjack!")
        else:
            if dealtHand.isPair():
                if player.strategy.shouldSplitPair(dealtHand.getHandValue() / 2, dealerUpcard.getValue()):
                    # The player *should* split the pair, but can they afford to?
                    print("Wanting to split pair...")
                    if player.calculateBetSize(self.tableMin, count.trueCount) <= player.bankroll:
                        print("Splitting pair...")
                        player.splitPair(self.tableMin, count.trueCount)
            
            # It's now possible that we have two hands that we need to simulate as the player could have split the pair.
            # Instatiate a new dealtHands object:
            for hand in player.hands:
                if hand.isSoftTotal():
                    print("We have a soft total!!!")
                    action: GameActions = player.strategy.softTotalOptimalDecision(hand, dealerUpcard.getValue())
                    print("Action: ", action)
            # Next for each hand, determine what our action is
            for hand in player.hands:
                playerWins = handNumber % 2 == 0
                if playerWins:
                    player.updateBankroll(5)
                else:
                    player.updateBankroll(-5)

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
            # Deal out the players cards
            for player in playersInGame:
                betSize = player.calculateBetSize(self.tableMin, count.trueCount)

                card1: Card = self.dealer.dealCard()
                card2: Card = self.dealer.dealCard()

                count.updateRunningCount(card1.getValue())
                count.updateRunningCount(card2.getValue())

                player.updateHand(Hand([card1, card2], betSize))
                player.getHand().printHand()
            
            # Deal out the dealers cards
            upcard = self.dealer.dealCard()
            count.updateRunningCount(upcard.getValue())

            # The hidden card is not added to the count yet as only the dealer knows this information
            hiddenCard = self.dealer.dealCard()
            dealerHand = Hand([upcard, hiddenCard], 0)
            self.dealer.updateHand(dealerHand)

            print("Dealer shows:")
            upcard.printCard()

            print("Dealer hides:")
            hiddenCard.printCard()

            if upcard.getValue == CardValue.Ace:
                # Todo offer insurance
                print("Insurance offered...")

            # Allow players to play out each round
            for player in playersInGame:
                self.playRound(player, upcard, handCount, count)
        
            handCount = handCount + 1

            # Collect the cards from each player before moving onto the next round and put the cards in the
            # discard pile
            for player in playersInGame:
                allHands = player.hands
                for hand in allHands:
                    print("Hand: ", hand.cards, " | Betsize: ", hand.betSize, " | type: ", type(hand))
                    self.dealer.discardCards(hand)
                player.clearHand()
            
            # Discard the dealer's cards and move them to the discard pile
            self.dealer.discardCards(self.dealer.hand)
            print("No missing cards? : ", self.dealer.ensureDeckCompleteness(True))

            # If we have exceeded or reached optimal shoe penetration, reset the shoe and the running count
            if self.dealer.deckPenetrationTooHigh():
                self.dealer.shuffle()
                count.resetCount()





if __name__ == '__main__':
    main()