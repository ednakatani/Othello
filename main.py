'''
Two Player Console Othello(NO AI)
Written by Patrick Feltes
11/2/15
'''


def printBoard(board):
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

def getScore(board):
	black = 0
	white = 0
	
	for r in board:
		for c in r:
			if c == 'B': 
				black += 1
			elif c == 'W':
				white += 1
	return (black, white)

def getPossibleMoves(board, player):
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

def isLegalMove(board, r, c, player):
	return board[r][c] == ' '

def getIncludedPieces(board, xStart, yStart, xDir, yDir, player):
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

	while (xMove, yMove) not in possibilites:
		while xMove < 0 or xMove >= len(board):
			print('Enter a x coordinate(column):')
			xMove = int(input())

		while yMove < 0 or yMove >= len(board):
			print('Enter a y coordinate(row):')
			yMove = int(input())

		if (xMove, yMove) not in possibilites:
			xMove = -1
			yMove = -1

	flip = getPiecesToFlip(board, xMove, yMove, player)
	board[yMove][xMove] = player

	board = flipPieces(board, flip, player)

	return board

def isBoardFull(board):
	full = True

	for r in board:
		for c in r:
			if c == ' ':
				full = False
	return full

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
		printBoard(board)

		# game over!
		if len(getPossibleMoves(board, player)) == 0 and len(getPossibleMoves(board, otherPlayer)) == 0: break

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
