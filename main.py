"""
Adventure Game
Author: Sean Clarke
Date: 7/25/2024
Description: A simple adventure game using Pygame.
"""

import pygame, sys
from settings import *  # Import settings such as WIDTH, HEIGHT, and FPS
from level import Level  # Import the Level class

class Game:
    def __init__(self):
        # General setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Set up the display window
        pygame.display.set_caption('Adventure')  # Set the window caption
        self.clock = pygame.time.Clock()  # Create a clock object to manage the game's frame rate
        self.level = Level()  # Initialize the game level

        # Sound setup
        main_sound = pygame.mixer.Sound('audio/main.ogg')  # Load the main background sound
        main_sound.set_volume(0.02)  # Set the volume for the sound
        main_sound.play(loops=-1)  # Play the sound in a loop

    def run(self):
        # Main game loop
        while True:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # If the user closes the window
                    pygame.quit()  # Quit the game
                    sys.exit()  # Exit the system
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:  # If the 'm' key is pressed
                        self.level.toggle_menu()  # Toggle the menu
                    elif event.key == pygame.K_ESCAPE and self.level.game_paused:  # If 'ESC' key is pressed and the game is paused
                        self.level.toggle_menu()  # Toggle the menu

            # Update the game screen
            self.screen.fill('black')  # Fill the screen with black color
            self.level.run()  # Run the level logic
            pygame.display.update()  # Update the display
            self.clock.tick(FPS)  # Maintain the game frame rate

if __name__ == '__main__':
    game = Game()  # Create a Game object
    game.run()  # Run the game
