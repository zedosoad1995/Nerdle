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
from helper import (
    get_possible_evals, 
    filter_zero_mult_div, 
    get_combinations_dict, 
    delete_refs, 
    remove_empty_lists, 
    has_red_or_green_instance,
    evaluate,
    get_score
)
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

            possible_combinations.append(full_calculation)

    return possible_combinations


def get_possible_combinations_from_list(possible_combinations, cmd):
    filtered_combinations = []
    
    cmd_slots = cmd.strip().split(' ')
    num_reds = {}
    num_greens = {}
    for slot in cmd_slots:
        digit, color = slot
        num_reds[digit] = num_reds.get(digit, 0)
        num_greens[digit] = num_greens.get(digit, 0)
        if color == 'r':
            num_reds[digit] += 1
        elif color == 'g':
            num_greens[digit] += 1

    for comb in possible_combinations:
        is_valid = True

        for i, slot in enumerate(cmd_slots):
            digit, color = slot

            if color == 'g':
                if comb[i] != digit:
                    is_valid = False
                    break

            elif color == 'r':
                if comb[i] == digit or comb.count(digit) < num_reds[digit]:
                    is_valid = False
                    break

            elif color == 'b':
                if comb[i] == digit or comb.count(digit) > num_reds[digit] + num_greens[digit]:
                    is_valid = False
                    break

        if is_valid:
            filtered_combinations.append(comb)

    return filtered_combinations

""" with open('all_starting_combinations_scores_ordered.pkl', 'rb') as f:
    lst = cPickle.load(f)

for comb in lst:
    print(comb)
    pass """


restrictions = {}

# 3b 3b 6g /b 4b 2b =g 8b
# 6b +b 6g -g 1r 1b =g 1b
cnt = 0
possible_combinations = get_all_combinations(restrictions)
possible_combinations = filter_zero_mult_div(possible_combinations)

while True:
    if cnt > 0:
        cmd = input('Write new cmd: ')
        possible_combinations = get_possible_combinations_from_list(possible_combinations, cmd)
    print('List of possible combinations', possible_combinations, len(possible_combinations))

    scores = []
    for fake_result in possible_combinations:
        evals_dict = {}
        for fake_guess in possible_combinations:
            eval_str = evaluate(fake_result, fake_guess)
            evals_dict[eval_str] = evals_dict.get(eval_str, 0) + 1

        score = get_score(evals_dict, len(possible_combinations))
        scores.append([fake_result, score])

        #print(fake_result, sorted(list(evals_dict.values())))
        #print(fake_result, score)

    scores.sort(key=lambda x: x[1], reverse=True)
    print(scores)

    cnt += 1

    with open('all_starting_combinations_scores_ordered.pkl', 'wb') as f:
        cPickle.dump(scores, f)


        
            

    """ for temp_dict in combinations_dict.values():
        for _vals in temp_dict.values():
            remove_empty_lists(_vals)

        ggbgbgbb

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
    """

