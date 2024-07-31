import os
import json
import print_color

# CONSTANTS
DEFAULT_PREFERENCES_PATH = os.path.join("config", "preferences.json")

DEFAULT_PREFERENCES = {
    "destination_folder": "",
    "in_secure_mode": True,
    "in_debug_mode": True,
    "root_camcorder": "",
    "size_limit": 2124000000,
    "H264_low": {
        "enabled": True,
        "bitrate": "4M"
    },
    "H264_high": {
        "enabled": True,
        "bitrate": "8M"
    },
    "H265_VBR": {
        "enabled": True,
        "CRF": "23"
    }
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
    # Ensure all required keys are present and valid
    for key, default_value in DEFAULT_PREFERENCES.items():
        if key not in preferences:
            print_color.yellow(f"Preference '{key}' is missing. Should be a {type(default_value).__name__}. Using default: {default_value}.")
            preferences[key] = default_value
        elif isinstance(default_value, dict):
            if not isinstance(preferences[key], dict):
                print_color.yellow(f"Preference '{key}' should be a dictionary. Using default: {default_value}.")
                preferences[key] = default_value
            else:
                for sub_key, sub_default_value in default_value.items():
                    if sub_key not in preferences[key]:
                        print_color.yellow(f"Preference '{key}.{sub_key}' is missing. Should be a {type(sub_default_value).__name__}. Using default: {sub_default_value}.")
                        preferences[key][sub_key] = sub_default_value
                    elif not isinstance(preferences[key][sub_key], type(sub_default_value)):
                        print_color.yellow(f"Preference '{key}.{sub_key}' should be a {type(sub_default_value).__name__}. Found: {type(preferences[key][sub_key]).__name__}. Using default: {sub_default_value}.")
                        preferences[key][sub_key] = sub_default_value
        elif not isinstance(preferences[key], type(default_value)):
            print_color.yellow(f"Preference '{key}' should be a {type(default_value).__name__}. Found: {type(preferences[key]).__name__}. Using default: {default_value}.")
            preferences[key] = default_value

    # Additional validation for 'destination_folder' and 'root_camcorder'
    if not isinstance(preferences.get('destination_folder'), str):
        print_color.yellow(f"Invalid 'destination_folder'. Should be a string. Found: {type(preferences.get('destination_folder')).__name__}. Using default: {DEFAULT_PREFERENCES['destination_folder']}.")
        preferences['destination_folder'] = DEFAULT_PREFERENCES['destination_folder']
    elif not os.path.isdir(preferences['destination_folder']):
        print_color.yellow(f"'destination_folder' should be a directory path. Validated as a string: {preferences['destination_folder']}. Using default: {DEFAULT_PREFERENCES['destination_folder']}.")
        preferences['destination_folder'] = DEFAULT_PREFERENCES['destination_folder']

    if not isinstance(preferences.get('root_camcorder'), str):
        print_color.yellow(f"Invalid 'root_camcorder'. Should be a string. Found: {type(preferences.get('root_camcorder')).__name__}. Using default: {DEFAULT_PREFERENCES['root_camcorder']}.")
        preferences['root_camcorder'] = DEFAULT_PREFERENCES['root_camcorder']
    elif not os.path.isdir(preferences['root_camcorder']):
        print_color.yellow(f"'root_camcorder' should be a directory path. Validated as a string: {preferences['root_camcorder']}. Using default: {DEFAULT_PREFERENCES['root_camcorder']}.")
        preferences['root_camcorder'] = DEFAULT_PREFERENCES['root_camcorder']

    return preferences

def validate_preferences_for_gui(preferences):
    error_messages = []

    # Ensure all required keys are present and valid
    for key, default_value in DEFAULT_PREFERENCES.items():
        if key not in preferences:
            error_messages.append(f"Preference '{key}' is missing. Should be a {type(default_value).__name__}. Using default: {default_value}.")
            preferences[key] = default_value
        elif isinstance(default_value, dict):
            if not isinstance(preferences[key], dict):
                error_messages.append(f"Preference '{key}' should be a dictionary. Using default: {default_value}.")
                preferences[key] = default_value
            else:
                for sub_key, sub_default_value in default_value.items():
                    if sub_key not in preferences[key]:
                        error_messages.append(f"Preference '{key}.{sub_key}' is missing. Should be a {type(sub_default_value).__name__}. Using default: {sub_default_value}.")
                        preferences[key][sub_key] = sub_default_value
                    elif not isinstance(preferences[key][sub_key], type(sub_default_value)):
                        error_messages.append(f"Preference '{key}.{sub_key}' should be a {type(sub_default_value).__name__}. Found: {type(preferences[key][sub_key]).__name__}. Using default: {sub_default_value}.")
                        preferences[key][sub_key] = sub_default_value
        elif not isinstance(preferences[key], type(default_value)):
            error_messages.append(f"Preference '{key}' should be a {type(default_value).__name__}. Found: {type(preferences[key]).__name__}. Using default: {default_value}.")
            preferences[key] = default_value

    # Additional validation for 'destination_folder' and 'root_camcorder'
    if not isinstance(preferences.get('destination_folder'), str):
        error_messages.append(f"Invalid 'destination_folder'. Should be a string. Found: {type(preferences.get('destination_folder')).__name__}. Using default: {DEFAULT_PREFERENCES['destination_folder']}.")
        preferences['destination_folder'] = DEFAULT_PREFERENCES['destination_folder']
    elif not os.path.isdir(preferences['destination_folder']):
        error_messages.append(f"'destination_folder' should be a directory path. Validated as a string: {preferences['destination_folder']}. Using default: {DEFAULT_PREFERENCES['destination_folder']}.")
        preferences['destination_folder'] = DEFAULT_PREFERENCES['destination_folder']

    if not isinstance(preferences.get('root_camcorder'), str):
        error_messages.append(f"Invalid 'root_camcorder'. Should be a string. Found: {type(preferences.get('root_camcorder')).__name__}. Using default: {DEFAULT_PREFERENCES['root_camcorder']}.")
        preferences['root_camcorder'] = DEFAULT_PREFERENCES['root_camcorder']
    elif not os.path.isdir(preferences['root_camcorder']):
        error_messages.append(f"'root_camcorder' should be a directory path. Validated as a string: {preferences['root_camcorder']}. Using default: {DEFAULT_PREFERENCES['root_camcorder']}.")
        preferences['root_camcorder'] = DEFAULT_PREFERENCES['root_camcorder']

    return error_messages


def preferences_routine(interactive=False):
    current_preferences = load_preferences()

    if current_preferences.get("in_debug_mode", True):
        print_color.purple("Current preferences:")
        print_color.purple(current_preferences)

    current_preferences = validate_preferences(current_preferences)

    if current_preferences.get("in_debug_mode", True):
        print_color.purple("Validated preferences:")
        print_color.purple(current_preferences)

    if interactive:
        if current_preferences.get("root_camcorder", "") == "":
            print_color.red("The root camcorder path is not set in the preferences file.")
            print_color.red("Please set the root camcorder path in the preferences file or enter it now.")
            input_root_camcorder = input("Camcorder root path: ")
            current_preferences["root_camcorder"] = input_root_camcorder
    
    return current_preferences
