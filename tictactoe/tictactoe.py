"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


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
    newboard = deepcopy(board)
    newboard[action[0]][action[1]] = current_player
    return(newboard)
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
    local_winner = winner(board)
    if local_winner == X:
        return(1)
    if local_winner == O:
        return(-1)

    return(0)
    raise NotImplementedError


def minimax(board):
    current_player = player(board)

    def max_value(state):
        v = -999
        if terminal(state):
            return utility(state)
        for action in actions(state):
            v = max(v, min_value(result(state, action)))
        return v

    def min_value(state):
        v = 999
        if terminal(state):
            return utility(state)
        for action in actions(state):
            v = min(v, max_value(result(state,action)))
        return v
    
    possible_actions = []

    if current_player == X:
        for action in actions(board):
            action_value = min_value(result(board, action))
            if action_value == 1:
                return action
            elif action_value == 0:
                possible_actions.append(action)
        return possible_actions[0]
    if current_player == O:
        for action in actions(board):
            action_value = max_value(result(board, action))
            if action_value == -1:
                return action
            elif action_value == 0:
                possible_actions.append(action)
        return possible_actions[0]
