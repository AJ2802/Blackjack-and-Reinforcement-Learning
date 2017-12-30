# Blackjack-and-Reinforcement-Learning
This project is to search for optimal player strategy of playing Blackjack in a 1 dealer and 1 player game.

Python version to run my script: 2.7.10

I. Demonstration and result:
1. Download deck.py, cardGames.py and test.py in this repository
2. Edit trainingIteration and simulationIteration in a test.py. TrainingIteration is used to train player's policy by Monte Carlo Simulation. With a good computer, trainingIteration is recommended to be 1000000 [could take 30min for training]. Otherwise, trainingIteration is recommended can be 100000 [take a few mins for training].
3. Run test.py by using python 2.7.10 (not python 3 or above)
4. Result of player's win, draw and loss percentage according to the player strategy after training is outputted.

From the demonstration, we can seen that if trainingIteration is too small, e.g. 100, the player's win percentage is around 30%. After well training, the player's win percentage can be as high as the dealer's percentage. I am not sure if there is a player strategy to boost player' s win percentage significantly higher than a nearly perfect dealer's signifcantly since the dealer has advantages in a Blackjack game: 1. player does not know both cards of dealer's hand in the beginning of a game and 2. dealer can make "hit" or "stick" decision based on player's decisions in its turn.

II. Dealer's policy (See SetDealer's policy in cardGames.py):
Dealer's policy is not a subject in this project and the policy is set by the following: after we finish his turn, a dealer will hit if his max. pts is less than our max. pts. A dealer will choose hold if his max. pts is higher than our max. pts. If  a dealer's max pts are tied with our pts, a dealer may choose to hit based on his conservative parameter and his score. 

III. Player's policy:
Player's policy (that is us) is a policy to be learned and to be optimized. We first illustrate a basic concept of the off policy Monte Carlo algorithm and then discuss the pseudo code of the off policy Monte Carlo algorithm on Blackjack. 

Background of the off policy Monte Carlo algorithm:
In the off-policy algorithm, there are target policy \pi and behavior policy \mu. Behavior policy is an exploratory policy in an action space while target policy is learned to be an optimal policy. One condition between \mu and \pi is \mu >> \pi [\pi is abs. continuous w.r.t. \mu]. There are three major components of the off policy Monte Carlo algorithm.

1. An episode/ a game which is a finite sequence of (state S_t, action A_t, intermediate return R_t+1) is simulated by the environment and behavior policy \mu.

2. The action-valued function Q^\pi (s,a) is the expected value of return starting at state s and action a and then following policy \pi. And Q^\pi (s,a) is updated by by the ideas of weighted importance sampling and online update for calculating mean.

3. The target policy \pi is improved by the greedy algorithm whenever the action-valued function Q^\pi (s,a) is updated . In the end, the target policy may converge to the optimal policy.

III. The off policy Monte Carlo algorithm on Blackjack (see offPolicyMonteCarloTraining in cardGames.py):
Parameters:
State space S: {max pts on our hand (2-21, >21), max pts on deal's hand (2-11), is any ace on our hand (1:yes, 0: no)}
action space A: hit or hold
reward G: Reward is 0 in any intermediate step of the game. Reward at the last step of the game is 1, 0 and -1 if we win, draw and loss respectively.
discount rate, labeled as r, is set to be 1.

Initialization Step: For all s in state space and a in action space, we do the following:
1. Q^\pi(s,a) is initialized by a Gaussian distribution with mean 0 and std 0.5
2. C(s,a) is all set to be 0 (it is used for online update for calculating mean. It stands for the current sum of all adjusted returns in sub-episodes starting at s and a during a Monte Carlo simulation)
3. \pi(s) is a target policy (could be deterministic) that is greedy w.r.t. Q^pi(s,a)

Update Step: Repeat the following many times and start at t=0
1. Generate an episode using a behavior policy \mu. A finite sequence of {(S_0, A_0, R_1),...,S_T, A_T, R_T+1)} is generated.
2. G<-0 and W<-1 (W is the importance sampling ratio of return starting at (S_t, A_t). W is first set to be 1 coz when Q(S_t, A_t) is updated, the occurrence of S_t and A_t is already assumed and hence the importance sampling ratio for this occurrence is 1.)
3. For t = T-1, T-2,...downto 0
      3.1 G<-rG+R
      3.2 C(S_t,A_t)<- C(S_t,A_t) + W
      3.3 Q(S_t,A_t)<- Q(S_t,A_t) + W/C(S_t,A_t) * {G-Q(S_t,A_t)}
      3.4 dem = exp(Q(S_t,Hit)) + exp(Q(S_t,Hold))
      3.5 \pi(Hit | S_t)<- exp(Q(S_t,Hit))/dem and \pi(Hold | S_t)<- exp(Q(S_t,Hold))/dem
      3.6 W<-W*\pi(A_t|S_t)/\mu(A_t|S_t)
Output: an optimal policy \pi such that if a state S_t is given, a decision is argmax_a \pi(a|S_t).


