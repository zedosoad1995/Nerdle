import functools
import itertools
import math
import copy
import _pickle as cPickle
from get_combinations_helper import (
    get_operation_combinations,
    map_indices,
    fill_digits, 
    get_equal_positions, 
    filter_operations, 
    get_valid_digits, 
    is_valid_digits,
    has_trailing_zeros
)
from helper import get_possible_evals, filter_zero_mult_div, get_combinations_dict, delete_refs, remove_empty_lists, has_red_or_green_instance
from params import word_size, operations, all_digits

def get_all_combinations(restrictions):
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

            if has_trailing_zeros(full_calculation):
                continue

            possible_combinations.append([full_calculation])

    return possible_combinations


def get_possible_combinations_from_list(combinations_dict, anti_combinations_dict, cmd):
    cmd_slots = cmd.split(' ')

    for i, cmd_slot in enumerate(cmd_slots):
        digit, color = cmd_slot
        if color == 'g':
            for key, vals in combinations_dict[str(i)].items():
                if key == digit:
                    continue
                delete_refs(vals)
        elif color == 'r':
            delete_refs(combinations_dict[str(i)][digit])
            if digit in anti_combinations_dict:
                delete_refs(anti_combinations_dict[digit])
        elif color == 'b':
            r_g = has_red_or_green_instance(cmd_slots, digit)
            if not has_red_or_green_instance(cmd_slots, digit):
                for vals in combinations_dict.values():
                    if digit in vals:
                        delete_refs(vals[digit])
            elif 'r' in r_g:
                delete_refs(combinations_dict[str(i)][digit])
                if digit in anti_combinations_dict:
                    delete_refs(anti_combinations_dict[digit])
            elif 'g' in r_g:
                for key, vals in combinations_dict.items():
                    if digit in vals and digit not in cmd_slots[int(key)]:
                        delete_refs(vals[digit])


restrictions = {}

# 3b 3b 6g /b 4b 2b =g 8b
# 6b +b 6g -g 1r 1b =g 1b
cmd = 'r r r r r r r r'
cnt = 0
possible_combinations = get_all_combinations(restrictions)
possible_combinations = filter_zero_mult_div(possible_combinations)
combinations_dict, anti_combinations_dict = get_combinations_dict(possible_combinations)
while True:
    cmd = input('Write new cmd: ')
    get_possible_combinations_from_list(combinations_dict, anti_combinations_dict, cmd)
    remove_empty_lists(possible_combinations)
    print('List of possible combinations', possible_combinations, len(possible_combinations))

    for temp_dict in combinations_dict.values():
        for _vals in temp_dict.values():
            remove_empty_lists(_vals)

    if cnt > -1:
        possible_evals = get_possible_evals(cmd)
        scores = []
        for comb in possible_combinations:
            comb = comb[0]
            print(comb)
            comb_lens = []
            for i, _eval in enumerate(possible_evals):
                temp_cmd = functools.reduce(lambda acc, iv: acc + comb[iv[0]] + iv[1] + ' ', enumerate(_eval), '')[:-1]
                
                #temp_restrictions = convert_cmd_to_restrictions(temp_cmd, copy.deepcopy(restrictions))
                tmp = [combinations_dict, anti_combinations_dict, possible_combinations]
                tmp1 = cPickle.loads(cPickle.dumps(tmp, -1))
                #tmp1 = copy.deepcopy(tmp)
                combinations_dict_cpy, anti_combinations_dict_cpy, possible_combinations_cpy = tmp1
                get_possible_combinations_from_list(combinations_dict_cpy, anti_combinations_dict_cpy, temp_cmd)
                #remove_empty_lists(possible_combinations_cpy)
                cnt_ = 0
                for ii in possible_combinations_cpy:
                    if ii != []:
                        cnt_ += 1
                num_combinations = cnt_
                
                if num_combinations > 0:
                    comb_lens.append(num_combinations)
                    print(_eval, num_combinations)

            score = 0
            for val in comb_lens:
                score = score - val/sum(comb_lens)*math.log2(val/len(possible_combinations))

            #score = functools.reduce(lambda acc, val: acc - val/sum(comb_lens)*math.log2(val/len(possible_combinations)), comb_lens)
            scores.append([score, comb])

            print('SCORE:', score)

        scores.sort(key=lambda x: x[0], reverse=True)
        print(scores)

    cnt += 1
