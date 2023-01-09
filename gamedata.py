from blackjack import BlackJackGame
from player import Player

class GameData:
    def __init__(self, game):
        self.game: BlackJackGame = game
        self.players = self.game.players
        self.dealer = self.game.dealer
    
    def getPlayerSnapshots(self):
        for player in self.players:
            print(player.bankrollSnapshots)
    
