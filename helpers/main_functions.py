import itertools
from alive_progress import alive_bar
import random
from helpers.get_combinations_helper import (
    get_operation_combinations,
    fill_digits, 
    has_trailing_zeros
)
from helpers.helper import (
    evaluate,
    get_score,
)
from helpers.params import word_size, operations, all_digits, all_equal_sign_positions

def get_all_combinations():
    possible_operation_combinations = []

    for equal_sign_pos in all_equal_sign_positions:
        calculation_str = '_' * equal_sign_pos
        operations_obj = next((op for op in operations if op['equal_sign_pos'] == equal_sign_pos), None)

        for positions in operations_obj['positions']:
            combs = get_operation_combinations(calculation_str, positions, operations_obj['symbols'])
            possible_operation_combinations.extend(combs)

    possible_combinations = []
    for calculation_str in possible_operation_combinations:

        digits_combinations = list(itertools.product(all_digits, repeat=calculation_str.count('_')))
        
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


def filter_combinations(possible_combinations, cmd):
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

    random.shuffle(filtered_combinations)
    return filtered_combinations


def get_suggestions(possible_combinations, max_combinations=None, verbose=False):
    scores = []
    with alive_bar(len(possible_combinations[:max_combinations]), disable=not verbose) as bar:
        for i in range(len(possible_combinations[:max_combinations])):
            fake_guess = possible_combinations[i]
            evals_dict = {}
            for fake_result in possible_combinations:
                if fake_result == fake_guess:
                    continue
                eval_str = evaluate(fake_guess, fake_result)
                evals_dict[eval_str] = evals_dict.get(eval_str, 0) + 1

            score = get_score(evals_dict, len(possible_combinations[:max_combinations]))
            scores.append([fake_guess, score])

            bar()

    scores.sort(key=lambda x: x[1], reverse=True)

    return scores
