import pygame
import random
import math
from utils import (
    # Visual Effects
    blood_drip_effect,
    fade_in,
    
    # Text & UI
    draw_blood_text,
    garnet_button,
    draw_tooltip,
    center_horizontal,
    blood_text_animation,
    
    # Audio
    load_sound,
    play_music,
    stop_music,
    
    # Fonts
    load_font
)

class ShadowbornCreation:
    # ======================
    # CLASS CONSTANTS
    # ======================
    DARK_TITLES = [
        "the Bloodsoaked",
        "of the Crimson Veil",
        "the Garnet Ghost",
        "Bearer of the Dark Shard",
        "the Void-Touched"
    ]

    DARK_CLASSES = {
        "Bloodmancer": {
            "stats": {"STR": 1, "DEX": 2, "CON": 2, "INT": 4, "WIS": 3, "CHA": 1},
            "desc": "Master of hemomancy\nExcels at blood magic\nWeak in melee combat",
            "color": (120, 0, 30)
        },
        "Nightblade": {
            "stats": {"STR": 3, "DEX": 4, "CON": 2, "INT": 1, "WIS": 1, "CHA": 2},
            "desc": "Shadowy assassin\nHigh critical chance\nLow magical defense",
            "color": (30, 0, 60)
        },
        "Harbinger": {
            "stats": {"STR": 2, "DEX": 1, "CON": 4, "INT": 2, "WIS": 3, "CHA": 1},
            "desc": "Tanky frontline fighter\nHigh health pool\nSlow movement speed",
            "color": (60, 30, 0)
        },
        "Garnet Apostle": {
            "stats": {"STR": 1, "DEX": 2, "CON": 3, "INT": 3, "WIS": 4, "CHA": 0},
            "desc": "Garnet magic specialist\nBalanced abilities\nNo charisma",
            "color": (90, 0, 0)
        }
    }

    # ======================
    # INITIALIZATION
    # ======================
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        
        # Font system
        self.blood_font = load_font("OldLondon.ttf", 40, "arial")
        self.title_font = load_font("OldLondon.ttf", 72, "arial")
        self.tooltip_font = load_font("OldLondon.ttf", 32, "arial")
        
        # Audio system
        self.sounds = {
            'start_creation': load_sound('creation_start.wav'),
            'name_confirm': load_sound('name_confirm.wav'),
            'class_select': load_sound('class_select.wav'),
            'creation_complete': load_sound('creation_complete.wav'),
            'drip': load_sound('blood_drip.wav'),
            'confirm': load_sound('confirm.wav'),
            'deny': load_sound('deny.wav')
        }
        
        # State variables
        self.name = ""
        self.name_entry_complete = False
        self.cursor_visible = True
        self.cursor_timer = 0
        self.blood_animation_pos = 0
        self.class_selected = None

    # ======================
    # NAME ENTRY SYSTEM
    # ======================
    def get_blood_name(self):
        """Dark interactive name input with animated blood writing"""
        play_music("name_entry.mp3")
        clock = pygame.time.Clock()
        input_width = 500
        input_rect = pygame.Rect(
            self.screen_rect.centerx - input_width//2, 
            self.screen_rect.centery, 
            input_width, 
            60
        )
        
        # Animation variables
        blood_surface = pygame.Surface((input_width, 60), pygame.SRCALPHA)
        animation_complete = False
        
        while not self.name_entry_complete:
            dt = clock.tick(60) / 1000.0
            self.cursor_timer += dt
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.name:  # Has name
                            if self.confirm_name():
                                self.name_entry_complete = True
                                self.sounds['name_confirm'].play()
                        else:  # No name - auto accept as Rouge
                            self.name = f"Rouge {random.choice(self.DARK_TITLES)}"
                            self.name_entry_complete = True
                            self.sounds['confirm'].play()
                    elif event.key == pygame.K_BACKSPACE:
                        self.name = self.name[:-1]
                        blood_surface.fill((0, 0, 0, 0))
                        animation_complete = False
                    elif event.unicode.isalnum() and len(self.name) < 12:
                        self.name += event.unicode
                        animation_complete = False
            
            # Animation logic
            if not animation_complete and self.name:
                blood_surface = blood_text_animation(
                    self.name, 
                    self.blood_font, 
                    min(self.blood_animation_pos, len(self.name)),
                    (200, 30, 50)
                )
                self.blood_animation_pos += dt * 10
                if self.blood_animation_pos >= len(self.name):
                    animation_complete = True
                    self.sounds['drip'].play()
            
            # Rendering
            self.screen.fill((20, 0, 10))
            blood_drip_effect(self.screen)
            
            # Title
            title = self.title_font.render("NAME YOUR SHADOWBORN", True, (180, 0, 30))
            title_pos = center_horizontal(title, self.screen_rect, -150)
            self.screen.blit(title, title_pos)
            
            # Input box
            pygame.draw.rect(self.screen, (80, 0, 0), input_rect, 3)
            
            # Blood drips
            for i in range(3):
                pygame.draw.line(
                    self.screen, (120, 0, 0),
                    (input_rect.left + 50 + i*100, input_rect.bottom),
                    (input_rect.left + 70 + i*100, input_rect.bottom + 20),
                    2
                )
            
            # Animated text
            if self.name:
                self.screen.blit(blood_surface, (input_rect.left + 20, input_rect.centery - 20))
            
            # Cursor
            if self.cursor_timer % 1.0 < 0.5 and not animation_complete:
                cursor_x = input_rect.left + 20 + self.blood_font.size(self.name[:int(self.blood_animation_pos)])[0]
                pygame.draw.line(
                    self.screen, (200, 0, 0),
                    (cursor_x, input_rect.centery - 20),
                    (cursor_x, input_rect.centery + 20),
                    3
                )
            
            # Prompt
            prompt_text = "Press ENTER to confirm" if self.name else "Press ENTER to be named Rouge"
            prompt = self.blood_font.render(prompt_text, True, (100, 0, 20))
            prompt_pos = center_horizontal(prompt, self.screen_rect, 150)
            self.screen.blit(prompt, prompt_pos)
            
            pygame.display.flip()
        
        stop_music()
        return self.name

    def confirm_name(self):
        """Enhanced confirmation screen with sound"""
        confirm_width, confirm_height = 600, 400
        confirm_rect = pygame.Rect(
            self.screen_rect.centerx - confirm_width//2,
            self.screen_rect.centery - confirm_height//2,
            confirm_width,
            confirm_height
        )
        
        clock = pygame.time.Clock()
        pulse = 0
        confirmed = False
        
        self.sounds['confirm'].play()
        
        while not confirmed:
            dt = clock.tick(60) / 1000.0
            pulse = (pulse + dt * 2) % 6.28
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        confirmed = True
                        return True
                    elif event.key == pygame.K_n:
                        self.sounds['deny'].play()
                        return False
            
            # Rendering
            self.screen.fill((15, 0, 10))
            
            # Pulsing border
            pygame.draw.rect(
                self.screen, 
                (150 + int(50 * abs(math.sin(pulse))), 0, 30), 
                confirm_rect.inflate(20, 20), 
                5
            )
            
            # Dialog background
            pygame.draw.rect(self.screen, (0, 0, 0, 200), confirm_rect)
            
            # Question text (positioned above garnet)
            question = self.title_font.render(f"Accept {self.name}?", True, (180, 0, 30))
            question_pos = (confirm_rect.centerx - question.get_width()//2, confirm_rect.top + 50)
            self.screen.blit(question, question_pos)
            
            # Prompt text (positioned below garnet)
            prompt = self.blood_font.render("(Y) Blood Oath  (N) Deny Name", True, (120, 0, 20))
            prompt_pos = (confirm_rect.centerx - prompt.get_width()//2, confirm_rect.bottom - 80)
            self.screen.blit(prompt, prompt_pos)
            
            # Animated garnet (centered)
            size = 30 + int(10 * math.sin(pulse * 2))
            points = [
                (confirm_rect.centerx, confirm_rect.centery - size),
                (confirm_rect.centerx + size, confirm_rect.centery),
                (confirm_rect.centerx, confirm_rect.centery + size),
                (confirm_rect.centerx - size, confirm_rect.centery)
            ]
            pygame.draw.polygon(
                self.screen, 
                (180, 0, 30), 
                points
            )
            
            pygame.display.flip()

    # ======================
    # CLASS SELECTION SYSTEM
    # ======================
    def select_dark_class(self):
        """Class selection with tooltips"""
        play_music("class_select.mp3")
        clock = pygame.time.Clock()
        
        # Create buttons
        buttons = []
        for i, (class_name, data) in enumerate(self.DARK_CLASSES.items()):
            btn_rect = pygame.Rect(0, 0, 300, 80)
            
            # Position in a 2x2 grid
            if i < 2:
                btn_rect.center = (self.screen_rect.centerx - 200, self.screen_rect.centery - 100 + i*200)
            else:
                btn_rect.center = (self.screen_rect.centerx + 200, self.screen_rect.centery - 100 + (i-2)*200)
            
            buttons.append({
                "rect": btn_rect,
                "class": class_name,
                "color": data["color"],
                "desc": data["desc"]
            })
        
        selecting = True
        hovered_class = None
        
        while selecting:
            mouse_pos = pygame.mouse.get_pos()
            hovered_class = None
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for btn in buttons:
                        if btn["rect"].collidepoint(mouse_pos):
                            self.class_selected = btn["class"]
                            selecting = False
                            self.sounds['class_select'].play()
            
            # Check hover state
            for btn in buttons:
                if btn["rect"].collidepoint(mouse_pos):
                    hovered_class = btn
            
            # Rendering
            self.screen.fill((15, 0, 10))
            
            # Title
            title = self.title_font.render("CHOOSE YOUR DAMNATION", True, (180, 0, 30))
            title_pos = center_horizontal(title, self.screen_rect, -200)
            self.screen.blit(title, title_pos)
            
            # Draw buttons
            for btn in buttons:
                # Button base
                pygame.draw.rect(self.screen, btn["color"], btn["rect"])
                pygame.draw.rect(self.screen, (40, 0, 0), btn["rect"], 3)
                
                # Class name
                class_text = self.blood_font.render(btn["class"], True, (220, 220, 220))
                class_pos = (btn["rect"].centerx - class_text.get_width()//2, 
                            btn["rect"].centery - class_text.get_height()//2)
                self.screen.blit(class_text, class_pos)
                
                # Garnet icon
                garnet_size = 15
                pygame.draw.polygon(
                    self.screen, (180, 0, 30),
                    [
                        (btn["rect"].centerx, btn["rect"].top + garnet_size),
                        (btn["rect"].right - garnet_size, btn["rect"].centery),
                        (btn["rect"].centerx, btn["rect"].bottom - garnet_size),
                        (btn["rect"].left + garnet_size, btn["rect"].centery)
                    ]
                )
            
            # Draw tooltip if hovering
            if hovered_class:
                draw_tooltip(
                    self.screen,
                    hovered_class["desc"],
                    (mouse_pos[0] + 20, mouse_pos[1] + 20),
                    self.tooltip_font
                )
            
            pygame.display.flip()
            clock.tick(60)
        
        stop_music()
        return self.class_selected

    # ======================
    # CHARACTER CREATION FLOW
    # ======================
    def roll_cursed_stats(self):
        """3d6 but lowest die becomes 6 (dark gift)"""
        stats = {}
        for stat in ["STR", "DEX", "CON", "INT", "WIS", "CHA"]:
            rolls = sorted([random.randint(1, 6) for _ in range(3)])
            rolls[0] = 6  # Dark blessing
            stats[stat] = sum(rolls) + self.DARK_CLASSES[self.class_selected]["stats"][stat]
        return stats

    def create_shadowborn(self):
        """Complete character creation flow"""
        self.sounds['start_creation'].play()
        name = self.get_blood_name()
        if name is None:  # User quit during name entry
            return None
        
        dark_class = self.select_dark_class()
        if dark_class is None:  # User quit during class selection
            return None
        
        self.sounds['creation_complete'].play()
        
        return {
            "name": name,
            "class": dark_class,
            "stats": self.roll_cursed_stats(),
            "crimson_tears": 3,
            "garnet_shards": 1,
            "inventory": {
                "weapons": ["Rusty Dagger"],
                "armor": ["Tattered Robes"],
                "relics": [],
                "gold": random.randint(5, 20)
            }
        }