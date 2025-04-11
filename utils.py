import pygame
import random
import math
from tkinter import font as tkfont
from PIL import Image, ImageTk

# ======================
# VISUAL EFFECTS
# ======================
def blood_drip_effect(surface, intensity=30):
    """Create dripping blood effect on screen edges"""
    for _ in range(intensity):
        x = random.randint(0, surface.get_width())
        y = random.randint(0, 50)
        length = random.randint(20, 100)
        width = random.randint(1, 3)
        for i in range(length):
            pygame.draw.line(
                surface, 
                (150 - i//2, 0, 0), 
                (x, y + i), 
                (x + random.randint(-2, 2), y + i + 1), 
                width
            )

def blood_splatter(damage_ratio):
    """Generate blood splatter proportional to damage"""
    surf = pygame.Surface((800, 600), pygame.SRCALPHA)
    drops = int(50 * damage_ratio)
    for _ in range(drops):
        pos = (random.randint(0, 800), random.randint(0, 600))
        radius = random.randint(1, int(10 * damage_ratio))
        alpha = random.randint(100, 200)
        pygame.draw.circle(
            surf, 
            (180 + random.randint(-20, 20), 0, 0, alpha), 
            pos, 
            radius
        )
    return surf

def fade_in(surface, color, duration):
    """Blood-red fade in effect"""
    fade_surf = pygame.Surface(surface.get_size())
    fade_surf.fill(color)
    for alpha in range(0, 255, 5):
        fade_surf.set_alpha(alpha)
        surface.blit(fade_surf, (0, 0))
        pygame.display.flip()
        pygame.time.delay(duration * 1000 // 255)

# ======================
# TEXT & UI RENDERING
# ====================== 
def draw_blood_text(surface, text, pos, font, pulse=False):
    """Render text with dripping blood effect"""
    text_surf = font.render(text, True, (180, 4, 45))
    shadow = font.render(text, True, (80, 0, 0))
    
    if pulse:
        alpha = 150 + int(100 * math.sin(pygame.time.get_ticks() / 300))
        text_surf.set_alpha(alpha)
    
    # Blood drip under text
    for i in range(3):
        pygame.draw.line(
            surface, (120, 0, 0),
            (pos[0] + 5 + i*2, pos[1] + text_surf.get_height()),
            (pos[0] + 15 + i*5, pos[1] + text_surf.get_height() + 10),
            1 + i
        )
    
    surface.blit(shadow, (pos[0]+2, pos[1]+2))
    surface.blit(text_surf, pos)
    return text_surf.get_rect(topleft=pos)

def garnet_button(surface, rect, text):
    """Create a garnet-stone styled button"""
    # Gemstone base
    pygame.draw.polygon(
        surface, (80, 0, 20),
        [
            (rect.left, rect.top + rect.height//2),
            (rect.left + rect.width//3, rect.top),
            (rect.right - rect.width//3, rect.top),
            (rect.right, rect.top + rect.height//2),
            (rect.right - rect.width//3, rect.bottom),
            (rect.left + rect.width//3, rect.bottom)
        ]
    )
    
    # Gem facets
    highlight_color = (random.randint(150, 200), 0, random.randint(30, 60))
    pygame.draw.polygon(
        surface, highlight_color,
        [
            (rect.left + rect.width//3, rect.top + 5),
            (rect.left + rect.width//2, rect.top + rect.height//3),
            (rect.right - rect.width//3, rect.top + 5)
        ],
        2
    )
    
    # Text
    font = pygame.font.Font("assets/fonts/necromancer.ttf", 20)
    text_surf = font.render(text, True, (255, 220, 220))
    surface.blit(text_surf, (
        rect.centerx - text_surf.get_width()//2,
        rect.centery - text_surf.get_height()//2
    ))
    return rect

def draw_tooltip(surface, text, position, font, bg_color=(20, 0, 10), text_color=(200, 200, 200)):
    """Draw a tooltip box with text"""
    lines = text.split('\n')
    line_surfaces = [font.render(line, True, text_color) for line in lines]
    
    # Calculate total size
    max_width = max(surf.get_width() for surf in line_surfaces)
    total_height = sum(surf.get_height() for surf in line_surfaces) + 10 * (len(lines) - 1)
    
    # Create background
    rect = pygame.Rect(position[0], position[1], max_width + 20, total_height + 10)
    pygame.draw.rect(surface, bg_color, rect)
    pygame.draw.rect(surface, (120, 0, 0), rect, 2)
    
    # Draw text lines
    y_offset = 5
    for line_surf in line_surfaces:
        surface.blit(line_surf, (rect.x + 10, rect.y + y_offset))
        y_offset += line_surf.get_height() + 5

def wrap_text(text, font, max_width):
    """Wrap text to fit within specified width"""
    words = text.split(' ')
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        test_width = font.size(test_line)[0]
        
        if test_width <= max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

# ======================
# AUDIO SYSTEM
# ======================
def load_sound(filename):
    """Robust sound loading that works with MP3/WAV"""
    class DummySound:
        def play(self): pass
        def set_volume(self, vol): pass

    try:
        # Initialize mixer if needed
        if pygame.mixer.get_init() is None:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        
        # Special handling for MP3
        if filename.endswith('.mp3'):
            try:
                return pygame.mixer.Sound(f"assets/sounds/{filename}")
            except:
                with open(f"assets/sounds/{filename}", 'rb') as f:
                    return pygame.mixer.Sound(buffer=f.read())
        else:
            return pygame.mixer.Sound(f"assets/sounds/{filename}")
    except Exception as e:
        print(f"Sound load failed: {e}")
        return DummySound()

def play_music(filename, volume=0.5, loops=-1):
    """Play background music with error handling"""
    try:
        pygame.mixer.music.load(f"assets/sounds/{filename}")
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loops)
    except Exception as e:
        print(f"Music error: {e}")

def stop_music():
    """Stop any playing music"""
    pygame.mixer.music.stop()

# ======================
# FONT SYSTEM
# ======================
def load_font(font_name, size, fallback_name=None):
    """Safe font loading with multiple fallback options"""
    try:
        # Try loading from assets/fonts first
        try:
            return pygame.font.Font(f"assets/fonts/{font_name}", size)
        except:
            # Fallback to system font if specified
            if fallback_name:
                return pygame.font.SysFont(fallback_name, size)
            # Ultimate fallback
            return pygame.font.Font(None, size)
    except Exception as e:
        print(f"Font loading failed: {e}")
        return pygame.font.Font(None, size)

def center_horizontal(surface, container_rect, y_offset=0):
    """Center surface horizontally within container"""
    rect = surface.get_rect(centerx=container_rect.centerx, y=container_rect.centery + y_offset)
    return rect

def blood_text_animation(text, font, progress, color):
    """Create animated blood text surface"""
    surface = pygame.Surface(font.size(text), pygame.SRCALPHA)
    for i, char in enumerate(text):
        if i <= progress:
            alpha = 255 if i < progress else int(255 * (progress - i + 1))
            char_surf = font.render(char, True, color)
            char_surf.set_alpha(alpha)
            surface.blit(char_surf, (font.size(text[:i])[0], 0))
            
            if i == int(progress):
                pygame.draw.line(
                    surface, (120, 0, 0, alpha),
                    (font.size(text[:i])[0] + 5, font.get_height()),
                    (font.size(text[:i])[0] + 15, font.get_height() + 10),
                    2
                )
    return surface

# ======================
# MATH UTILITIES
# ======================
def calculate_blood_cost(spell_power, sacrifice_ratio=0.1):
    """Determine HP cost for dark magic"""
    base_cost = spell_power * 2
    return max(1, int(base_cost * (1 + random.random() * sacrifice_ratio)))

def corrupt_stat(stat_value):
    """Apply random corruption to a stat"""
    return max(1, stat_value + random.randint(-2, 1))