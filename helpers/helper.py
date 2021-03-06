import re
import math
from helpers.params import word_size


def filter_lone_zero(possible_combinations):
    filtered_comb = []
    for comb in possible_combinations:
        if not re.search("^0|[^\d]0\/|[\-|\+|\*]0", comb):
            filtered_comb.append(comb)

    return filtered_comb


def evaluate(guess, result):
    eval_lst = ['g'] * word_size 

    guess = list(guess)
    result = list(result)

    for i, c in enumerate(guess):
        if c == result[i]:
            guess[i] = '_'
            result[i] = '_'
    
    for i, c in enumerate(guess):
        if c == '_':
            continue
        
        if result.count(c) > 0:
            eval_lst[i] = 'r'
            result[result.index(c)] = '_'
        else:
            eval_lst[i] = 'b'

    return ''.join(eval_lst)


def get_score(evals_dict, num_possibilities):
    score = 0
    for val in evals_dict.values():
        score = score - val/num_possibilities*math.log2(val/num_possibilities)

    return score


def eval_str_to_cmd(eval_str, calculations):
    cmd = ''
    for c_eval, c_calc in zip(list(eval_str), list(calculations)):
        cmd += f'{c_calc}{c_eval} '

    return cmd[:-1]


def load_all_moves(filename='data/all_starting_guesses.txt'):
    with open(filename, "r") as f:
        return f.read().splitlines()