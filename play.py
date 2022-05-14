import re
from helpers.helper import load_all_moves
from helpers.main_functions import filter_combinations, get_suggestions


def is_cmd_valid(str):
    pattern = re.compile("([0-9+\-*\/=][rgb]\s){7}[0-9][rgb]")
    p = pattern.match(str)
    if p is None and len(str) != 3*7 + 2:
        return None
    
    return p


def play():
    possible_combinations = load_all_moves()
    while True:
        print('Best Guess: 48-32=16')
        cmd = input('Write new cmd: ')
        if is_cmd_valid(cmd) is None:
            print('Invalid command. Example of valid cmd: 4g 8b -r 1g 2g =g 3r 6b\n' + \
                'Must contain 8 slots, and each slot must have 2 characters:\n' + \
                '\t-Digit (0-9) or operations (+-*/=)\n' + \
                '\t-g (green), r (red) or b (black)')
            continue
        possible_combinations = filter_combinations(possible_combinations, cmd)
        print('List of possible combinations:', possible_combinations, len(possible_combinations))

        suggestion = get_suggestions(possible_combinations)[0][0]
        print('Best Guess:', suggestion)