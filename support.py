from csv import reader  # Import the CSV reader for reading CSV files
import os  # Import OS module for interacting with the operating system
import pygame  # Import Pygame for game development
from os import walk  # Import walk function for directory traversal

def import_csv_layout(path):
    """
    Import a CSV layout from the given file path.
    Returns a list of lists representing the terrain map.
    """
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=',')
        for row in layout:
            terrain_map.append(list(row))
    return terrain_map

def import_folder(path):
    """
    Import all images from the specified folder.
    Returns a list of surfaces representing the images.
    """
    surface_list = []
    
    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = os.path.join(path, image)
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list
