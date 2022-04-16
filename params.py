word_size = 8

all_digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

all_equal_sign_positions = [4, 5, 6]

all_possible_operations = ['*', '/', '+', '-']

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