#scrabble game logic
import random
from copy import deepcopy

class Constants:
    LETTERS = ['blank', 'blank', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E',
               'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'I', 'I', 'I', 'I', 'I', 'I', 'I',
               'I', 'I', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'N', 'N', 'N', 'N', 'N', 'N',
               'R', 'R', 'R', 'R', 'R', 'R', 'T', 'T', 'T', 'T', 'T', 'T', 'L', 'L', 'L', 'L',
               'S', 'S', 'S', 'S', 'U', 'U', 'U', 'U', 'D', 'D', 'D', 'D', 'G', 'G', 'G', 'B',
               'B', 'C', 'C', 'M', 'M', 'P', 'P', 'F', 'F', 'H', 'H', 'V', 'V', 'W', 'W', 'Y',
               'Y', 'K', 'J', 'X', 'Q', 'Z']

    def make_letters_points():
        D = dict()
        D['blank'] = 0
        D['A'] = 1
        D['B'] = 3
        D['C'] = 3
        D['D'] = 2
        D['E'] = 1
        D['F'] = 4
        D['G'] = 2
        D['H'] = 4
        D['I'] = 1
        D['J'] = 8
        D['K'] = 5
        D['L'] = 1
        D['M'] = 3
        D['N'] = 1
        D['O'] = 1
        D['P'] = 3
        D['Q'] = 10
        D['R'] = 1
        D['S'] = 1
        D['T'] = 1
        D['U'] = 1
        D['V'] = 4
        D['W'] = 4
        D['X'] = 8
        D['Y'] = 4
        D['Z'] = 10
        return D

    LETTER_POINTS = make_letters_points()

    BOARD = [['3W', ' ', ' ', '2L', ' ', ' ', ' ', '3W', ' ', ' ', ' ', '2L', ' ', ' ', '3W'],
             [' ', '2W', ' ', ' ', ' ', '3L', ' ', ' ', ' ', '3L', ' ', ' ', ' ', '2W', ' '],
             [' ', ' ', '2W', ' ', ' ', ' ', '2L', ' ', '2L', ' ', ' ', ' ', '2W', ' ', ' '],
             ['2L', ' ', ' ', '2W', ' ', ' ', ' ', '2L', ' ', ' ', ' ', '2W', ' ', ' ', '2L'],
             [' ', ' ', ' ', ' ', '2W', ' ', ' ', ' ', ' ', ' ', '2W', ' ', ' ', ' ', ' '],
             [' ', '3L', ' ', ' ', ' ', '3L', ' ', ' ', ' ', '3L', ' ', ' ', ' ', '3L', ' '],
             [' ', ' ', '2L ', ' ', ' ', ' ', '2L', ' ', '2L', ' ', ' ', ' ', '2L', ' ', ' '],
             ['3W', ' ', ' ', '2L', ' ', ' ', ' ', 'STAR', ' ', ' ', ' ', '2L', ' ', ' ', '3W'],
             [' ', ' ', '2L ', ' ', ' ', ' ', '2L', ' ', '2L', ' ', ' ', ' ', '2L', ' ', ' '],
             [' ', '3L', ' ', ' ', ' ', '3L', ' ', ' ', ' ', '3L', ' ', ' ', ' ', '3L', ' '],
             [' ', ' ', ' ', ' ', '2W', ' ', ' ', ' ', ' ', ' ', '2W', ' ', ' ', ' ', ' '],
             ['2L', ' ', ' ', '2W', ' ', ' ', ' ', '2L', ' ', ' ', ' ', '2W', ' ', ' ', '2L'],
             [' ', ' ', '2W', ' ', ' ', ' ', '2L', ' ', '2L', ' ', ' ', ' ', '2W', ' ', ' '],
             [' ', '2W', ' ', ' ', ' ', '3L', ' ', ' ', ' ', '3L', ' ', ' ', ' ', '2W', ' '],
             ['3W', ' ', ' ', '2L', ' ', ' ', ' ', '3W', ' ', ' ', ' ', '2L', ' ', ' ', '3W']]


#helper methods for dealing with coordinates
def get_direction(coord1, coord2):
    if coord1[0] == coord2[0]:
        return 'y'
    else:
        return 'x'

def opposite_direction(direction):
    if direction == 'x':
        return 'y'
    else:
        return 'x'

def incr_coord(coord, direction):
        if direction == 'x':
            return (coord[0]+1, coord[1])
        else:
            return (coord[0], coord[1]+1)

def decr_coord(coord, direction):
    if direction == 'x':
        return (coord[0]-1, coord[1])
    else:
        return (coord[0], coord[1]-1)

def compare_coords(coord1, coord2):
        if coord1[1]==coord2[1]:
            if coord1[0]>=coord2[0]:
                return coord1
            else:
                return coord2
        else:
            if coord1[1]>=coord2[1]:
                return coord1
            else:
                return coord2


