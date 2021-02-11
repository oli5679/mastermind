import itertools
import random
from collections import Counter
from functools import lru_cache
import logging
import datetime
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)

"""Mastermind

Tools for playing the game Mastermind - https://en.wikipedia.org/wiki/Mastermind_(board_game)

Including minimax solver

Classes:
    Game - keeps track of mastermind game's state
    Solver - minimax filter to find best guesses for game

Functions:
    solve_game - finds guess strategy from starting position (useful for performance measurement)
"""

COLOURS = {
    0: "blue",
    1: "green",
    2: "orange",
    3: "pink",
    4: "white",
    5: "yellow",
}

NUM_COLOURS, NUM_CELLS = 6, 4  # also requires tweak to itertools.product


def find_guess_results(hidden_position, guess):
    """
    Finds results from guess, given hidden postion
    """
    exact_matches = sum((c == g for (c, g) in zip(hidden_position, guess)))
    counter_hidden = Counter(hidden_position)
    counter_guess = Counter(guess)
    value_matches = sum(
        min(counter_hidden[k], counter_guess.get(k, 0)) for k in counter_hidden.keys()
    )
    wrong_position = value_matches - exact_matches
    return exact_matches, wrong_position


class Game:
    """
    Mastermind Game -  https://en.wikipedia.org/wiki/Mastermind_(board_game)
    One player chooses hidden values, the other guesses, and is told information on accuracy of their guess.
    """

    def __init__(self, hidden_choices):
        self.hidden_choices = tuple(hidden_choices)
        self.prev_guesses = []

    def guess(self, guess):
        """
        Guessing player is told:
            (a) number of correct colours in right position
            (b) number of correct colours in the wrong position
        """
        guess_result = find_guess_results(tuple(self.hidden_choices), tuple(guess))
        self.prev_guesses.append((guess, guess_result))
        return guess_result


class Solver:
    """
    Filters out invalid board positions from latest guess, then uses minimax heuristic to find guessing strategy
    """

    def __init__(self, guess, guess_outcome, starting_possible=None):
        if starting_possible is None:
            starting_possible = list(
                itertools.product(
                    range(NUM_COLOURS),
                    range(NUM_COLOURS),
                    range(NUM_COLOURS),
                    range(NUM_COLOURS),
                )
            )
            random.shuffle(starting_possible)
        self.possible_choices = self._filter_possible_choices(
            starting_possible, guess, guess_outcome
        )
        self.possible_choice_outcomes = [
            p for p in itertools.product(range(6), range(6)) if sum(p) <= 4
        ]

    def _filter_possible_choices(self, starting_results, guess, guess_outcome):
        """
        Removes hidden choices not possible based on the latest guess
        """
        return [
            r for r in starting_results if find_guess_results(guess, r) == guess_outcome
        ]

    def __call__(self):
        """
        Finds the strategy that leads to largest reduction in possible hidden choices, in the worst case scenario
        (1) Loop through all possible guesses
        (2) Loop through all responses you could recieve from these guesses
        Find the largest worst-case improvement
        """
        min_poss_val, min_choice = (
            1e10,
            None,
        )  # placeholders for hidden_choice_count and choice
        for c in self.possible_choices:  # loop through all choices
            max_poss = 0  #  placeholder for maximum improvement, starting @ 0
            for o in self.possible_choice_outcomes:  # loop through all choice outcomes
                valid_hidden_vals = len(
                    self._filter_possible_choices(self.possible_choices, c, o)
                )  # how many hidden choices valid under this choice outcome

                max_poss = max(
                    max_poss, valid_hidden_vals
                )  # update if this is the worst choice outcome yet seen

                if max_poss >= min_poss_val:
                    break  # break early if this is already weakly worse than another worst-case for different possible choice
            if (
                max_poss < min_poss_val
            ):  # update if this has the best 'worst-case' yet seen
                min_poss_val = max_poss
                min_choice = c
        # return best found case
        return min_choice, min_poss_val, self.possible_choices


def solve_game(hidden_position):
    """
    Helper method - test how long solver takes, and what it's doing
    """
    g = Game(hidden_position)
    guess_count, remain_possible, start_possible = 0, 1e10, None
    guess = tuple(random.sample(range(0, NUM_COLOURS), NUM_CELLS))
    logging.debug("hidden position")
    logging.debug([COLOURS[g] for g in hidden_position])
    while remain_possible > 1:
        guess_count += 1
        res = g.guess(guess)
        guess, remain_possible, start_possible = Solver(
            guess=guess, guess_outcome=res, starting_possible=start_possible
        )()
        logging.debug(
            f"""guess {guess_count} \n
            {[COLOURS[g] for g in guess]}
            results {res[0]} red {res[1]} white
              remaining 
              possible {len(start_possible)}"""
        )
    logging.debug(f"Solution {[COLOURS[c] for c in start_possible[0]]}")
    return start_possible[0], guess_count


if __name__ == "__main__":
    start = datetime.datetime.now()
    solve_guesses = 0
    for _ in tqdm(range(1000)):
        pos = tuple(random.sample(range(0, NUM_COLOURS), NUM_CELLS))
        _, c = solve_game(pos)
        solve_guesses += c
    print(f"guesses {solve_guesses/ 1000}")
    end = datetime.datetime.now()
    print(f"time {(end-start).total_seconds()}")
