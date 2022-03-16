# !/user/bin/env/python

# tic tac to game with two human users
# accept and validate keyboard input
# print board after each move

board = [['1','2','3'],['4','5','6'],['7','8','9']]


def draw_board():
    global board
    row_border = '+-------+-------+-------+'
    column_border = '|       |       |       |\n'
    rows = ['|   ' + '   |   '.join(board[i]) + '   |\n' for i in range(len(board))]
    print('', row_border)
    for i in range(len(board)):
        print('', column_border, rows[i], column_border, row_border)


def get_free_fields():
    global board
    return [int(field) for row in board for field in row if field not in ['X', 'O']]


def get_user_choice(player):
    try:
        move = int(input(f'Please enter your move Player {player}:') ) # Probably need to change this
    except ValueError:
        print('Move must be an integer number')
        get_user_choice(player)

    # validate user input
    valid_moves = get_free_fields()
    while move not in valid_moves:
        print('Move must be available on the board')
        move = int(input('Please enter your move again:'))

    return move

def update_board(player, selection):
    global board
    # translate selection to coords
    row = (selection-1)//3
    if selection % 3 == 1:
        column = 0
    elif selection % 3 == 2:
        column = 1
    else:
        column = 2

    board[row][column] = player


def victory_reached():
    global board
    # rows all the same
    for row in board:
        if row[0] == row[1] and row[1] == row[2] and row[0] == row[2]:  # feel like that last and is redundant:
            return row[0]
    # columns all the same
    for column in range(3):
        if board[0][column] == board[1][column] and board [1][column] == board[2][column]:
            return board[0][column]
    # diagonals all the same
    if board[0][0] == board [1][1] and board[1][1] == board[2][2]:
        return board[1][1]
    elif board[0][2] == board [1][1] and board [1][1] == board [2][0]:
        return board[1][1]
    return 'no-one'



def play_a_round():
    global board
    players = ['O', 'X']
    for player in players:
        draw_board()
        move = get_user_choice(player)
        update_board(player, move)

        if victory_reached() in players or len(get_free_fields()) == 0:
            break
    return victory_reached()

def main():
    while len(get_free_fields())>0:
        print(get_free_fields())
        result = play_a_round()
        if result in ['X', 'O']:
            print(f'Victory for {result}')
            break
    else:
        print('Game ends in a draw')


if __name__ == '__main__':
    main()