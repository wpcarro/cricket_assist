import re, sys
from itertools import cycle


DEBUG = False


def init_board(player_name):
    # 50 will be a bullseye
    b = dict((k, 0) for k in range(20, 14, -1))
    b.update({50: 0})
    b['player_name'] = player_name

    return b


def create_game(player_name_1, player_name_2, is_three_player=False):
    score_1 = init_board(player_name_1)
    score_2 = init_board(player_name_2)

    return (score_1, score_2)


def create_n_games(player_names):
    return [init_board(pn) for pn in player_names]


def record_scores(board, *scores):
    for s in scores:
        try:
            board[s] += 1
        except KeyError as ke:
            if DEBUG:
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


def print_board(board):
    print(board['player_name'])

    for (k, v) in board.items():
        if k == 'player_name':
            continue
        v = clamp(0, 3, v)
        print('{num}      {s} '.format(
            num=num_to_symbol(k),
            s=score_to_symbol(v)
        ))

    print('----------\n')


def print_game(board_1, board_2):
    if DEBUG:
        print('-- DEBUG --')
        print('board_1')
        print(board_1)

        print('board_2')
        print(board_2)
        print()

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


def convert_score(score):
    alt_score_formats = {
        'b': '50',
        'be': '50'
    }

    try:
        score = alt_score_formats[score]
    except KeyError as ke:
        score = score

    return score


def process_input(score_string):
    results = []
    regex = re.compile(r'(\d+)x(\d{1,2}|be)')

    for s in re.split(r'\s+', score_string.lower()):
        try:
            multiplier, score = regex.match(s).groups()
            score = convert_score(score)
            score = expand_shorthand(multiplier, score)
        except AttributeError as ae:
            score = convert_score(s)

        results.append(score)

    return [int(x) for x in ' '.join(results).split(' ')]


def prompt_debug():
    result = input('DEBUG (y/N)? ').lower()
    DEBUG = re.compile(r'y(?:es)?').match(result) != None


def prompt_num_players():
    result = input('Number of players: ')
    return int(result)


def prompt_and_record_scores(current_board):
    keep_asking = True

    while keep_asking:
        try:
            scores_string = input('Report %s\'s scores ... ' % current_board['player_name'])
            scores = process_input(scores_string)
            test_board = current_board.copy()
            test_scores = scores.copy()
            # Attempt to record the scores on a test board
            record_scores(test_board, *scores)
            keep_asking = False
        except ValueError:
            print('Invalid input: %s' % scores_string)
            pass

    record_scores(current_board, *scores)


def run_n_players(player_count):
    player_names = []

    if not DEBUG:
        player_names = [input('Enter a name for player: ') for player in range(player_count)]
    else:
        player_names = ['player %d' % x for x in range(player_count)]

    if DEBUG:
        print('player_names: %s' % player_names)

    boards = create_n_games(player_names)
    player_index_cycle = cycle(range(player_count))
    winning_board = None

    should_continue = True

    while should_continue:
        current_player_index = next(player_index_cycle)
        current_board = boards[current_player_index]

        prompt_and_record_scores(current_board)

        is_last_player = current_player_index + 1 == player_count

        if is_last_player:
            print_boards(boards)

        if not winning_board:
            winning_board = current_board if is_winning_board(current_board) else None

        should_continue = not (winning_board and is_last_player)

    print('%s wins!' % winning_board['player_name'])
    print('-- Winning Board --')
    print_board(winning_board)

    return 0


def print_boards(boards):
    for board in boards:
        print_board(board)


def run():
    prompt_debug()

    n = prompt_num_players()
    return run_n_players(n)


if __name__ == '__main__':
    try:
        sys.exit(run())
    except KeyboardInterrupt as ki:
        print('\nThanks for playing!')
        sys.exit(1)

