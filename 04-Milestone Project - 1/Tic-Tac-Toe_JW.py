
###Creating Global Parameter Values###
game_board = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
player_one_symbol = ''
player_two_symbol = ''
turn_number = 1
player_one_positions = []
player_two_positions = []
winning_combinations = [[1,2,3],[4,5,6],[7,8,9],[1,4,7],[2,5,8],[3,6,9],[1,5,9],[3,5,7]]
victory_text = ''
player1_victory = False
player2_victory = True

###Creating a function to print the Game Board###
def game_intro():
    '''Creating a funciton to present the intro to the game'''
    global game_board
    global player_one_symbol
    global turn_number
    global player_one_positions
    global player_two_positions
    global victory_text
    global player1_victory
    global player2_victory
    game_board = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
    player_one_symbol = ''
    player_two_symbol = ''
    turn_number = 1
    player_one_positions = []
    player_two_positions = []
    victory_text = ''
    player1_victory = False
    player2_victory = True
    print ('Welcome to Tic-Tac-Toe!')
    print('Player 1: Choose X or O')

###Creating a function to print the Game Board###
def pick_letter():
    global player_one_symbol
    global player_two_symbol
    select_letter = input()
    if select_letter == 'end game':
        print('Okay maybe another time. Have a great day!')
        
    elif select_letter.upper() == 'X':
        player_one_symbol = 'X'
        player_two_symbol = 'O'    
    elif select_letter.upper() == 'O':
        player_one_symbol = 'O'
        player_two_symbol = 'X'
    else:
        print ('Whoops! Player1: Choose X or O')
        pick_letter()
    print('Great! Player One chose "{}"'.format(player_one_symbol))
    print('Let\'s get Started!')
    

###Creating a function to print the Game Board###
def print_game_board():
    
    ### Creating the Game Board Values ###

    game_board_heading = '----GAME BOARD----'
    top_row_game = '  {}  |  {}  |  {} '.format(game_board[6], game_board[7], game_board[8])
    mid_row_game = '  {}  |  {}  |  {} '.format(game_board[3], game_board[4], game_board[5])
    bot_row_game = '  {}  |  {}  |  {} '.format(game_board[0], game_board[1], game_board[2])
    
    ### Creating horizontal and vertical bars for rows without values###
    dashes = '_____|_____|_____'
    pipes = ' '*5 + '|' + ' '*5 + '|' + ' '*5
    blank_row = ''

    ### Creating the Position Key Board Vaules###
    key_heading = '   POSITION KEY'
    position_key = ['1','2','3','4','5','6','7','8','9']
    top_row_key = '  {}  |  {}  |  {} '.format(position_key[6], position_key[7], position_key[8])
    mid_row_key = '  {}  |  {}  |  {} '.format(position_key[3], position_key[4], position_key[5])
    bot_row_key = '  {}  |  {}  |  {} '.format(position_key[0], position_key[1], position_key[2])
    
    print(game_board_heading + '\t'*2 + key_heading) 
    print(blank_row)
    print(pipes + '\t'*2 + pipes)
    print(top_row_game + '\t'*2 + top_row_key)
    print(dashes + '\t'*2 + dashes)
    print(pipes + '\t'*2 + pipes)
    print(mid_row_game + '\t'*2 + mid_row_key)
    print(dashes + '\t'*2 + dashes)
    print(pipes + '\t'*2 + pipes)
    print(bot_row_game + '\t'*2 + bot_row_key)
    print(pipes + '\t'*2 + pipes)
    print(blank_row)

###Fuction to print the rules to the game###
def game_rules():
    print('On your turn place your letter in a spot by typing the corresponding value in the Position Key')
    print('First one to get three-in-a-row Wins!')

