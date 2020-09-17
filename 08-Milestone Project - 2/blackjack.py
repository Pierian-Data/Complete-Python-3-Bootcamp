###Black Jack game###

import random ###import random so that we can shuffle cards###

###Create the 4 card suits###
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs') 

###Create the 13 card types###
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')

###Set values to the various cards####
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        '''
        Set phrase to be returned when printing the Card class
        '''
        return f'{self.rank} of {self.suit}'


class Deck:
    
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
                
    def __str__(self):
        deck_comp = ''  # start with an empty string
        for card in self.deck:
            deck_comp += '\n '+card.__str__() # add each Card object's print string
        return 'The deck has:' + deck_comp
    
    def shuffle (self):
        random.shuffle(self.deck)


    def deal (self):
        pass
                
    
x = Deck()

x.shuffle()

print(x)


