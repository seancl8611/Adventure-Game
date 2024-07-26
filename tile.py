import pygame  # Import Pygame for game development
from settings import *  # Import game settings
import os  # Import OS module for interacting with the operating system

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((TILESIZE, TILESIZE))):
        """
        Initialize a tile sprite.
        
        Parameters:
        - pos: Tuple representing the position of the tile.
        - groups: Groups the sprite belongs to.
        - sprite_type: Type of the sprite (e.g., 'trees', 'invisible').
        - surface: Surface representing the image of the tile. Defaults to a blank surface of TILESIZE.
        """
        super().__init__(groups)  # Initialize the sprite with the given groups
        self.sprite_type = sprite_type  # Set the sprite type
        y_offset = HITBOX_OFFSET[sprite_type]  # Get the hitbox offset for the sprite type
        self.image = surface  # Set the image of the tile

        # Adjust the position for tree sprites
        if sprite_type == 'trees':
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft=pos)

        self.hitbox = self.rect.inflate(0, y_offset)  # Inflate the hitbox with the y offset
