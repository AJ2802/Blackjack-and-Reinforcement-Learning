# Blackjack-and-Reinforcement-Learning
This project is to search for optimal player strategy of playing Blackjack in a 1 dealer and 1 player game.

Detailed manual Instruction and notes about off policy Monte Carlo update will be uploaded later.

Demonstration:
1. Download deck.py, cardGames.py and test.py in this repository
2. Edit trainingIteration and simulationIteration in a test.py. TrainingIteration is used to train player's policy by Monte Carlo Simulation. With a good computer, trainingIteration is recommended to be 1000000 [could take 30min for training]. Otherwise, trainingIteration is recommended can be 100000 [take a few mins for training].
3. Run test.py by using python 2.7.10 (not python 3 or above)
4. Result of win, draw and loss percentage according to the player strategy after training is outputted.

