import itertools
import re
import csv
from alive_progress import alive_bar
import random
import matplotlib.pyplot as plt
from get_combinations_helper import (
    get_operation_combinations,
    fill_digits, 
    has_trailing_zeros
)
from helper import (
    filter_lone_zero, 
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

    random.shuffle(filtered_combinations)
    return filtered_combinations


def get_suggestion(possible_combinations, max_combinations=None, verbose=False):
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


def is_cmd_valid(str):
    pattern = re.compile("([0-9+\-*\/=][rgb]\s){7}[0-9][rgb]")
    p = pattern.match(str)
    print(p)
    print(len(str))
    if p is None and len(str) != 3*7 + 2:
        return None
    
    return p


def play():
    possible_combinations = load_all_possibilities()
    while True:
        cmd = input('Write new cmd: ')
        if is_cmd_valid(cmd) is None:
            print('Invalid command. Example of valid cmd: 4g 8b -r 1g 2g =g 3r 6b\n' + \
                'Must contain 8 slots, and each slot must have 2 characters:\n' + \
                '\t-Digit (0-9) or operations (+-*/=)\n' + \
                '\t-g (green), r (red) or b (black)')
            continue
        possible_combinations = get_possible_combinations_from_list(possible_combinations, cmd)
        print('List of possible combinations:', possible_combinations, len(possible_combinations))

        suggestion = get_suggestion(possible_combinations)[0][0]
        print('Best Guess:', suggestion)


def plot_simulation(ax, tries_dict, avg_tries, i):
    ax.clear()
    ax.set_xlabel('num. tries')
    ax.set_ylabel('freq.')
    bars = ax.bar(tries_dict.keys(), tries_dict.values(), color=(0.2, 0.4, 0.6, 1))
    for p in bars:
        width = p.get_width()
        height = p.get_height()
        x, y = p.get_xy()
        
        plt.text(x+width/2,
                y+height*1.01,
                str(round(height/(i+1)*100, 3))+'%',
                ha='center')
    
    x_disp = (ax.get_xlim()[-1] - ax.get_xlim()[0])*0.98 + ax.get_xlim()[0]
    plt.text(x_disp, 
            ax.get_ylim()[-1]*0.98, 
            'Avg. tries: ' + str(round(avg_tries, 3)), 
            fontsize = 12, 
            ha='right', 
            va='top')

    plt.pause(0.001)

def simulation(n_solutions=None, 
                starting_guess='48-32=16', 
                sug_possibilities_th=100, 
                fig_name='sim_res',
                strategy='best',
                plot_live=False):
    all_possible_combinations = load_all_possibilities()

    if n_solutions is not None or True:
        random.shuffle(all_possible_combinations)
    random_solutions = all_possible_combinations[:n_solutions]

    tries_dict = {}
    n_tries_lst = []
    avg_tries = 0

    if plot_live:
        _, ax = plt.subplots()

    with alive_bar(len(random_solutions)) as bar:
        for i, solution in enumerate(random_solutions):
            n_tries = 1
            while True:
                if n_tries == 1:
                    possible_combinations = all_possible_combinations
                    guess = starting_guess

                if guess == solution:
                    n_tries_lst.append([solution, n_tries])
                    avg_tries = (avg_tries*i + n_tries)/(i + 1)
                    tries_dict[n_tries] = tries_dict.get(n_tries, 0) + 1


                    if plot_live and i%40 == 0:
                        plot_simulation(ax, tries_dict, avg_tries, i)
                    break

                eval_str = evaluate(guess, solution)
                cmd = eval_str_to_cmd(eval_str, guess)
                possible_combinations = get_possible_combinations_from_list(possible_combinations, cmd)

                if strategy == 'best':
                    guess = get_suggestion(possible_combinations, 
                                            max_combinations=min(sug_possibilities_th, len(possible_combinations)))[0][0]
                elif strategy == 'worst':
                    guess = get_suggestion(possible_combinations, 
                                            max_combinations=min(sug_possibilities_th, len(possible_combinations)))[-1][0]
                elif strategy == 'random':
                    guess = possible_combinations[random.randrange(len(possible_combinations))]

                n_tries += 1

            bar()

    if fig_name:
        _, ax = plt.subplots()
        plot_simulation(ax, tries_dict, avg_tries, i)
        plt.savefig(fig_name.split('.')[0] + '.png')



def get_initial_guesses_scores(filename='all_starting_guesses_scores', verbose=False):
    all_possible_combinations = load_all_possibilities()

    scores = get_suggestion(all_possible_combinations, verbose=verbose)

    filename_without_extension = filename.split('.')[0]
    with open(f"{filename_without_extension}.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(scores)


def get_all_initial_guesses(filename='all_starting_guesses'):
    all_combinations = get_all_combinations()
    all_combinations = filter_lone_zero(all_combinations)
    filename_without_extension = filename.split('.')[0]
    with open(f"{filename_without_extension}.txt", "w") as f:
        for comb in all_combinations:
            f.write(comb + "\n")
