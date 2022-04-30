# Nerdle Solver

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

You may also run the bot for other nerdle game type:
```bash
python3 scrape.py --url https://instant.nerdlegame.com/
```

for the [instant](https://instant.nerdlegame.com/) version, for example.

Currently we support the [classic](https://nerdlegame.com/), the [instant](https://instant.nerdlegame.com/) and the [speed](https://speed.nerdlegame.com/) game type. The [mini](https://mini.nerdlegame.com/) game type is not yet done.

You may also run the bot to play for previous days. For instance, if you wish to play the instant version from 15/04/2022, you must run:

```bash
python3 scrape.py --url https://instant.nerdlegame.com/20220415
```
