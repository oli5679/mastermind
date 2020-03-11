import pytest
import mastermind
import random

game = mastermind.Game([1, 2, 3, 4])


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


"""
def test_solve_game_specific():
    HIDDEN_POSITION = (0, 1, 3, 2, 1)
    res = mastermind.solve_game(HIDDEN_POSITION)

    assert res[0] == tuple(HIDDEN_POSITION) and res[1] < 7



def test_solve_game_specific_2():
    HIDDEN_POSITION = (0, 1, 5, 4,6)
    res = mastermind.solve_game(HIDDEN_POSITION)

    assert res[0] == tuple(HIDDEN_POSITION) and res[1] < 7


def test_solve_game_specific_3():
    HIDDEN_POSITION = (0,0,0,0,0)
    res = mastermind.solve_game(HIDDEN_POSITION)

    assert res[0] == tuple(HIDDEN_POSITION) and res[1] < 7

def test_solve_game_specific_random_1():
    HIDDEN_POSITION = random.sample(range(0, 8), 5)
    res = mastermind.solve_game(HIDDEN_POSITION)
    assert res[0] == tuple(HIDDEN_POSITION) and res[1] < 7

def test_solve_game_specific_random_2():
    HIDDEN_POSITION = random.sample(range(0, 8), 5)
    res = mastermind.solve_game(HIDDEN_POSITION)
    assert res[0] == tuple(HIDDEN_POSITION) and res[1] < 7

def test_solve_game_specific_random_3():
    HIDDEN_POSITION = random.sample(range(0, 8), 5)
    res = mastermind.solve_game(HIDDEN_POSITION)
    assert res[0] == tuple(HIDDEN_POSITION) and res[1] < 7
"""
