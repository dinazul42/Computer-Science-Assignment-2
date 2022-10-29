import game_of_life_interface
import numpy as np
import matplotlib.pyplot as plt



class GameOfLife(game_of_life_interface.GameOfLife):  # This is the way you construct a class that heritage properties

    def __init__ (self, size_of_board, board_start_mode, rules, rle, pattern_position) :  # constructor
        # declare and initialize variables
        self.size_of_board = size_of_board
        self.board_start_mode = board_start_mode
        self.board = np.zeros ((size_of_board, size_of_board))
        self.rules = rules
        self.B = list (map (int, rules.split ("/") [ 0 ] [ 1 : ]))
        self.S = list (map (int, rules.split ("/") [ 1 ] [ 1 : ]))
        self.pattern_position = pattern_position
        self.rle = rle
        self.alive = 255
        self.dead = 0
        if board_start_mode == 1 and self.rle == "" :

            self.board = np.random.choice ([ 0, 255 ], (size_of_board, size_of_board), p=[ 0.5, 0.5 ]).reshape (
                self.size_of_board, self.size_of_board)
        elif board_start_mode == 2 and self.rle == "" :
            self.board = np.random.choice ([ 255, 0 ], (size_of_board, size_of_board), p=[ 0.8, 0.2 ]).reshape (
                self.size_of_board, self.size_of_board)

        elif board_start_mode == 3 and self.rle == "" :
            self.board = np.random.choice ([ 0, 255 ], (size_of_board, size_of_board), p=[ 0.2, 0.8 ]).reshape (
                self.size_of_board, self.size_of_board)

        elif board_start_mode == 4 and self.rle == "" :  # glider gun board
            self.board = np.zeros ((self.size_of_board, self.size_of_board), dtype=int)
            self.board [ 14, 11 ] = 255
            self.board [ 15, 11 ] = 255
            self.board [ 14, 10 ] = 255
            self.board [ 15, 10 ] = 255
            self.board [ 14, 20 ] = 255
            self.board [ 15, 20 ] = 255
            self.board [ 16, 20 ] = 255
            self.board [ 13, 21 ] = 255
            self.board [ 17, 21 ] = 255
            self.board [ 12, 22 ] = 255
            self.board [ 18, 22 ] = 255
            self.board [ 12, 23 ] = 255
            self.board [ 18, 23 ] = 255
            self.board [ 15, 24 ] = 255
            self.board [ 13, 25 ] = 255
            self.board [ 17, 25 ] = 255
            self.board [ 14 :17, 26 ] = 255
            self.board [ 15, 27 ] = 255
            self.board [ 12 :15, 30 ] = 255
            self.board [ 12 :15, 31 ] = 255
            self.board [ 11, 32 ] = 255
            self.board [ 15, 32 ] = 255
            self.board [ 10 :12, 34 ] = 255
            self.board [ 15 :17, 34 ] = 255
            self.board [ 12 :14, 44 ] = 255
            self.board [ 12 :14, 45 ] = 255
        else :
            self.transform_rle_to_matrix (self.rle)
    def if_check (self, k, m, board) :#checks the index in some board insert returns true or false
        return 1 if board [ k ] [ m ] == self.alive else 0
    def check_neighbours (self,i, j,current_board) :#checks the neighbors val according to the rules
        count = 0
        size = self.size_of_board
        count = count + self.if_check((i - 1) % size, (j - 1) % size,current_board)  # left-upper1
        count = count + self.if_check((i - 1) % size, j,current_board )  # upper1
        count = count + self.if_check((i - 1) % size, (j + 1) % size,current_board)  # right-upper1
        count = count + self.if_check(i , (j - 1) % size,current_board)  # left1
        count = count + self.if_check(i, (j + 1) % size,current_board)  # right1
        count = count + self.if_check((i + 1) % size, (j - 1) % size,current_board)  # left-down1
        count = count + self.if_check((i + 1) % size, j,current_board)  # down1
        count = count + self.if_check((i + 1) % size, (j + 1) % size,current_board)  # right down1
        if (current_board[i][j]==0 and count in self.B) or (current_board[i][j]==255 and count in self.S):
            return True
        else:
            return False
    def copy_board(self):#this function makes a deep copy of a board
        list_to_ret = []
        for i in range (self.size_of_board) :
            temp_list = []
            for j in range (self.size_of_board) :
                temp_list.append(self.board[i][j])
            list_to_ret.append(temp_list)
        return list_to_ret
    def update(self): # update the board based on given rules
        current_board = self.copy_board()
        for i in range(self.size_of_board):
            for j in range(self.size_of_board):
                if self.check_neighbours(i,j,current_board) == True:
                    self.board[i][j] = self.alive # 255
                else:
                    self.board[i][j] = self.dead # 0



        #  wrote many lines to update ,but changed it according to study about modulo.
        #RuleBook - Main interface for game rules
