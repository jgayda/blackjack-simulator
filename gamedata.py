from blackjack import BlackJackGame
from player import Player
import matplotlib.pyplot as plt
import numpy as np

class GameData:
    def __init__(self, game):
        self.game: BlackJackGame = game
        self.players = self.game.players
        self.dealer = self.game.dealer
        self.bankrollData = {}
        self.getPlayerBankrollSnapshots()
    
    def getPlayerBankrollSnapshots(self):
        numHands = self.game.numHands
        for player in self.players:
            self.bankrollData.update({player.name: player.bankrollSnapshots})
    
    def plotBankrollTime(self):
        roundAxis = [item for item in range(1, numHands + 1)]

        plt.plot(roundAxis, self.bankrollData.get("Optimal"))
    