class Game:
    def __init__(self):
        self.board = Board()
        self.bag = Bag()
        self.player1 = Player(self.bag.draw(7))
        self.player2 = Player(self.bag.draw(7))
        self.turn = None
        self.last_word = (None, 0)
        self.end = 0

    
    #checks if the game is over and returns the winner if it is
    def end_check(self):
        if end == 2:
            if self.player1.score > self.player2.score:
                return player1
            elif self.player2.score> self.player1.score:
                return player2
            else:
                return "tie"

    #dumps specified letters of turn and switches turn
    #addes to end counter if the bag is empty
    def dump(self, letters):
        if not self.bag.empty:
            for let in letters:
                self.turn.tray.remove(let)
                self.bag.letters.append(let)
            self.turn.draw(self.bag)
        else:
            self.end+=1

        if self.turn == self.player1:
            self.turn = self.player2
        else:
            self.turn = self.player1

    #picks who goes first
    def pick_order(self):
        blank = True
        while blank:
            let1, let2 = self.bag.pick_order_letter()
            if let1 != 'blank' and let2 != 'blank':
                blank = False
        
        if let1>let2:
            self.turn = self.player2
            return (self.player2, let1, let2)
        elif let1<let2:
            self.turn = self.player1
            return (self.player1, let1, let2)
        else:
            return self.pick_order()

    #takes in a word dictionary and returns a list of the letters, the first coordinate, and the last coordinate
    #output goes in to player method for placing the word
    def find_start_and_end(self, word):
        start = None
        end = None
        word_list = []
        for let, coord_set in word.items():
            for coord in coord_set:
                word_list.append(let)
                if start is None:
                    start = coord
                    end = coord
                elif compare_coords(start, coord) == start:
                    start = coord
                elif compare_coords(end, coord) == coord:
                    end = coord

        direction = get_direction(start, end)
        extend = True
        temp_start = decr_coord(start, direction)
        while extend:
            if not self.board.check_spot(temp_start):
                start = temp_start
                temp_start = decr_coord(start, direction)
            else:
                extend = False

        extend = True
        temp_end = incr_coord(end, direction)
        while extend:
            if not self.board.check_spot(temp_end):
                end = temp_end
                temp_end = incr_coord(end, direction)
            else:
                extend = False

        return start, end, word_list

    #executes one turn that isn't a pass
    #word is dictionary mapping letters to coordinates
    def play(self, word):
        start, end, word_list = self.find_start_and_end(word)
        self.turn.place_word(self.board, word_list, start, end)       

    #takes the last word off the board if the challenge is successful
    #draws for the player that just played
    #switches the turn since time for challenging has passed
    def challenge(self, valid):
        if valid:
            self.turn.retract_word(self.board)
            return self.turn

        self.turn.draw(self.bag)

        if self.turn == self.player1:
            self.turn = self.player2
        else:
            self.turn = self.player1


class Bag:
    def __init__(self, D=None):
        self.empty = False
        self.letters_points = deepcopy(Constants.BOARD)
        if D is not None:
            self.letters = D
        else:
            self.letters = Constants.LETTERS.copy()

    #randomly removes the given number of letters from the bag
    def draw(self, num_draw):
        result = []

        if self.empty:
            return result

        for i in range(num_draw):
            if len(self.letters) == 0:
                self.empty = True
                return result
            ind = random.randint(0, len(self.letters)-1)
            result.append(self.letters.pop(ind))
        return result

    #draws a letter from the bag for both players and replaces it
    def pick_order_letter(self):
        ind1 = random.randint(0, len(self.letters)-1)
        ind2 = random.randint(0, len(self.letters)-1)
        if ind1 == ind2:
            return self.pick_order_letter()
        else:
            let1 = self.letters[ind1]
            let2 = self.letters[ind2]
            return (let1, let2)


