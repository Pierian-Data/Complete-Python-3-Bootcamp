from module.deck import Deck
from module.player import Player
from module.hand import Hand

#First Step -> Starts by fixing all the player
'''
@return players: list of all players
'''
def setupPlayers():
	players = []
	number_players = int(input("Insert number of players: "))
	for i in range(number_players):
		name = input("Insert name: ")
		wallet = int(input("Inset amount of money available: "))

		player = Player(name, wallet)
		players.append(player)

	return players

#Second Step -> manage the manche of each player
'''
@return score: return the score of the single player
'''
def match(player, deck, total_bet):
	deck.shuffle()
	
	hand = Hand()
	hand.cards.append(deck.hit())			
	hand.cards.append(deck.hit())			
	
	player.wallet -= 5
	total_bet += 5

	while True:
		print(f"Your current Hand:\n{hand}")
		
		if hand.getscore() == "Bust":
			return -1
		
		print("Menu: \n   1- New Card \n   2- Add New Bet \n   3- Stay")
		choise = int(input("Your choise: "))
		if choise == 1:
			hand.cards.append(deck.hit())
		elif choise == 2:
			bet = int(input("Amount of bet: "))
			if bet > player.wallet:
				print(player)
				print(f"Your wallet contains {player.wallet}$")
			else:
				player.wallet -= bet
				total_bet += bet
		else:
			return hand.getscore()

def findWinner(matchs):
	winner, max_score = matchs.pop()
	for player, score in matchs:
		if score > max_score:
			max_score = score
			winner = player
	return (winner, max_score)

def setupNextMatch(players):
	#check who, for willing and availabilty can continue to play
	for player in players:
		print(player)
		if player.wallet < 5:
			print(f"{player.name} you have not enough money. Bye!")
			players.remove(player)
		else:
			print("Insert 1 for continue the match")
			print("Insert 2 for leave")
			choise = int(input("choise: "))
			if choise == 2:
				print(f"{player.name} Bye!")
				players.remove(player)	

def main():
	# STEP 1 -> SETUP player and Deck
	players = setupPlayers()
	deck = Deck()
	
	# STEP 2 -> MANCHE MANAGING
	while len(players) > 0:
		#Environment for the current match
		currentMatch = [] #it contains all the pairs (player, score)
		total_bet = 0 #it contains the amount of all the bet

		print("****** Currently on match are: ******")
		for player in players:
			print(player)
		print("*************************************")

		
		for player in players:
			print(f"It's the {player.name} turn")
			score = match(player, deck, total_bet)
			currentMatch.append((player, score))
		
		winner, score = findWinner(currentMatch)
		print(f"{player} :{score}")
		input()
		winner.wallet += total_bet

	# STEP 3 -> Check who rest or leave
	setupNextMatch(players)

if __name__ == "__main__":
	main()
