import random
import os
from sys import exit

#0.5 - changed the way place_ship appends shit to the board list.
#    - built test_ship_gen for testing the for/while loop for building ships
#    - added counter to while loop (20) to keep track of runaway loops until 
#      we have better checks on input.

#0.6 - changed check guess legal to work with dict structure
#    - added hits key in ships dict
#    - added store hit and store miss

#0.7 - added guess function, works well so far.
#    - Changed check_guess_hit, as it was pointlessly making things complicated.
#    - Added turns to the board dict so I can track the number of turns the user 
#      has had. Missing increments this.

#0.8 - pulled together the guess function into a while loop with exit conditions
#    - Lost track.
#    - Changed guess function so no more errors if guess out of scope.
#    - added OS clear, so no more buildup of boards
#    - changed get_guess so it would catch value errors and ask again for input.
#    - changed a few raw_input calls so it would figure out how long the board is.
#    - added get_int_input function for returning 
#      an int value when you pass it a string.
#    - changed test_ship _gen to use the above
#    - changed get_ship_info to do the same
#    - fixed a bug where you could break rand function 
#      by entering a ship larger than board.
#    - removed redundant board placement function
#    - changed gen_board and board_dict to just take the param dict.

#0.9 - added josh's improvements.
#    - Added Doc info to functions

#0.10 - Changed check_guess_legal to remove the unnecessary list and stop using in range()
#     - Removed redundant checks for if something is true.
#     - Used _ instead of i in place_ship_coords as the var is temporary
#     - added vector to ship building dict instead of creating it in another function
#     - built out board dict instead of adding keys one by one.
#     - Improved gen_board so it uses list comprehension.
#     - Ensured ship and param dicts weren't being added one by one.
#     - Changed gen_env to use better string formatting.
#     - changed check_cell_guessed to check object more efficiently.
#     - adjusted place_ship_coords to take argument to be passed explicitly to function.
#     - Changed check_ship_loc for the same reason as above.
#     - changed check_game_over to be nicer and not use exit()
#     - tweaked gen_env to user a better while loop and 
#       raise ship placing exception in else block
#     - cleaned up get guess
#     - Changed place_ship to be less complicated
#     - Rather than storing vector in a string, var 
#       is now called is_vertical and value is True/False
#     - changed get_rand_startpos to return the value, rather than store and return
#     - Renamed guess function to process guess as guess is already a variable.
#     - Changed get_rand_startpos so it is more readable and PEP8 compliant
#     - Changed check_ship_loc to use gen expression. See 19. on improvement list.
#     - Implemented int_input in get_guess
 

def battleships():
    board, ships, param = gen_env()
    
    while True:
        print "You have had %s turns!" % (board['turns'])
        print_board(board['field'])
        process_guess(board, ships)
        if check_game_over(board, ships):
            break
    
    print_board(board['field'])
    print "Congrats. You sunk My Battleship in %s turns" % board['turns']

#Board Functions

def gen_board(param):
    """This function generates the board, accepts the width of the board as an int"""
    board = [["0"] * param for _ in range(param)]
    return board

def board_dict(param):
    """This function is to build out the dict for 
    storing boards and ship coords for collision detection"""
    board = {'field' : gen_board(param), 'ships' : [], 'turns' : 0}
    return board

def print_board(board):		#function for printing the board out pretty
    """Prints the board pretty with -- as border"""
    print "--" * len(board)
    for i in board:
        print " ".join(i)		#join uses list objects without quotes
    print "--" * len(board)

#Ship Functions
    
def place_ship_coords(is_vertical, length, coords):
    """This function builds out the coordinates for the boat based on the variables it 
    takes, board and ship. ship should contain a dict with at least vector, length 
    and coords. Returns ship with updated coords values."""
    if is_vertical == True:
        for _ in range(length-1):
            coords.append((coords[-1][0]+1,coords[-1][1]))
    else:
        for _ in range(length-1):
            coords.append((coords[-1][0],coords[-1][1]+1))
    return coords

def check_ship_loc(coords, ships):
    """This function is used to check the ship's location against existing ships."""
    return all(i not in ships for i in coords)

def place_ship(board, ship):
    """Places the ship in the board so we can later detect hits 
    and total length of the ships"""
    board['ships'].extend(ship['coords'])
    return board

def gen_ship(board, ship_info):
    """takes in board and ship_info, returns board and ship_info. Builds out the ship
    variable by getting random vector and startpos, then building out the tuple coords
    then assigns it to the coords key in board for comparison later. 
    Used by gen_env to build out ships in for loop"""
    ship_info['is_vertical'] = get_rand_vector()
    ship_info['coords'] = get_rand_startpos(board['field'], 
                                            ship_info['is_vertical'], 
                                            ship_info['length'])
    ship_info['coords'] = place_ship_coords(ship_info['is_vertical'], 
    										ship_info['length'], 
    										ship_info['coords'])
    return ship_info

