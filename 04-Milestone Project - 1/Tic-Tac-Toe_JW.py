
###Creating Global List for the Game Board Values###
game_board = [' ',' ',' ',' ',' ',' ',' ',' ',' ']

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
    print(blank_row)###Creating Global List for the Game Board Values###
game_board = [' ',' ',' ',' ',' ',' ',' ',' ',' ']

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

###Adding User Input to the game###
game_board[5] = 'x'
print_board()


