import sys
import copy

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

    # Returns reduced domain for an unfilled variable in puzzle
    def domain(self, coordinate, puzzle):
        row = coordinate[0]
        col = coordinate[1]
        # add used values in row to used_values
        row_values = puzzle[row]
        used = set(row_values)
        # add used values in col to used_values
        for row in puzzle:
            column_value = row[col]
            used.add(column_value)
        # add used values in grid to used_values
        grid = self.grid(coordinate)
        for row in puzzle[grid[0]]:
            for num in row[grid[1]]:
                used.add(num)
        # reduce domain by deleting used values
        available = [0,1,2,3,4,5,6,7,8,9]
        for num in used:
            available.remove(num)
        return available

    # Heuristic: select variable with most constrained variable
    def MCV(self, coordinates, puzzle):
        # Returns MCV, domain of MCV
        all_domains = []
        all_domains_size = []
        for coordinate in coordinates:
            all_domains.append(self.domain(coordinate,puzzle))
        for domain in all_domains:
            all_domains_size.append(len(domain))
        index = all_domains_size.index(min(all_domains_size))
        return coordinates[index], all_domains[index]

    # Backtracking search
    def backtrack(self, puzzle):
        if self.is_complete(puzzle):
            self.ans = puzzle
            return True
        # Select the MCV
        variables = []
        for i in range(0,9):
            for j in range(0,9):
                if puzzle[i][j] == 0:
                    variables.append((i,j))
        coordinates, var_domain = self.MCV(variables, puzzle)
        row, col = coordinates
        # Try a value and solve further (recursively), backtrack when stuck
        for value in var_domain:
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
