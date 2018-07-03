'''
Player class
contains two property: name and wallet
'''

class Player:

	def __init__(self, name="Anonimous", wallet=1):
		self.name = name
		self.wallet = wallet

	def __str__(self):
		return f"Player: {self.name} - Wallet: {self.wallet}"