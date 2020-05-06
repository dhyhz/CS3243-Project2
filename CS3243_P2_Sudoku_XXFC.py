import sys
import copy
import math
import random

# Running script: given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt

x1 = slice(0, 3)
y1 = slice(0, 3)
x2 = slice(3, 6)
y2 = slice(3, 6)
x3 = slice(6, 9)
y3 = slice(6, 9)

sections = [x1, x2, x3]

subgrid1 = (x1, y1)
subgrid2 = (x1, y2)
subgrid3 = (x1, y3)
subgrid4 = (x2, y1)
subgrid5 = (x2, y2)
subgrid6 = (x2, y3)
subgrid7 = (x3, y1)
subgrid8 = (x3, y2)
subgrid9 = (x3, y3)

grids = [
        subgrid1, subgrid2, subgrid3,
        subgrid4, subgrid5, subgrid6,
        subgrid7, subgrid6, subgrid9
        ]

class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists

    
    def grid(self, coordinate): # Returns the subgrid that coordinate is located
        row = coordinate[0]
        col = coordinate[1]
        c1 = sections[row//3]
        c2 = sections[col//3]
        grid = (c1, c2)
        return grid # ((row index),(col index))

    def is_complete(self, puzzle): # Check whether puzzle is completed
        for row in puzzle:
            for num in row:
                if num == 0:
                    return False
                    break
        else:
            return True

    # Constraints and other functions
    def transpose(self, puzzle):
        transpose = copy.deepcopy(puzzle)
        for x in range(0,9):
            for y in range(0,9):
                transpose[x][y] = puzzle[y][x]
        return transpose

    def pass_check(self, puzzle): # check if puzzle passes the constraints
        check = 0
        for row in puzzle:
            if len(set(row)) != 9 :
                check += 1
                return False
                break

        for row in self.transpose(puzzle):
            if len(set(row)) != 9 :
                check += 1
                return False
                break
            
        for subgrid in grids:
            num = set()
            for row in puzzle[subgrid[0]]:
                for value in row[subgrid[1]]:
                    num.add(value)
            if len(num) != 9:
                return False
                break
        else:
            return True

    # FOrward check (Need to be debuuged and edited)
    def forward_check(self, value_domains, value, row, col ):    

        for i in range(9):
            if i == col:
                continue    
            
            x = value_domains[row][i]
                
            if len(x) == 1:
                if x[0] == value:
                    return False
     
        for i in range(9):
            if i == row:
                continue
            
            x = value_domains[i][col]
            if len(x) == 1:
                if x[0] == value:
                    return False

        block_row = row/3
        block_col = col/3  
        for i in range(3):
            for j in range(3):
            
                if [block_row*3+i, block_col*3+j] == [row, col]:
                    continue            
            
                x = value_domains[block_row*3+i][block_col*3+j]
                if len(x) == 1:
                    if x[0] == value:
                        return False                                  
        return True

    # Returns a 2d list containing list of the remaining potential values for the 81 squares
    def value_domains(self, puzzle ):
        value_domains = copy.deepcopy(puzzle)
        # initialize all remaining values to the full domain
        for row in range(9):
            for col in range(9):
                if puzzle[row][col] != 0:
                    value_domains[row][col] = []
                    # remove value from domain 
                    value = puzzle[row][col]  
                    value_domains = self.remove_values( row, col, value, value_domains)
                else:
                    value_domains[row][col] = [1,2,3,4,5,6,7,8,9]   
                
        return value_domains     
                        
                        
    # Removes the specified value from constrained squares and returns the new list
    def remove_values(self, row, col, value, value_domains):
    
        # Remove the specified value from each row
        for value_domain in value_domains[row]:
            if isinstance(value_domain, list) and value in value_domain:
                value_domain.remove(value)

        # Remove the specified value from each col
        for i in range(9):
            if isinstance(value_domains[i][col], list) and value in value_domains[i][col]:
                value_domains[i][col].remove(value)
    
        # Remove the specified value from each grid
        grid = self.grid((row,col))
        for i in value_domains[grid[0]]:
            for value_domain in i[grid[1]]:
                if isinstance(value_domain, list) and value in value_domain:
                    value_domain.remove(value)

        return value_domains
   
                    
    # randomly select square
    def get_random_square(self, empty_squares ):   
        # randomly pick one of the empty squares to expand and return it
        return empty_squares[ int(math.floor(random.random()*len(empty_squares))) ]  
    
    
    # return the list of empty squares indices for the puzzle
    def get_empty_squares (self, puzzle ):
        empty_squares = []
        # scan the whole puzzle for empty cells
        for row in range(len( puzzle )):
            for col in range(len( puzzle[1] )):
                if puzzle[row][col] == 0:
                    empty_squares.append( [row,col] ) 
        return empty_squares

    # Backtracking search
    def backtrack(self, puzzle):
        if self.is_complete(puzzle):
            self.ans = puzzle
            return True
        
        # get a list of the empty squares (remaining variables)
        empty_squares = self.get_empty_squares( puzzle )
    
        square = self.get_random_square( empty_squares )
        row = square[0]
        col = square[1]
    
        value_domains = self.value_domains( puzzle )
   
        values = value_domains[row][col]
    
        while len( values ) != 0:        
            value = values[ int( math.floor( random.random()*len( values ) ) ) ]
            values.remove(value)        
            if self.forward_check( value_domains, value, row, col ):
                puzzle[row][col] = value
                if self.backtrack(puzzle):
                    return True
                else:
                    puzzle[row][col] = 0        
        return False

       
    def solve(self):
        # TODO: Write your code here
        
        # solve using backtracking algorithm on self.puzzle
        self.backtrack(self.puzzle)

        # returns the completed puzzle which should always be correct if given puzzle is valid
        if self.pass_check(self.ans):
            return self.ans

    # you may add more classes/functions if you think is useful
    # However, ensure all the classes/functions are in this file ONLY
    # Note that our evaluation scripts only call the solve method.
    # Any other methods that you write should be used within the solve() method.

if __name__ == "__main__":
    # STRICTLY do NOT modify the code in the main function here
    if len(sys.argv) != 3:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise IOError("Input file not found!")

    puzzle = [[0 for i in range(9)] for j in range(9)]
    lines = f.readlines()

    i, j = 0, 0
    for line in lines:
        for number in line:
            if '0' <= number <= '9':
                puzzle[i][j] = int(number)
                j += 1
                if j == 9:
                    i += 1
                    j = 0

    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()

    with open(sys.argv[2], 'a') as f:
        for i in range(9):
            for j in range(9):
                f.write(str(ans[i][j]) + " ")
            f.write("\n")
