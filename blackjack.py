import click
from shoe import Shoe
from player import Player
from count import HiLoCount
from hand import Hand
from card import Card, CardValue
from dealer import Dealer
from strategies import BasicStrategy

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
    print("Dealer has rules: ")
    print("Deck Penetration %: ", penetration, " | Dealer stands on ", dealersettings[0], " | Double after split offered? ", dealersettings[1], " | Players can re-split aces? ", dealersettings[2], " Surrender offered? ", dealersettings[3])
    game = BlackJackGame(shoesize, bankroll, hands, tablemin, penetration, dealersettings)
    game.startGame()
class BlackJackGame:
    def __init__(self, shoeSize, bankroll, hands, tableMin, penetration, dealerSettings):
        print("Initializing players and dealer...")
        self.shoeSize = shoeSize
        self.shoe = Shoe(self.shoeSize)
        self.hands = hands
        #self.players = [Player("Optimal", bankroll, BasicStrategy), Player("BasicStrat", bankroll, BasicStrategy), Player("Default", bankroll, NoStrategy)]
        dealerStandValue = dealerSettings[0]
        doubleAfterSplitOffered = dealerSettings[1]
        resplitAcesOffered = dealerSettings[2]
        surrenderOffered = dealerSettings[3]
        self.dealer = Dealer(dealerStandValue, doubleAfterSplitOffered, resplitAcesOffered, surrenderOffered, penetration)
        self.players = [Player("Optimal", bankroll, BasicStrategy(doubleAfterSplitOffered))]
    
    def playRound(self, player: Player, dealerUpcard: Card):
        # First, determine if we have a pair and if we should split:
        dealtHand = player.getHand()
        if dealtHand.isPair():
            if player.strategy.shouldSplitPair(dealtHand.card1.getValue(), dealerUpcard.getValue()):
                # The player *should* split the pair, but can they afford to?
                if player.calculateBetSize() <= player.bankroll:
                    player.splitPair()
            
        # Next for each hand, determine what our action is
        for hand in player.hands:
            count = 1

    def startGame(self):
        self.shoe.resetShoe()
        print("Starting new blackjack game:")
        print("Shoe size: ", self.shoeSize, " | Number of players: ", len(self.players))

        handCount = 1
        playersInGame = []

        for player in self.players:
            playersInGame.append(player)
            print("Player: ", player.name, " has joined the round.")

        count = HiLoCount()

        # Play the game! 
        while (handCount <= self.hands and len(playersInGame) > 0):
            print("Round: ", handCount, " Count: ", count.runningCount)
            # Deal out the players cards
            for player in playersInGame:
                betSize = player.calculateBetSize()
                card1: Card = self.shoe.drawCard()
                count.updateRunningCount(card1.getValue())
                card2: Card = self.shoe.drawCard()
                count.updateRunningCount(card2.getValue())
                playerHand = Hand(card1, card2, betSize)
                player.updateHand(playerHand)
                playerHand.printHand()
            
            # Deal out the dealers cards
            upcard = self.shoe.drawCard()
            count.updateRunningCount(upcard.getValue())

            # The hidden card is not added to the count yet as only the dealer knows this information
            hiddenCard = self.shoe.drawCard()
            dealerHand = Hand(upcard, hiddenCard)

            print("Dealer shows:")
            upcard.printCard()

            if upcard.getValue == CardValue.Ace:
                # Todo offer insurance
                print("Insurance offered...")

            # Allow players to play out each round
            for player in playersInGame:
                self.playRound(player, upcard)
        
            handCount = handCount + 1

            # Collect the cards from each player before moving onto the next round
            for player in playersInGame:
                allHands = player.hands
                for hand in allHands:
                    self.shoe.discardCards([hand.card1, hand.card2])
                player.clearHand()

            # If we have exceeded or reached optimal shoe penetration, reset the shoe and the running count
            if self.shoe.getPenetration() > self.dealer.penetration:
                self.shoe.resetShoe()
                count.resetCount()





if __name__ == '__main__':
    main()