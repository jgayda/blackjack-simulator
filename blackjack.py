import click
from shoe import Shoe
from player import Player
from count import HiLoCount
from strategies import BasicStrategy, NoStrategy

@click.command()
@click.option('-s', '--shoesize', default=6, help='An integer representing the amount of decks to use in the shoe. Default is 6 decks.')
@click.option('-b', '--bankroll', default=1000, help='Determines the amount of dollars that each player begins the game with in their bankroll. Default is $1000.')
@click.option('-h', '--hands', default=1000, help='Determines the number of hands to deal. Default is 1000.')
@click.option('-t', '--tablemin', default=5, help='Determines the minimum table bet. Default is 5.')
@click.option('-p', '--penetration', default=0.84, help='Dictates the deck penetration by the dealer. Default is 0.84 which means that the dealer will penetrate 84 percent of the shoe before re-shuffling')
def main(shoesize, bankroll, hands, tablemin):
    print("Running blackjack simulation with variables:")
    print("Shoe size: ", shoesize, " | Bankroll: ", bankroll, " | Number of hands to simulate: ", hands, " | Minimum Table Bet: ", tablemin)
    game = BlackJackGame(shoesize, bankroll, hands)
class BlackJackGame:
    def __init__(self, shoeSize, bankroll, hands):
        print("Starting new blackjack game...")
        self.shoeSize = shoeSize
        self.shoe = Shoe(self.shoeSize)
        self.hands = hands
        #self.players = [Player("Optimal", bankroll, BasicStrategy), Player("BasicStrat", bankroll, BasicStrategy), Player("Default", bankroll, NoStrategy)]
        self.players = [Player("Optimal", bankroll, BasicStrategy)]

    def startGame(self):
        self.shoe.resetShoe()
        print("Starting new blackjack game:")
        print("Shoe size: ", self.shoeSize, " | Number of players: ", len(self.players))

        hand = 1
        playersInGame = []

        for player in self.players:
            playersInGame.append(player)

        count = HiLoCount()

        while (hand <= self.hands & len(playersInGame) > 0):
            # Deal out the players cards
            for player in playersInGame:
                card1 = self.shoe.drawCard()
                count.updateRunningCount(card1)
                card2 = self.shoe.drawCard()
                count.updateRunningCount(card2)
                player.updateHand(card1, card2)
            
            # Deal out the dealers cards
            upcard = self.shoe.drawCard()
            count.updateRunningCount(upcard)
            hiddenCard = self.shoe.drawCard()

            # Allow players to play out each hand
            for player in playersInGame:
                




if __name__ == '__main__':
    main()