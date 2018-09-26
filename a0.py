#!/usr/bin/env python
# nrooks.py : Solve the N-Rooks problem!
# D. Crandall, 2016
# Updated by Zehua Zhang, 2017
# Updated by Roja Raman, 2018
#
# N Queens and N Rooks Problem
# Input : program , N , Number of Unavailable states , coordinates

import sys
from timeit import default_timer as timer
import numpy

# Count # of pieces in given row
def count_on_row(board, row):
    return sum( board[row] ) 

# Count # of pieces in given column
def count_on_col(board, col):
    return sum( [ row[col] for row in board ] ) 

# Count total # of pieces on board
def count_pieces(board):
    return sum([ sum(row) for row in board ] )

#Code Reference : https://www.programcreek.com/python/example/102184/numpy.fliplr  - START
def count_diag(board, row, col):
    #Converting to array
    boardArr = numpy.asarray(board)
    #numpy.diagonal(a, offset=0, axis1=0, axis2=1)
    numpySum = sum(numpy.diagonal(boardArr, col - row, 0, 1))
    if numpySum == 0:
        boardFlip = numpy.fliplr(boardArr)
        new_col = N - 1 - col
        sumOfDiagonal = sum(numpy.diagonal(boardFlip, new_col - row, 0, 1))
        if sumOfDiagonal == 0:
            return True
    return False
# Citation END
    
# Return a string with the board rendered in a human-friendly format
def printable_board(board):
    if problem == 'nqueens':
        key = "Q"
    else:
        key = "R"
    return "\n".join([" ".join([key if col == 1 else "_" if col == 0 else "X" for col in row]) for row in board])
    #return "\n".join([ " ".join([ "R" if col else "_" for col in row ]) for row in board])

# Add a piece to the board at the given position, and return a new board (doesn't change original)
def add_piece(board, row, col):
    return board[0:row] + [board[row][0:col] + [1,] + board[row][col+1:]] + board[row+1:]


def successors4(board):
    succ = []
    for r in range(0,N):
        #To check number of rooks in a row is exactly 1
        if count_on_row(board,r) == 1:
           continue
        for c in range(0,N):
            #To check number of rooks in a column is exactly 1
            #check for blocked state if yes then place rook in the next or previous position
            if count_on_col(board,c)== 1 or all([(r == i[0]-1  and c== i[1]-1) for i in coordinates]):
                continue
            temp_board = add_piece(board,r,c)
            if count_pieces(temp_board) <= N:
                if temp_board != board:
                   succ.append(temp_board)
    return succ

#Solving nQueens!
def successors_nQueen(board):
    succnQ = []
    visited =  False
    for r in range(0,N):
        #To check number of queens in a row is exactly 1
        if count_on_row(board,r) == 1:
           continue
        for c in range(0,N):
            #To check number of rooks in a column is exactly 1
            #check for blocked state if yes then place rook in the next or previous position
            if count_on_col(board,c)== 1 : #or all([(r == i[0]-1  and c== i[1]-1) for i in coordinates]):
                continue
            temp_board = []
            if count_pieces(temp_board) <= N:
                if temp_board != board:
                    if count_diag(board, r, c):
                        temp_board = add_piece(board, r, c)
                        succnQ.append(temp_board)
            visited = True
        if visited:
            break
    return succnQ

# check if board is a goal state
def is_goal(board):
    return count_pieces(board) == N and \
        all( [ count_on_row(board, r) <= 1 for r in range(0, N) ] ) and \
        all( [ count_on_col(board, c) <= 1 for c in range(0, N) ] ) and \
        all([ board[i[0]][i[1]] == 0 for i in coordinates ])

# Solve n-rooks! - DFS
def solve(initial_board , problem):
    fringe = [initial_board]
    while len(fringe) > 0:
        if(problem == "nrooks"):
            for s in successors4( fringe.pop()):
                if is_goal(s):
                    return(s)
                fringe.append(s)
        if(problem == "nqueens"):
            for s in successors_nQueen(fringe.pop()):
                if is_goal(s):
                    return(s)
                fringe.append(s)
    return False

# This is N, the size of the board. It is passed through command line arguments.
coordinates = []
problem =  str(sys.argv[1])  #program 
N = int(sys.argv[2])
No_Unavailable = int(sys.argv[3]) # number of coordinates
#print(sys.argv[3:])
temp = sys.argv[4:]
temp2 = []
for x in range(len(temp)):
    #print(int(temp[x]))
    temp2.append(int(temp[x]))
coordinates = [temp2[x:x+2] for x in range(0, len(temp2), 2)]
#print(coordinates)

# The board is stored as a list-of-lists. Each inner list is a row of the board.
# A zero in a given square indicates no piece, and a 1 indicates a piece.
initial_board = [[0]*N]*N
print ("Starting from initial board:\n" + printable_board(initial_board) + "\n\nLooking for solution...\n")
start = timer()
solution = solve(initial_board,problem)
for i in coordinates:
    #print(i)
    solution[i[0]][i[1]] = -1

end = timer()
print (printable_board(solution) if solution else "Sorry, no solution found. :(")
print("Time Taken : ",end - start)


