'''
Two Player Console Othello(NO AI)
Written by Patrick Feltes
11/2/15
'''

import copy
from os import system, name


WEIGHTS = [

  [ 4, -3,  2,  2,  2,  2, -3,  4],
  [-3, -4, -1, -1, -1, -1, -4, -3],
  [ 2, -1,  1,  0,  0,  1, -1,  2],
  [ 2, -1,  0,  1,  1,  0, -1,  2],
  [ 2, -1,  0,  1,  1,  0, -1,  2],
  [ 2, -1,  1,  0,  0,  1, -1,  2],
  [-3, -4, -1, -1, -1, -1, -4, -3],
  [ 4, -3,  2,  2,  2,  2, -3,  4]

]

IA = 'W'
MIN = -999
MAX = 999
DEPTH = 5

def cls():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def getotherPlayer(player) -> str:
	if player == 'W':
		return 'B'
	else:
		return 'W'

def printBoard(board: list) -> None:
	'''
	Print game board in console
	'''
	print('  0 1 2 3 4 5 6 7 ')
	for r in range(len(board)):
		s = str(r) + '|'
		for c in range(len(board[r])):
			s += board[r][c] + '|'
		print(s + str(r))

	print('  0 1 2 3 4 5 6 7 ')
	(black, white) = getScore(board)
	print('SCORE:')
	print('B: ' + str(black))
	print('W: ' + str(white))

def getScore(board: list) -> tuple:
	'''
	For each record in board list count blacks and whites
	'''
	black = 0
	white = 0
	
	for r in board:
		for c in r:
			if c == 'B': 
				black += 1
			elif c == 'W':
				white += 1
	return (black, white)

def getPossibleMoves(board: list, player) -> list:
	'''
	Iterate over the game board, searching possible moves for the player
	'''
	# seems like this could be made more efficient, why populate so many lists if unnecessary?
	moves = []

	for x in range(len(board)):
		for y in range(len(board)):
			if not isLegalMove(board, y, x, player): 
				continue
			else:
				if len(getPiecesToFlip(board, x, y, player)) > 0:
					moves.append((x, y))
	return moves

def isLegalMove(board: list, r: int, c: int, player) -> bool:
	'''
	Verify if is possible to insert a piece in a position
	'''
	return board[r][c] == ' '

def getIncludedPieces(board, xStart, yStart, xDir, yDir, player) -> list:
	included = []

	if player == 'B':
		otherPlayer = 'W'
	else:
		otherPlayer = 'B'

	# distance is 7 spaces
	for dist in range(1, 8):
		xCurr = xStart + dist * xDir
		yCurr = yStart + dist * yDir

		# if the current position is off the board, return [] because the pieces are not bounded
		if xCurr < 0 or xCurr >= len(board) or yCurr < 0 or yCurr >= len(board):
			return []

		if board[yCurr][xCurr] == otherPlayer:
			included.append((xCurr, yCurr))
		elif board[yCurr][xCurr] == player:
			return included
		else:
			return []

	return []

def getPiecesToFlip(board, x, y, player):
	# get positions of all pieces to be flipped by a move
	flip = []

	# all different directions, xDir = 0 and yDir = 0 not included because then there wouldn't be a direction!
	flip.extend((getIncludedPieces(board, x, y, 1, 1, player)))
	flip.extend((getIncludedPieces(board, x, y, 1, -1, player)))
	flip.extend((getIncludedPieces(board, x, y, -1, 1, player)))
	flip.extend((getIncludedPieces(board, x, y, 0, 1, player)))
	flip.extend((getIncludedPieces(board, x, y, 0, -1, player)))
	flip.extend((getIncludedPieces(board, x, y, 1, 0, player)))
	flip.extend((getIncludedPieces(board, x, y, -1, 0, player)))
	flip.extend((getIncludedPieces(board, x, y, -1, -1, player)))

	##print(list(set(flip)))

	# use a set to remove duplicates
	return list(set(flip))

def flipPieces(board, flip, player):
	for pos in flip:
		board[pos[1]][pos[0]] = player

	return board

