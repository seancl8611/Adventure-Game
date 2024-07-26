import pygame
from math import sin  # Import the sin function from the math module

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.1  # Adjusted speed for slower animation
        self.direction = pygame.math.Vector2()  # Initialize direction as a vector

    def move(self, speed):
        """
        Move the entity in the direction vector at the given speed.
        Handles both horizontal and vertical movement and checks for collisions.
        """
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # Move horizontally and check for collisions
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')

        # Move vertically and check for collisions
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')

        # Update the position of the sprite's rectangle
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        """
        Check and resolve collisions in the given direction (horizontal or vertical).
        Adjust the hitbox position to prevent overlapping with obstacle sprites.
        """
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # Moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # Moving left
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # Moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # Moving up
                        self.hitbox.top = sprite.hitbox.bottom

    def wave_value(self):
        """
        Calculate a wave value based on the current time.
        Returns 255 if the value is non-negative, otherwise returns 0.
        This can be used for creating a wave-like animation effect.
        """
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0
