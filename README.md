# Blackjack Strategy Simulator

A collection of python scripts aimed at simulating the relationship between different playstyles of Blackjack and the effect it has on a player's bankroll over time.

## Overview

### The Game of Blackjack

In the game of Blackjack, the objective is to have a hand value of 21 or as close to 21 as possible without going over. Each player is dealt two cards, with the option to "hit" and receive additional cards in an attempt to improve their hand value. The values of the cards in the player's hand are added up, with face cards (Jack, Queen, King) counting as 10 and an Ace counting as either 1 or 11, depending on which value would be more beneficial for the player. The dealer also receives two cards, but typically only shows one of them. The dealer must hit until their hand value is at least 17. If a player's hand exceeds 21, they lose. If the player's hand is closer to 21 than the dealer's, the player wins. If the dealer's hand exceeds 21, the player wins.

### Player Actions

In a game of Blackjack, a player has several options for actions they can take:
* "Hit" - This action allows the player to receive an additional card in an attempt to improve their hand value.
* "Stand" - This action means that the player is satisfied with their current hand value and does not wish to receive any more cards.
* "Double Down" - This action allows the player to double their initial bet and take one more card.
* "Split" - This action is available when a player has two cards of the same value. It allows them to split the pair and play two separate hands.
* "Surrender" - This action is available at some casinos, it allows the player to forfeit half of their bet and end the round.
* "Insurance" - This action is available when the dealer's face-up card is an Ace, it allows the player to make a side bet on whether the dealer has a blackjack or not.
It's worth noting that some casinos or variations of the game might not offer all the actions mentioned above. In this Python script, users can specify the house rules that they want to play with which can alter the outcome of the game slightly. 

### House Edge

The casino has an advantage in Blackjack, known as the "house edge," because the rules of the game are slightly in favor of the casino. The main reason for this is that players must act before the dealer and therefore may bust (go over 21) before the dealer even plays their hand. Additionally, if the player busts, they automatically lose their wager, regardless of what the dealer's hand is.

Another reason is that the dealer follows a strict set of rules for playing their hand, which is known as the "dealer's rule." The dealer must hit if their hand is below 17 and must stand on 17 or higher. This means that the dealer must take cards when they have a lower chance of busting and must stop taking cards when they have a higher chance of busting, while the player can choose their own strategy. Finally, when the player and the dealer have the same hand value, the player loses (this is known as a push) and the casino keeps the bet, this is another way the casino has an edge. All these advantages give the casino an approximate edge of 1-5% depending on the rules of the game and the strategy used by the player.

### Basic Strategy

Basic strategy in Blackjack is a set of rules that players can use to make the best possible decision in any given situation. These decisions are based on mathematical calculations and probability, and take into account the player's hand, the dealer's face-up card, and the number of decks being used.

Basic strategy provides players with a recommended action for every possible combination of cards that can be dealt. For example, it will tell a player when it is best to hit, stand, double down, split, or take insurance. By following basic strategy, players can reduce the house edge and increase their chances of winning.

