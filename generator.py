import random
import copy

def is_safe_gen(board, row, col, num):
    for x in range(9):
        if board[row][x] == num or board[x][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False
    return True

def fill_board(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums) 
                for num in nums:
                    if is_safe_gen(board, i, j, num):
                        board[i][j] = num
                        if fill_board(board):
                            return True
                        board[i][j] = 0
                return False
    return True

def generate_sudoku(remove_count):
   
    board = [[0]*9 for _ in range(9)]
    fill_board(board)
    
    puzzle = copy.deepcopy(board)
    count = remove_count
    while count > 0:
        i, j = random.randint(0, 8), random.randint(0, 8)
        if puzzle[i][j] != 0:
            puzzle[i][j] = 0
            count -= 1
    return puzzle