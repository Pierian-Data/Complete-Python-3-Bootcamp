
###Creating Global Parameter Values###
game_board = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
player_one = ''
player_two = ''
turn_number = 1

###Creating a function to print the Game Board###
def game_intro():
    '''Creating a funciton to present the intro to the game'''
    print ('Welcome to Tic-Tac-Toe!')
    print('At any time input "end game" to shut the game down')
    print('Player 1: Choose X or O')

###Creating a function to print the Game Board###
def pick_letter():
    global player_one
    global player_two
    select_letter = input()
    if select_letter == 'end game':
        print('Okay maybe another time. Have a great day!')
        
    elif select_letter.upper() == 'X':
        player_one = 'X'
        player_two = 'O'    
    elif select_letter.upper() == 'O':
        player_one = 'O'
        player_two = 'X'
    else:
        print ('Whoops! Player1: Choose X or O')
        pick_letter()
    print('Great! Player One chose "{}"'.format(player_one))
    print('Let\'s get Started!')
    

###Creating a function to print the Game Board###
def print_board():
    
    ### Creating the Game Board Values ###

    board_heading = '----GAME BOARD----'
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
    
    print(board_heading + '\t'*2 + key_heading) 
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

def game_rules():
    print('On your turn place your letter in a spot by typing the corresponding value in the Position Key')
    print('First one to get three-in-a-row Wins!')

###Determining what happens during Player 1's turn###
def player1_turn():
    global player_one
    print('Player 1: It\'s your turn\nPick a space between 1 and 9 that hasn\'t already been taken')
    print_board()
    player1_input = input()
    if player1_input == 'end game':
        print('Thanks for playing, goodbye')
    elif not player1_input.isdigit():
        print('Value is not a number \nPlease input a number between 1 and 9 that isn\'t already taken')
        player1_turn()
    elif int(player1_input) <=0 or int(player1_input) > 9:
        print('Value is out of range \nPlease input a number between 1 and 9 that isn\'t already taken')
        player1_turn()
    elif game_board[int(player1_input)-1] != ' ':
        print('Too Bad, this spot is already taken. \nPick a number between 1 and 9 that isn\'t already taken')
        player1_turn()
    else:
        game_board[int(player1_input)-1] = player_one
        

###Determining what happens during Player 2's turn###
def player2_turn():
    global player_two
    print('Player 2: It\'s your turn\nPick a space between 1 and 9 that hasn\'t already been taken')
    print_board()
    player2_input = input()
    if player2_input == 'end game':
        print('Thanks for playing, goodbye')
    elif not player2_input.isdigit():
        print('Value is not a number \nPlease input a number between 1 and 9 that isn\'t already taken')
        player2_turn()
    elif int(player2_input) <=0 or int(player2_input) > 9:
        print('Value is out of range \nPlease input a number between 1 and 9 that isn\'t already taken')
        player2_turn()
    elif game_board[int(player2_input)-1] != ' ':
        print('Too Bad, this spot is already taken. \nPick a number between 1 and 9 that isn\'t already taken')
        player2_turn()
    else:
        game_board[int(player2_input)-1] = player_two
        

###Adding the gameplay function ###
def gameplay():
    game_rules()
    global player_one
    global game_board
    global turn_number

    while True:

        if 1==0:
            ###Enter Winning Scenario Code Here###
            pass
        elif turn_number == 10:
            player2_turn
            ##Enter Winning Scenario Code Here###
            break
        elif (turn_number % 2) == 1:
            player1_turn()
            turn_number += 1
            
        elif (turn_number % 2) == 0: 
            print('Player 2: It\'s your turn\nPick a space between 1 and 9 that hasn\'t already been taken')
            player2_turn()
            turn_number += 1
    
        else:
            print('error')
        
    print_board()

    if 1==0:
        ###Enter Winning Scneario Code Here###
        print('winner')

    else:
        print('Ope, the Cat got this game')

    
    
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


    
def play_the_game():
    game_intro()       
    pick_letter()
    gameplay()
    play_again()

play_the_game()