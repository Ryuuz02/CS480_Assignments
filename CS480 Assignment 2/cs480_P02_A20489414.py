from copy import deepcopy
import sys
import time

# return start time
start_time = time.time()
def print_sudoku(sudoku):
    for i in range(9):
        for j in range(9):
            if j == 8:
                print(sudoku[i][j])
            else:
                print(sudoku[i][j], end=",")

def find_sudoku_nums(sudoku, y, x):
    row = sudoku[x]
    column = [sudoku[i][y] for i in range(9)]
    sudoku_nums = list(range(1, 10))
    for val in row:
        if val != "X":
            val = int(val)
            if val in sudoku_nums:
                sudoku_nums.remove(val)
    for val in column:
        if val != "X":
            val = int(val)
            if val in sudoku_nums:
                sudoku_nums.remove(val)
    if sudoku_nums == []:
        sudoku_nums = ["X"]
    return sudoku_nums

def solve_position(sudoku, y, x):
    if x >= 9 or x < 0:
        return
    elif y >= 9 or y < 0:
        return
    else:
        if sudoku[x][y] == "X":
            sudoku_nums = find_sudoku_nums(sudoku, y, x)
            if len(sudoku_nums) == 0:
                return
            sudoku_lst = []
            for i in sudoku_nums:
                new_sudoku = deepcopy(sudoku)
                new_sudoku[x][y] = i
                sudoku_lst.append(new_sudoku)
            return sudoku_lst
        else:
            return [sudoku]


def check_solved(sudoku):
    for x in range(9):
        column_nums = []
        for y in range(9):
            if sudoku[x][y] == "X":
                return False
            else:
                if sudoku[x][y] in column_nums:
                    return False
                else:
                    column_nums.append(sudoku[x][y])
            if sudoku[x].count(sudoku[x][y]) > 1:
                return False
                


args = sys.argv[1:]
if len(args) != 2:
    print("ERROR: Not enough/too many/illegal input arguments.")
    sys.exit()

start_data = []
try:
    with open(args[0], 'r') as f:
        lines = f.readlines()
        for line in lines:
            if "\n" in line:
                line = line.replace("\n", "")
            split_line = line.split(",")
            start_data.append(split_line)
    sudoku = deepcopy(start_data)
except:
    print("ERROR: Not enough/too many/illegal input arguments.")
    sys.exit()

















if args[1] == "1":
    alg = "Brute Force Search"
    potentials = [sudoku]
    nodes = 0
    for i in range(9):
        for j in range(9):
            potentials2 = []
            for p in potentials:
                temp = solve_position(p, i, j)
                nodes += len(temp)
                potentials2 += temp
            potentials = potentials2
    sudoku = potentials[0]


elif args[1] == "2":
    alg = "Constraint Satisfaction Problem back-tracking search"

    # Very similar to brute force, but only back track if the sudoku hits an invalid, then go back to the last node that had a choice and go through it again from there
    nodes = 1
    x_counter = 0
    y_counter = 0
    sol_history = {}
    while x_counter <= 9 and y_counter < 9:
        if x_counter == 9:
            y_counter += 1
            x_counter = 0
        else:
            if sudoku[x_counter][y_counter] == "X":
                possibles = find_sudoku_nums(sudoku, y_counter, x_counter)
                if possibles != ["X"]:
                    if len(possibles) > 1:
                        sol_history[(x_counter,y_counter)] = possibles[1:]
                    else:
                        sol_history[(x_counter,y_counter)] = ["X"]
                    sudoku[x_counter][y_counter] = possibles[0]
                    x_counter += 1
                else:
                    while True: # This is a loop that will break when it finds a valid solution
                        if x_counter > 0:
                            x_counter -= 1
                        elif y_counter > 0:
                            y_counter -= 1
                            x_counter = 8
                        else:
                            print("No solution")
                            sys.exit()
                        if sol_history[(x_counter,y_counter)] != ["X"]:
                            nodes += 1
                            sudoku[x_counter][y_counter] = sol_history[(x_counter,y_counter)].pop(0)
                            if sol_history[(x_counter,y_counter)] == []:
                                sol_history[(x_counter,y_counter)] = ["X"]
                            break
                        else:
                            sudoku[x_counter][y_counter] = "X"
            else:
                sol_history[(x_counter,y_counter)] = ["X"]
                x_counter += 1


elif args[1] == "3":
    alg = "CSP with forward-checking and MRV heuristics"
    # Find the potential values for all empty spaces, then find the one with the least amount of potential values and fill in that one, 
    # checking to ensure that no other empty space would become invalid. When you replace a value, make sure to update the potential values for all empty spots again
    nodes = 1
    possible_values = {}
    for x in range(9):
        for y in range(9):
            if sudoku[x][y] == "X":
                possible_values[(x,y)] = find_sudoku_nums(sudoku, y, x)
    for i in range(len(possible_values)):
        min_value = 10
        min_key = (0,0)
        for key in possible_values:
            if len(possible_values[key]) < min_value:
                min_value = len(possible_values[key])
                min_key = key
        (x,y) = min_key
        sudoku[x][y] = possible_values[min_key][0]
        possible_values.pop(min_key)
        # Take that value out of all other possible values in its row/column
        for key in possible_values:
            if key[0] == x or key[1] == y:
                if sudoku[x][y] in possible_values[key]:
                    possible_values[key].remove(sudoku[x][y])


elif args[1] == "4":
    alg = "Solved"
else:
    print("ERROR: Not enough/too many/illegal input arguments.")
    sys.exit()

end_time = time.time()
# Output block
print("Bode, Jacob, A20489414 Solution:")
print("Input file: " + args[0])
print("Algorithm: " + alg)
print("Input Puzzle:")
print_sudoku(start_data)
if alg != "Solved":
    print("Number of search tree nodes generated: " + str(nodes))
    print("Search Time: " + str(end_time-start_time))
    print("Solved Puzzle: ")
    print_sudoku(sudoku)
else:
    correct = check_solved(sudoku)
    if correct:
        print("This is a valid, solved, Sudoku puzzle.")
    else:
        print("This is NOT a valid, solved, Sudoku puzzle.")
    sys.exit()

