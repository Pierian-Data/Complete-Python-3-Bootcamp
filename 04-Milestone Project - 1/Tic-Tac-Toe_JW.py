
###Creating Global Parameter Values###
game_board = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
player_one = ''
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
    select_letter = input()
    if select_letter == 'end game':
        print('Okay maybe another time. Have a great day!')
        
    elif select_letter.upper() == 'X':
        player_one = 'X'
            
    elif select_letter.upper() == 'O':
        player_one = 'O'

    else:
        print ('Whoops! Player1: Choose X or O')
        pick_letter()
    print('Great! Player One chose "{}"'.format(player_one))
    print('Let\'s get Started!')
    game_rules()
    

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

###Determining what happens during X's turn###
def x_turn():
    print_board()
    x_input = input()
    if x_input == 'end game':
        print('Thanks for playing, goodbye')
    elif not x_input.isdigit():
        print('Value is not a number \nPlease input a number between 1 and 9 that isn\'t already taken')
        x_turn()
    elif int(x_input) <=0 or int(x_input) > 9:
        print('Value is out of range \nPlease input a number between 1 and 9 that isn\'t already taken')
        x_turn()
    elif game_board[int(x_input)-1] != ' ':
        print('Too Bad, this spot is already taken. \nPick a number between 1 and 9 that isn\'t already taken')
        x_turn()
    else:
        game_board[int(x_input)-1] = 'X'
        end_of_turn()

###Determining what happens during O's turn###
def o_turn():
    print_board()
    o_input = input()
    if o_input == 'end game':
        print('Thanks for playing, goodbye')
    elif not o_input.isdigit():
        print('Value is not a number \nPlease input a number between 1 and 9 that isn\'t already taken')
        o_turn()
    elif int(o_input) <=0 or int(o_input) > 9:
        print('Value is out of range \nPlease input a number between 1 and 9 that isn\'t already taken')
        o_turn()
    elif game_board[int(o_input)-1] != ' ':
        print('Too Bad, this spot is already taken. \nPick a number between 1 and 9 that isn\'t already taken')
        o_turn()
    else:
        game_board[int(o_input)-1] = 'O'
        

###Adding Rules for the End of Each Turn###
def gameplay():
    global player_one
    global game_board
    global turn_number
    if player_one == 'X':
        odd_turn = x_turn()
        even_turn = o_turn()
    else:
        odd_turn = o_turn()
        even_turn = x_turn()
    
    while turn_number <= 9:
        
        if turn_number % 2 == 1:
            print('Player 1: It\'s your turn\nPick a space between 1 and 9 that hasn\'t already been taken')
            odd_turn
            turn_number += 1
            
        else: 
            turn_number % 2 == 0
            print('Player 2: It\'s your turn\nPick a space between 1 and 9 that hasn\'t already been taken')
            even_turn
            turn_number += 1
            

    if 1==0:
        print('winner')

    else:
        print('Ope, the Cat got this game')

    
    
    


    

game_intro()       
pick_letter()
gameplay()