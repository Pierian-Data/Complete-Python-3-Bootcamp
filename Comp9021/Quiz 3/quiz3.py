direction_vertical = 'VERTICAL'
direction_horizontal = 'HORIZONTAL'
paintBlack = '\N{black large square}'
paintWhite = '\N{white large square}'
toothpickHalfLen =2
centerPosition = (0, 0)
freeTips_tracker = {centerPosition: direction_vertical}
historical_removed_Tips_tracker = dict()


def tooth_picks(stage, top_left_corner, bottom_right_corner):
    board = initializeBoard(top_left_corner, bottom_right_corner)
    addToothspicksToBoard(stage, board)
    printBoard(board, top_left_corner, bottom_right_corner)


def initializeBoard(top_left_corner, bottom_right_corner):
    initialBoard = generateBoard(top_left_corner, bottom_right_corner)
    addingToothpick(initialBoard, centerPosition, direction_vertical)
    return initialBoard


def addToothspicksToBoard(stage, m1):
    while stage:
        progressStage(m1)
        stage -= 1


def generateBoard(top_left_corner, bottom_right_corner):
    x_l, y_t = top_left_corner
    x_r, y_b = bottom_right_corner
    board_coordinates = dict()

    for y in range(y_t, y_b-1, -1):
        for x in range(x_l, x_r+1, 1):
            board_coordinates[(x, y)] = paintWhite
    return board_coordinates


def printBoard(board, top_left_corner, bottom_right_corner):
    if board:
        x_l, y_t = top_left_corner
        x_r, y_b = bottom_right_corner
        lenOfLine = x_r - x_l + 1
        lineContent = str()
        count = lenOfLine
        lineContent = constructLine(board, lenOfLine, lineContent, count)
        print(lineContent)

def constructLine(board, lenOfLine, lineContent, count):
    for coordinate in board:
        if count:
            lineContent += board[coordinate]
            count -= 1
        elif count == 0:
            print(lineContent)
            count = lenOfLine-1
            lineContent = board[coordinate]
    return lineContent


def addingToothpick(board, coordinate, direction):
    x, y = coordinate

    if toothspickFits(board, direction, x, y):
        if toothpickShouldPaintVertically(direction):
            paintToothspickVertically(board, x, y)
        else:
            paintToothspickHorizontally(board, x, y)

def toothpickShouldPaintVertically(direction):
    return direction == direction_vertical


def paintToothspickHorizontally(board, x, y):
    for w in range(x-toothpickHalfLen, x+toothpickHalfLen+1, 1):
        board[(w, y)] = paintBlack


def paintToothspickVertically(board, x, y):
    for h in range(y-toothpickHalfLen, y+toothpickHalfLen+1, 1):
        board[(x, h)] = paintBlack


def toothspickFits(Matrix, direction, x, y):
    toothPickFitsTheboard = True
    if direction == direction_vertical:
        for h in range(y-toothpickHalfLen, y+toothpickHalfLen+1, 1):
            if (x, h) not in Matrix:
                toothPickFitsTheboard = False
    else:
        for w in range(x-toothpickHalfLen, x+toothpickHalfLen+1, 1):
            if (w, y) not in Matrix:
                toothPickFitsTheboard = False
    return toothPickFitsTheboard


def progressStage(board):

    for tip in dict(freeTips_tracker):
        x, y = tip

        if freeTipFacingUpOrDown(tip):
            removeFromFreeTips_tracker(tip)
            processCandiate((x-toothpickHalfLen, y),direction_vertical)
            processCandiate((x+toothpickHalfLen, y),direction_vertical)

        else:
            removeFromFreeTips_tracker(tip)
            processCandiate((x, y-toothpickHalfLen),direction_horizontal)
            processCandiate((x, y+toothpickHalfLen),direction_horizontal)

    addToothspicksForFreeTips(board)

def freeTipFacingUpOrDown(tip):
    return freeTips_tracker[tip] == direction_horizontal

def processCandiate(FreeTip_candiate_1,direction):
    if FreeTip_candiate_1 in freeTips_tracker:
        removeFromFreeTips_tracker(FreeTip_candiate_1)
    elif FreeTip_candiate_1 not in historical_removed_Tips_tracker:
        freeTips_tracker[FreeTip_candiate_1] = direction

def removeFromFreeTips_tracker(tip):
    historical_removed_Tips_tracker[tip] = freeTips_tracker[tip]
    freeTips_tracker.pop(tip)


def addToothspicksForFreeTips(board):
    for tip in freeTips_tracker:
        addingToothpick(board, tip, freeTips_tracker[tip])
