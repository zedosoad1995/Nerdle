import itertools
import re
from params import all_equal_sign_positions, all_possible_operations, all_digits

def get_operation_combinations(calculation, positions, symbols):
    possible_calculations = []

    possible_combinations = list(itertools.product(*([symbols] * len(positions))))

    for symbols in possible_combinations:
        calc = list(calculation)
        for i, symbol in enumerate(symbols):
            pos = positions[i]
            calc[pos] = symbol
        
        possible_calculations.append("".join(calc))

    return possible_calculations


def fill_digits(calculation, digits):
    calc = list(calculation)

    digit_pos = 0
    for digit in digits:
        digit_pos = calc.index('_', digit_pos)
        calc[digit_pos] = digit
        digit_pos += 1

    return ''.join(calc)


def get_equal_positions(restrictions):
    all_pos = all_equal_sign_positions

    if '=' not in restrictions:
        return all_pos

    equal_restrictions = restrictions['=']

    if 'positions' in equal_restrictions:
        all_pos = equal_restrictions['positions']
    elif 'not in positions' in equal_restrictions:
        for pos in equal_restrictions['not in positions']:
            all_pos.remove(pos) 

    return all_pos


def is_invalid_calculation(restrictions, indices):
    return ('does not exist' in restrictions and restrictions['does not exist'] and len(indices) > 0) or \
                ('positions' in restrictions and not (set(restrictions['positions']) <= set(indices))) or \
                ('not in positions' in restrictions and set(restrictions['not in positions']) & set(indices)) or \
                ('number of instances' in restrictions and len(indices) != restrictions['number of instances'])


def filter_operations(calculations, restrictions):
    all_operations = all_possible_operations

    filtered_calculations = []

    for calc in calculations:
        is_valid = True

        for operation in all_operations:
            if operation not in restrictions:
                continue

            op_restrictions = restrictions[operation]
            op_indices = [i for i, x in enumerate(list(calc)) if x == operation]

            if is_invalid_calculation(op_restrictions, op_indices):
                is_valid = False
                break

        if not is_valid:
            continue

        filtered_calculations.append(calc)

    return filtered_calculations


def get_valid_digits(restrictions):
    valid_digits = []

    for digit in all_digits:
        if digit not in restrictions:
            valid_digits.append(digit)
            continue

        digit_restrictions = restrictions[digit]

        if 'does not exist' in digit_restrictions and digit_restrictions['does not exist']:
            continue

        valid_digits.append(digit)

    return valid_digits

def is_valid_digits(calculation, restrictions, digits):
    for digit in digits:
        if digit not in restrictions:
            continue

        digit_restrictions = restrictions[digit]
        digit_indices = [i for i, x in enumerate(list(calculation)) if x == digit]

        if is_invalid_calculation(digit_restrictions, digit_indices):
            return False

    return True


def has_result_valid_digits(result, restrictions):
    for digit in result:
        if digit not in restrictions:
            continue

        digit_restrictions = restrictions[digit]

        if 'does not exist' in digit_restrictions and digit_restrictions['does not exist']:
            return False

    return True

def has_trailing_zeros(str):
    return any(numbers for numbers in re.split("[^0-9]", str) if len(numbers) > 1 and numbers[0] == '0')