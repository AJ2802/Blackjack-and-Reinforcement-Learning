from deck import Deck
import random
import math
action =['hit', 'stick']
strNumber = set(['2','3','4','5','6','7','8','9','10'])
strJQK = set(['J','Q','K'])
strA = set(['A'])
class Player():
    def __init__(self, name, identity, deck, num, bet):
        self.name = name
        self.identity = identity #either dealer or player
        self.hand = deck.hand(num)
        self.usableAce = False
        for card in self.hand:
            if card.character == 'A':
                self.usableAce = True
                break
        self.num = num #number of cards on hand
        self.bet = bet
        self.score = 0
        self.betReturn = 0
        self.status = None #L(Loss), D(Draw), W(Win)
        self.policy = None


    def getHand(self, deck, num, bet):
        self.hand = deck.hand(num)
        self.usableAce = False
        for card in self.hand:
            if card.character == 'A':
                self.usableAce = True
                break
        self.num = num #number of cards on hand
        self.bet = bet
        self.score = 0
        self.betReturn = 0
        self.status = None #L(Loss), D(Draw), W(Win)


    def hit(self, deck):
        card = deck.getCard()
        if self.usableAce == False and card.character == 'A':
            self.usableAce = True
        self.hand.append(card)
        self.num += 1

    def count(self): #maxValue
        numA = 0
        value = 0
        for card in self.hand:
            if card.holeCard:
                continue
            if card.character in strJQK:
                value += 10
            if card.character in strNumber:
                value += int(card.character)
            if card.character in 'A':
                value += 1
                numA += 1

        for i in range(numA):
            if value + 10 <= 21:
                value += 10
            else:
                break
        return value

    def numHand(self):
        return self.num

    def showHand(self):
        string = self.name + ": "
        for card in self.hand:
            if card.holeCard:
                string = string + ("( *, * ), ")
            else:
                string = string + "( " + card.character + ", " + card.suit +" ), "
        return string[:-1]

    def isBurst(self):
        if self.count() > 21:
            return True
        else:
            return False

    def isBlackJack(self):
        if self.num == 2:
            flag1 = self.hand[0] in strJQK and self.hand[1] in strA
            flag2 = self.hand[1] in strJQK and self.hand[0] in strA
            return flag1 or flag2
        return False

    def computeScore(self):
        if self.isBurst():
            self.score = 1
            return
        self.score = self.count()
        return

    def holeCard(self, holdCardIndex, action): #action = set or release
        if action == 'set' and self.identity == "dealer" and self.num == 2:
            self.hand[holdCardIndex].holeCard = True
        if action == 'release' and self.identity == "dealer" and self.num == 2:
            self.hand[holdCardIndex].holeCard = False

class SampleState():
    def __init__(self, state, decision , returnValue):
        self.state = state
        self.decision = decision
        self.returnValue = returnValue


