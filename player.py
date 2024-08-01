import pygame
import os
from settings import *  # Import game settings
from support import import_folder  # Import the function to import images from folders
from entity import Entity  # Import the Entity base class

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic):
        # Initialize the Player class
        super().__init__(groups)
        self.image_path = os.path.join("graphics", "player.png")
        self.image = pygame.image.load(self.image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-6, HITBOX_OFFSET['player'])

        # Graphics setup
        self.import_player_assets()
        self.status = 'down'

        # Movement
        self.attacking = False
        self.attack_cooldown = 300  # Cooldown duration for attacks
        self.attack_time = None
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.obstacle_sprites = obstacle_sprites

        # Weapon
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.switch_duration_cooldown = 200

        # Magic
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        # Stats
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 5}
        self.max_stats = {'health': 300, 'energy': 140, 'attack': 20, 'magic': 10, 'speed': 10}
        self.upgrade_cost = {'health': 100, 'energy': 100, 'attack': 100, 'magic': 100, 'speed': 100}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.gold = 0
        self.speed = self.stats['speed']
        
        # Keys
        self.keys = 0

        # Damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

        # Import sound
        self.weapon_attack_sound = pygame.mixer.Sound('audio/attack/sword.wav')
        self.weapon_attack_sound.set_volume(0.015)

    def import_player_assets(self):
        """
        Import player animations from the specified folder.
        """
        character_path = 'graphics/player/'
        self.animations = {
            'up': [], 'down': [], 'left': [], 'right': [],
            'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
            'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []
        }

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        """
        Handle player input for movement, attacks, and magic.
        """
        keys = pygame.key.get_pressed()

        if not self.attacking:
            # Movement input
            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0

        # Attack input
        if keys[pygame.K_SPACE] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.create_attack()
            self.weapon_attack_sound.play()

        # Magic input
        if keys[pygame.K_LCTRL] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()

            style = list(magic_data.keys())[self.magic_index]
            strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
            cost = list(magic_data.values())[self.magic_index]['cost']
            self.create_magic(style, strength, cost)

        # Switch magic input
        if keys[pygame.K_e] and self.can_switch_magic:
            self.can_switch_magic = False
            self.magic_switch_time = pygame.time.get_ticks()

            if self.magic_index < len(list(magic_data.keys())) - 1:
                self.magic_index += 1
            else:
                self.magic_index = 0

            self.magic = list(magic_data.keys())[self.magic_index]

    def get_status(self):
        """
        Update player status based on movement and actions.
        """
        if self.direction.x == 0 and self.direction.y == 0 and not self.attacking:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    def cooldowns(self):
        """
        Handle cooldowns for attacks, magic switching, and invulnerability.
        """
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def animate(self):
        """
        Handle player animation based on the current status.
        """
        animation = self.animations[self.status]

        # Loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.attacking = False  # Reset attacking state
                self.frame_index = len(animation) - 1  # Ensure the last frame is shown
            else:
                self.frame_index = 0

        # Set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)
        
        # Flicker effect when not vulnerable
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
        
    def get_full_weapon_damage(self):
        """
        Calculate the full weapon damage including base and weapon-specific damage.
        """
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage

    def get_full_magic_damage(self):
        """
        Calculate the full magic damage including base and spell-specific damage.
        """
        base_damage = self.stats['magic']
        spell_damage = magic_data[self.magic]['strength']
        return base_damage + spell_damage

    def get_value_by_index(self, index):
        """
        Get the value of a stat by its index.
        """
        return list(self.stats.values())[index]

    def get_cost_by_index(self, index):
        """
        Get the upgrade cost of a stat by its index.
        """
        return list(self.upgrade_cost.values())[index]

    def energy_recovery(self):
        """
        Recover player's energy over time.
        """
        if self.energy < self.stats['energy']:
            self.energy += 0.01 * self.stats['magic']
        else:
            self.energy = self.stats['energy']

    def add_keys(self, amount):
        """
        Add keys to the player's inventory.
        """
        self.keys += amount

    def update(self):
        """
        Update the player's state and actions.
        """
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.stats['speed'])
        self.energy_recovery()
