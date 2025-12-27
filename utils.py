# utils.py
import os
import datetime
from config import LOG_FILE

def clear_screen():
    
    os.system('cls' if os.name == 'nt' else 'clear')

def print_board(board, steps=0):
    clear_screen()
    print(f"\n--- SUDOKU AI SOLVER (Steps: {steps}) ---")
    print("-------------------------")
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -")
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")
    print("-------------------------")

def save_log(difficulty, steps, success, duration):
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "THÀNH CÔNG" if success else "THẤT BẠI"
    
    
    log_line = f"[{timestamp}] Độ khó: {difficulty:<10} | {status} | Steps: {steps:<5} | Time: {duration}s\n"
    
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_line)
        print(f"\n[LOG] Đã lưu: {difficulty} - {status} - {duration}s")
    except Exception as e:
        print(f"\n[Lỗi] Không thể ghi log: {e}")