class Player:
    def __init__(self, letters):
        #letters should be the result of a draw call of 7 to Bag
        self.tray = letters.copy()
        self.score = 0

        self.last_word = None
        #self.last_coords = None
        self.last_score = None

    #puts a word with specified start and end on the board
    #word is the letters from the player's tray - function will account for letters already on the board
    #removes used letters from tray
    #assumes that word is selected from the tray
    #DOESN'T DRAW AT THE END - NEEDS GAME TO CALL THIS COMMAND ONCE CHALLENGE IS SETTLED

    def place_word(self, board, word, start, end):
        points = 0
        side_points = 0
        direction = 'x'
        modifiers = set()
        self.last_word = dict()

        #determines whether the word is vertical or horizontal
        if start[0] == end[0]:
            direction = 'y'

        #places each letter, checks for modifiers, checks for sidewords, adds points for sidewords
        coord = start
        last_coord = None
        ind = -1
        board_val = None

        while coord[0]<=end[0] and coord[1]<=end[1]:
            if board_val != 'taken':
                ind+=1
                try:
                    letter = word[ind]
                except IndexError:
                    if coord != end:
                        raise ValueError("Bad word or bad coordinates - Index out of range!")
            
            output = self.get_let_points(board, letter, coord)
            points += output[0]
            modifiers.update(output[1])
            board_val = output[2]

            if board_val != 'taken' and len(board.check_adjacent(coord, {last_coord, incr_coord(coord, direction)}))>0:
                side_val = self.calc_sideword(board, coord, direction, board_val, output[0])
                side_points += side_val

            if board_val != 'taken':
                if letter in self.last_word:
                    self.last_word[letter].add(coord)
                else:
                    self.last_word[letter] = {coord}
            
            last_coord = coord
            coord = incr_coord(coord, direction)

        #calculates total score
        mult = 1
        for mod in modifiers:
            if mod == 'STAR':
                mult = mult*2
            else:
                mult = mult*int(mod[0])

        #adds modified points from original word
        points = points*mult 
        #adds points from sidewords
        points+= side_points
        #adds bonus points for using all letters
        if len(word) == 7:
            points+=50

        #removes used letters from tray
        for letter in word:
            self.tray.remove(letter)

        #adds points
        self.score += points

        #sets up for challenge
        self.last_score = points

    #calculates points for sidewords
    def calc_sideword(self, board, coord, direction, mod, let_point):
        #assumes that one sideword moves in only one direction
        points = let_point
        if direction == 'x':
            new_dir = 'y'
            start_check = (coord[0], coord[1]-1)
            end_check = (coord[0], coord[1]+1)
        else:
            new_dir = 'x'
            start_check = (coord[0]-1, coord[1])
            end_check = (coord[0]+1, coord[1])

        new_start = coord
        while len(board.check_adjacent(start_check, {new_start}))>0:
            temp = start_check
            if new_dir == 'x':
                start_check = (new_start[0]-2, new_start[1])
            else:
                start_check = (new_start[0], new_start[1]-2)
            new_start = temp
            board_val = board.board[new_start[0]][new_start[1]]
            if board_val == " ":
                break
            to_add = Constants.LETTER_POINTS[board_val]
            points += to_add

        new_end = coord
        while len(board.check_adjacent(end_check, {new_end}))>0:
            temp = end_check
            if new_dir == 'x':
                end_check = (new_end[0]+2, new_end[1])
            else:
                end_check = (new_end[0], new_end[1]+2)
            new_end = temp
            board_val = board.board[new_end[0]][new_end[1]]
            if board_val == " ":
                break
            to_add = Constants.LETTER_POINTS[board_val]
            points += to_add

        if mod is not None and type(mod) != str:
            points = points*mod
        return points

    #returns the amount of points for one letter, any modifiers, 
    #and the value of the board at that spot
    def get_let_points(self, board, letter, coord):
        points = Constants.LETTER_POINTS[letter]
        modifiers = set()
        
        try:
            board_val = board.place_letter(letter, coord)
        except ValueError:
            board_val = 'taken'
            L = board.board[coord[0]][coord[1]]
            points = Constants.LETTER_POINTS[L]
        
        if board_val != ' ' and board_val != 'taken':
            if 'W' in board_val or board_val == 'STAR':
                modifiers.add(board_val)
                if board_val == 'STAR':
                    board_val = 2
                else:
                    board_val = int(board_val[0])
            else:
                mult = int(board_val[0])
                points = points*mult
                board_val = None

        return points, modifiers, board_val

    #undoes the last action in the case of a successful challenge
    def retract_word(self, board):
        #code to take the last action off the board
        for let, coord_set in self.last_word.items():
            for coord in coord_set:
                self.tray.append(let)
                board.remove_letter(let, coord)

        #this code returns player states
        self.score -= self.last_score

        self.last_word = None
        self.last_score = None

    #adds an amount of letters from the bag to the tray to make 7
    #removes those letters from the bag
    def draw(self, bag):
        to_draw = 7-len(self.tray)
        self.tray.extend(bag.draw(to_draw))



