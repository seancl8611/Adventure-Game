import pygame
from support import import_folder  # Import the function to import images from folders
from random import choice  # Import choice for random selection

class AnimationPlayer:
    def __init__(self):
        # Initialize animation frames for various effects
        self.frames = {
            # Magic effects
            'flame': import_folder('graphics/particles/fire_frames'),
            'heal': import_folder('graphics/particles/heal_frames'),
            'aura': import_folder('graphics/particles/aura'),

            # Attack effects
            'claw': import_folder('graphics/particles/claw'),
            'slash': import_folder('graphics/particles/slash'),

            # Monster death effects
            'spirit': import_folder('graphics/particles/smoke_orange'),
            'slime': import_folder('graphics/particles/smoke'),
            'raccoon': import_folder('graphics/particles/nova'),
            'cyclops': import_folder('graphics/particles/nova'),
            'flam': import_folder('graphics/particles/smoke_orange'),
            'tengu': import_folder('graphics/particles/nova'),

            # Destroy particles
            'destroy': (
                import_folder('graphics/particles/destroy1'),
                import_folder('graphics/particles/destroy2'),
                self.reflect_images(import_folder('graphics/particles/destroy1')),
                self.reflect_images(import_folder('graphics/particles/destroy2'))
            )
        }

    def reflect_images(self, frames):
        """
        Create reflected (flipped) versions of the given frames.
        """
        new_frames = []

        for frame in frames:
            flipped_frame = pygame.transform.flip(frame, True, False)  # Flip the frame horizontally
            new_frames.append(flipped_frame)
        return new_frames

    def create_destroy_particles(self, pos, groups):
        """
        Create destroy particles at the given position.
        """
        animation_frames = choice(self.frames['destroy'])  # Randomly select a destroy animation
        ParticleEffect(pos, animation_frames, groups)

    def create_particles(self, animation_type, pos, groups):
        """
        Create particles of the specified animation type at the given position.
        """
        animation_frames = self.frames[animation_type]  # Get the frames for the specified animation type
        ParticleEffect(pos, animation_frames, groups)

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups):
        # Initialize the particle effect sprite
        super().__init__(groups)
        self.sprite_type = 'magic'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        """
        Animate the particle effect by updating the frame index.
        Kill the sprite if the animation is complete.
        """
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()  # Remove the sprite from all groups
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        """
        Update the particle effect animation.
        """
        self.animate()
