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


def map_indices(str):
    indices = []
    for i, c in enumerate(str):
        if c == '_':
            indices.append(i)

    return indices


def fill_digits(calculation, digits):
    calc = list(calculation)

    digit_pos = 0
    for digit in digits:
        digit_pos = calc.index('_', digit_pos)
        calc[digit_pos] = digit
        digit_pos += 1

    return ''.join(calc)


def get_equal_positions(restrictions):
    all_pos = all_equal_sign_positions.copy()

    if '=' not in restrictions:
        return all_pos

    equal_restrictions = restrictions['=']

    if 'positions' in equal_restrictions:
        all_pos = equal_restrictions['positions']
    elif 'not in positions' in equal_restrictions:
        for pos in equal_restrictions['not in positions']:
            all_pos.remove(pos) 

    return all_pos


def is_invalid_calculation(restrictions, operation, calc):
    restriction = restrictions[operation]
    indices = [i for i, x in enumerate(list(calc)) if x == operation]

    return ('does not exist' in restriction and restriction['does not exist'] and len(indices) > 0) or \
                ('positions' in restriction and not (set(restriction['positions']) <= set(indices))) or \
                ('not in positions' in restriction and set(restriction['not in positions']) & set(indices)) or \
                ('number of instances' in restriction and len(indices) != restriction['number of instances']) or \
                ('number of instances' not in restriction and len(indices) == 0 and 'does not exist' not in restriction)


def filter_operations(calculations, restrictions):
    all_operations = all_possible_operations.copy()

    filtered_calculations = []

    for calc in calculations:
        is_valid = True

        for operation in all_operations:
            if operation not in restrictions:
                continue

            if is_invalid_calculation(restrictions, operation, calc):
                is_valid = False
                break

        if not is_valid:
            continue

        filtered_calculations.append(calc)

    return filtered_calculations


def get_valid_digits(restrictions, mapped_indices):
    valid_digits = []

    for i, mapped_idx in enumerate(mapped_indices):
        valid_digits.append([])
        for digit in all_digits:
            if digit not in restrictions:
                valid_digits[i].append(digit)
                continue

            digit_restrictions = restrictions[digit]

            if 'does not exist' in digit_restrictions and digit_restrictions['does not exist']:
                continue

            if 'not in positions' in digit_restrictions and mapped_idx in digit_restrictions['not in positions']:
                continue

            if 'positions' in digit_restrictions and mapped_idx in digit_restrictions['positions']:
                valid_digits[i] = [digit]
                break

            valid_digits[i].append(digit)

    return valid_digits

def is_valid_digits(calculation, restrictions, valid_digits):
    for digit in valid_digits:
        if digit not in restrictions:
            continue

        if is_invalid_calculation(restrictions, digit, calculation):
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