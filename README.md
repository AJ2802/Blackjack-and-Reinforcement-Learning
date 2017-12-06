# Blackjack-and-Reinforcement-Learning
This project is to search for optimal player strategy of playing Blackjack in a 1 dealer and 1 player game.

Detailed manual Instruction and notes about off policy Monte Carlo algorithm on Blackjack will be uploaded later.

Demonstration:
1. Download deck.py, cardGames.py and test.py in this repository
2. Edit trainingIteration and simulationIteration in a test.py. TrainingIteration is used to train player's policy by Monte Carlo Simulation. With a good computer, trainingIteration is recommended to be 1000000 [could take 30min for training]. Otherwise, trainingIteration is recommended can be 100000 [take a few mins for training].
3. Run test.py by using python 2.7.10 (not python 3 or above)
4. Result of player's win, draw and loss percentage according to the player strategy after training is outputted.

From the demonstration, we can seen that if trainingIteration is too small, e.g. 100, the player's win percentage is around 30%. After well training, the player's win percentage can be as high as the dealer's percentage. I am not sure if there is a player strategy to boost player' s win percentage significantly higher than dealer's signifcantly since the dealer has advantages in a Blackjack game: 1. player does not know both cards of dealer's hand in the beginning of a game and 2. dealer can make "hit" or "stick" decision based on player's decisions in its turn.

