import itertools
from utils import (
    get_operation_combinations, 
    fill_digits, get_equal_positions, 
    filter_operations_positions, 
    get_valid_digits, 
    is_valid_digits,
    has_result_valid_digits
)

word_size = 8

all_digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

operations = [
    {
        "equal_sign_pos": 4,
        "symbols": ["+", "*"],
        "positions": [[1], [2]]
    },
    {
        "equal_sign_pos": 5,
        "symbols": ["+", "*", "-", "/"],
        "positions": [[1], [2], [3], [1, 3]]
    },
    {
        "equal_sign_pos": 6,
        "symbols": ["+", "*", "-", "/"],
        "positions": [[3], [1, 3], [1, 4], [2, 4]]
    }
]

restrictions = {
    "=": {
        'positions': [5]
    },
    "+": {
        'not in positions': [1, 3],
        'number of instances': 1,
        'positions': [2]
    },
    "*": {
        "does not exist": True
    },
    "-": {
        "does not exist": True
    },
    "/": {
        "does not exist": True,
    },
    "0": {
        "does not exist": True,
    },
    "1": {
        'not in positions': [2, 6, 7],
        'positions': [3]
    },
    "2": {
        "does not exist": True,
    },
    "3": {
        'not in positions': [0],
        'positions': [4],
        'number of instances': 1,
    },
    "4": {
        'not in positions': [2, 6]
    },
    "5": {
        "does not exist": True,
    },
    "6": {
        'not in positions': [5],
        'positions': [0]
    },
    "7": {
        'not in positions': [0, 2],
        'positions': [6]
    },
    "8": {
        "does not exist": True,
    },
    "9": {
        "does not exist": True,
    },
}

possible_operation_combinations = []

for equal_sign_pos in get_equal_positions(restrictions):
    calculation_str = '_' * equal_sign_pos
    operations_obj = next((op for op in operations if op['equal_sign_pos'] == equal_sign_pos), None)

    for positions in operations_obj['positions']:
        possible_operation_combinations.extend(get_operation_combinations(calculation_str, positions, operations_obj['symbols']))

possible_operation_combinations = filter_operations_positions(possible_operation_combinations, restrictions)

pos = 0
for base_calculation_str in possible_operation_combinations:

    valid_digits = get_valid_digits(all_digits, restrictions)

    digits_combinations = list(itertools.product(*([valid_digits] * base_calculation_str.count('_'))))
    
    for digits in digits_combinations:
        calc = fill_digits(base_calculation_str, digits)

        try:
            res = eval(calc)
            if res == 67:
                pass
            if not (isinstance(res, int) or res.is_integer()) or word_size - 1 - len(str(int(res))) != len(base_calculation_str) or res < 0:
                continue

            full_calculation = f'{calc}={int(res)}'

            if not is_valid_digits(full_calculation, restrictions, valid_digits):
                continue

            if not has_result_valid_digits(str(res), restrictions):
                continue

            print(full_calculation)
        except:
            pass


