direction_vertical = 'VERTICAL'
direction_horizontal = 'HORIZONTAL'
paintBlack = '\N{black large square}'
paintWhite = '\N{white large square}'
toothpickHalfLen = 2
centerPosition = (0, 0)
freeTips_tracker = {centerPosition: direction_vertical}
historical_removed_Tips_tracker = dict()


def tooth_picks(stage, top_left_corner, bottom_right_corner):
    board = initializeBoard(top_left_corner, bottom_right_corner)
    addMultipleRoundsOfToothspicksToBoard(stage, board)
    printBoard(board, top_left_corner, bottom_right_corner)


def initializeBoard(top_left_corner, bottom_right_corner):
    initialBoard = generateBoard(top_left_corner, bottom_right_corner)
    addingToothpick(initialBoard, centerPosition, direction_vertical)
    return initialBoard


def addMultipleRoundsOfToothspicksToBoard(stage, board):
    while stage:
        addToothpicksForCurrentRound(board)
        stage -= 1


def generateBoard(top_left_corner, bottom_right_corner):
    (a, b) = top_left_corner
    (c, d) = bottom_right_corner
    board_coordinates = dict()

    for y in range(b, d-1, -1):
        for x in range(a, c+1, 1):
            board_coordinates[(x, y)] = paintWhite
    return board_coordinates


def printBoard(board, top_left_corner, bottom_right_corner):
    if board:
        (a, b) = top_left_corner
        (c, d) = bottom_right_corner
        lenOfLine = c - a + 1
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
    (x, y) = coordinate

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


def addToothpicksForCurrentRound(board):

    for tip in dict(freeTips_tracker):
        (x, y) = tip

        if freeTipFacingUpOrDown(tip):
            removeFreeTipFromTrackerAndMarkTheTip(tip)
            processNewFreeTipCandiate(
                (x-toothpickHalfLen, y), direction_vertical)
            processNewFreeTipCandiate(
                (x+toothpickHalfLen, y), direction_vertical)

        else:
            removeFreeTipFromTrackerAndMarkTheTip(tip)
            processNewFreeTipCandiate(
                (x, y-toothpickHalfLen), direction_horizontal)
            processNewFreeTipCandiate(
                (x, y+toothpickHalfLen), direction_horizontal)

    addToothspicksForFreeTips(board)


def freeTipFacingUpOrDown(tip):
    return freeTips_tracker[tip] == direction_horizontal


def processNewFreeTipCandiate(FreeTip_candiate, direction):
    if FreeTip_candiate in freeTips_tracker:
        removeFreeTipFromTrackerAndMarkTheTip(FreeTip_candiate)
    elif FreeTip_candiate in historical_removed_Tips_tracker:
        return
    else:
        freeTips_tracker[FreeTip_candiate] = direction


def removeFreeTipFromTrackerAndMarkTheTip(tip):
    historical_removed_Tips_tracker[tip] = freeTips_tracker[tip]
    freeTips_tracker.pop(tip)


def addToothspicksForFreeTips(board):
    for tip in freeTips_tracker:
        addingToothpick(board, tip, freeTips_tracker[tip])