#Get Functions

def get_ship_info(board):
    """Queries the user for information regarding the name of the ship and the length. 
    Also builds the ship dict to be used in later functions"""
    ship = {'length': None, 'name' : None,'coords' : None, 'is_vertical' : None}
    while True:
        ship['length'] = get_int_input("How long do you want ship to be?: ")
        if ship['length'] <= len(board):
            break
        else:
            print "Ship is longer than the board, try again."
    ship['name'] = raw_input("What's the name of this ship?: ")
    return ship

def get_rand_vector():
    """Randomly assigns a vector for the ship."""
    return random.choice([True,False])

def get_rand_startpos(board, is_vertical, ship_length):
    """This function is used for generating a random ship start position. It takes 
    board, ship vector and ship length to determine which coords are valid for 
    generation. Returns the ship pos as a set of coordinates in a tuple."""
    x = random.randrange(0, len(board) - ship_length + 1)
    y = random.randint(0, len(board) - 1)
    return [(x,y)] if is_vertical == True else [(y,x)]

def get_game_params():
    """Collects the size of the board and the number of ships."""
    param = {'boardsize' : get_int_input('How large do you want the board? '),
    		 'ships' : get_int_input('How many ships? ')}
    return param

def get_int_input(question, retry="Please enter a positive integer."):
    """this function is to simplify the process of collecting an int from the user 
    without getting an error."""
    while True:
        try:
            intput = int(raw_input(question))
            return intput
        except ValueError:
            print retry

def get_guess(board):
    """Retrieve the guess from the user. If user enters anything other than positive 
    integer it catches the error and asks again. returns the guess as a tuple."""
    boardlimit = (len(board['field']) - 1)
    guess_col = get_int_input("Guess your col (0 - %s): " % boardlimit,
                              "Please enter a number from 0 to %s: " % boardlimit)
    guess_row = get_int_input("Guess your row (0 - %s): " % boardlimit,
                              "Please enter a number from 0 to %s: " % boardlimit)
    return (guess_row,guess_col)

#Check Functions Here

def check_guess_legal(board, guess):
    """Function to check if guess is legal, returns True or false."""
    return 0 <= guess[0] < len(board['field']) and 0 <= guess[1] < len(board['field'])

def check_guess_hit(board, guess):
    """Checks if the guess is in any of the ship coords. Returns true if yes."""
    return guess in board['ships']

def check_cell_guessed(board, guess):
    """Checks if the guess matches any of the already guessed coords on the board. 
    Returns true if guessed"""
    guess_row, guess_col = guess
    return board['field'][guess_row][guess_col] in ['/', 'X']

def check_game_over(board, ships):
    """Checks if ships['hits'] equals the total length of the ships on the board.
    If game is over exit game with success message"""
    return ships['hits'] == len(board['ships'])

        
#Store Functions:

def store_miss(board, guess):
    """Store miss on the board as a '/'"""
    guess_row, guess_col = guess
    board['field'][guess_row][guess_col] = '/'
    return board

def store_hit(board, ships, guess):
    """Store the hit in the board as an 'X'"""
    guess_row, guess_col = guess
    board['field'][guess_row][guess_col] = 'X'
    ships['hits'] += 1
    return (board, ships)

#Parent Functions Below, pulls together most of the above

def process_guess(board, ships):
    """Gets the guess. Checks it is a legal guess, checks it is not yet guessed,
    checks it's a hit. If anything fails it loops again, collecting guess again.
    returns board and ships. returning ships is for later, when building individual
    ship sinking detection."""
    while True:
        guess = get_guess(board)
        os.system('clear')
        if check_guess_legal(board, guess):
            if not check_cell_guessed(board, guess):
                if check_guess_hit(board, guess):
                    print "Hit!"
                    board, ships = store_hit(board, ships, guess)
                    break
                else:
                    print "Miss!"
                    board = store_miss(board, guess)
                    board['turns'] += 1
                    break
            else:
                print "You already guessed that!"
                print_board(board['field'])
        else:
            print "Sorry, guess out of scope of board, try again."
            print_board(board['field'])
    return (board, ships)

def gen_env():  
    #Ultimately part of battleships()
    param = get_game_params()
    
    board = board_dict(param['boardsize'])
    
    ships = {'hits' : 0}
    counter = 0
    for i in range(1, param['ships'] + 1):
        ship_info = get_ship_info(board['field'])
        while counter <= 20:
            counter += 1
            ship_var = 'ship%s' % i
            ships[ship_var] = gen_ship(board, ship_info)
            if check_ship_loc(ships[ship_var]['coords'], board['ships']):
                board = place_ship(board, ships[ship_var])
                break
        else:
            exit("Counter on placement loop reached 20, maybe something is borken.")
    
    return (board, ships, param)
        
#Boilerplate

if __name__ == '__main__':
    battleships()
