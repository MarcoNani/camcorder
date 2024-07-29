import os # for the files paths and other useful stuffs
import json # for reading the preferences file
import print_color # for the colored prints

# CONSTANTS
DEFAULT_PREFERENCES_PATH = os.path.join("config", "preferences.json")

DEFAULT_PREFERENCES = {
    "destination_folder": "transferred_videos",
    "in_secure_mode": True,
    "in_debug_mode": True,
    "root_camcorder": "",
    "size_limit": 2124000000
}


# FUNCTIONS
def load_preferences(filename=DEFAULT_PREFERENCES_PATH):
    try:
        with open(filename, 'r') as file:
            preferences = json.load(file)
    except FileNotFoundError:
        print_color.red("Preferences file not found. Using default preferences.")
        preferences = DEFAULT_PREFERENCES
    except json.JSONDecodeError:
        print_color.red("Corrupted or invalid preferences file. Using default preferences.")
        preferences = DEFAULT_PREFERENCES
    return preferences

def save_preferences(preferences, filename=DEFAULT_PREFERENCES_PATH):
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    with open(filename, 'w') as file:
        json.dump(preferences, file, indent=4)

def validate_preferences(preferences):
    if not isinstance(preferences.get('destination_folder'), str):
        print_color.yellow(f"Invalid destination folder (must be a string). Using default preference: {DEFAULT_PREFERENCES['destination_folder']}.")
        preferences['destination_folder'] = DEFAULT_PREFERENCES['destination_folder']
    if not isinstance(preferences.get('in_secure_mode'), bool):
        print_color.yellow(f"Invalid in secure mode (must be true or false). Using default preference: {DEFAULT_PREFERENCES['in_secure_mode']}.")
        preferences['in_secure_mode'] = DEFAULT_PREFERENCES['in_secure_mode']
    if not isinstance(preferences.get('in_debug_mode'), bool):
        print_color.yellow(f"Invalid in debug mode (must be true or false). Using default preference: {DEFAULT_PREFERENCES['in_debug_mode']}.")
        preferences['in_debug_mode'] = DEFAULT_PREFERENCES['in_debug_mode']
    if not isinstance(preferences.get('root_camcorder'), str):
        print_color.yellow(f"Invalid root camcorder path (must be a string). Using default preference: {DEFAULT_PREFERENCES['root_camcorder']}.")
        preferences['root_camcorder'] = DEFAULT_PREFERENCES['root_camcorder']
    if not isinstance(preferences.get('size_limit'), int):
        print_color.yellow(f"Invalid size limit (must be a number (bytes)). Using default preference: {DEFAULT_PREFERENCES['size_limit']}.")
        preferences['size_limit'] = DEFAULT_PREFERENCES['size_limit']
    return preferences

def preferences_routine():
    current_preferences = load_preferences()

    if current_preferences["in_debug_mode"]:
        print_color.purple("Current preferences:")
        print_color.purple(current_preferences)

    current_preferences = validate_preferences(current_preferences)

    if current_preferences["in_debug_mode"]:
        print_color.purple("Validated preferences:")
        print_color.purple(current_preferences)

    if current_preferences["root_camcorder"] == "":
        print_color.red("The root camcorder path is not set in the preferences file.")
        print_color.red("Please set the root camcorder path in the preferences file or enter it now.")
        # request of the root camcorder path
        input_root_camcorder = input("Camcorder root path: ")
        current_preferences["root_camcorder"] = input_root_camcorder
    
    return current_preferences
