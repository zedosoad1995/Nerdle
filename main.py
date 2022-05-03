import itertools
import _pickle as cPickle
import csv
from alive_progress import alive_bar
import random
from get_combinations_helper import (
    get_operation_combinations,
    fill_digits, 
    has_trailing_zeros
)
from helper import (
    filter_zero_mult_div, 
    evaluate,
    get_score,
    eval_str_to_cmd,
    load_all_possibilities
)
from params import word_size, operations, all_digits, all_equal_sign_positions

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


def get_suggestion(possible_combinations, max_combinations=None, verbose=False):
    scores = []
    with alive_bar(len(possible_combinations[:max_combinations]), disable=not verbose) as bar:
        for i in range(len(possible_combinations[:max_combinations])):
            fake_guess = possible_combinations[i]
            evals_dict = {}
            for fake_result in possible_combinations:
                eval_str = evaluate(fake_guess, fake_result)
                evals_dict[eval_str] = evals_dict.get(eval_str, 0) + 1

            score = get_score(evals_dict, len(possible_combinations))
            scores.append([fake_guess, score])

            bar()

    scores.sort(key=lambda x: x[1], reverse=True)

    return scores


def play():
    possible_combinations = load_all_possibilities()

    while True:
        cmd = input('Write new cmd: ')
        possible_combinations = get_possible_combinations_from_list(possible_combinations, cmd)
        print('List of possible combinations', possible_combinations, len(possible_combinations))

        suggestion = get_suggestion(possible_combinations)[0]
        print('Best Guess', suggestion)


def simulation(n_solutions):
    all_possible_combinations = load_all_possibilities()

    random.shuffle(all_possible_combinations)
    random_solutions = all_possible_combinations[:n_solutions]

    diccc = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0}
    n_tries_lst = []
    avg_tries = 0
    for i, solution in enumerate(random_solutions):
        n_tries = 1
        while True:
            if n_tries == 1:
                possible_combinations = cPickle.loads(cPickle.dumps(all_possible_combinations, -1))
                guess = '48-32=16'
                #guess = '86*8=688'
                #guess = all_possible_combinations[math.floor(random.random()*len(all_possible_combinations))]

            if guess == solution:
                n_tries_lst.append(n_tries)
                avg_tries = (avg_tries*i + n_tries)/(i + 1)
                diccc[n_tries] += 1
                disp_dic = {}
                for key, val in diccc.items():
                    disp_dic[key] = round(val/(i + 1), 4)
                print(solution, n_tries, disp_dic, avg_tries)
                break

            eval_str = evaluate(guess, solution)
            cmd = eval_str_to_cmd(eval_str, guess)
            possible_combinations = get_possible_combinations_from_list(possible_combinations, cmd)

            if len(possible_combinations) > 500:
                guess = possible_combinations[0]
            else:
                guess = get_suggestion(possible_combinations)[0]

            n_tries += 1

    return n_tries_lst


def get_best_initial_guesses(filename='all_starting_guesses_scores', verbose=False):
    all_possible_combinations = load_all_possibilities()

    scores = get_suggestion(all_possible_combinations, verbose=verbose)

    filename_without_extension = filename.split('.')[0]
    with open(f"{filename_without_extension}.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(scores)


def get_all_initial_guesses(filename='all_starting_guesses'):
    all_combinations = get_all_combinations()
    all_combinations = filter_zero_mult_div(all_combinations)
    filename_without_extension = filename.split('.')[0]
    with open(f"{filename_without_extension}.txt", "w") as f:
        for comb in all_combinations:
            f.write(comb + "\n")
