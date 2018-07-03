'''
Hand class
'''

class Hand:
	'''
	@input cards: initial cards
	'''
	def __init__(self):
		self.cards = []

	'''
	@input: tuple card (suit, rank)
	'''
	def __str__(self):
		str = ""
		for card in self.cards:
			str += f"{card[1]}-of-{card[0]}\n"
		return str

	'''
	@return score: check the score on current hand
	'''
	def getscore(self):
		score = 0
		numbers_A = 0
		for card in self.cards:
			if card[1] == "King" or card[1] == "Queen" or card[1] == "Jack" or card[1] == "10": 
				score += 10
			elif card[1] == "Ace":
				score += 11
				numbers_A += 1
			else:
				score += int(card[1])

		if score <= 21:
			return score
		else:
			for i in range(numbers_A):
				score -= 10
				if score <= 21:
					return score
			return "Bust"
