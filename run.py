import argparse
from main import simulation

from scrape import scrape

SCRAPE = 'scrape'
SIMULATE = 'simulate'

# Strategy names
BEST = 'best'
WORST = 'worst'
RANDOM = 'random'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Play Nerdle")
    parser.add_argument('-m',
                        '--mode',
                        help='Run mode. Default scrape',
                        choices=[SCRAPE, SIMULATE],
                        default=None,
                        required=True)
    parser.add_argument('--url', 
                        type=str, 
                        default='https://nerdlegame.com/', 
                        help="Nerdle Url for the bot to play the game")
    parser.add_argument('--guess', 
                        type=str, 
                        default='48-32=16', 
                        help="Initial guess. The default value is the best starting value we've found out")
    parser.add_argument('-a', 
                        '--all', 
                        action='store_true', 
                        help="Flag to run all daily games")
    parser.add_argument('--suggestions_th', 
                        type=int, 
                        default=100, 
                        help='Max number of possible combinations that the algo will consider.' + \
                            'If None is passed, then there is no limit.' + \
                            'The reasone for this parameter to exist, is to make the simulation faster.' + \
                            'A lower value will make the simulation quicker, with the expense of not being 100% optimized' + \
                            'However, if the user chooses a good starting guess (e.g 48-32=16), the default value of 100 ' + \
                            'will probably never be passed. There will always be less than 100 choices.')
    parser.add_argument('--n_solutions', 
                        type=int, 
                        default=None, 
                        help="Number of combinations that will be tested in the simulation." + \
                            "The default None, means that all possibilities (17,723) will be simulated.")
    parser.add_argument('--fig_name', 
                        type=str, 
                        default='sim_res', 
                        help="The name of the figure, which will contain the statistics of the simulations." + \
                            "If the user passes None, then nothing will be saved")
    parser.add_argument('--strategy', 
                        type=str,
                        choices=[BEST, WORST, RANDOM],
                        default=BEST, 
                        help='Strategy type for the algo to simulate.')
    parser.add_argument('--plot_live', 
                        action='store_true',
                        default=False,
                        help="Allows to see a plot of the statistics of the simulation live")
    args = parser.parse_args()

    if args.mode == SCRAPE:
        scrape(args.url, args.guess, args.all)
    elif args.mode == SIMULATE:
        simulation(n_solutions=args.n_solutions, 
                    starting_guess=args.guess, 
                    sug_possibilities_th=args.suggestions_th, 
                    fig_name=args.fig_name, 
                    strategy=args.strategy,
                    plot_live=args.plot_live)