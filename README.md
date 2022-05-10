# Nerdle Solver

The aim of this code is to provide a solver for the game [Nerdle](https://nerdlegame.com/), that can beat the average human, not only in the number of tries, but also in speed.

And to make it "cooler", more visually appealing, and allow the user to rest and watch a robot do its magic for him, we made it so a bot would solve it live.

<p align="center">
<img src="media/nerdle_bot.gif" alt="Nerdle bot"  width="500" />
</p>

The algorithm behind it, makes use of Information Theory techniques, which this [video](https://www.youtube.com/watch?v=v68zYyaEmEA) describes in detail how to do it for the [Wordle](https://wordlegame.org/) game.

Inspired by it, I wanted to try this fascinating mechanism, but with Nerdle.

But what really triggered me to begin this was to beat my family, and ruin their fun ;)

## Rules
Nerdle is a game based on the core idea of Wordle, but using math operations instead of words.

<p align="center">
<img src="media/nerdle.png" alt="Nerdle" width="300"/>
</p>

The basic idea is to guess a mathematically valid operation. For each guess, the computer will assign each character with a color: red, green or black. This will give information about the solution. 

The meaning of each color is the following:
* green - correct character in the right place
* red - correct character in the wrong place
* black - character does not exist

To see more about the rules, check this link: https://faqs.nerdlegame.com/



## Installation

This code uses: 
* Python 3.10.2

To install the requirements, run the following command:
```bash
pip3 install -r requirements.txt
```

## Run bot solver

You can run a robot to solve in real-time a nerdle puzzle on the [official website](https://nerdlegame.com/) with:

```bash
python3 scrape.py
```

You may also run the bot for other nerdle game with:
```bash
python3 scrape.py --url https://instant.nerdlegame.com/
```

for the [instant](https://instant.nerdlegame.com/) version, for example.

Currently we support the [classic](https://nerdlegame.com/), the [instant](https://instant.nerdlegame.com/) and the [speed](https://speed.nerdlegame.com/) game types. The [mini](https://mini.nerdlegame.com/) game type is not yet done.

You may also run the bot to play for previous days. For instance, if you wish to play the instant version from 15/04/2022, you must run:

```bash
python3 scrape.py --url https://instant.nerdlegame.com/20220415
```
## So, what is the best starter?

48-32=16.

From all the possible 17,723 starting combinations the combination with the highest entropy was "48-32=16". You can check all the starters ordered by score in [here](data/all_starting_guesses_scores.csv).

If we simulate using all possible solution, starting with "48-32=16" and always playing the best suggestions from our algorithm, we end up with the following results:

<p align="center">
<img src="data/best_start_best_sug.png" alt="Best Start, best suggestions" width="500"/>
</p>

So, an average of 3.077 tries, where 83.423% of the solutions take 3 or less tries to complete. And zero cases where we lose (more than 6 tries).

#### How much does the starter matter?

Let's forget for a moment the algorithm suggestion. And instead just play randomly, but always starting with the magic number: "48-32=16". 
How much would that matter? And how much better it would be from the worst starter (86*8=688)?

<p align="center">
<img src="data/table_compare_starter_random_suggestions.png" alt="Table starter comparison, random suggestions" width="700"/>
</p>

We can clearly observe that the starter does indeed make a considerable difference. If we compare the best starter vs the worst, we get 9.44% vs 1.44% wins in 2 tries, which means that we are 6.5 times more likely to do it in 2 tries.

#### Importance of the algorithm's suggestion

Now let's analyze the influence of using the top plays that the algorithm suggests.

If we compare using the algorithm vs random plays, we get the following table (both with the starter 48-32=16):

<p align="center">
<img src="data/table_compare_random_best.png" alt="Table random vs algo" width="700"/>
</p>

As we can observe, using our algo does contribute for an improvement from 3.228 to 3.077 average tries. Or in other words, 83.423% vs 71.185% of the times with a win in 3 or less tries.

The number of wins with 2 tries is almost the same. The biggest diffence appearing with more tries. For 4 tries, random choice will happen 1.6 times more often than with the algorithm; 4.1 times more times for 5 tries; and 10.3 times more times for 6 tries. The algorithm gets exponencially better, the longer the game goes on.

#### Just for fun: the worst possible plays

Just for fun, what would be the results for the worst possible plays? This means, the worst starter (86*8=688), combined with the lowest ranked suggestions given by the algorithm.

<p align="center">
<img src="data/worst_start_worst_sug.png" alt="Worst possible play" width="500"/>
</p>

(Being technically accurate, these are the low 1% suggestions, not the worst. As the simulation with the worst suggestion would take a very long time)