###Function to check if a player has won the game###
def victory_check():
    global victory_text
    global player1_victory
    global player2_victory
    player1_victory = ((game_board[6] == player_one_symbol and game_board[7] == player_one_symbol and game_board[8] == player_one_symbol) or # across the top
        (game_board[3] == player_one_symbol and game_board[4] == player_one_symbol and game_board[5] == player_one_symbol) or # across the middle
        (game_board[0] == player_one_symbol and game_board[1] == player_one_symbol and game_board[2] == player_one_symbol) or # across the bottom
        (game_board[6] == player_one_symbol and game_board[3] == player_one_symbol and game_board[0] == player_one_symbol) or # down the middle
        (game_board[7] == player_one_symbol and game_board[4] == player_one_symbol and game_board[1] == player_one_symbol) or # down the middle
        (game_board[8] == player_one_symbol and game_board[5] == player_one_symbol and game_board[2] == player_one_symbol) or # down the right side
        (game_board[6] == player_one_symbol and game_board[4] == player_one_symbol and game_board[2] == player_one_symbol) or # diagonal
        (game_board[8] == player_one_symbol and game_board[4] == player_one_symbol and game_board[0] == player_one_symbol)) # diagonal
    
    
    
    player2_victory = ((game_board[6] == player_two_symbol and game_board[7] == player_two_symbol and game_board[8] == player_two_symbol) or # across the top
        (game_board[3] == player_two_symbol and game_board[4] == player_two_symbol and game_board[5] == player_two_symbol) or # across the middle
        (game_board[0] == player_two_symbol and game_board[1] == player_two_symbol and game_board[2] == player_two_symbol) or # across the bottom
        (game_board[6] == player_two_symbol and game_board[3] == player_two_symbol and game_board[0] == player_two_symbol) or # down the middle
        (game_board[7] == player_two_symbol and game_board[4] == player_two_symbol and game_board[1] == player_two_symbol) or # down the middle
        (game_board[8] == player_two_symbol and game_board[5] == player_two_symbol and game_board[2] == player_two_symbol) or # down the right side
        (game_board[6] == player_two_symbol and game_board[4] == player_two_symbol and game_board[2] == player_two_symbol) or # diagonal
        (game_board[8] == player_two_symbol and game_board[4] == player_two_symbol and game_board[0] == player_two_symbol)) # diagonal
    
    if player1_victory == True:
         victory_text = 'Player 1 Wins!'
         print (victory_text)

    elif player2_victory == True:
        victory_text = 'Player 2 Wins!'
        print (victory_text)
    

def final_victory_check():
    global victory_text
    global player1_victory
    global player2_victory
    player1_victory = ((game_board[6] == player_one_symbol and game_board[7] == player_one_symbol and game_board[8] == player_one_symbol) or # across the top
        (game_board[3] == player_one_symbol and game_board[4] == player_one_symbol and game_board[5] == player_one_symbol) or # across the middle
        (game_board[0] == player_one_symbol and game_board[1] == player_one_symbol and game_board[2] == player_one_symbol) or # across the bottom
        (game_board[6] == player_one_symbol and game_board[3] == player_one_symbol and game_board[0] == player_one_symbol) or # down the middle
        (game_board[7] == player_one_symbol and game_board[4] == player_one_symbol and game_board[1] == player_one_symbol) or # down the middle
        (game_board[8] == player_one_symbol and game_board[5] == player_one_symbol and game_board[2] == player_one_symbol) or # down the right side
        (game_board[6] == player_one_symbol and game_board[4] == player_one_symbol and game_board[2] == player_one_symbol) or # diagonal
        (game_board[8] == player_one_symbol and game_board[4] == player_one_symbol and game_board[0] == player_one_symbol)) # diagonal
    
    
    
    player2_victory = ((game_board[6] == player_two_symbol and game_board[7] == player_two_symbol and game_board[8] == player_two_symbol) or # across the top
        (game_board[3] == player_two_symbol and game_board[4] == player_two_symbol and game_board[5] == player_two_symbol) or # across the middle
        (game_board[0] == player_two_symbol and game_board[1] == player_two_symbol and game_board[2] == player_two_symbol) or # across the bottom
        (game_board[6] == player_two_symbol and game_board[3] == player_two_symbol and game_board[0] == player_two_symbol) or # down the middle
        (game_board[7] == player_two_symbol and game_board[4] == player_two_symbol and game_board[1] == player_two_symbol) or # down the middle
        (game_board[8] == player_two_symbol and game_board[5] == player_two_symbol and game_board[2] == player_two_symbol) or # down the right side
        (game_board[6] == player_two_symbol and game_board[4] == player_two_symbol and game_board[2] == player_two_symbol) or # diagonal
        (game_board[8] == player_two_symbol and game_board[4] == player_two_symbol and game_board[0] == player_two_symbol)) # diagonal
    
    if player1_victory == True:
         victory_text = 'Player 1 Wins!'
         print (victory_text)

    elif player2_victory == True:
        victory_text = 'Player 2 Wins!'
        print (victory_text)

    elif turn_number == 10 and player1_victory == False and player2_victory == False:
        victory_text = 'Ope, looks like the cat got this game.'
        print (victory_text)

