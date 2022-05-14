import csv
from helpers.helper import filter_lone_zero, load_all_moves
from helpers.main_functions import get_all_combinations, get_suggestions


def get_initial_guesses_scores(filename='../data/all_starting_guesses_scores', verbose=False):
    all_possible_combinations = load_all_moves()

    scores = get_suggestions(all_possible_combinations, verbose=verbose)

    filename_without_extension = filename.split('.')[0]
    with open(f"{filename_without_extension}.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(scores)


def get_all_initial_guesses(filename='../data/all_starting_guesses'):
    all_combinations = get_all_combinations()
    all_combinations = filter_lone_zero(all_combinations)
    filename_without_extension = filename.split('.')[0]
    with open(f"{filename_without_extension}.txt", "w") as f:
        for comb in all_combinations:
            f.write(comb + "\n")