#!/usr/bin/env python
# nrooks.py : Solve the N-Rooks problem!
# D. Crandall, 2016
# Updated by Zehua Zhang, 2017
# Modified by Roja Raman, 2018
#
# The N-rooks problem is: Given an empty NxN chessboard, place N rooks on the board so that no rooks
# can take any other, i.e. such that no two rooks share the same row or column.

import sys
from timeit import default_timer as timer

# Count # of pieces in given row
def count_on_row(board, row):
    return sum( board[row] ) 

# Count # of pieces in given column
def count_on_col(board, col):
    return sum( [ row[col] for row in board ] ) 

# Count total # of pieces on board
def count_pieces(board):
    return sum([ sum(row) for row in board ] )

# Return a string with the board rendered in a human-friendly format
def printable_board(board):
    return "\n".join([ " ".join([ "R" if col else "_" for col in row ]) for row in board])

# Add a piece to the board at the given position, and return a new board (doesn't change original)
def add_piece(board, row, col):
    return board[0:row] + [board[row][0:col] + [1,] + board[row][col+1:]] + board[row+1:]

# Get list of successors of given board state
# Modified by Roja Raman
def successors(board):
    #print("S: ",board)
    temp_board = []
    for r in range(0, N):
        for c in range(0,N):
            temp = add_piece(board, r, c)
            if temp != board:                           
                temp_board.append(temp)
    #return [ add_piece(board, r, c) for r in range(0, N) for c in range(0,N) ]
    #print(l)
    return temp_board

# Get list of successors of given board state such that it is not conflicting with 
# other rooks i.e. utmost one rook in a row or a column and at any point of time, 
# total number of rooks is less than or equal to N - Successor2
def successors2(board):
    succ = []
    for r in range(0,N):
        #To check number of rooks in a row is exactly 1
        if count_on_row(board,r) == 1:
           continue
        for c in range(0,N):
            #To check number of rooks in a column is exactly 1
            if count_on_col(board,c)== 1:
                continue
            temp_board = add_piece(board,r,c)
            succ.append(temp_board)
          
    return succ

def successors3(board):
    succ = []
    visited =  False
    for r in range(0,N):
        #To check number of rooks in a row is exactly 1
        if count_on_row(board,r) == 1:
           continue
        for c in range(0,N):
            #To check number of rooks in a cclumn is exactly 1
            if count_on_col(board,c)== 1:
                continue
            temp_board = add_piece(board,r,c)
            if count_pieces(temp_board) <= N:
                if temp_board != board:
                   succ.append(temp_board)
            visited = True
        if visited:
            break
    return succ

# check if board is a goal state
def is_goal(board):
    return count_pieces(board) == N and \
        all( [ count_on_row(board, r) <= 1 for r in range(0, N) ] ) and \
        all( [ count_on_col(board, c) <= 1 for c in range(0, N) ] )

# Solve n-rooks!
def solve(initial_board):
    fringe = [initial_board]
    while len(fringe) > 0:
        for s in successors3( fringe.pop() ):
            if is_goal(s):
                return(s)
            fringe.append(s)
    return False

# Solve n-rooks using BFS
def solveBFS(initial_board):
    fringe = [initial_board]
    while len(fringe) > 0:
        fringeLen = len(fringe)
        for s in successors3(fringe.pop(fringeLen - 1)):
            if is_goal(s):
                return (s)
            fringe.append(s)
    return False
# This is N, the size of the board. It is passed through command line arguments.
N = int(sys.argv[1])

# The board is stored as a list-of-lists. Each inner list is a row of the board.
# A zero in a given square indicates no piece, and a 1 indicates a piece.
initial_board = [[0]*N]*N
print ("Starting from initial board:\n" + printable_board(initial_board) + "\n\nLooking for solution...\n")
start = timer()
solution = solve(initial_board)
end = timer()
print (printable_board(solution) if solution else "Sorry, no solution found. :(")
print("Time Taken : ",end - start)


