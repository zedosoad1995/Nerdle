import re
import math
from params import word_size


def filter_zero_mult_div(possible_combinations):
    filtered_comb = []
    for comb in possible_combinations:
        if not re.search("[^\d]0\*|\*0|^0|[^\d]0\/", comb):
            filtered_comb.append(comb)

    return filtered_comb


def evaluate(result, guess):
    eval_lst = ['g'] * word_size 

    result = list(result)
    guess = list(guess)

    for i, c in enumerate(result):
        if c == guess[i]:
            result[i] = '_'
            guess[i] = '_'
    
    for i, c in enumerate(result):
        if c == '_':
            continue
        
        if guess.count(c) > 0:
            eval_lst[i] = 'r'
            guess[guess.index(c)] = '_'
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