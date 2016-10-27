# Cricket Game

def init_board(player_name):
	# 14 will be a bullseye
	b = dict((k, 0) for k in range(20, 13, -1))
	b['player_name'] = player_name
	
	return b

def create_game(player_name_1, player_name_2):
	score_1 = init_board(player_name_1)
	score_2 = init_board(player_name_2)
	
	return (score_1, score_2)


def record_scores(board, a, b, c):
	for s in [a, b, c]:
		try:
			board[s] += 1
		except KeyError as ke:
			print('%d is not a score in cricket...' % s)
			
	
def is_winning_board(board):
	return all(v >= 3 for k, v in board.items() if k != 'player_name')
	
	
def clamp(mn, mx, x):
	return max(min(x, mx), mn)


def score_to_symbol(score):
	symbol_dict = {
		0: '.',
		1: '/',
		2: 'X',
		3: '©'
	}
	
	return symbol_dict[clamp(0, 3, score)]


def num_to_symbol(num):
	return num if num != 14 else 'BE'


def print_game(board_1, board_2):
	
	print('-- Current Game --')
	
	for (k1, v1), (k2, v2) in zip(board_1.items(), board_2.items()):
		if k1 == 'player_name':
			continue
		v1, v2 = clamp(0, 3, v1), clamp(0, 3, v2)
		print(' {s1}      {num}      {s2} '.format(
			s1=score_to_symbol(v1),
			num=num_to_symbol(k1),
			s2=score_to_symbol(v2))
		)
	
	
def main():
	score_1, score_2 = create_game('Magnus', 'William')
	
	is_first_player = True
	
	current_board = score_1
	previous_board = score_2
	
	winning_board = None
	
	while winning_board == None:
		scores = input('Report %s\'s scores ... ' % current_board['player_name'])
		scores = [int(s) for s in scores.split(' ')]
		record_scores(current_board, *scores)
		
		if is_first_player:
			print_game(current_board, previous_board)
		else:
			print_game(previous_board, current_board)
		
		winning_board = current_board if is_winning_board(current_board) else None
		
		is_first_player = not is_first_player
		current_board, previous_board = previous_board, current_board
		
	print('%s wins!' % winning_board['player_name'])
