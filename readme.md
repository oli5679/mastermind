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
    game = mastermind.Game([1, 2, 3, 4],6,4)

    FIRST_GUESS = (1, 2, 6, 6)
    # make a guess
    guess_result = game.guess(FIRST_GUESS)    

    guess_result
    # 2, 0 since we got two 'red' exactly right (1,2) and no 'white' right counter wrong position

    # get recommendation of best move
    rec = mastermind.find_best_guess(game.all_guesses, game.remaining_possible)
    # (0,0,1,1) pro tip optimal first move is two of two different colours