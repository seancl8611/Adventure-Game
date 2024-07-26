import pygame  # Import Pygame for game development
from settings import *  # Import game settings
import os  # Import OS module for interacting with the operating system

class UI:
    def __init__(self):
        """
        Initialize the UI class.
        """
        # General setup
        self.display_surface = pygame.display.get_surface()  # Get the display surface
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)  # Set the font for UI text

        # Medium-sized font for the upgrade menu text
        self.medium_font = pygame.font.Font(UI_FONT, int(UI_FONT_SIZE * 0.75))

        # Bar setup
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)  # Rect for the health bar
        self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)  # Rect for the energy bar

        # Convert magic dictionary to graphics
        self.magic_graphics = []
        for magic in magic_data.values():
            magic = pygame.image.load(magic['graphic']).convert_alpha()
            self.magic_graphics.append(magic)
            
        # Load the key icon image and enlarge it
        self.key_image = pygame.image.load(os.path.join('graphics', 'keys', 'key_icon.png')).convert_alpha()
        self.key_image = pygame.transform.scale(self.key_image, (64, 64))  # Adjust size as needed

        # Load the gold icon image
        self.gold_image = pygame.image.load(os.path.join('graphics', 'gold', 'gold.png')).convert_alpha()
        self.gold_image = pygame.transform.scale(self.gold_image, (32, 32))  # Adjust size as needed

    def show_bar(self, current, max_amount, bg_rect, color):
        """
        Display a bar (health or energy) on the screen.
        """
        # Draw background
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # Convert stat to pixel ratio
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # Draw the bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_gold(self, gold):
        """
        Display the gold count on the screen.
        """
        # Position the gold icon and text
        screen_width = self.display_surface.get_size()[0]
        x_icon = screen_width - 130
        y_icon = self.display_surface.get_size()[1] - 50
        gold_icon_rect = self.gold_image.get_rect(topleft=(x_icon, y_icon))

        text_surf = self.font.render(str(int(gold)), False, TEXT_COLOR)
        text_rect = text_surf.get_rect(midleft=(gold_icon_rect.right + 22, gold_icon_rect.centery))

        # Draw background for text
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)

        # Blit gold icon and text to the display
        self.display_surface.blit(self.gold_image, gold_icon_rect)
        self.display_surface.blit(text_surf, text_rect)

    def show_keys(self, keys):
        """
        Display the key count on the screen.
        """
        # Position the key icon
        screen_width = self.display_surface.get_size()[0]
        x_icon = screen_width - 160
        y_icon = self.display_surface.get_size()[1] - 115
        key_rect = self.key_image.get_rect(topleft=(x_icon, y_icon))

        # Position the key count text to the right of the key icon
        text_surf = self.font.render(str(int(keys)), False, TEXT_COLOR)
        text_rect = text_surf.get_rect(midleft=(key_rect.right + 20, key_rect.centery))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)
        self.display_surface.blit(self.key_image, key_rect)
        self.display_surface.blit(text_surf, text_rect)

    def show_upgrade_menu_text(self):
        """
        Display the upgrade menu prompt on the screen.
        """
        text_surf = self.medium_font.render("(M): Upgrade Menu", False, TEXT_COLOR)
        screen_width = self.display_surface.get_size()[0]
        text_rect = text_surf.get_rect(midtop=(screen_width - 100, self.display_surface.get_size()[1] - 130))

        self.display_surface.blit(text_surf, text_rect)

    def selection_box(self, left, top, has_switched):
        """
        Draw a selection box for items such as weapons or magic.
        """
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        return bg_rect

    def magic_overlay(self, magic_index, has_switched):
        """
        Display the current magic selection overlay.
        """
        bg_rect = self.selection_box(10, 630, has_switched)
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center=bg_rect.center)

        self.display_surface.blit(magic_surf, magic_rect)

    def display(self, player):
        """
        Display all UI elements including bars, gold, keys, and magic.
        """
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)

        self.show_gold(player.gold)
        self.show_keys(player.keys)
        self.show_upgrade_menu_text()

        self.magic_overlay(player.magic_index, not player.can_switch_magic)
