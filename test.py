from cardGames import BlackJack
import random

trainingIteration = 100000
simulationIteration = 1000
game = BlackJack()
game.offPolicyMonteCarloTraining(trainingIteration)
game.playGame(simulationIteration)
