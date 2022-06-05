"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def main():
    board = (initial_state())
    test = result(initial_state(), (0,0))
    
    print(test)

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]



def player(board):
    X_count = 0
    O_count = 0
    for line in board:
        for cell in line:
            if cell == X:
                X_count += 1
            if cell == O:
                O_count += 1
    if X_count <= O_count:
        return(X)
    else:
        return(O)



def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    i = 0
    for line in board:
        j = 0
        for cell in line:
            if cell == EMPTY:
                actions.add((i,j))
            j += 1
        i += 1
    
    return(actions)

    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    current_player = player(board)
    board[action[0]][action[1]] = current_player
    return(board)
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    line_X = 0
    line_O = 0
    col_X = [0, 0, 0]
    col_O = [0, 0, 0]

    i = 0
    for line in board:
        j = 0
        for cell in line:
            if cell == X:
                line_X += 1
                col_X[j] += 1
            if cell == O:
                line_O += 1
                col_O[j] += 1
            j += 1
        if line_X == 3:
            return(X)
        if line_O == 3:
            return(O)
        i += 1
        line_X = 0
        line_O = 0
    
    if 3 in col_X:
        return(X)
    if 3 in col_O:
        return(O)

    diagonals = [[(0,0),(1,1),(2,2)],[(2,0), (1,1), (0,2)]]
    # check diagonals

    middle = board[1][1]
    if middle != EMPTY:
        if board[0][0] == middle and board[2][2] == middle:
            return(middle)
        if board[0][2] == middle and board[2][0] == middle:
            return(middle)
            
    return(None)
    raise NotImplementedError


def terminal(board):
    empty_cells = 0
    
    for line in board:
        for cell in line:
            if cell == EMPTY:
                empty_cells += 1
    if empty_cells == 0:
        return(True)
    
    if winner(board) != None:
        return(True)

    return(False)
    
    raise NotImplementedError


def utility(board):
    winner = winner(board)
    if winner == X:
        return(1)
    if winner == O:
        return(-1)

    return(0)
    raise NotImplementedError


def minimax(board):
    current_player = player(board)

    while 
    
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError

main()