import pygame 

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        """
        Initialize the Weapon sprite.
        
        Parameters:
        - player: The player instance to which the weapon belongs.
        - groups: The sprite groups to which the weapon will be added.
        """
        super().__init__(groups)  # Initialize the sprite with the given groups
        self.sprite_type = 'weapon'  # Set the sprite type to 'weapon'
        direction = player.status.split('_')[0]  # Get the direction the player is facing

        # Load the weapon graphic
        full_path = f'graphics/weapons/{player.weapon}.png'
        try:
            self.image = pygame.image.load(full_path).convert_alpha()  # Load the weapon image
        except pygame.error as e:
            print(f"Cannot load image: {full_path}")
            raise SystemExit(e)

        # Place the weapon based on the player's direction
        if direction == 'right':
            self.rect = self.image.get_rect(midleft=player.rect.midright + pygame.math.Vector2(-90, 0))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright=player.rect.midleft + pygame.math.Vector2(90, 0))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop=player.rect.midbottom + pygame.math.Vector2(0, -90))
        else:  # direction == 'up'
            self.rect = self.image.get_rect(midbottom=player.rect.midtop + pygame.math.Vector2(0, 90))
