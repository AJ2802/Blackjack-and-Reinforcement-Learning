import random

class Card():
    def __init__(self, suit, character):
        self.character = character
        self.suit = suit
        self.holeCard = False

class Deck():

    def __init__(self, numOfDeck):
        self.numOfDeck = numOfDeck
        self.cards = []
        self.characters = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
        self.suits = ['club', 'diamond', 'heart', 'spade']
        self.numCards = len(self.characters)*len(self.suits)*self.numOfDeck
        for k in range(numOfDeck):
            for character in self.characters:
                for suit in self.suits:
                    self.cards.append(Card(suit, character))
        #self.shuffle()???

    def getCard(self):
        self.numCards -= 1
        return self.cards.pop()

    def shuffle(self):
        random.shuffle(self.cards)

    def newDeck(self):
        self.cards = []
        self.numCards = len(self.characters)*len(self.suits)*self.numOfDeck
        for k in range(self.numOfDeck):
            for character in self.characters:
                for suit in self.suits:
                    self.cards.append(Card(suit, character))
        self.shuffle()

    def numOfCardRemaining(self):
        return self.numCards

    def emptyDeck(self):
        if len(self.numCards) == 0:
            return True
        else:
            return False

    def hand(self, numOnHand):
        return [self.getCard() for i in range(numOnHand)]
