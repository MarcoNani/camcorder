import hashlib # for generating file hashs
import os # for the files paths and other useful stuffs
import shutil # for copying files
import filecmp # for checking if two files are identycal
import json # for reading the preferences file
import print_color # for the colored prints

# CONSTANTS


DEFAULT_PREFERENCES_PATH = os.path.join("config", "preferences.json")

default_preferences = {
    "destination_folder": "transferred_videos",
    "in_secure_mode": True,
    "in_debug_mode": True,
    "root_camcorder": ""
}

# Calculate the path of the videos on the camcorder
IN_SECURE_MODE = True # if true the script will also check if the copy happened succesfully, it take more time

ROOT_CAMCORDER = os.path.join("fs_sim","camcorder")
VIDEO_PATH_FROM_ROOT = os.path.join("PRIVATE", "AVCHD", "BDMV", "STREAM")

EXTENSION = ".MTS"

# FUNCTIONS
def load_preferences(filename=DEFAULT_PREFERENCES_PATH):
    try:
        with open(filename, 'r') as file:
            preferences = json.load(file)
    except FileNotFoundError:
        print_color.red("Preferences file not found. Using default preferences.")
        preferences = default_preferences
    except json.JSONDecodeError:
        print_color.red("Corrupted or invalid preferences file. Using default preferences.")
        preferences = default_preferences
    return preferences

def save_preferences(preferences, filename=DEFAULT_PREFERENCES_PATH):
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    with open(filename, 'w') as file:
        json.dump(preferences, file, indent=4)

def validate_preferences(preferences):
    if not isinstance(preferences.get('destination_folder'), str):
        print_color.yellow(f"Invalid destination folder (must be a string). Using default preference: {default_preferences['destination_folder']}.")
        preferences['destination_folder'] = default_preferences['destination_folder']
    if not isinstance(preferences.get('in_secure_mode'), bool):
        print_color.yellow(f"Invalid in secure mode (must be true or false). Using default preference: {default_preferences['in_secure_mode']}.")
        preferences['in_secure_mode'] = default_preferences['in_secure_mode']
    if not isinstance(preferences.get('in_debug_mode'), bool):
        print_color.yellow(f"Invalid in debug mode (must be true or false). Using default preference: {default_preferences['in_debug_mode']}.")
        preferences['in_debug_mode'] = default_preferences['in_debug_mode']
    if not isinstance(preferences.get('root_camcorder'), str):
        print_color.yellow(f"Invalid root camcorder path (must be a string). Using default preference: {default_preferences['root_camcorder']}.")
        preferences['root_camcorder'] = default_preferences['root_camcorder']
    return preferences

def preferences_routine():
    current_preferences = load_preferences()

    if current_preferences["in_debug_mode"]:
        print("Current preferences:")
        print(current_preferences)

    current_preferences = validate_preferences(current_preferences)

    if current_preferences["in_debug_mode"]:
        print("Validated preferences:")
        print(current_preferences)

    if current_preferences["root_camcorder"] == "":
        print_color.red("The root camcorder path is not set in the preferences file.")
        print_color.red("Please set the root camcorder path in the preferences file or enter it now.")
        # request of the root camcorder path
        input_root_camcorder = input("Camcorder root path: ")
        current_preferences["root_camcorder"] = input_root_camcorder
    
    return current_preferences



def calculate_file_hash(file_path, algorithm='sha256'):
    """
    Calculate the hash of a file using the specified algorithm.

    :param file_path: Path of the file to calculate the hash.
    :param algorithm: Name of the hashing algorithm (default: 'sha256').
    :return: Hexadecimal string of the calculated hash.
    """
    # Create the hash object
    h = hashlib.new(algorithm)
    
    # Read the file in binary mode
    with open(file_path, 'rb') as file:
        # Read and update the hash for blocks
        while block := file.read(8192):
            h.update(block)

    # Return the hash in hexadecimal format
    return h.hexdigest()

