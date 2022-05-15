import argparse
from running_modes.play import play
from running_modes.simulate import simulation
from running_modes.run_bot import run_bot

RUN_BOT = 'run_bot'
SIMULATE = 'simulate'
PLAY = 'play'

# Strategy names
BEST = 'best'
WORST = 'worst'
RANDOM = 'random'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Play Nerdle")
    parser.add_argument('-m',
                        '--mode',
                        help='Run mode. Default run_bot',
                        choices=[RUN_BOT, SIMULATE, PLAY],
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
                            'A lower value will make the simulation quicker, with the expense of not being 100%% optimized' + \
                            'However, if the user chooses a good starting guess (e.g 48-32=16), the default value of 100 ' + \
                            'will probably never be passed. There will always be less than 100 choices.')
    parser.add_argument('--n_solutions', 
                        type=int, 
                        default=None, 
                        help="Number of combinations that will be tested in the simulation." + \
                            "The default None, means that all possibilities (17,723) will be simulated.")
    parser.add_argument('--fig_path', 
                        type=str, 
                        default='data/sim_res', 
                        help="The path of the figure, which will contain the statistics of the simulations. " + \
                            "If the user passes None, then nothing will be saved")
    parser.add_argument('--strategy', 
                        type=str,
                        choices=[BEST, WORST, RANDOM],
                        default=BEST, 
                        help='Strategy type for the algo to simulate.')
    parser.add_argument('--hide_plot_live', 
                        action='store_true',
                        default=False,
                        help="Hide live plot of the statistics of the simulation")
    args = parser.parse_args()

    if args.mode == RUN_BOT:
        run_bot(args.url, args.guess, args.all)
    elif args.mode == SIMULATE:
        simulation(n_solutions=args.n_solutions, 
                    starting_guess=args.guess, 
                    sug_possibilities_th=args.suggestions_th, 
                    fig_path=args.fig_path, 
                    strategy=args.strategy,
                    plot_live=not args.hide_plot_live)
    elif args.mode == PLAY:
        play()