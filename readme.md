# Mastermind

Tools for playing the game Mastermind - https://en.wikipedia.org/wiki/Mastermind_(board_game)

Including minimax solver

## Prerequesites

Python 3+, see here one way to install https://docs.anaconda.com/anaconda/install/

## Getting started

    pip install -r requirements.txt

## Running tests

    pytest .

## Examples

    import mastermind
    
    # create a game
    game = mastermind.Game([1, 2, 3, 4])

    FIRST_GUESS = (1, 2, 6, 6)
    # make a guess
    guess_result = game.guess(FIRST_GUESS)    

    guess_result
    # 2, 0 since we got two 'red' exactly right (1,2) and no 'white' right counter wrong position

    # get remaining possible positions and next optimal guess, given a guess
    second_guess, remain_possible, start_possible = mastermind.Solver(
            guess=FIRST_GUESS, guess_outcome=guess_result
        )()

    # can also account for previous guesses by passing in 'starting_possible'
    second_guess_result = game.guess(second_guess)
    third_guess, second_remain_possible, second_start_possible = mastermind.Solver(
            guess=FIRST_GUESS, guess_outcome=guess_result
        )()
