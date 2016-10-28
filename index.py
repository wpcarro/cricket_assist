import re, sys


def init_board(player_name):
    # 50 will be a bullseye
    b = dict((k, 0) for k in range(20, 14, -1))
    b.update({50: 0})
    b['player_name'] = player_name

    return b


def create_game(player_name_1, player_name_2):
    score_1 = init_board(player_name_1)
    score_2 = init_board(player_name_2)

    return (score_1, score_2)


def record_scores(board, *scores):
    for s in scores:
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
    return num if num != 50 else 'BE'


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
    print('------------------')
    print(' %3d          %3d ' % (compute_sum(board_1), compute_sum(board_2)))


def compute_sum(board):
    blacklist_keys = [
        'player_name',
        'BE'
    ]
    return sum(int(k) * v for k, v in board.items() if k not in blacklist_keys)


def expand_shorthand(multiplier, score):
    return ' '.join([score for x in range(int(multiplier))])


def process_input(score_string):
    results = []
    regex = re.compile(r'(\d+)[xX](\d{1,2})')

    for s in score_string.split(' '):
        try:
            multiplier, score = regex.match(s).groups()
            score = expand_shorthand(multiplier, score)
        except AttributeError as ae:
            score = s

        results.append(score)

    return map(lambda x: int(x), ' '.join(results).split(' '))


def run():
    """
    player_name_1 = input('Enter name for player 1: ')
    player_name_2 = input('Enter name for player 2: ')

    score_1, score_2 = create_game('Magnus', 'William')
    """

    score_1, score_2 = create_game('Magnus', 'William')

    is_first_player = True

    current_board = score_1
    previous_board = score_2

    winning_board = None

    while winning_board == None:
        scores = input('Report %s\'s scores ... ' % current_board['player_name'])
        scores = process_input(scores)
        record_scores(current_board, *scores)

        if is_first_player:
            print_game(current_board, previous_board)
        else:
            print_game(previous_board, current_board)

        winning_board = current_board if is_winning_board(current_board) else None

        is_first_player = not is_first_player
        current_board, previous_board = previous_board, current_board

    print('%s wins!' % winning_board['player_name'])
    return 0


if __name__ == '__main__':
    try:
        sys.exit(run())
    except KeyboardInterrupt as ki:
        print('\nThanks for playing!')
        sys.exit(1)

