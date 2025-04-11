import pygame
import sys
import random
from utils import (
    load_font,
    load_sound,
    play_music,
    stop_music,
    fade_in,
    wrap_text,
    center_horizontal
)

class DarkRPG:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("GARNET: Shadowborn")
        self.clock = pygame.time.Clock()
        
        # Font system
        self.font_title = load_font("OldLondon.ttf", 96, "arial")
        self.font_subtitle = load_font("OldLondon.ttf", 64, "arial")
        self.font_crimson = load_font("OldLondon.ttf", 42, "arial")
        self.font_regular = load_font("OldLondon.ttf", 36, "arial")
        
        # Game states
        self.current_state = "title"
        self.player = None
        self.current_music = None

        # Title screen garnet sprite
        try:
            self.title_garnet = pygame.image.load("assets/sprites/title_garnet.png").convert_alpha()
            self.title_garnet = pygame.transform.scale(self.title_garnet, (300, 300))
        except:
            # Fallback if sprite missing
            self.title_garnet = pygame.Surface((300, 300), pygame.SRCALPHA)
            pygame.draw.polygon(self.title_garnet, (180, 0, 30), 
                              [(150, 0), (300, 150), (150, 300), (0, 150)])

    def show_title_screen(self):
        """Enhanced title screen with subtitle"""
        # Pulsing background effect
        pulse = int(pygame.time.get_ticks() / 300) % 10
        self.screen.fill((10 + pulse//2, 0, 5 + pulse//3))
        
        # Draw title garnet sprite (centered)
        garnet_pos = (
            self.screen.get_width()//2 - self.title_garnet.get_width()//2,
            self.screen.get_height()//2 - self.title_garnet.get_height()//2 - 50
        )
        self.screen.blit(self.title_garnet, garnet_pos)
        
        # Main title with shadow
        title = self.font_title.render("GARNET", True, (180, 4, 45))
        title_shadow = self.font_title.render("GARNET", True, (80, 0, 0))
        title_pos = (self.screen.get_width()//2 - title.get_width()//2, 150)
        self.screen.blit(title_shadow, (title_pos[0]+5, title_pos[1]+5))
        self.screen.blit(title, title_pos)
        
        # Subtitle
        subtitle = self.font_subtitle.render("Shadowborn", True, (150, 30, 30))
        sub_pos = (self.screen.get_width()//2 - subtitle.get_width()//2, 250)
        self.screen.blit(subtitle, sub_pos)
        
        # Pulsing prompt with wrapped text
        if pygame.time.get_ticks() % 2000 < 1000:
            prompt_text = "Press SPACE to begin your dark journey"
            prompt_lines = wrap_text(prompt_text, self.font_crimson, self.screen.get_width() - 200)
            
            for i, line in enumerate(prompt_lines):
                prompt = self.font_crimson.render(line, True, (200, 200, 200))
                prompt_pos = (
                    self.screen.get_width()//2 - prompt.get_width()//2,
                    550 + i * 50
                )
                self.screen.blit(prompt, prompt_pos)

    def show_character_summary(self):
        """Enhanced character summary with wrapped text"""
        self.screen.fill((15, 0, 10))
        
        # Title with shadow
        title = self.font_title.render("SHADOWBORN CREATED", True, (180, 0, 30))
        title_shadow = self.font_title.render("SHADOWBORN CREATED", True, (80, 0, 0))
        title_pos = (self.screen.get_width()//2 - title.get_width()//2, 50)
        self.screen.blit(title_shadow, (title_pos[0]+3, title_pos[1]+3))
        self.screen.blit(title, title_pos)
        
        # Character info with wrapped text
        info_lines = [
            f"{self.player['name']}",
            f"{self.player['class']}",
            "",
            f"STR: {self.player['stats']['STR']}  DEX: {self.player['stats']['DEX']}",
            f"CON: {self.player['stats']['CON']}  INT: {self.player['stats']['INT']}",
            f"WIS: {self.player['stats']['WIS']}  CHA: {self.player['stats']['CHA']}",
            "",
            "Inventory:",
            f"Weapon: {self.player['inventory']['weapons'][0]}",
            f"Armor: {self.player['inventory']['armor'][0]}",
            f"Gold: {self.player['inventory']['gold']}"
        ]
        
        y_offset = 150
        for line in info_lines:
            if not line:  # Empty line for spacing
                y_offset += 30
                continue
                
            wrapped = wrap_text(line, self.font_regular, self.screen.get_width() - 200)
            for wrapped_line in wrapped:
                text = self.font_regular.render(wrapped_line, True, (200, 100, 100))
                self.screen.blit(text, (self.screen.get_width()//2 - text.get_width()//2, y_offset))
                y_offset += 40
        
        # Confirmation prompt with wrapped text
        prompt_text = "Are you happy with your Shadowborn? (Y) Yes  (N) No"
        prompt_lines = wrap_text(prompt_text, self.font_crimson, self.screen.get_width() - 200)
        
        for i, line in enumerate(prompt_lines):
            prompt = self.font_crimson.render(line, True, (180, 30, 30))
            prompt_pos = (
                self.screen.get_width()//2 - prompt.get_width()//2,
                600 + i * 50
            )
            self.screen.blit(prompt, prompt_pos)

    def run(self):
        """Main game loop with improved state handling"""
        running = True
        play_music("title_theme.mp3")
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # State transitions
                if event.type == pygame.KEYDOWN:
                    if self.current_state == "title" and event.key == pygame.K_SPACE:
                        fade_in(self.screen, (0, 0, 0), 2)
                        self.current_state = "creation"
                        play_music("creation_theme.mp3")
                    
                    elif self.current_state == "summary":
                        if event.key == pygame.K_y:
                            self.current_state = "game"
                            play_music("game_theme.mp3")
                        elif event.key == pygame.K_n:
                            self.current_state = "creation"
                            play_music("creation_theme.mp3")
                            self.player = None
            
            # State rendering
            if self.current_state == "title":
                self.show_title_screen()
            
            elif self.current_state == "creation":
                if not self.player:
                    from character import ShadowbornCreation
                    creator = ShadowbornCreation(self.screen)
                    self.player = creator.create_shadowborn()
                    if self.player:
                        # Add random title to player name if not Rouge
                        if not self.player['name'].startswith("Rouge"):
                            titles = [
                                "the Bloodsoaked", "of the Crimson Veil", 
                                "the Cursed", "the Shadow Walker",
                                "the Dark Herald", "the Forsaken"
                            ]
                            self.player['name'] = f"{self.player['name']} {random.choice(titles)}"
                        
                        self.current_state = "summary"
                        play_music("summary_theme.mp3")
            
            elif self.current_state == "summary":
                self.show_character_summary()
            
            elif self.current_state == "game":
                self.screen.fill((0, 10, 20))
                # Main game rendering would go here
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = DarkRPG()
    game.run()