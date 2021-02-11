import random
from collections import Counter
import logging
import datetime
from copy import copy
from functools import lru_cache
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)

"""
Minimax solver for game of Mastermind

https://en.wikipedia.org/wiki/Mastermind_(board_game)
"""


@lru_cache(1000)
def get_all_combs(num_colours: int, num_cells: int) -> list:
    if num_cells == 1:
        return [[x] for x in range(num_colours)]
    else:
        return [[x] + c for x in range(num_colours) for c in get_all_combs(num_colours, num_cells - 1)]

def find_guess_results(hidden_position: tuple, guess: tuple) -> tuple:
    """
    Finds results from guess, given hidden postion
    """
    exact_matches = sum((c == g for (c, g) in zip(hidden_position, guess)))
    counter_hidden = Counter(hidden_position)
    counter_guess = Counter(guess)
    value_matches = sum(
        min(counter_hidden[k], counter_guess.get(k, 0)) for k in counter_hidden.keys()
    )
    return exact_matches, value_matches - exact_matches


class Game:
    """
    Mastermind Game -  https://en.wikipedia.org/wiki/Mastermind_(board_game)
    One player chooses hidden values, the other guesses, and is told information on accuracy of their guess.
    """

    def __init__(self, hidden_choices: tuple, num_colours: int, num_cells: int):
        self.hidden_choices = tuple(hidden_choices)
        self.prev_guesses = []
        self.remaining_possible = random.sample(
            [tuple(x) for x in get_all_combs(num_colours, num_cells)],
            num_colours ** num_cells,
        )
        self.all_guesses = copy(self.remaining_possible)

    def guess(self, guess: tuple) -> tuple:
        """
        Guessing player is told:
            (a) number of correct colours in right position
            (b) number of correct colours in the wrong position
        """
        guess_result = find_guess_results(tuple(self.hidden_choices), tuple(guess))
        self.prev_guesses.append((guess, guess_result))
        self.remaining_possible = [p for p in self.remaining_possible if find_guess_results(p, guess) == guess_result]
        return guess_result


def find_best_guess(all_moves: list, remaining_valid: list) -> tuple:
    """
    Finds the strategy that leads to largest reduction in possible hidden choices, in the worst case scenario
        (1) Loop through all possible guesses
        (2) Loop through all responses you could recieve from these guesses
    Find the largest worst-case improvement
    """
    minimax_val, minimax_choice = 1e10, None # placeholders for hidden_choice_count and choice
    for m in all_moves:  # loop through all choices
        poss_counts = Counter()
        for o in remaining_valid:  # loop through all choice outcomes
            guess_outcome = find_guess_results(o, m)
            poss_counts[guess_outcome] += 1
            if poss_counts[guess_outcome] >= minimax_val:
                break  # break early if this is already weakly worse than another worst-case for different possible choice
        max_poss = max(poss_counts.values())
        if max_poss < minimax_val:  # update if this has the best 'worst-case' yet seen
            minimax_val, minimax_choice = max_poss, m
    return minimax_choice


def solve_game(hidden_position: tuple, num_colours: int, num_cells: int) -> int:
    """
    Helper method - test how long solver takes, and what it's doing
    """
    g = Game(hidden_position, num_colours, num_cells)
    guess_count = 0
    logging.info(f"hidden position {hidden_position}")
    while len(g.remaining_possible) > 1:
        recommendation = find_best_guess(g.all_guesses, g.remaining_possible)
        logging.info(recommendation)
        guess_count += 1
        res = g.guess(recommendation)
    assert g.remaining_possible[0] == hidden_position
    return g.remaining_possible[0], guess_count


NUM_COLOURS, NUM_CELLS = 6, 4
if __name__ == "__main__":
    start = datetime.datetime.now()
    solve_guesses = 0
    for _ in tqdm(range(5)):
        pos = tuple(random.sample(range(0, NUM_COLOURS), NUM_CELLS))
        final_pos, guess_count = solve_game(pos, NUM_COLOURS, NUM_CELLS)
        solve_guesses += guess_count
    logging.info(f"guesses {solve_guesses/ 50}")
    end = datetime.datetime.now()
    logging.info(f"time {(end-start).total_seconds()}")
