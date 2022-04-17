import functools
import itertools
import math
import copy
from get_combinations_helper import (
    get_operation_combinations,
    map_indices,
    fill_digits, 
    get_equal_positions, 
    filter_operations, 
    get_valid_digits, 
    is_valid_digits,
    has_result_valid_digits,
    has_trailing_zeros
)
from helper import get_possible_evals, filter_zero_mult_div
from params import word_size, operations, all_digits

def get_possible_combinations(restrictions):
    possible_operation_combinations = []

    for equal_sign_pos in get_equal_positions(restrictions):
        calculation_str = '_' * equal_sign_pos
        operations_obj = next((op for op in operations if op['equal_sign_pos'] == equal_sign_pos), None)

        for positions in operations_obj['positions']:
            combs = get_operation_combinations(calculation_str, positions, operations_obj['symbols'])
            possible_operation_combinations.extend(combs)

    possible_operation_combinations = filter_operations(possible_operation_combinations, restrictions)

    possible_combinations = []
    for calculation_str in possible_operation_combinations:

        mapped_indices = map_indices(calculation_str)
        valid_digits = get_valid_digits(restrictions, mapped_indices)
        digits_combinations = list(itertools.product(*valid_digits))
        
        for digits in digits_combinations:
            calc = fill_digits(calculation_str, digits)

            try:
                result = eval(calc)
            except:
                continue

            if not (isinstance(result, int) or result.is_integer()) or \
                word_size - 1 - len(str(int(result))) != len(calculation_str) or \
                result < 0:
                continue

            result = int(result)

            full_calculation = f'{calc}={result}'

            #valid_digits = list(set(item for sublist in valid_digits for item in sublist))

            if not is_valid_digits(full_calculation, restrictions, all_digits) or \
                has_trailing_zeros(full_calculation):
                continue

            possible_combinations.append(full_calculation)

    return possible_combinations


def get_possible_combinations_from_list(prev_combinations, restrictions):
    possible_combinations = []
    
    for comb in prev_combinations:
        if not is_valid_digits(comb, restrictions, all_digits + ['*', '+', '/', '-', '=']) or \
                has_trailing_zeros(comb):
                continue

        possible_combinations.append(comb)

    return possible_combinations



def convert_cmd_to_restrictions(cmd_str, restrictions={}):
    '''
    format example: 2r 4b +g ... =g ...
    r-red, g-green, b-black
    '''  

    digit_cmds = cmd_str.split(' ')

    for i, (digit, cmd) in enumerate(digit_cmds):
        if digit not in restrictions:
            restrictions[digit] = {}

        if cmd == 'r':
            if 'not in positions' in restrictions[digit]:
                if i not in restrictions[digit]['not in positions']:
                    restrictions[digit]['not in positions'].append(i)
            else:
                restrictions[digit]['not in positions'] = [i]
        elif cmd == 'g':
            if 'positions' in restrictions[digit]:
                if i not in restrictions[digit]['positions']:
                    restrictions[digit]['positions'].append(i)
            else:
                restrictions[digit]['positions'] = [i]
        
    digits = [cmd[0] for cmd in digit_cmds]
    cmd_types = [cmd[1] for cmd in digit_cmds] 

    # Run 2nd time for the black boxes
    for digit, cmd in digit_cmds:
        if cmd == 'b':
            if len(restrictions[digit]) == 0:
                restrictions[digit]['does not exist'] = True
                continue

            if 'does not exist' in restrictions[digit] and restrictions[digit]['does not exist']:
                continue

            num_valid_instances = len([d for i, d in enumerate(digits) if d == digit and cmd_types[i] != 'b'])
            restrictions[digit]['number of instances'] = num_valid_instances

    return restrictions


restrictions = {}

# 3b 3b 6g /b 4b 2b =g 8b
# 6b +b 6g -g 1r 1b =g 1b
cmd = 'r r r r r r r r'
cnt = 0
while True:
    cmd = input('Write new cmd: ')
    restrictions = convert_cmd_to_restrictions(cmd, restrictions)
    possible_combinations = get_possible_combinations(restrictions)
    possible_combinations = filter_zero_mult_div(possible_combinations)
    print('List of possible combinations', possible_combinations, len(possible_combinations))

    if cnt > -1:
        possible_evals = get_possible_evals(cmd)
        scores = []
        for comb in possible_combinations:
            print(comb)
            comb_lens = []
            for i, _eval in enumerate(possible_evals):
                temp_cmd = functools.reduce(lambda acc, iv: acc + comb[iv[0]] + iv[1] + ' ', enumerate(_eval), '')[:-1]
                temp_restrictions = convert_cmd_to_restrictions(temp_cmd, copy.deepcopy(restrictions))
                out_combinations = get_possible_combinations_from_list(possible_combinations, temp_restrictions)
                num_combinations = len(out_combinations)
                
                if num_combinations > 0:
                    comb_lens.append(num_combinations)
                    print(comb, _eval, num_combinations)

            print(comb, comb_lens)
            score = 0
            for val in comb_lens:
                score = score - val/sum(comb_lens)*math.log2(val/len(possible_combinations))

            #score = functools.reduce(lambda acc, val: acc - val/sum(comb_lens)*math.log2(val/len(possible_combinations)), comb_lens)
            scores.append([score, comb])

            print('SCORE:', score)

        scores.sort(key=lambda x: x[0], reverse=True)
        print(scores)

    cnt += 1
