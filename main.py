import itertools
from get_combinations_helper import (
    get_operation_combinations, 
    fill_digits, get_equal_positions, 
    filter_operations, 
    get_valid_digits, 
    is_valid_digits,
    has_result_valid_digits
)
from params import word_size, operations

restrictions = {
    "=": {
        'positions': [5]
    },
    "+": {
        'not in positions': [1, 3],
        'number of instances': 1,
        'positions': [2]
    },
    "9": {
        "does not exist": True,
    },
}

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

        valid_digits = get_valid_digits(restrictions)
        digits_combinations = list(itertools.product(*([valid_digits] * calculation_str.count('_'))))
        
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

            full_calculation = f'{calc}={int(result)}'

            if not is_valid_digits(full_calculation, restrictions, valid_digits) or \
                not has_result_valid_digits(str(result), restrictions):
                continue

            possible_combinations.append(full_calculation)

    return possible_combinations

print(get_possible_combinations(restrictions))