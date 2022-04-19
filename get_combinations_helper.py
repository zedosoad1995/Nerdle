import itertools
import re

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


def has_trailing_zeros(str):
    return any(numbers for numbers in re.split("[^0-9]", str) if len(numbers) > 1 and numbers[0] == '0')