class BlackJack():

    def __init__(self):
        numOfDec = 4
        self.deck = Deck(4)
        self.deck.shuffle()
        self.mu = None # player's behavior policy distribution
        self.pi = None # player's target policy
        self.Q = None # action-state value
        self.C = None # accumulated sum of importance sampling ratio
        self.gamma = None #discounted rate


    def winOrLoss(self, player, dealer):
        if player.score < dealer.score or player.isBurst():
            dealer.betReturn += player.bet
            player.betReturn = 0
            player.status = "L"
        if player.score > dealer.score or (player.isBlackJack() and not dealer.isBlackJack()):
            dealer.betReturn -= player.bet
            player.betReturn = 2*player.bet
            player.status = "W"
        if player.score == dealer.score and not player.isBurst() and (player.isBlackJack() and dealer.isBlackJack()):
            player.betReturn = player.bet
            player.status = "D"
        return

    def hitDecision(self, state, distribution = None, deterministic = False):
        return 'hit'
    def stickDecision(self, state, distribution = None, deterministic = False):
        return 'stick'
    def randomDecision(self, state, distribution = None, deterministic = False, conservative = 0.5, critical_value = 15): #conservativeis between 0 and 1
        (playerScore, dealerScore, playerUsableAce) = state
        if dealerScore < critical_value and random.random() > conservative * dealerScore /(critical_value+1):
            return 'hit'
        else:
            return 'stick'

    def setDealerPolicy(self): #conservativeis between 0 and 1
        # j stands for dealerValue: 1->burst, 2..21->handVaue
        # i stands for playerValue: 1->burst, 2..21->handVaue
        dealerPolicy = {}

        for i in range(1, 22):
            for j in range(1, 22):
                for k in range(0,2):
                    playerComputeScore = i
                    dealerComputeScore = j
                    usableAce = k
                    state = (playerComputeScore, dealerComputeScore, usableAce)
                    if j == 1:
                        dealerPolicy[state] = self.stickDecision
                    else:
                        if i < j:
                            dealerPolicy[state] =  self.stickDecision
                        if i == j:
                            dealerPolicy[state] = self.randomDecision
                        if i > j:
                            dealerPolicy[state] = self.hitDecision

        return dealerPolicy

    def muDistribution(self):
        mu = {}
        # i stands for playerValue: 2..21->handCount
        # j stands for non holeCard dealerValue:  2..11->handCount
        # k stands for usableAce: 0-> False, 1-> True
        # mu stands for soft behavior policy distribution
        # Note mu[(state, 'hit')] + mu[(state, 'stick')] = 1
        for i in range(2,22):
            for j in range(2,12):
                for k in range(0,2):
                    state = (i,j,k)
                    pair = (state, 'hit')
                    mu[pair] = 0.5
                    mu[(state,"stick")] = 1 - mu[pair]
        return mu

    def softRandomDecision(self, state, distribution, deterministic = False):

        (playerComputeScore, dealerComputeScore, usableAce) = state
        pair = (state, 'hit')
        if deterministic:
            if distribution[(state, 'hit')] > distribution[(state, 'stick')]:
                return 'hit'
            if distribution[(state, 'hit')] < distribution[(state, 'stick')]:
                return 'stick'
            if distribution[(state, 'hit')] == distribution[(state, 'stick')]:
                if random.random() < 0.5:
                    return 'hit'
                else:
                    return 'False'
        if random.random() < distribution[pair]:
            return 'hit'
        else:
            return 'stick'

    def setPlayerPolicy(self): #conservativeis between 0 and 1
        # i stands for playerValue: 2..21->handCount
        # j stands for non holeCard dealerValue:  2..11->handCount
        # k stands for usableAce: 0-> False, 1-> True
        behaviorPolicy = {}

        for i in range(2, 22):
            for j in range(2, 12):
                for k in range(0,2):
                    playerComputeScore = i
                    dealerComputeScore = j
                    usableAce = k
                    state = (playerComputeScore, dealerComputeScore, usableAce)
                    if i == 21:
                        behaviorPolicy[state] =  self.stickDecision
                    else:
                        behaviorPolicy[state] =  self.softRandomDecision
        return behaviorPolicy

    def generateAnEpisode(self, distribution, deterministic):
        self.deck.newDeck()
        dealer = Player(name = "dealer", identity = "dealer", deck = self.deck, num = 2, bet = 0)
        dealer.policy = self.setDealerPolicy()


        player = Player(name = "player", identity = "player", deck = self.deck, num = 2, bet = 0)

        behaviorPolicy = self.setPlayerPolicy()

        dealer.getHand(deck = self.deck, num = 2, bet = 1)
        dealer.holeCard(holdCardIndex = 0, action = "set")
        dealer.computeScore()

        sampleStateList = []
        player.getHand(deck = self.deck, num = 2, bet = 1)
        player.computeScore()
        state = (player.score, dealer.score, player.usableAce)

        #Player 's Turn
        while(True):
            decision = behaviorPolicy[state](state = state, distribution = distribution, deterministic = deterministic)
            sampleState = SampleState(state, decision, 0)
            sampleStateList.append(sampleState)
            if decision == 'hit':
                player.hit(self.deck)
                player.computeScore()
                if player.isBurst():
                    break
                state = (player.score, dealer.score, player.usableAce)
            else:
                break
        #dealer's Turn
        dealer.holeCard(holdCardIndex = 0, action = "release")
        while(True):
            decision = dealer.policy[state](state = state)

            if decision == 'hit':
                dealer.hit(self.deck)
                dealer.computeScore()
                state = (player.score, dealer.score, player.usableAce)
            else:
                break
        self.winOrLoss(player = player, dealer = dealer)
        if player.status == 'W':
            sampleStateList[-1].returnValue = 1
        if player.status == 'L':
            sampleStateList[-1].returnValue = -1
        #for sampleState in sampleStateList:
        #    print(sampleState.state, sampleState.decision, sampleState.returnValue)
        #print("player " + player.showHand())
        #print("dealer" + dealer.showHand())
        #print
        return sampleStateList

    def updatePolicy(self, sampleStateList):
        #gamma -> discount rate, C = {}, Q = {}, mu, behaviorPolicyDistribution, pi = targetPolicy
        #self.gamma, self.C, self.Q, self.pi
        G = 0
        W = 1
        while(len(sampleStateList) > 0):
            sampleState = sampleStateList.pop()
            (state, decision, returnValue) = (sampleState.state, sampleState.decision, sampleState.returnValue)
            G = self.gamma * G + returnValue
            pair = (state, decision)
            if pair in self.C:
                self.C[pair] = self.C[pair] + W
            else:
                self.C[pair] = W
            self.Q[pair] = self.Q[pair] + W/self.C[pair]*(G - self.Q[pair])
            #action = ["hit", "stick"]
            termHit = math.exp(self.Q[(state, "hit")])
            termStick = math.exp(self.Q[state, "stick"])
            dem = termHit + termStick
            self.pi[(state, "hit")] = termHit/dem
            self.pi[(state, "stick")] = termStick/dem
            W = W*self.pi[pair]/self.mu[pair]


            """
            if self.Q[(state, "hit")] >= self.Q[(state, "stick")]:
                self.pi[state] = "hit"
            else:
                self.pi[state] = "stick"
            if decision != self.pi[state]:
                break
            W = W*1/self.mu[pair]
            """



    def initial_Q_And_pi(self):
        # i stands for playerValue: 2..21->handCount
        # j stands for non holeCard dealerValue:  2..11->handCount
        # k stands for usableAce: 0-> False, 1-> True
        Q = {}
        pi = {}
        for i in range(2,22):
            for j in range(2,12):
                for k in range(0,2):
                    state = (i, j ,k)
                    for decision in action:
                        pair = (state, decision)
                        Q[pair] = random.gauss(0,0.5)
                    #softmax
                    termHit = math.exp(Q[(state, "hit")])
                    termStick = math.exp(Q[state, "stick"])
                    dem = termHit + termStick
                    pi[(state, "hit")] = termHit/dem
                    pi[(state, "stick")] = termStick/dem
                    """
                    if Q[(state, "hit")] >= Q[(state, "hit")]:
                        pi[state] = "hit"
                    else:
                        pi[state] = "stick"
                    """
        return Q, pi


    def offPolicyMonteCarloTraining(self, trainingIteration):
        self.Q, self.pi = self.initial_Q_And_pi()
        self.C = {}
        self.gamma = 1
        self.mu = self.muDistribution()
        for i in range(trainingIteration):
            sampleStateList = self.generateAnEpisode(distribution = self.mu, deterministic = False)
            self.updatePolicy(sampleStateList)

    def playGame(self, simulationIteration):
        result = {'D':0, 'W':0, 'L':0}
        for i in range(simulationIteration):
            sampleStateList =self.generateAnEpisode(distribution = self.pi, deterministic = True)
            returnValue = sampleStateList[-1].returnValue
            if returnValue == 0:
                result['D'] = result['D'] + 1
            if returnValue == 1:
                result['W'] = result['W']  + 1
            if returnValue == -1:
                result['L'] = result['L'] + 1
        print("win percentage: ", float(result['W'])/simulationIteration)
        print("draw percentage: ", float(result['D'])/simulationIteration)
        print("loss percentage: ", float(result['L'])/simulationIteration)