def promptMove(board, player):
	print(player + " player's turn!")
	
	possibilites = getPossibleMoves(board, player)
	
	# move can't be made! let other player move!
	if len(possibilites) == 0:
		return False

	xMove = -1
	yMove = -1

	
	if player == IA:
		max = (MIN,)
		for (b,(x,y)) in getMoves(board, player):
			h = minimax(b, player, DEPTH, MIN, MAX, True)
			print(x,y, ':', h)
			if h > max[0]:
				max = (h,x,y)
		
		xMove = max[1]
		yMove = max[2]	
	
	else:

		while (xMove, yMove) not in possibilites:
			while xMove < 0 or xMove >= len(board):
				xMove = int(input('X: '))

			while yMove < 0 or yMove >= len(board):
				yMove = int(input('Y: '))

			if (xMove, yMove) not in possibilites:
				xMove = -1
				yMove = -1
	

	flip = getPiecesToFlip(board, xMove, yMove, player)
	board[yMove][xMove] = player

	board = flipPieces(board, flip, player)

	return board

def MakeMove(board, x, y, player):
	temp_board = [x[:] for x in board]
	temp_flip = getPiecesToFlip(temp_board, x, y, player)
	temp_board[y][x] = player

	temp_board = flipPieces(temp_board, temp_flip, player)
	(b,w) = getScore(temp_board)
	if player == "B":
		return (temp_board,w)
	
	return (temp_board,b)

def isBoardFull(board) -> bool:
	full = True

	for r in board:
		for c in r:
			if c == ' ':
				full = False
	return full

def gameOver(board):
	return len(getPossibleMoves(board, 'W')) == 0 and len(getPossibleMoves(board, 'B')) == 0

def getMoves(board,player):
	possibilites = getPossibleMoves(board, player)
	moves = []
	
	for p in possibilites:

		move = []

		temp_board = [x[:] for x in board]
		x = p[0]
		y = p[1]

		temp_flip = getPiecesToFlip(temp_board, x, y, player)
		temp_board[y][x] = player

		temp_board = flipPieces(temp_board, temp_flip, player)
		
		
		moves.append((temp_board,(x,y)))

		#print(p,':',heuristic(player,temp_board))

	return moves

def getTree(board, depth, player):
	p = ''
	for i in range(depth):
		if i%2 == 0: 
			p = player
		else:
			p = getotherPlayer(player) 
		
		getMoves(board, p)

def heuristic(board, player):
	(b,w) = getScore(board)
	total = 0
	for x in range(len(board)):
		for y in range(len(board[x])):
			if board[x][y] == player:
				total += WEIGHTS[x][y]
			elif board[x][y] != '':
				total -= WEIGHTS[x][y]
	
	if player == 'W':
		return total + int(w/2)
	else:
		return total + int(b/2) 


def minimax(board, player, depth, alfha, beta,  maximizingPlayer):
	
	if depth == 0 or gameOver(board):
		return heuristic(board, player)
	
	if maximizingPlayer:
		max_val = MIN
		for (b,(x,y)) in getMoves(board, player):
			val = minimax(copy.deepcopy(b),player,depth-1, alfha, beta, False)
			max_val = max(max_val, val)
			alfha = max(alfha, val)
			if beta <= alfha:
				break
		
		return max_val

	else:
		min_val = MAX
		for (b,(x,y)) in getMoves(board, player):
			val = minimax(copy.deepcopy(b),player,depth-1, alfha, beta, True)
			min_val = min(min_val, val)
			beta = min(beta, val)
			if beta <= alfha:
				break
		
		return min_val


def run():
	# create 8 by 8 board
	board = []
	for x in range(8):
		board.append([' '] * 8)
	


	board[3][3] = 'W'
	board[3][4] = 'B'
	board[4][3] = 'B'
	board[4][4] = 'W'

	player = 'B'
	otherPlayer = 'W'

	while not isBoardFull(board):
		#cls()
		printBoard(board)

		# game over!
		if gameOver(board): break

		tmp = promptMove(board, player)
		if not tmp == False:
			board = tmp
			
		(player, otherPlayer) = (otherPlayer, player)	

	(black, white) = getScore(board)

	if black > white:
		print('Black wins!')
	elif black < white:
		print('White wins!')
	else:
		print('Tie?')

run()
