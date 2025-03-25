import pygame
import numpy as np

class HandSensor:
    def __init__(self, rect, depth_min, depth_max, width, height, id=0):
        self.rect = rect
        self.depth_min = depth_min
        self.depth_max = depth_max
        self.width = width
        self.height = height
        self.hand_detected = False
        self.id = id
        
        self.inactive_color = (255, 0, 0)
        self.active_color = (0, 255, 0)
        
    def update(self, depth_frame):
        depth_2d = depth_frame.reshape(self.height, self.width)
        
        x, y, w, h = self.rect
        roi = depth_2d[y:y+h, x:x+w]
        
        valid_pixels = (roi >= self.depth_min) & (roi <= self.depth_max)
        
        valid_pixel_count = np.sum(valid_pixels)
        threshold = 0.05 * roi.size
        
        self.hand_detected = valid_pixel_count > threshold
        
    def draw(self, surface):
        color = self.active_color if self.hand_detected else self.inactive_color
        
        s = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        
        if self.hand_detected:
            s.fill((0, 255, 0, 128))
            surface.blit(s, (self.rect.x, self.rect.y))
        
        pygame.draw.rect(surface, color, self.rect, 2)
        
        font = pygame.font.SysFont(None, 24)
        text = font.render(f"Sensor {self.id}", True, color)
        text_x = self.rect.x + self.rect.width + 5
        text_y = self.rect.y + (self.rect.height // 2) - 10
        surface.blit(text, (text_x, text_y))