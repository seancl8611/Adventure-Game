# Screen settings
WIDTH = 1280  # Width of the game window
HEIGHT = 720  # Height of the game window
FPS = 60  # Frames per second
TILESIZE = 64  # Size of each tile in pixels

# Hitbox offsets for different objects
HITBOX_OFFSET = {
    'player': -26,
    'trees': -100,
    'invisible': -30,
    'keys': -30,
    'key1': -30,
    'door': -30,
    'cave': 0
}

# UI settings
BAR_HEIGHT = 20  # Height of the health and energy bars
HEALTH_BAR_WIDTH = 200  # Width of the health bar
ENERGY_BAR_WIDTH = 140  # Width of the energy bar
ITEM_BOX_SIZE = 80  # Size of the item box
UI_FONT = 'graphics/font/joystix.ttf'  # Font used for UI text
UI_FONT_SIZE = 18  # Font size for UI text

# General colors
WATER_COLOR = '#71ddee'  # Color of the water
UI_BG_COLOR = '#222222'  # Background color of the UI
UI_BORDER_COLOR = '#111111'  # Border color of the UI
TEXT_COLOR = '#EEEEEE'  # Text color for the UI

# UI colors
HEALTH_COLOR = 'red'  # Color of the health bar
ENERGY_COLOR = 'blue'  # Color of the energy bar
UI_BORDER_COLOR_ACTIVE = 'gold'  # Border color when an item is active

# Upgrade menu colors
TEXT_COLOR_SELECTED = '#111111'  # Text color when selected in the upgrade menu
BAR_COLOR = '#EEEEEE'  # Color of the bar in the upgrade menu
BAR_COLOR_SELECTED = '#111111'  # Color of the selected bar in the upgrade menu
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'  # Background color of the selected item in the upgrade menu

# Weapon data
weapon_data = {
    'sword': {'cooldown': 100, 'damage': 15, 'graphic': '/graphics/weapons/sword.png'}
}

# Magic data
magic_data = {
    'flame': {'strength': 5, 'cost': 20, 'graphic': 'graphics/particles/fire.png'},
    'heal' : {'strength': 20, 'cost': 10, 'graphic': 'graphics/particles/heal.png'}
}

# Enemy data
monster_data = {
    'spirit': {
        'health': 100,
        'gold': 150,
        'damage': 10,
        'attack_type': 'slash',
        'attack_sound': 'audio/enemies/fireball.wav',
        'speed': 2,
        'resistance': 3,
        'attack_radius': 50,
        'notice_radius': 360
    },
    'slime': {
        'health': 70,
        'gold': 160,
        'damage': 5,
        'attack_type': 'slash',
        'attack_sound': 'audio/enemies/slash.wav',
        'speed': 3,
        'resistance': 3,
        'attack_radius': 50,
        'notice_radius': 350
    },
    'raccoon': {
        'health': 300,
        'gold': 300,
        'damage': 20,
        'attack_type': 'claw',
        'attack_sound': 'audio/enemies/claw.wav',
        'speed': 2,
        'resistance': 3,
        'attack_radius': 110,
        'notice_radius': 350
    },
    'cyclops': {
        'health': 300,
        'gold': 300,
        'damage': 20,
        'attack_type': 'claw',
        'attack_sound': 'audio/enemies/claw.wav',
        'speed': 2,
        'resistance': 3,
        'attack_radius': 100,
        'notice_radius': 350
    },
    'flam': {
        'health': 200,
        'gold': 300,
        'damage': 20,
        'attack_type': 'claw',
        'attack_sound': 'audio/enemies/claw.wav',
        'speed': 2,
        'resistance': 3,
        'attack_radius': 110,
        'notice_radius': 350
    },
    'tengu': {
        'health': 300,
        'gold': 300,
        'damage': 20,
        'attack_type': 'claw',
        'attack_sound': 'audio/enemies/claw.wav',
        'speed': 2,
        'resistance': 3,
        'attack_radius': 100,
        'notice_radius': 350
    }
}