#GOLRuleBook - Regular Game of Life rules implementing RuleBook
#Cell - An interface for a living organism :) Which lives or dies according to the rules in rulebook. A cell can answer are you alive question.
#AliveCell - Represents a living cell
#DeadCell - Represents a dead cell
#Board - The game world. Holds all the cells, and their locations. Can tell each cells number of neighbours.
#Player - The player of the game. Player is just responsible for generation change of the board.
#CellFactory - Responsible for cell creation (Gives the same instance for all the alive cells, and gives the same instance for all the dead cells)
#Populator - Cell generators
#StrLoadingPopulator - Load initial cells from new line delimited string such as [A D A]\n[D D D]
#RandomPopulator - Given number of rows and number of columns randomly generate cells
#Main - Main class. Number of rows, number of columns and number of generations are collecte

    def transform_rle_to_matrix (self, rle) :#this function goes threw the list of rle on the insert and describes it on the board

        z, w = self.pattern_position  # position tupple for w,z axis
        space = ""
        self.board = [ [ 0 for i in range (self.size_of_board) ] for j in range (self.size_of_board) ]

        for i in rle :
            if i != "!" :
                if i != "$" :
                    if str (i).isdigit ( ) :
                        space += i
                    if i == "o" :
                        if space == "" :
                            space = 1
                        for j in range (w, w + int (space)) :
                            self.board [ z ] [ j ] = self.alive
                        w = w + int (space)
                        space = ""
                    if i == "b" :
                        if space == "" :
                            space = 1
                        for j in range (w, w + int (space)) :
                            self.board [ z ] [ j ] = self.dead
                        w = w + int (space)
                        space = ""
                else :
                    if space == "" :
                        space = 1
                    z = z + int (space)
                    space = ""
                    w = self.pattern_position [ 1 ]

        # initialize board based on starting position
    def save_board_to_file(self, file_name):#this function saves the board files each iteration
        plt.imsave(file_name, self.board)
    def display_board(self):#this function make a display of the board
       plt.imshow(self.board)
       plt.pause(0.0001)
    def return_board (self): #this function returns a list of the board position after checking if it is a list
        if type(self.board)==list:
            return self.board
        else:
            return self.board.tolist ( )


if __name__ == '__main__':
    # You should keep this line for our auto-grading code.
    # game = GameOfLife(120 , 4,"b3/s23","","")
    game = GameOfLife (100, 4, "b3/s23",
                       "5b3o11b3o5b$4bo3bo9bo3bo4b$3b2o4bo7bo4b2o3b$2bobob2ob2o5b2ob2obobo2b$b2obo4bob2ob2obo4bob2ob$o4bo3bo2bobo2bo3bo4bo$12bobo12b$2o7b2obobob2o7b2o$12bobo12b$6b3o9b3o6b$6bo3bo9bo6b$6bobo4b3o11b$12bo2bo4b2o5b$15bo11b$11bo3bo11b$11bo3bo11b$15bo11b$12bobo!",
                       (40, 40))
    for i in range (180) :
        print ("updating iteration number " + str (i))
        game.update ( )
        game.display_board ( )

    game = GameOfLife(100 , 4,"b3/s23", "5b3o11b3o5b$4bo3bo9bo3bo4b$3b2o4bo7bo4b2o3b$2bobob2ob2o5b2ob2obobo2b$b2obo4bob2ob2obo4bob2ob$o4bo3bo2bobo2bo3bo4bo$12bobo12b$2o7b2obobob2o7b2o$12bobo12b$6b3o9b3o6b$6bo3bo9bo6b$6bobo4b3o11b$12bo2bo4b2o5b$15bo11b$11bo3bo11b$11bo3bo11b$15bo11b$12bobo!",(40,40))
    # game = GameOfLife(100 , 4,"b3/s23", "5b3o11b3o5b$4bo3bo9bo3bo4b$3b2o4bo7bo4b2o3b$2bobob2ob2o5b2ob2obobo2b$b2obo4bob2ob2obo4bob2ob$o4bo3bo2bobo2bo3bo4bo$12bobo12b$2o7b2obobob2o7b2o$12bobo12b$6b3o9b3o6b$6bo3bo9bo6b$6bobo4b3o11b$12bo2bo4b2o5b$15bo11b$11bo3bo11b$11bo3bo11b$15bo11b$12bobo!",(40,40))










