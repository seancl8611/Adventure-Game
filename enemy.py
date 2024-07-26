import pygame
from entity import Entity  # Import the Entity base class
from support import import_folder  # Import the function to import graphics from a folder
from settings import *  # Import game settings

class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player, trigger_death_particles, add_gold):
        super().__init__(groups)
        self.sprite_type = 'enemy'

        # Graphics setup
        self.status = 'idle'
        self.frame_index = 0
        self.import_graphics(monster_name)

        # Movement setup
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites

        # Stats setup
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.gold = monster_info['gold']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']

        # Player interaction setup
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles
        self.add_gold = add_gold

        # Invincibility timer setup
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300

        # Sounds setup
        self.death_sound = pygame.mixer.Sound('audio/attack/death.wav')
        self.hit_sound = pygame.mixer.Sound('audio/attack/Hit.wav')
        self.attack_sound = pygame.mixer.Sound(monster_info['attack_sound'])
        self.death_sound.set_volume(0.02)
        self.hit_sound.set_volume(0.02)
        self.attack_sound.set_volume(0.02)

    def import_graphics(self, name):
        # Load enemy animations
        self.animations = {'idle': [], 'move': [], 'attack': []}
        main_path = f'graphics/enemies/{name}/'
        for animation in self.animations.keys():
            full_path = main_path + animation
            self.animations[animation] = import_folder(full_path)

        # Ensure there are animation frames for the current status
        if not self.animations[self.status]:
            raise ValueError(f"No animation frames found for status '{self.status}' in '{main_path}'")

        self.image = self.animations[self.status][self.frame_index]

    def get_player_distance_direction(self, player):
        # Calculate distance and direction to the player
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()
        
        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance, direction)

    def get_status(self, player):
        # Determine the enemy's status based on distance to the player
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def actions(self, player):
        # Define enemy actions based on status
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)
            self.attack_sound.play()
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        # Handle enemy animation
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldowns(self):
        # Handle attack and invincibility cooldowns
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
        
        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def get_damage(self, player, attack_type):
        # Handle damage taken by the enemy
        if self.vulnerable:
            self.hit_sound.play()
            self.direction = self.get_player_distance_direction(player)[1]
            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage()
            else:
                self.health -= player.get_full_magic_damage()
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        # Check if the enemy is dead
        if self.health <= 0:
            self.kill()
            self.trigger_death_particles(self.rect.center, self.monster_name)
            self.add_gold(self.gold)
            self.death_sound.play()

    def hit_reaction(self):
        # Handle enemy's reaction to being hit
        if not self.vulnerable:
            self.direction *= -self.resistance

    def update(self):
        # Update enemy behavior and status
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldowns()
        self.check_death()

    def enemy_update(self, player):
        # Update enemy's status and actions based on the player's position
        self.get_status(player)
        self.actions(player)
