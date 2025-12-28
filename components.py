import pygame
from constants import *

class Button:
    def __init__(self, x, y, w, h, text, font, callback=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.callback = callback
        self.color = BTN_COLOR

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            current_color = BTN_HOVER
        else:
            current_color = self.color
        pygame.draw.rect(screen, current_color, self.rect, border_radius=8)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=8) 
        text_surf = self.font.render(self.text, True, BTN_TEXT_COL)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                if self.callback:
                    self.callback()