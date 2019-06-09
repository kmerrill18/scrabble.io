#scrabble game logic
import random
import copy

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

class Game:
    def __init__(self):
        self.board = Board()
        self.bag = Bag()
        self.player1 = Player(self.bag.draw(7))
        self.player2 = Player(self.bag.draw(7))
        self.active = None
        self.end_game = 'going'
    
    #TODO: needs some way of determining the end of the game
    #TODO: needs some way to pass

    def dump(self):
    	self.turn.dump()
    	if bag.empty:
    		if self.end_game == 'pass':
    			self.end_game = 'end'
    		else:
    			self.end_game = 'pass'


    def pick_order(self):
        blank = True
        while blank:
            let1, let2 = self.bag.pick_order_letter()
            if let1 != 'blank' and let2 != 'blank':
                blank = False
        
        if let1>let2:
            self.active = self.player2
            return (self.player2, let1, let2)
        elif let1<let2:
            self.active = self.player1
            return (self.player1, let1, let2)
        else:
            return self.pick_order()

    #TODO: for challanging a word placement. Returns true or false
    def challenge(self):
        return False

    def turn(self, word, start, end, dump=False):
    	#returns the winner at the end of the game
    	if self.end_game == 'end':
    		self.player1.subtract_unused()
    		self.player2.subtract_unused()
    		if self.player1.score>self.player2.score:
    			return self.player1
    		elif self.player1.score<self.player2.score:
    			return self.player2
    		else:
    			return 'tie'

    	#handles passing
    	if dump:
    		self.active.dump(word, self.bag)
    	#handles word placement
    	else:
	        self.active.place_word(self.board, word, start, end)
	        if self.challenge():
	            self.active.retract_word(self.board)
	            return self.turn()
	        self.active.draw(self.bag)

	        if self.active == self.player1:
	            self.active = self.player2
	        else:
	            self.active = self.player1


class Bag:
    def __init__(self, D=None):
        self.empty = False
        if D is not None:
            self.letters = D
        else:
            self.letters = Constants.LETTERS.copy()

    def draw(self, num_draw):
        result = []

        if self.empty:
            return result

        for i in range(num_draw):
            if len(self.letters) == 0:
                self.empty = True
                return result
            ind = random.randint(0, len(self.letters))
            result.append(self.letters.pop(ind))
        return result

    def pick_order_letter(self):
        ind1 = random.randint(0, len(self.letters))
        ind2 = random.randint(0, len(self.letters))
        if ind1 == ind2:
            print('recursing')
            return pick_order_letter()
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
        self.last_coords = None
        self.last_score = None

    def place_word(self, board, word, start, end):
        #needs code to put the word on to the board and update the score, accounting for board modifiers
        #removes used letters from tray
        #points will be number of points for the word
        #assumes that word is selected from the tray
        #DOESN'T DRAW AT THE END - NEEDS GAME TO CALL THIS COMMAND ONCE CHALLENGE IS SETTLED
        points = 0
        direction = 'x'
        modifiers = set()

        #determines whether the word is vertical or horizontal
        if start[0] == end[0]:
            direction = 'y'

        #places each letter, checks for modifiers, checks for sidewords, adds points for sidewords
        coord = start
        last_coord = None

        for letter in word:
            output = self.get_let_points(board, letter, coord)
            points += output[0]
            modifiers.update(output[1])
            board_val = output[2]

            if len(board.check_adjacent(coord, {last_coord}))>0:
                points += self.calc_sideword(board, coord, direction, board_val, let_point)

            last_coord = coord
            if direction == 'x':
                coord = (coord[0]+1, coord[1])
            else:
                coord = (coord[0], coord[1]+1)

        #calculates total score
        mult = 1
        for mod in modifiers:
            if mod == 'STAR':
                mult = mult*2
            else:
                mult = mult*int(mod[0])

        points = points*mult        

        #removes used letters from tray
        for letter in word:
            tray.remove(letter)

        #sets up for challenge
        self.last_word = word
        self.last_coords = (start, end)
        self.last_score = points

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
                start_check = (new_start[0]-1, new_start[1])
            else:
                start_check = (new_start[0], new_start[1]-1)
            new_start = temp
            board_val = board.board[new_start[0]][new_start[1]]
            points += Constants.LETTER_POINTS[board_val]

        new_end = coord
        while len(board.check_adjacent(end_check, {new_end}))>0:
            temp = end_check
            if new_dir == 'x':
                end_check = (new_end[0]+1, new_end[1])
            else:
                end_check = (new_end[0], new_end[1]+1)
            new_end = temp
            board_val = board.board[new_end[0]][new_end[1]]
            points += Constants.LETTER_POINTS[board_val]

        if mod is not None:
            points = points*mod
        return points

    def get_let_points(self, board, letter, coord):
        points = Constants.LETTER_POINTS[letter]
        modifiers = set()
        
        board_val = board.place_letter(letter, coord)
        
        if board_val != ' ':
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

    #TODO: code to remove the last word placed from the board
    def retract_word(self, board):
        #code to take the last action off the board
        start = self.last_coord[0]
        end = self.last_coord[1]

        if start[0] == end[0]:
        	coord = start
        	while coord[1] <= end[1]:
        		board.board[coord[0]][coord[1]] = Constants.BOARD[coord[0]][coord[1]]
        		coord = (coord[0], coord[1]+1)
        else:
        	coord = start
        	while coord[0] <= end[0]:
        		board.board[coord[0]][coord[1]] = Constants.BOARD[coord[0]][coord[1]]
        		coord = (coord[0]+1, coord[1])

        #this code returns player states
        self.score -= self.last_score
        for letter in self.last_word:
            self.tray.append(letter)

        self.last_word = None
        self.last_score = None
        self.last_coords = None

    def dump(self, letters, bag):
    	if bag.empty:
    		return

    	for let in letters:
    		self.tray.remove(let)
    	self.draw()

    def draw(self, bag):
        to_draw = 7-len(self.tray)
        self.tray.extend(bag.draw(to_draw))

    def subtract_unused(self):
    	for let in self.tray:
    		self.score -= Constants.LETTER_POINTS[let]


class Board:
    def __init__(self):
        self.board = copy.deepcopy(Constants.BOARD)

    def place_letter(self, letter, coord):
        x = coord[0]
        y = coord[1]
        board_val = board[x][y]

        if check_spot(coord):
            self.board[x][y] = letter
            return board_val
        else:
            raise ValueError('There is already a letter at that spot!')

    def check_spot(self, coord):
        x = coord[0]
        y = coord[1]
        board_val = board[x][y]

        if board_val == ' ' or board_val == '2L' or board_val == '3L' or board_val == '2W' or \
                board_val == '3W' or board_val == 'STAR':
            return True
        return False

    def check_adjacent(self, coord, omit=set()):
        to_check = {(coord[0], coord[1]-1), (coord[0], coord[1]+1), (coord[0]-1, coord[1]), (coord[0]+1, coord[1])}
        result = set()

        for spot in to_check:
            if spot not in omit and not check_spot(spot):
                result.add(spot)

        return result

if __name__ == '__main__':
	game = Game()
	print(game.pick_order())
	print(vars(game))
	print()
	print(vars(game.player1))
	print()
	print(vars(game.player2))
	print()
	# print(vars(game.bag))
	# print()
	word = game.active.tray[0]+game.active.tray[1]
	game.turn(word, (7,7), (7,8))
	print(vars(game.board))
	print()
	print(vars(game.player1))
	print()
	print(vars(game.player2))
	print()
	print(vars(game))