def files_in(directory, extension):
    list_of_files = []
    for file_name in os.listdir(directory):
        # Build the complete file path
        complete_path = os.path.join(directory, file_name)

        # Check if it is a file and has the desired extension
        if os.path.isfile(complete_path) and file_name.endswith(extension):
            list_of_files.append(complete_path)
    return list_of_files

def copy_file(source, destination_dir, hash_file):
    has_been_copied = False
    # copy the file to the destination_dir folder
    try:
        # Create the destination directory if it doesn't exist
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        # Copy the file while preserving metadata
        shutil.copy2(source, destination_dir)
        print_color.green("File copied successfully!")
        has_been_copied = True
        
        if current_preferences["in_secure_mode"]:
            # Verify if the files are identical
            destination_file_path = os.path.join(destination_dir, os.path.basename(source))
            if filecmp.cmp(source, destination_file_path, shallow=True): # check if the two files are identical based on metadata
                # check if the hash passed to the function and the hash of the copied file are identical
                if hash_file == calculate_file_hash(destination_file_path):
                    print_color.green("Copy verification successful, the files are identical.")
                    has_been_copied = True
                else:
                    print_color.red("Error: The files content (checked with the ash) are not identical after copying.")
                    has_been_copied = False
            else:
                print_color.red("Error: The files metadata are not identical after copying.")
                has_been_copied = False

    except FileNotFoundError:
        print_color.red(f"Error: The file {source} does not exist.")
        has_been_copied = False
    except PermissionError:
        print_color.red("Error: Permission denied.")
        has_been_copied = False
    except Exception as e:
        print_color.red(f"An error occurred: {e}")
        has_been_copied = False

    # add the file ash to the COPIED_FILES_LOG file if the copy happened succesfully
    if has_been_copied:
        with open(COPIED_FILES_LOG, 'a') as file:
            file.write(hash_file + "\n")
            if current_preferences["in_debug_mode"]:
                print(f"The hash {hash_file} has been added to the copied files log")

def main():
    global current_preferences
    current_preferences = preferences_routine() # load the preferences in the global variable and ask the user for the root camcorder path if it is not set

    global COPIED_FILES_LOG
    COPIED_FILES_LOG = os.path.join(current_preferences["destination_folder"], "copied_files.txt")


    # Iterate over all files in the directory
    video_files = files_in(os.path.join(current_preferences["root_camcorder"], VIDEO_PATH_FROM_ROOT), EXTENSION)

    print (f"Found {len(video_files)} video files:")
    for video_path in video_files:
        print(os.path.basename(video_path))

    # calculate the ash of every file and copy the ones that haven't been copied yet
    print("Calculating the hash of the files...")
    for video_path in video_files:
        hash_file = calculate_file_hash(video_path, 'sha256')
        if current_preferences["in_debug_mode"]:
            print(f"The SHA-256 hash of the file {os.path.basename(video_path)} is: {hash_file}")
        # check if the file has already been copied (looking in the COPIED_FILES_LOG)
        if not os.path.exists(COPIED_FILES_LOG):
            # Create the destination directory if it doesn't exist
            if not os.path.exists(current_preferences["destination_folder"]):
                os.makedirs(current_preferences["destination_folder"])
            # Create the COPIED_FILES_LOG file if it doesn't exist
            with open(COPIED_FILES_LOG, 'w') as file:
                pass
        with open(COPIED_FILES_LOG, 'r') as file:
            if hash_file in file.read():
                print_color.green(f"The file {os.path.basename(video_path)} has already been copied")
            else:
                print(f"The file {os.path.basename(video_path)} has not been copied yet")
                # if the file has not been copied yet, copy it to the destination folder
                copy_file(video_path, current_preferences["destination_folder"], hash_file)
    
    # save the preferences
    save_preferences(current_preferences)
                


if __name__ == "__main__":
    main()