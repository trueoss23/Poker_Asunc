from cards import deck
import time
from functools import wraps
import multiprocessing


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f'{func.__name__} took {end - start:.6f} seconds to complete')
        return result
    return wrapper


def is_flash_nahd(suits_comb_str: str):
    return suits_comb_str.count('c') == 5 or \
        suits_comb_str.count('d') == 5 or \
        suits_comb_str.count('h') == 5 or \
        suits_comb_str.count('s') == 5


def is_straight_comb(comb: str):
    straight_num = 0
    for i, elem in enumerate(comb):
        if i != 0:
            if ord(comb[i - 1]) - 1 == ord(comb[i]):
                straight_num += 1
            else:
                straight_num -= 1

    return straight_num > 4


def calc_duplication(comb: str):
    result = {'caret': 0, 'trips': 0, 'pair': 0}
    for elem in set(comb):
        count_elem = comb.count(elem)
        if count_elem == 4:
            result['caret'] += 1
        elif count_elem == 3:
            result['trips'] += 1
        elif count_elem == 2:
            result['pair'] += 1
    return result


def getcombDetails(comb: str) -> tuple:
    copy_comb = comb.split(' ')
    detail_comb = ''
    suits_comb_str = ''
    for elem in copy_comb:
        detail_comb += deck[elem]
        suits_comb_str += elem[1]
    return (''.join(sorted(detail_comb)), is_flash_nahd(suits_comb_str))


def is_high_straight_comb(comb: str):
    return is_straight_comb(comb) and 'A' in comb and 'K' in comb \
        and 'Q' in comb


def calc_rank_comb(comb: tuple):
    high_straight = is_high_straight_comb(comb[0])
    flash = comb[1]
    straight = is_straight_comb(comb[0])
    caret = calc_duplication(comb[0])['caret'] > 0
    trips = calc_duplication(comb[0])['trips'] > 0
    two_pair = calc_duplication(comb[0])['pair'] > 1
    one_pair = calc_duplication(comb[0])['pair'] > 0
    rank = \
        (flash and high_straight and 1) or \
        (flash and straight and 2) or \
        (caret and 3) or \
        (trips and one_pair and 4) or \
        (flash and 5) or \
        (straight and 6) or \
        (trips and 7) or \
        (two_pair and 8) or \
        (one_pair and 9) or \
        (10)
    return rank


def comparecombs(h1, h2):
    comb_one = getcombDetails(h1)
    comb_two = getcombDetails(h2)
    rank1 = calc_rank_comb(comb_one)
    rank2 = calc_rank_comb(comb_two)
    if rank1 == rank2:
        if comb_one < comb_two:
            return "Win"
        elif comb_one > comb_two:
            return "Lose"
        else:
            return "Draw"
    return rank1 < rank2 if "Win" else "Lose"


@timeit
def calc_options():
    for i in range(100_000):
        comparecombs('2c 5c 3c 4c 5h 7c Ad', 'Ac Ac 3c 4c 5h 7c 6d')


def tmp_func():
    for i in range(100_000):
        comparecombs('2c 5c 3c 4c 5h 7c Ad', 'Ac Ac 3c 4c 5h 7c 6d')


@timeit
def paralel_calc_options():
    processes = []
    for i in range(8):
        proc = multiprocessing.Process(target=tmp_func)
        processes.append(proc)
        proc.start()
    for elem in processes:
        elem.join()


paralel_calc_options()
calc_options()
