# gui_game.py
import pygame
import sys
import time
from constants import *
from components import Button
from agent import SudokuAgent     
from generator import generate_sudoku
from config import DIFFICULTY_LEVELS
from utils import save_log

class SudokuGameApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("SUDOKU AI - PAUSE & RESUME")
        
        try:
            font_name = 'segoeui' if 'segoeui' in pygame.font.get_fonts() else 'arial'
            self.font_num = pygame.font.SysFont(font_name, 40, bold=True)
            self.font_ui = pygame.font.SysFont(font_name, 18, bold=True)
        except:
            self.font_num = pygame.font.SysFont('arial', 40, bold=True)
            self.font_ui = pygame.font.SysFont('arial', 18, bold=True)

        self.start_x = (WIDTH - GRID_SIZE) // 2
        self.start_y = 30

        self.board = None
        self.original_board = None
        self.agent = SudokuAgent()
        
        self.running = True
        self.solving = False
        self.finished = False
        self.message = "Sẵn sàng!"
        self.current_diff_name = "DỄ"
        self.use_heuristic = True 

        self.setup_ui()
        self.reset_game('1')

    def setup_ui(self):
        y_btn = 700
        self.buttons = [
            Button(45, y_btn, 80, 50, "DỄ", self.font_ui, lambda: self.reset_game('1')),
            Button(135, y_btn, 80, 50, "VỪA", self.font_ui, lambda: self.reset_game('2')),
            Button(225, y_btn, 80, 50, "KHÓ", self.font_ui, lambda: self.reset_game('3')),
            
            Button(325, y_btn, 110, 50, "MODE: AI", self.font_ui, self.toggle_mode),
            
            Button(445, y_btn, 100, 50, "DỪNG", self.font_ui, self.toggle_pause),
            
            Button(555, y_btn, 120, 50, "GIẢI NGAY", self.font_ui, self.start_agent)
        ]
        self.btn_mode = self.buttons[3]
        self.btn_pause = self.buttons[4] 

    def toggle_pause(self):
        if self.solving:
            self.agent.is_paused = not self.agent.is_paused
            
            if self.agent.is_paused:
                self.btn_pause.text = "TIẾP TỤC"
                self.message = "Đã TẠM DỪNG. Bấm TIẾP TỤC để chạy."
            else:
                self.btn_pause.text = "DỪNG"
                mode = "AI" if self.use_heuristic else "DFS"
                self.message = f"Đang chạy {mode}..."

    def toggle_mode(self):
        if self.solving: return
        self.use_heuristic = not self.use_heuristic
        if self.use_heuristic:
            self.btn_mode.text = "MODE: AI"
            self.message = "Chế độ: AI (Heuristic) - Nhanh"
        else:
            self.btn_mode.text = "MODE: DFS"
            self.message = "Chế độ: Vét cạn - Chậm"

    def reset_game(self, level_key):
        if self.solving: return
        names = {'1': "DỄ", '2': "VỪA", '3': "KHÓ"}
        self.current_diff_name = names[level_key]
        self.message = f"Mức {self.current_diff_name}. Sẵn sàng!"
        self.finished = False
        self.agent.steps_taken = 0
        self.board = generate_sudoku(DIFFICULTY_LEVELS[level_key])
        self.original_board = [row[:] for row in self.board]
        
        self.agent.is_paused = False
        self.btn_pause.text = "DỪNG"

    def start_agent(self):
        if self.solving or self.finished: return
        self.solving = True
        self.agent.is_paused = False
        self.btn_pause.text = "DỪNG"
        
        mode_name = "AI" if self.use_heuristic else "DFS"
        self.message = f"Đang chạy {mode_name}..."
        self.agent.steps_taken = 0
        
        start_t = time.time()
        success = self.agent.act_solve(self.board, visualizer_func=self.render, use_heuristic=self.use_heuristic)
        
        duration = round(time.time() - start_t, 2)
        self.solving = False
        if success:
            self.finished = True
            self.message = f"XONG! {duration}s | Steps: {self.agent.steps_taken}"
            save_log(f"{self.current_diff_name}-{mode_name}", self.agent.steps_taken, True, duration)
        else:
            self.finished = False
            self.message = "KHÔNG TÌM THẤY LỜI GIẢI!"
            save_log(f"{self.current_diff_name}-{mode_name}", self.agent.steps_taken, False, duration)
        self.agent.is_paused = False
        self.btn_pause.text = "DỪNG"

    def draw_grid(self):
        for i in range(10):
            thick = 4 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, BLACK, 
                             (self.start_x, self.start_y + i * CELL_SIZE), 
                             (self.start_x + GRID_SIZE, self.start_y + i * CELL_SIZE), thick)
            pygame.draw.line(self.screen, BLACK, 
                             (self.start_x + i * CELL_SIZE, self.start_y), 
                             (self.start_x + i * CELL_SIZE, self.start_y + GRID_SIZE), thick)
        pygame.draw.rect(self.screen, BLACK, (self.start_x, self.start_y, GRID_SIZE, GRID_SIZE), 4)

    def draw_numbers(self):
        for i in range(9):
            for j in range(9):
                val = self.board[i][j]
                if val != 0:
                    color = RED if self.original_board[i][j] != 0 else BLUE
                    text = self.font_num.render(str(val), True, color)
                    x = self.start_x + j * CELL_SIZE + (CELL_SIZE - text.get_width()) // 2
                    y = self.start_y + i * CELL_SIZE + (CELL_SIZE - text.get_height()) // 2
                    self.screen.blit(text, (x, y))

    def render(self, board=None, current_cell=None):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if self.solving:
                for btn in self.buttons:
                    if btn.text in ["DỪNG", "TIẾP TỤC"]: 
                        btn.handle_event(event)

        self.screen.fill(WHITE)
        
        if current_cell:
            r, c = current_cell
            surface = pygame.Surface((GRID_SIZE, CELL_SIZE), pygame.SRCALPHA)
            surface.fill(HIGHLIGHT_COLOR)
            self.screen.blit(surface, (self.start_x, self.start_y + r * CELL_SIZE))
            surface_v = pygame.transform.rotate(surface, 90)
            self.screen.blit(surface_v, (self.start_x + c * CELL_SIZE, self.start_y))

        self.draw_grid()
        self.draw_numbers()
        
        stt_color = GREEN if self.finished else (ORANGE if self.agent.is_paused else BLACK)
        msg_surf = self.font_ui.render(self.message, True, stt_color)
        msg_rect = msg_surf.get_rect(center=(WIDTH // 2, 780))
        self.screen.blit(msg_surf, msg_rect)
        
        for btn in self.buttons:
            btn.draw(self.screen)
        
        pygame.display.update()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.running = False
                if not self.solving:
                    for btn in self.buttons: btn.handle_event(event)
            self.render()
        pygame.quit()

if __name__ == "__main__":
    app = SudokuGameApp()
    app.run()