class Board:
    def __init__(self):
        self.board = deepcopy(Constants.BOARD)

    #puts a letter on the board in the specified spot
    def place_letter(self, letter, coord):
        x = coord[0]
        y = coord[1]
        board_val = self.board[x][y]

        if self.check_spot(coord):
            self.board[x][y] = letter
            return board_val
        else:
            raise ValueError('There is already a letter at that spot! ' + str(coord))

    #removes a given letter from the board in the case of successful challenge
    def remove_letter(self, letter, coord):
        x = coord[0]
        y = coord[1]
        board_val = Constants.BOARD[x][y]
        self.board[x][y] = board_val

    #checks if a spot has a letter in it
    def check_spot(self, coord):
        x = coord[0]
        y = coord[1]
        board_val = self.board[x][y]

        if board_val == ' ' or board_val == '2L' or board_val == '3L' or board_val == '2W' or \
                board_val == '3W' or board_val == 'STAR':
            return True
        return False

    #checks adjacent coordinates and returns any coordinates with letters in them
    def check_adjacent(self, coord, omit=set()):
        to_check = {(coord[0], coord[1]-1), (coord[0], coord[1]+1), (coord[0]-1, coord[1]), (coord[0]+1, coord[1])}
        result = set()

        for spot in to_check:
            if spot not in omit and not self.check_spot(spot):
                result.add(spot)

        return result

#some code for testing different features
#ctrl+shift+/ to block comment
if __name__ == '__main__':
    print("printout for testing")

    game = Game()
    game.pick_order()
    print("bag len: " + str(len(game.bag.letters)))

    word = game.turn.tray[0:5]
    print(word)
    word_dict = dict()
    coord = (7,7)
    for let in word:
        if let in word_dict:
            word_dict[let].add(coord)
        else:
            word_dict[let] = {coord}
        coord = (coord[0], coord[1]+1)
    game.play(word_dict)
    game.challenge(False)
    print(game.player1.score)
    print(game.player2.score)
    print("bag len: " + str(len(game.bag.letters)))
    print()
    
    word = game.turn.tray[0:2]
    print(word)
    word_dict = dict()
    coord = (8,7)
    for let in word:
        if let in word_dict:
            word_dict[let].add(coord)
        else:
            word_dict[let] = {coord}
        coord = (coord[0], coord[1]+1)
    game.play(word_dict)
    game.challenge(False)
    print(game.player1.score)
    print(game.player2.score)
    print("bag len: " + str(len(game.bag.letters)))
    print()
    
    word = game.turn.tray[0:4]
    print(word)
    word_dict = dict()
    coord = (3,11)
    for let in word:
        if let in word_dict:
            word_dict[let].add(coord)
        else:
            word_dict[let] = {coord}
        coord = (coord[0]+1, coord[1])
    game.play(word_dict)
    game.challenge(False)
    print(game.player1.score)
    print(game.player2.score)
    print("bag len: " + str(len(game.bag.letters)))
    print()

    word = game.turn.tray[0:2]
    print(word)
    word_dict = {word[0]:{(5,10)}, word[1]:{(5,12)}}
    game.play(word_dict)
    print(game.board.board)
    game.challenge(True)

    print(game.player1.score)
    print(game.player2.score)
    print(game.player1.tray)
    print(game.player2.tray)
    print("bag len: " + str(len(game.bag.letters)))
    print()

    print(game.board.board)

##UNUSED CODE
# def place_word(self, board, word):
    #     points = 0
    #     side_points = 0
    #     direction = 'x'
    #     modifiers = set()
    #     self.last_word = deepcopy(word)

    #     used_spaces = set()

    #     coord1 = None
    #     coord2 = None

    #     for let, coord_set in word.items():
    #         for coord in coord_set:
    #             if coord1 is not None and coord2 is not None:
    #                 break
    #             if coord1 is None:
    #                 coord1 = coord
    #             elif coord2 is None:
    #                 coord2 = coord
    #         if coord1 is not None and coord2 is not None:
    #             if coord1[0] == coord2[0]:
    #                 direction = 'y'
    #                 break

    #     word_len = 0

    #     for letter, coord_set in word.items():
    #         for coord in coord_set:
    #             word_len += 1
    #             self.tray.remove(letter)
    #             used_coords.add(coord)
                
    #             output = self.get_let_points(board, letter, coord)
    #             points += output[0]
    #             modifiers.update(output[1])
    #             board_val = output[2]

    #             if board_val != 'taken' and len(board.check_adjacent(coord, {self.decr_coord(coord, direction), self.incr_coord(coord, direction)}))>0:
    #                 side_val = self.calc_sideword(board, coord, direction, board_val, output[0])
    #                 side_points += side_val

    #             #NEEDS SOMETHING TO CALCULATE THE LETTERS IN THE WORD THAT ARE NOT DIRECTLY PLACED
    #             #AND ARE NOT SIDEWORDS

    #     #calculates total score
    #     mult = 1
    #     for mod in modifiers:
    #         if mod == 'STAR':
    #             mult = mult*2
    #         else:
    #             mult = mult*int(mod[0])

    #     #adds modified points from original word
    #     points = points*mult 
    #     #adds points from sidewords
    #     points+= side_points
    #     #adds bonus points for using all letters
    #     if word_len == 7:
    #         points+=50

    #     #adds points
    #     self.score += points

    #     #sets up for challenge
    #     self.last_score = points