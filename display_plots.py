import matplotlib.pyplot as plt
import pandas as pd

best_start_best_sug = [0.006, 9.474, 73.943, 16.024, 0.502, 0.051, 0, 0, 3.077]
best_start_random = [0.006, 9.44, 61.739, 26.13, 2.054, 0.525, 0.096, 0.011, 3.228]
worst_start_random = [0.006, 1.444, 52.722, 12.035, 1.202, 0.361, 0.13, 0.034, 3.812]

best_start_random = [str(val)+'%' if i < len(best_start_random) - 1 else str(val) for i, val in enumerate(best_start_random)]
worst_start_random = [str(val)+'%' if i < len(worst_start_random) - 1 else str(val) for i, val in enumerate(worst_start_random)]

""" x = [1, 2, 3, 4, 5, 6, 7, 8]
plt.bar([_x-0.2 for _x in x], worst_start_random, width=0.4, color=(0.689, 0, 0))
plt.bar([_x+0.2 for _x in x], best_start_random, width=0.4, color='green')
plt.show() """

x = ['1', '2', '3', '4', '5', '6', '7', '8', 'Avg. tries']

arr = [
    {x[i]:val for i, val in enumerate(best_start_random)},
    {x[i]:val for i, val in enumerate(worst_start_random)}
]

df = pd.DataFrame(arr, index=['best starter', 'worst starter'])
print(df)

""" 
worst = [0.005, 9.255, 44.821, 36.615, 7.699, 1.147, 0.355, 0.104, 3.481]
rnd = [0.005, 8.965, 61.414, 26.754, 2.26, 0.459, 0.12, 0.022, 3.243]
best = [0.005, 9.489, 73.241, 16.555, 0.601, 0.093, 0.016, 0, 3.086]

rnd_worst_start = [0.005, 1.611, 30.445, 53.372, 12.509, 1.42, 0.464, 0.142, 3.838]
rnd_avg_start = [0.005, 5.154, 51.93, 37.554, 4.297, 0.737, 0.24, 0.082, 3.446]
rnd_best_start = [0.005, 8.965, 61.414, 26.754, 2.26, 0.459, 0.12, 0.022, 3.243]
x = [1, 2, 3, 4, 5, 6, 7, 8]

arr = [
    {(i+1):val for i, val in enumerate(best)},
    {(i+1):val for i, val in enumerate(rnd)},
    {(i+1):val for i, val in enumerate(worst)}
]

df = pd.DataFrame(arr, index=['best', 'random', 'worst'])
print(df)

arr = [
    {(i+1):val for i, val in enumerate(rnd_best_start)},
    {(i+1):val for i, val in enumerate(rnd_avg_start)},
    {(i+1):val for i, val in enumerate(rnd_worst_start)}
]

df = pd.DataFrame(arr, index=['best', 'random', 'worst'])
print(df)
 """

""" plt.bar(x, worst)
plt.bar(x, rnd, bottom=worst)
plt.bar(x, best, bottom=[w + z for w, z in zip(worst, rnd)]) """
""" plt.bar([_x-0.1 for _x in x], worst[:8], width=0.1, color='red')
plt.bar(x, rnd[:8], width=0.1, color='orange')
plt.bar([_x+0.1 for _x in x], best[:8], width=0.1, color='green')

plt.plot([_x-0.1 for _x in x], worst[:8], '-o', color='red')
plt.plot(x, rnd[:8], '-o', color='orange')
plt.plot([_x+0.1 for _x in x], best[:8], '-o', color='green')
plt.show()

plt.bar([_x-0.2 for _x in x], rnd_worst_start[:8], width=0.2)
plt.bar(x, rnd_avg_start[:8], width=0.2)
plt.bar([_x+0.2 for _x in x], rnd_best_start[:8], width=0.2)
plt.show()

plt.plot(x, worst[:8], '-o', color='red')
plt.plot(x, rnd[:8], '-o', color='orange')
plt.plot(x, best[:8], '-o', color='green')
plt.show()

plt.plot(x, rnd_worst_start[:8], '-o', color='red')
plt.plot(x, rnd_avg_start[:8], '-o', color='orange')
plt.plot(x, rnd_best_start[:8], '-o', color='green')
plt.show() """