###Determining what happens during Player 1's turn###
def player1_turn():
    global player_one_symbol
    print('Player 1: It\'s your turn\nPick a space between 1 and 9 that hasn\'t already been taken')
    print_game_board()
    player1_input = input()
    if not player1_input.isdigit():
        print('Value is not a number \nPlease input a number between 1 and 9 that isn\'t already taken')
        player1_turn()
    elif int(player1_input) <=0 or int(player1_input) > 9:
        print('Value is out of range \nPlease input a number between 1 and 9 that isn\'t already taken')
        player1_turn()
    elif game_board[int(player1_input)-1] != ' ':
        print('Too Bad, this spot is already taken. \nPick a number between 1 and 9 that isn\'t already taken')
        player1_turn()
    else:
        game_board[int(player1_input)-1] = player_one_symbol
        player_one_positions.append(int(player1_input))

###Determining what happens during Player 2's turn###
def player2_turn():
    global player_two_symbol
    print('Player 2: It\'s your turn\nPick a space between 1 and 9 that hasn\'t already been taken')
    print_game_board()
    player2_input = input()
    if not player2_input.isdigit():
        print('Value is not a number \nPlease input a number between 1 and 9 that isn\'t already taken')
        player2_turn()
    elif int(player2_input) <=0 or int(player2_input) > 9:
        print('Value is out of range \nPlease input a number between 1 and 9 that isn\'t already taken')
        player2_turn()
    elif game_board[int(player2_input)-1] != ' ':
        print('Too Bad, this spot is already taken. \nPick a number between 1 and 9 that isn\'t already taken')
        player2_turn()
    else:
        game_board[int(player2_input)-1] = player_two_symbol
        player_two_positions.append(int(player2_input))
        

###Adding the gameplay function ###
def gameplay():
    game_rules()
    global player_one_symbol
    global game_board
    global turn_number
    global player1_victory
    global player2_victory
    while True:

        if turn_number == 10:
            player2_turn
            break

        elif (turn_number % 2) == 1:
            player1_turn()
            victory_check()
            if player1_victory == True:
                break   
            turn_number += 1
            
        elif (turn_number % 2) == 0: 
            player2_turn()
            victory_check()
            if player2_victory == True:
                break   
            turn_number += 1
    
        else:
            print('error')
        
    print_game_board()

    final_victory_check()


    
###Function to ask if the user wants to play again###
def play_again():
    print('Would you like to play again?\nAnswer Yes or No')
    play_again_input = input()
    if play_again_input.upper() == 'NO':
        print('Thanks for playing, goodbye')
    elif play_again_input.upper() == 'YES':
        play_the_game()
    else:
        print('Sorry I couldn\'t understand that. \nDo you want to play again?\nAnswer Yes or No')
        play_again() 


###Grouping all gameplay into one fuction###
def play_the_game():
    game_intro()       
    pick_letter()
    gameplay()
    play_again()

play_the_game()