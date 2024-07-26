import pygame
from settings import *  # Import game settings
from random import randint  # Import randint for random number generation

class MagicPlayer:
    def __init__(self, animation_player):
        # Initialize the MagicPlayer with an animation player
        self.animation_player = animation_player
        self.sounds = {
            'heal': pygame.mixer.Sound('audio/attack/heal.wav'),  # Load healing sound
            'flame': pygame.mixer.Sound('audio/attack/Fireball.wav')  # Load flame sound
        }

    def heal(self, player, strength, cost, groups):
        """
        Heal the player if they have enough energy.
        Play healing sound and create healing particles.
        """
        if player.energy >= cost:
            # Play healing sound
            self.sounds['heal'].set_volume(0.06)
            self.sounds['heal'].play()

            # Increase player's health and decrease energy
            player.health += strength
            player.energy -= cost

            # Ensure player's health does not exceed maximum
            if player.health >= player.stats['health']:
                player.health = player.stats['health']

            # Create healing particles
            self.animation_player.create_particles('aura', player.rect.center, groups)
            self.animation_player.create_particles('heal', player.rect.center + pygame.math.Vector2(0, -60), groups)

    def flame(self, player, cost, groups):
        """
        Create a flame attack if the player has enough energy.
        Play flame sound and create flame particles in the direction the player is facing.
        """
        if player.energy >= cost:
            # Decrease player's energy
            player.energy -= cost

            # Play flame sound
            self.sounds['flame'].set_volume(0.016)
            self.sounds['flame'].play()

            # Determine the direction of the flame attack
            if player.status.split("_")[0] == 'right':
                direction = pygame.math.Vector2(1, 0)
            elif player.status.split("_")[0] == 'left':
                direction = pygame.math.Vector2(-1, 0)
            elif player.status.split("_")[0] == 'up':
                direction = pygame.math.Vector2(0, -1)
            else:
                direction = pygame.math.Vector2(0, 1)

            # Create flame particles in the determined direction
            for i in range(1, 6):
                if direction.x:  # Horizontal direction
                    offset_x = (direction.x * i) * TILESIZE
                    x = player.rect.centerx + offset_x + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles('flame', (x, y), groups)
                else:  # Vertical direction
                    offset_y = (direction.y * i) * TILESIZE
                    x = player.rect.centerx + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + offset_y + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles('flame', (x, y), groups)
