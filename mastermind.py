import itertools
import random
from collections import Counter
from functools import lru_cache
import numba


COLOURS = {
    0: "blue",
    1: "green",
    2: "orange",
    3: "pink",
    4: "white",
    5: "yellow",
    6: "green",
    7: "grey",
}


@lru_cache(maxsize=int(1e9))
@numba.njit
def find_guess_results(hidden_position, guess):
    """
    Finds results from guess, given hidden postion

    Args:
        hidden_position (tuple): values hidden from guessing player
        guess (tuple): values guessed by guessing player

    Returns:
        (red (int): exact matches, right colour and position,
        white (int): correct colour, but in wrong position)
    """
    exact_matches = 0

    for i in range(5):
        if guess[i] == hidden_position[i]:
            exact_matches += 1

    value_matches = 0
    for n in range(8):
        guess_c = 0
        hp_c = 0
        for i in range(5):
            if guess[i] == n:
                guess_c += 1
            if hidden_position[i] == n:
                hp_c += 1
        value_matches += min(guess_c, hp_c)

    wrong_position = value_matches - exact_matches
    return exact_matches, wrong_position


def find_guess_results(hidden_position, guess):
    """
    Finds results from guess, given hidden postion

    Args:
        hidden_position (tuple): values hidden from guessing player
        guess (tuple): values guessed by guessing player

    Returns:
        (red (int): exact matches, right colour and position,
        white (int): correct colour, but in wrong position)
    """
    exact_matches = sum([c == g for (c, g) in zip(hidden_position, guess)])
    c1 = Counter(hidden_position)
    c2 = Counter(guess)
    value_matches = sum(min(c1[k], c2.get(k, 0)) for k in c1.keys())
    wrong_position = value_matches - exact_matches
    return exact_matches, wrong_position


class Game:
    """
    Mastermind Game -  https://en.wikipedia.org/wiki/Mastermind_(board_game)
    One player chooses hidden values, the other guesses, and is told information on accuracy of their guess.

    Attributes:
        hidden_choices (list): hidden choices to be guessed - numbers between 0-7
        prev_guesses (list): list of previous guesses of the hidden values - tuples
        prev_guess_results (list): list of results - tuples
        guess (method): get guess results for new guess

    NOTE - for now hardcoded, size 5, with 8 possible values
    """

    def __init__(self, hidden_choices):
        self.hidden_choices = tuple(hidden_choices)
        self.prev_guesses = []
        self.prev_guess_results = []

    def guess(self, guess):
        """
        Guessing player is told:
            (a) number of correct colours in right position
            (b) number of correct colours in the wrong position

        Args:  
            guess (tuple): colours guessed for positions 1-5

        Returns:
            (exact_matches, wrong_position): tuple, number of correct colours in right and wrong position 
        """
        guess_result = find_guess_results(tuple(self.hidden_choices), tuple(guess))
        self.prev_guesses.append(guess)
        self.prev_guess_results.append(guess_result)
        return guess_result


class Solver:
    """
    Filters out invalid board positions from latest guess, then uses minimax heuristic to find guessing strategy

    Attributes:
        guess (tuple): values guessed for positions 1-5
        guess_outcome (exact_matches, wrong_position): tuple, number of correct colours in right and wrong position from this guess
        starting_possible (list): all possible values for hidden values, if None calcualated as all permiuations
        find_strat (method): find a strategy

    """

    def __init__(self, guess, guess_outcome, starting_possible=None):
        if starting_possible is None:
            starting_possible = list(
                itertools.product(range(8), range(8), range(8), range(8), range(8))
            )
            random.shuffle(starting_possible)
        self.possible_choices = self._filter_possible_choices(
            starting_possible, guess, guess_outcome
        )
        self.possible_choice_outcomes = [
            p for p in itertools.product(range(6), range(6)) if sum(p) <= 5
        ]

    def _filter_possible_choices(self, starting_results, guess, guess_outcome):
        """
        Removes hidden choices not possible based on the latest guess

        Args:  
            starting_results (list): results possible before guess
            guess (tuple): latest guess
            guess_outcome (tuple): results of this guess

        Returns:
            possible_results (list): starting results, filtered to exclude those not possible
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

        Returns:
            min_choice (tuple): chosen guess
            min_poss_val (tuple): worst case number of possibilities
            possible_choices (list): valid hidden_choices before the guess
        """
        # placeholders for hidden_choice_count and choice
        min_poss_val = 1e10
        min_choice = None
        # loop through all choices
        for c in self.possible_choices:
            #  placeholder for maximum improvement, starting @ 0
            max_poss = 0
            # loop through all choice outcomes
            for o in self.possible_choice_outcomes:
                # how many hidden choices valid under this choice outcome
                valid_hidden_vals = len(
                    self._filter_possible_choices(self.possible_choices, c, o)
                )
                # update if this is the worst choice outcome yet seen
                max_poss = max(max_poss, valid_hidden_vals)
                # break early if this is already weakly worse than another worst-case for different possible choice
                if max_poss >= min_poss_val:
                    break
            # update if this has the best 'worst-case' yet seen
            if max_poss < min_poss_val:
                min_poss_val = max_poss
                min_choice = c
        # return best found case
        return min_choice, min_poss_val, self.possible_choices


def solve_game(hidden_position):
    """
    Helper method - test how long solver takes, and what it's doing
    """
    g = Game(hidden_position)
    guess_count = 0
    remain_possible = 1e10
    start_possible = None
    guess = tuple(random.sample(range(0, 8), 5))
    print("hidden position")
    print([COLOURS[g] for g in hidden_position])
    while remain_possible > 1:
        guess_count += 1
        res = g.guess(guess)
        guess, remain_possible, start_possible = Solver(
            guess=guess, guess_outcome=res, starting_possible=start_possible
        )()
        print(
            f"""guess {guess_count} \n
            {[COLOURS[g] for g in guess]}
            results {res[0]} red {res[1]} white
              remaining possible {len(start_possible)}"""
        )

    return start_possible[0], guess_count