Basic strategy can vary slightly depending on the specific rules of the game being played, such as the number of decks used, whether the dealer hits or stands on soft 17, and whether the player is allowed to surrender. Some players use a strategy card or chart as a guide to help them remember the correct play for each situation, but it's also possible to learn it by heart. The chart that was used for this project was taken from [Blackjack Apprenticeship's Webpage](https://www.blackjackapprenticeship.com/blackjack-strategy-charts/).

It's worth noting that Basic strategy is not a guarantee of winning, but it's a useful tool to help players make the best possible decisions, and reduce the house edge. It's also important to remember that even with the use of basic strategy, luck still plays a role in the outcome of each hand. In fact, learning basic strategy isn't enough to take down the house. To do this, players will need to learn the art of counting cards.

### Card Counting

Card counting is a technique used by some Blackjack players to gain an advantage over the casino. It involves keeping track of which cards have been dealt from the deck or shoe (the device used to hold multiple decks of cards) and adjusting the player's betting and playing strategy based on that information. The basic idea behind card counting is that when the remaining deck or shoe has a higher proportion of high cards (10s, face cards, and aces) the player has a higher chance of getting a blackjack or a strong hand, so they should increase their bets. On the other hand, when the remaining deck or shoe has a higher proportion of low cards (2s, 3s, 4s, 5s, and 6s) the player's chance of getting a blackjack or a strong hand decreases, so they should decrease their bets.

Card counting gives an advantage to the player because it allows them to make more informed decisions about when to hit, stand, double down, split, etc. and also when to increase or decrease their bets. The advantage comes from the fact that when the remaining deck or shoe has a higher proportion of high cards, the player's chances of winning are increased, and when the remaining deck or shoe has a higher proportion of low cards, the player's chances of winning are decreased.

It's worth noting that card counting is not illegal, but it is generally not allowed in casinos and if caught, a player can be banned from playing blackjack. Additionally, it's a difficult skill to master and requires a lot of practice and concentration, also it's not a guarantee of winning.

## Running the Simulation

You can run the Blackjack simulation by running the command:
```
python blackjack.py
```
Which will run the simulation with the default settings and the pre-listed players within the `blackjack.py` file. To change any game settings within the simulation, use the below flags:
* `-s` or `--shoesize` - This determines the amount of decks in the shoe. Default is 6 decks in a shoe.
* `-b` or `--bankroll` - This determines the dollar amount that each player's bankroll begins the game with. Default is $10,000
* `-h` or `--hands` - Determines the number of hands to deal in the game. Default is 1000 hands.
* `-t` or `--tablemin` - Determines the minimum table bet. Default is $10.
* `-p` or `--penetration` - Dictates the maximum deck penetration by the dealer. Deck penetration is represented as a decimal percentage and tells the dealer at what point to reshuffle the shoe. Default is 0.84. (In other words, the dealer deals 84% of the shoe before reshuffling)
* `-d` or `--dealersettings` - An array of length 5 that determines what the casino's house rules are. To change the dealer settings, input an array of length 5 that contains the values for each of the above settings. (e.g. `[houseStandValue, DASoffered, RSAoffered, LSoffered, DSToffered]`)
  * House Stand Value - An integer that represents the hand value threshold for which the dealer must stand. Default is `17`.
  * Double-After-Split (DAS) Offered - Determines if the dealer allows players to double their bet after the player has split their pair. Default is `True`.
  * Re-Split Aces (RSA) Offered - Determines if the player is allowed to re-split their aces given that they have already split aces. Default is `True`.
  * Late Surrender (LS) Offered - Determines if the player is allowed to late surrender their hand. Default is `True`.
  * Double on Soft Total (DST) Offered - Determines if the player is allowed to double on a soft total. Default is `True`.
 * `-v` or `--verbose` - Enables verbose printing. Default is `False`.
 
 ### Creating new players
 
 To create new players, simply instantiate a new `Player` object in the constructor of the `BlackJackGame` class and add it to its `players` field. The `Player` object takes in the following parameters:
 * `playerName` - A string representing the name of the player.
 * `bankroll` - An integer representing the player's starting bankroll. It's recommended that you use the default value so that all players start with an equal bankroll. 
 * `strategy` - A `Strategy` object. Can be any of them (`BasicStrategy`, `RandomStrategy`, `CasinoStrategy` or another custom strategy).
 * `betSpread` - A `BetSpread` object that the player uses to determine their bets.
 * `isVerbose` - Whether or not we wish to print information about how this particular player plays their hands.
 
 ### Creating new strategies
 
 To create new strategy, simply add a new strategy class within the `strategy.py` file and extend the `StrategyInterface` class. New strategies must implement the following methods:
 * `hardTotalOptimalDecision()` - Determines the optimal hard total decision and returns a `GameAction`.
 * `shouldSplitPair()` - Returns a boolean representing whether or not it's in the player's best interest to split their pair.
 * `softTotalOptimalDecision()` - Determines the optimal soft total decision and returns a `GameAction`.
 * `willTakeInsurance()` - Returns a boolean representing whether or not it's in the player's best interest to take insurance.
 
 ### Adding new bet-spreads

To add a new bet-spread, add a new spread class within the `bet.py` file and extend the `BetSpreadInterface` class. New bet spreads must implement the following method:
* `getBetSpreads()` - Returns the $ amount that the player should bet given the true count and the table minimum bet. 
