import pygame
import os
from settings import *  # Import game settings
from tile import Tile  # Import the Tile class
from player import Player  # Import the Player class
from support import *  # Import supporting functions
from weapon import Weapon  # Import the Weapon class
from ui import UI  # Import the UI class
from enemy import Enemy  # Import the Enemy class
from particles import AnimationPlayer  # Import the AnimationPlayer class
from magic import MagicPlayer  # Import the MagicPlayer class
from upgrade import Upgrade  # Import the Upgrade class
from random import choice, randint  # Import choice and randint functions for randomness

class Level:
    def __init__(self):
        # Get the display surface
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False  # Game pause state

        # Sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # Attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # Sprite setup
        self.create_map()

        # User interface
        self.ui = UI()
        self.upgrade = Upgrade(self.player)

        # Particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

        # Initialize end components
        self.target_tiles = [(86, 78), (87, 78)]  # End condition tiles
        self.game_over = False
        self.end_screen_displayed = False
        self.end_screen_surface = None

    def create_map(self):
        """
        Create the game map by loading CSV layouts and graphics.
        Initialize player, enemies, and other entities based on the map.
        """
        # Paths to CSV files
        csv_file_boundary = os.path.join("level", "level_0_floorblocks.csv")
        csv_file_entities = os.path.join("level", "level_0_entities.csv")
        csv_file_trees = os.path.join("level", "level_0_trees.csv")
        csv_file_keys = os.path.join("level", "level_0_key.csv")
        csv_file_key1 = os.path.join("level", "level_0_key1.csv")
        csv_file_cave = os.path.join("level", "level_0_cave.csv")
        csv_file_door = os.path.join("level", "level_0_door.csv")

        # Import layouts from CSV files
        layouts = {
            'boundary': import_csv_layout(csv_file_boundary),
            'entities': import_csv_layout(csv_file_entities),
            'trees': import_csv_layout(csv_file_trees),
            'keys': import_csv_layout(csv_file_keys),
            'key1': import_csv_layout(csv_file_key1),
            'cave': import_csv_layout(csv_file_cave),
            'door': import_csv_layout(csv_file_door)
        }

        # Import graphics
        graphics = {
            'trees': import_folder('graphics/trees'),
            'keys': import_folder('graphics/keys'),
            'cave': [pygame.image.load('graphics/cave/cave.png').convert_alpha()],
            'door': [pygame.image.load('graphics/door/door.png').convert_alpha()]
        }

        # Create tiles and entities based on the layouts
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                        elif style == 'entities':
                            if col == '167':
                                self.player = Player(
                                    (1220, 570),
                                    [self.visible_sprites],
                                    self.obstacle_sprites,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_magic)
                            else:
                                # Assign monster type based on the CSV value
                                if col == '27': monster_name = 'raccoon'
                                elif col == '29': monster_name = 'slime'
                                elif col == '33': monster_name = 'cyclops'
                                elif col == '34': monster_name = 'flam'
                                elif col == '35': monster_name = 'tengu'
                                else: monster_name = 'spirit'
                                Enemy(monster_name,
                                      (x, y),
                                      [self.visible_sprites, self.attackable_sprites],
                                      self.obstacle_sprites,
                                      self.damage_player,
                                      self.trigger_death_particles,
                                      self.add_gold)
                        elif style == 'trees':
                            surf = graphics['trees'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'trees', surf)
                        elif style == 'keys':
                            surf = graphics['keys'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites], 'keys', surf)
                        elif style == 'key1':
                            surf = graphics['keys'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites], 'key1', surf)
                        elif style == 'cave':
                            surf = graphics['cave'][0]
                            Tile((x, y,), [self.visible_sprites], 'cave', surf)
                        elif style == 'door':
                            surf = graphics['door'][0]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites], 'door', surf)

    def create_attack(self):
        """Create an attack if there isn't an active one."""
        if not self.current_attack:
            self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def create_magic(self, style, strength, cost):
        """Create a magic effect based on the specified style."""
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])
        elif style == 'flame':
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        """Destroy the current attack."""
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        """Handle the logic for player attacks, including collisions."""
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'keys':
                            pos = target_sprite.rect.center
                            for particle in range(randint(3, 6)):
                                self.animation_player.create_destroy_particles(pos, [self.visible_sprites])
                            target_sprite.kill()
                            self.player.add_keys(1)  # Add 1 key to the player's count
                        elif target_sprite.sprite_type == 'key1':
                            if self.player.gold >= 2000:
                                pos = target_sprite.rect.center
                                for particle in range(randint(3, 6)):
                                    self.animation_player.create_destroy_particles(pos, [self.visible_sprites])
                                target_sprite.kill()
                                self.player.add_keys(1)  # Add 1 key to the player's count
                                self.player.gold -= 2000
                        elif target_sprite.sprite_type == 'door':
                            if self.player.keys == 3:
                                pos = target_sprite.rect.center
                                for particle in range(randint(3, 6)):
                                    self.animation_player.create_destroy_particles(pos, [self.visible_sprites])
                                target_sprite.kill()
                        elif hasattr(target_sprite, 'get_damage'):  # Check if target_sprite has get_damage method
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        """Damage the player if they are vulnerable."""
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])
            if self.player.health <= 0:
                self.player.health = 0
                self.player.alive = False

    def trigger_death_particles(self, pos, particle_type):
        """Trigger death particles at the given position."""
        self.animation_player.create_particles(particle_type, pos, self.visible_sprites)

    def add_gold(self, amount):
        """Add gold to the player's total."""
        self.player.gold += amount

    def toggle_menu(self):
        """Toggle the game pause state."""
        self.game_paused = not self.game_paused

    def reset_level(self):
        """Reset the level by reinitializing it."""
        self.__init__()

    def check_end_condition(self):
        """Check if the player has reached the end condition."""
        player_tile = self.player.rect.centerx // TILESIZE, self.player.rect.centery // TILESIZE
        if player_tile in self.target_tiles:
            self.game_over = True
            self.display_end_screen()

    def display_end_screen(self):
        """Display the end screen when the game is over."""
        self.end_screen_displayed = True
        self.end_screen_surface = pygame.Surface(self.display_surface.get_size())
        self.end_screen_surface.fill((0, 0, 0))  # Black background
        font = pygame.font.Font(None, 74)
        text = font.render('You Win! Play Again?', True, (255, 255, 255))  # White text
        text_rect = text.get_rect(center=(self.display_surface.get_width() // 2, self.display_surface.get_height() // 2))
        self.end_screen_surface.blit(text, text_rect)

        prompt_font = pygame.font.Font(None, 50)
        prompt_text = prompt_font.render('Yes (Enter)', True, (255, 255, 255))
        prompt_rect = prompt_text.get_rect(center=(self.display_surface.get_width() // 2, self.display_surface.get_height() // 2 + 40))
        self.end_screen_surface.blit(prompt_text, prompt_rect)

        self.display_surface.blit(self.end_screen_surface, (0, 0))
        pygame.display.update()

    def handle_end_screen_input(self):
        """Handle user input on the end screen."""
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Press Enter to play again
                    self.reset_level()
                elif event.key == pygame.K_ESCAPE:  # Press Escape to quit
                    pygame.quit()
                    exit()

    def run(self):
        """Run the game loop, updating sprites and handling input."""
        if self.end_screen_displayed:
            self.display_surface.blit(self.end_screen_surface, (0, 0))
            pygame.display.update()
            self.handle_end_screen_input()
        else:
            self.visible_sprites.custom_draw(self.player)
            self.ui.display(self.player)

            if self.game_paused:
                # Display upgrade menu
                self.upgrade.display()
            else:
                # Run the game
                if self.player.alive:
                    self.visible_sprites.update()
                    self.visible_sprites.enemy_update(self.player)
                    self.player_attack_logic()
                    self.check_end_condition()
                else:
                    self.reset_level()

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        # General setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # Creating the floor
        self.png_path = os.path.join("level", "level_0_test.png")
        self.floor_surf = pygame.image.load(self.png_path).convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        """Custom draw method to handle the camera and rendering."""
        # Getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # Drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        # Draw sprites sorted by their y-coordinate
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        """Update all enemy sprites."""
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
