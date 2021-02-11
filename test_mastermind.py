import pytest
import mastermind
import random

game = mastermind.Game([1, 2, 3, 4], 6, 4)

FIXTURE_SPECIFIC = [(0, 1, 3, 2), (0, 1, 5, 4), (0, 0, 0, 0)]

FIXTURE_RANDOM = [tuple(random.sample(range(5), 3)) for _ in range(5)]


def test_guess_all_right():
    guess_red, guess_white = game.guess((1, 2, 3, 4))

    assert guess_red == 4 and guess_white == 0


def test_guess_none_right():
    guess_red, guess_white = game.guess((6, 6, 6, 6))
    assert guess_red == 0 and guess_white == 0


def test_guess_two_right():
    guess_red, guess_white = game.guess((1, 2, 6, 6))
    assert guess_red == 2 and guess_white == 0


def test_guess_all_right_wrong_order():
    guess_red, guess_white = game.guess((4, 3, 2, 1))
    assert guess_red == 0 and guess_white == 4


@pytest.mark.parametrize("hidden_position", FIXTURE_SPECIFIC)
def test_solve_game_specific(hidden_position):
    print(hidden_position)
    res, count_val = mastermind.solve_game(hidden_position, 6, 4)
    assert res == tuple(hidden_position) and count_val < 7


@pytest.mark.parametrize("hidden_position", FIXTURE_RANDOM)
def test_solve_game_random(hidden_position):
    res, count_val = mastermind.solve_game(hidden_position, 5, 3)
    assert res == tuple(hidden_position) and count_val < 7
