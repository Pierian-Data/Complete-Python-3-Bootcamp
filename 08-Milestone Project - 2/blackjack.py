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

class Hand:
    def __init__(self):
        self.deck = [] #start with an empty list
        self.value = 0 #start with zero value
        self.aces = 0 #add an attribute to keep track of aces

    def add_card(self,card):
        pass

    def adjust_for_ace(self):
        pass


class Chips:

    def __init__(self):
        self.total = 500

        self.bet = 0

    def win_bet(self):
        pass

    def lose_bet(self):
        pass


def take_bet():

    pass #maybe use try/except. Make sure you have enough chips

def hit(deck,hand):

    pass #hit adds cards until the players bust

def stand(deck,hand):

    pass #function to stop taking cards

def hit_or_stand(deck,hand):

    pass #prompt the player to hit or to stand


def show_some(player,dealer):

    pass #show only some of the cards (dealer only shows 1)

def show_all(player,dealer):

    pass #show all of the cards in a hand

def player_busts():
    
    pass #End of Game scenario where the player busts

def player_wins():

    pass #End of Game scenario where the player wins

def dealer_busts():

    pass #End of Game scenario where the dealer busts

def dealer_wins():

    pass #End of Game scenario where the dealer wins

def push():

    pass #End of Game scenario where the dealer and player tie




x = Deck()

x.shuffle()

print(x)

x.deal()

def play_blackjack():
    while True:
    # Print an opening statement

    
    # Create & shuffle the deck, deal two cards to each player

    
        
    # Set up the Player's chips
    
    
    # Prompt the Player for their bet

    
    # Show cards (but keep one dealer card hidden)

        pass

    #while playing:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        
        
        # Show cards (but keep one dealer card hidden)
 
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        

            #break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    
    
        # Show all cards
    
        # Run different winning scenarios
        
    
    # Inform Player of their chips total 
    
    # Ask to play again
        
            #pass
        