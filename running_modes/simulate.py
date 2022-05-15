import random
from alive_progress import alive_bar
from matplotlib import pyplot as plt

from helpers.helper import eval_str_to_cmd, evaluate, load_all_moves
from helpers.main_functions import filter_combinations, get_suggestions


def plot_simulation(ax, tries_dict, avg_tries, i):
    ax.clear()
    ax.set_xlabel('num. tries')
    ax.set_ylabel('freq.')
    bars = ax.bar(tries_dict.keys(), tries_dict.values(), color=(0.2, 0.4, 0.6, 1))
    for p in bars:
        width = p.get_width()
        height = p.get_height()
        x, y = p.get_xy()
        
        plt.text(x+width/2,
                y+height*1.01,
                str(round(height/(i+1)*100, 3))+'%',
                ha='center')
    
    x_disp = (ax.get_xlim()[-1] - ax.get_xlim()[0])*0.98 + ax.get_xlim()[0]
    plt.text(x_disp, 
            ax.get_ylim()[-1]*0.98, 
            'Avg. tries: ' + str(round(avg_tries, 3)), 
            fontsize = 12, 
            ha='right', 
            va='top')

    plt.pause(0.001)

def simulation(n_solutions=None, 
                starting_guess='48-32=16', 
                sug_possibilities_th=100, 
                fig_path='sim_res',
                strategy='best',
                plot_live=False):
    all_possible_combinations = load_all_moves()

    if n_solutions is not None or True:
        random.shuffle(all_possible_combinations)
    random_solutions = all_possible_combinations[:n_solutions]

    tries_dict = {}
    n_tries_lst = []
    avg_tries = 0

    if plot_live:
        _, ax = plt.subplots()

    with alive_bar(len(random_solutions)) as bar:
        for i, solution in enumerate(random_solutions):
            n_tries = 1
            while True:
                if n_tries == 1:
                    possible_combinations = all_possible_combinations
                    guess = starting_guess

                if guess == solution:
                    n_tries_lst.append([solution, n_tries])
                    avg_tries = (avg_tries*i + n_tries)/(i + 1)
                    tries_dict[n_tries] = tries_dict.get(n_tries, 0) + 1


                    if plot_live and i%40 == 0:
                        plot_simulation(ax, tries_dict, avg_tries, i)
                    break

                eval_str = evaluate(guess, solution)
                cmd = eval_str_to_cmd(eval_str, guess)
                possible_combinations = filter_combinations(possible_combinations, cmd)

                if strategy == 'best':
                    guess = get_suggestions(possible_combinations, 
                                            max_combinations=min(sug_possibilities_th, len(possible_combinations)))[0][0]
                elif strategy == 'worst':
                    guess = get_suggestions(possible_combinations, 
                                            max_combinations=min(sug_possibilities_th, len(possible_combinations)))[-1][0]
                elif strategy == 'random':
                    guess = possible_combinations[random.randrange(len(possible_combinations))]

                n_tries += 1

            bar()

    if fig_name:
        _, ax = plt.subplots()
        plot_simulation(ax, tries_dict, avg_tries, i)
        plt.savefig(fig_name.split('.')[0] + '.png')