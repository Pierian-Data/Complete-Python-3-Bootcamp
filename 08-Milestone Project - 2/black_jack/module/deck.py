'''
Deck class

'''
import random

class Deck:
	suits = ['Clubs', 'Spades', 'Diamonds', 'Hearts']
	ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
	deck = []

	'''
	Build a desk as new
	'''
	def __init__(self):
		for suit in self.suits:
			for rank in self.ranks:
				self.deck.append((suit, rank))

	'''
	shuffle the card's deck
	'''
	def shuffle(self):
		random.shuffle(self.deck)

	'''
	@return: a card (suit, rank), -1 otherwise
	'''
	def hit(self):
		try:
			return self.deck.pop()
		except:
			__init__()
			return self.deck.pop()