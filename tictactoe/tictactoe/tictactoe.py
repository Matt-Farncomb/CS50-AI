"""
Tic Tac Toe Player
"""

import math
import copy

from typing import Tuple, List, Union, Optional
from tools import InvalidActionError
from operator import itemgetter

X = "X"
O = "O"
EMPTY = None

Action = Tuple[int, int]
Player = str


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

# NOTE: Assume all functions that accept 'board' as input have a valid board, meaning...
# it contains a list of three rows containing x, o or EMPTY   
# DONT modify function arguments

# args: board state
# returns: if it is x's or o's turn (x gets the first turn, then it alternates)
def player(board):
    """
    Returns player who has the next turn on a board.

    ME: Counts how many Xs and Os there are. If more Xs, it is Os turn
        Else if less or equal Xs, it is Xs turn becaus ehe goes first and should therefore...
        have more or equal.
    """
    # if is x's turn, turn is now o's turn.
    # else is x's turn

    
    player = X

    xCount = 0
    oCount = 0

    for row in board:
        for col in row:
            if col is X:
                xCount += 1
            elif col is O:
                oCount += 1
    
    if  xCount > oCount:
        player = O
    return player

# args: board state used to determine which actions can be taken
# returns: a set of all possible actions than can be taken on the provided board
# actions are a tuple of coords for the possible move e.g:
# Action = Tuple[int, int]  - ints range from 0 - 2
def actions(board) -> List[Action]:
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    # for each box in board grid:
    #   # if box unoccupied:
    #       # add box to list of boxes
    # return box list

    actions: List[Action] = []

    for row in range(3):
        for col in range(3):
            if board[row][col] is EMPTY:
                action:Action = (row, col)
                actions.append(action)
    return actions


    # for row in board:
    #     for col in row:
    #         if col is EMPTY:
    #             col_number:int = row.index(col)
    #             row_number:int = board.index(row)
    #             action:Action = (row_number, col_number)
    #             actions.append(action)
    # return actions


# args: board - contains the player's turn and the board map
#       action - a tuple of coords for the next move
def result(board, action:Action) -> List[List[Optional[Player]]]:
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy.deepcopy(board)
    row = action[0]
    col = action[1]
    for x in range(3):
        if row == x:
            for y in range(3):
                if col == y:
                    current_player = player(board)
                    if new_board[row][col] is EMPTY:
                        new_board[row][col] = current_player
                    # else:
                    #     print(new_board)
                    #     raise InvalidActionError(action)
    
    return new_board
    # if action is invalid, eg: move is impossible, raise an exception.
    # make a "deep cpy" of the board, don't change the original.
    #       # this is because the algorithm needs to consider many board states that will be different from eqch other.
    #       # this therefore it may  require many deep copies each time it runs (if it is recursively called)


# returns x if x wins, o if o wins, else no winner return None
def winner(board) -> Optional[Player]:
    """
    Returns the winner of the game, if there is one.
    """
    # assume it is impossible to have more than one winner
    # player wins if their pieces are 3 in a row horizontally, verticalls or diagonally.
    def check_three_in_row(row: List[Optional[Player]]) -> Optional[Player]:
        first_square: Optional[Player] = row[0]
        for square in row:
            if square is not first_square:
                return None
        return first_square

    win = False

    for x in range(3):
        # check horizontal
        row = [board[x][0], board[x][1], board[x][2]]
        winning_player = check_three_in_row(row)
        if winning_player:
            #print(" win row")
            return  winning_player
        else: 
            # check vertical
            column = [board[0][x], board[1][x], board[2][x]]
            winning_player = check_three_in_row(column)
            if winning_player:
                #print(" win down")
                return winning_player
            else:
                # check diagonal
                if x == 0:
                    diag = [board[x][0], board[x+1][1], board[x+2][2]]
                elif x == 2:
                    diag = [board[x][0], board[x-1][1], board[x-2][2]]
                
                winning_player = check_three_in_row(diag)
                if winning_player:
                    #print(" win diag")
                    return winning_player
    return None


def terminal(board: List[List[Optional[Player]]]) -> bool:

    """
    Returns True if game is over, False otherwise.
    """

    # retuns true if game finished, regardless if winner or not
    # returns false if there are still actions available to make.

    if winner(board) is not None:
        #print(f"winner found: {winner(board)} ")
        return True
    else:
        actions_remaining = len(actions(board))
        # print(actions_remaining)
        # return (game_finished := actions_remaining == 0)
        return actions_remaining == 0
     

    




def utility(board) -> int:
    # assume utility will only be called if terminal(board) is true, meaning utility is only called when the game has ended.
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    # utility = 0
    game_winner = winner(board)

    # if winner == X:
    #     utility = 1
    # elif winner == O:
    #     utility = -1
    
    return -1 if game_winner is O else (1 if game_winner is X else 0)

    # return utility
    
def minimax(board) -> Optional[Action]:

    def func(board):
        remaining_actions = actions(board)
        scores = []

        for action in remaining_actions:
            resulting_board = result(board, action)
            # return the winning move
            # if no winning move, must be only one action left
            if terminal(resulting_board):
                score = utility(resulting_board)
                # if last action is a tie end of game movie
                if len(remaining_actions) == 1 and score == 0:
                    return score
                # else don't care who the player is because a player cant ,ake a losing move
                elif score != 0:
                    return score
            else:     
                score = func(resulting_board)
                scores.append(score)

        desc = True if player(board) == X else False
        # sort list of tuples
        
        sorted_scores = sorted(scores, reverse=desc)
        return sorted_scores[0]

    ####################################

    remaining_actions = actions(board)
    scores = []
    current_player = player(board)

    for action in remaining_actions:
            resulting_board = result(board, action)
            # return the winning move
            # if no winning move, must be only one action left
            if terminal(resulting_board):
                score = utility(resulting_board)
                # if last action is a tie end of game movie
                if (len(remaining_actions) == 1 and score == 0) or score != 0:
                    # return action
                    scores.append( (score, action) )
                # else don't care who the player is because a player cant ,ake a losing move
                # elif score != 0:
                #     # return action
                #     scores.append( (score, action) )
            else:     
                score = (func(resulting_board), action)
                scores.append(score)
    
    desc = True if current_player == X else False
    # sort list of tuples
        
    sorted_scores = sorted(scores, key=lambda x: x[0], reverse=desc)
    print(sorted_scores)
    return sorted_scores[0][1]
        
    













        






