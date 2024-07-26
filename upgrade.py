import pygame  # Import Pygame for game development
from settings import *  # Import game settings
import os  # Import OS module for interacting with the operating system

class Upgrade:
    def __init__(self, player):
        """
        Initialize the Upgrade class.
        """
        # General setup
        self.display_surface = pygame.display.get_surface()  # Get the display surface
        self.player = player  # Reference to the player object
        self.attribute_nr = len(player.stats)  # Number of attributes
        self.attribute_names = list(player.stats.keys())  # Names of the attributes
        self.max_values = list(player.max_stats.values())  # Maximum values of the attributes
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)  # Set the font for UI text
        self.gold_image = pygame.image.load('graphics/gold/gold.png').convert_alpha()  # Load the gold icon image
        self.gold_image = pygame.transform.scale(self.gold_image, (20, 20))  # Resize the gold icon image

        # Item creation
        self.height = self.display_surface.get_size()[1] * 0.8  # Height of each item
        self.width = self.display_surface.get_size()[0] // 6  # Width of each item
        self.create_items()  # Create the items

        # Selection system
        self.selection_index = 0  # Currently selected item index
        self.selection_time = None  # Time of the last selection
        self.can_move = True  # Flag to check if the selection can be moved

    def input(self):
        """
        Handle user input for navigating the upgrade menu.
        """
        keys = pygame.key.get_pressed()

        if self.can_move:
            if keys[pygame.K_RIGHT] and self.selection_index < self.attribute_nr - 1:
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_LEFT] and self.selection_index >= 1:
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

            if keys[pygame.K_SPACE]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.item_list[self.selection_index].trigger(self.player)

    def selection_cooldown(self):
        """
        Handle the cooldown between selections to prevent rapid switching.
        """
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 300:
                self.can_move = True

    def create_items(self):
        """
        Create the upgrade items based on player attributes.
        """
        self.item_list = []

        for item, index in enumerate(range(self.attribute_nr)):
            # Horizontal position
            full_width = self.display_surface.get_size()[0]
            increment = full_width // self.attribute_nr
            left = (item * increment) + (increment - self.width) // 2

            # Vertical position
            top = self.display_surface.get_size()[1] * 0.1

            # Create the item object
            item = Item(left, top, self.width, self.height, index, self.font)
            self.item_list.append(item)

    def display(self):
        """
        Display the upgrade menu and handle user input.
        """
        self.input()
        self.selection_cooldown()

        for index, item in enumerate(self.item_list):
            # Get attributes
            name = self.attribute_names[index]
            value = self.player.get_value_by_index(index)
            max_value = self.max_values[index]
            cost = self.player.get_cost_by_index(index)
            item.display(self.display_surface, self.selection_index, name, value, max_value, cost, self.gold_image)

class Item:
    def __init__(self, l, t, w, h, index, font):
        """
        Initialize an Item object for the upgrade menu.
        
        Parameters:
        - l: Left position of the item
        - t: Top position of the item
        - w: Width of the item
        - h: Height of the item
        - index: Index of the item
        - font: Font used for rendering text
        """
        self.rect = pygame.Rect(l, t, w, h)  # Rectangle representing the item's area
        self.index = index  # Index of the item
        self.font = font  # Font used for rendering text

    def display_names(self, surface, name, cost, selected, gold_image):
        """
        Display the name and cost of the upgrade item.
        """
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR

        # Title
        title_surf = self.font.render(name, False, color)
        title_rect = title_surf.get_rect(midtop=self.rect.midtop + pygame.math.Vector2(0, 20))

        # Cost
        cost_surf = self.font.render(f'{int(cost)}', False, color)
        cost_rect = cost_surf.get_rect(midbottom=self.rect.midbottom - pygame.math.Vector2(0, 20))

        # Gold image
        gold_image_rect = gold_image.get_rect(midbottom=self.rect.midbottom - pygame.math.Vector2(35, 20))
        
        # Draw elements
        surface.blit(title_surf, title_rect)
        surface.blit(gold_image, gold_image_rect)
        surface.blit(cost_surf, cost_rect)

    def display_bar(self, surface, value, max_value, selected):
        """
        Display the progress bar representing the attribute's value.
        """
        # Drawing setup
        top = self.rect.midtop + pygame.math.Vector2(0, 60)
        bottom = self.rect.midbottom - pygame.math.Vector2(0, 60)
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR

        # Bar setup
        full_height = bottom[1] - top[1]
        relative_number = (value / max_value) * full_height
        value_rect = pygame.Rect(top[0] - 15, bottom[1] - relative_number, 30, 10)

        # Draw elements
        pygame.draw.line(surface, color, top, bottom, 5)
        pygame.draw.rect(surface, color, value_rect)

    def trigger(self, player):
        """
        Trigger the upgrade for the player's attribute.
        """
        upgrade_attribute = list(player.stats.keys())[self.index]
        
        if player.gold >= player.upgrade_cost[upgrade_attribute] and player.stats[upgrade_attribute] < player.max_stats[upgrade_attribute]:
            player.gold -= player.upgrade_cost[upgrade_attribute]
            player.stats[upgrade_attribute] *= 1.2
            player.upgrade_cost[upgrade_attribute] *= 1.4

        if player.stats[upgrade_attribute] > player.max_stats[upgrade_attribute]:
            player.stats[upgrade_attribute] = player.max_stats[upgrade_attribute]

    def display(self, surface, selection_num, name, value, max_value, cost, gold_image):
        """
        Display the upgrade item, including its name, cost, and progress bar.
        """
        if self.index == selection_num:
            pygame.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)
        else:
            pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)

        self.display_names(surface, name, cost, self.index == selection_num, gold_image)
        self.display_bar(surface, value, max_value, self.index == selection_num)
