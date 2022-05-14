'''
Scripts to generate tables in the README.md file
'''

import pandas as pd

best_start_best_sug = [0.006, 9.474, 73.943, 16.024, 0.502, 0.051, 0, 0, 3.077]
best_start_random = [0.006, 9.44, 61.739, 26.13, 2.054, 0.525, 0.096, 0.011, 3.228]
worst_start_random = [0.006, 1.444, 52.722, 12.035, 1.202, 0.361, 0.13, 0.034, 3.812]

best_start_random = [str(val)+'%' if i < len(best_start_random) - 1 else str(val) for i, val in enumerate(best_start_random)]
worst_start_random = [str(val)+'%' if i < len(worst_start_random) - 1 else str(val) for i, val in enumerate(worst_start_random)]

x = ['1', '2', '3', '4', '5', '6', '7', '8', 'Avg. tries']

arr = [
    {x[i]:val for i, val in enumerate(best_start_random)},
    {x[i]:val for i, val in enumerate(worst_start_random)}
]

df = pd.DataFrame(arr, index=['best starter', 'worst starter'])

#################################################################

best_start_best_sug = [0.006, 9.474, 73.943, 16.024, 0.502, 0.051, 0, 0, 3.077]
best_start_random = [0.006, 9.44, 61.739, 26.13, 2.054, 0.525, 0.096, 0.011, 3.228]
times_greater = [round(rand/best, 3) if best != 0 else '\u221e' for rand, best in zip(best_start_random, best_start_best_sug)]
times_greater[-1] = '-'

best_start_random = [str(val)+'%' if i < len(best_start_random) - 1 else str(val) for i, val in enumerate(best_start_random)]
best_start_best_sug = [str(val)+'%' if i < len(best_start_best_sug) - 1 else str(val) for i, val in enumerate(best_start_best_sug)]

x = ['1', '2', '3', '4', '5', '6', '7', '8', 'Avg. tries']

arr = [
    {x[i]:val for i, val in enumerate(best_start_best_sug)},
    {x[i]:val for i, val in enumerate(best_start_random)},
    {x[i]:val for i, val in enumerate(times_greater)}
]

df = pd.DataFrame(arr, index=['algo', 'rand', 'rand/algo'])