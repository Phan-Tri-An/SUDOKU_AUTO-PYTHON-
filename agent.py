# agent.py
import time
from config import DELAY_SPEED

class SudokuAgent:
    def __init__(self):
        self.steps_taken = 0     
        self.is_paused = False  

    def perceives_constraint(self, board, row, col, num):
        for x in range(9):
            if board[row][x] == num or board[x][col] == num: return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[i + start_row][j + start_col] == num: return False
        return True

    def get_best_action(self, board):
        min_domain = 10 
        best_loc = None
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    domain = 0
                    for num in range(1, 10):
                        if self.perceives_constraint(board, i, j, num): domain += 1
                    if domain == 0: return None, True 
                    if domain < min_domain:
                        min_domain = domain
                        best_loc = (i, j)
        return best_loc, False

    def find_first_empty(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0: return (i, j)
        return None

    def act_solve(self, board, visualizer_func=None, use_heuristic=True):
        while self.is_paused:
            if visualizer_func: visualizer_func(board, current_cell=None)
            time.sleep(0.1)
        if use_heuristic:
            target_cell, is_dead_end = self.get_best_action(board)
        else:
            target_cell = self.find_first_empty(board)
            is_dead_end = False 

        if is_dead_end: return False 
        if not target_cell: return True 
        
        row, col = target_cell

        for num in range(1, 10):
            while self.is_paused:
                if visualizer_func: visualizer_func(board, current_cell=(row, col))
                time.sleep(0.1)

            if self.perceives_constraint(board, row, col, num):
                board[row][col] = num
                
                if visualizer_func:
                    self.steps_taken += 1
                    visualizer_func(board, current_cell=(row, col))
                    time.sleep(DELAY_SPEED)
                
                if self.act_solve(board, visualizer_func, use_heuristic):
                    return True
                
                board[row][col] = 0
                if visualizer_func:
                    visualizer_func(board, current_cell=(row, col))
        return False