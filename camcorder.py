import hashlib # for generating file hashs
import os # for the files paths and other useful stuffs
import shutil # for copying files
import filecmp # for checking if two files are identycal

# CONSTANTS
# Calculate the path of the videos on the camcorder
IN_SECURE_MODE = True # if true the script will also check if the copy happened succesfully, it take more time

ROOT_CAMCORDER = os.path.join("fs_sim","camcorder")
REMOTE_VIDEO_DIRECTORY = os.path.join(ROOT_CAMCORDER, "PRIVATE", "AVCHD", "BDMV", "STREAM")

EXTENSION = ".MTS"

COPIED_FILES_LOG = os.path.join("fs_sim","pc","destination","copied_files.txt")

DESTINATION_FOLDER = os.path.join("fs_sim","pc","destination")

# FUNCTIONS

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
        # Copy the file while preserving metadata
        shutil.copy2(source, destination_dir)
        print("File copied successfully!")
        has_been_copied = True
        
        if IN_SECURE_MODE:
            # Verify if the files are identical
            destination_file_path = os.path.join(destination_dir, os.path.basename(source))
            if filecmp.cmp(source, destination_file_path, shallow=True): # check if the two files are identical based on metadata
                # check if the hash passed to the function and the hash of the copied file are identical
                if hash_file == calculate_file_hash(destination_file_path):
                    print("Copy verification successful, the files are identical.")
                    has_been_copied = True
                else:
                    print("Error: The files content (checked with the ash) are not identical after copying.")
                    has_been_copied = False
            else:
                print("Error: The files metadata are not identical after copying.")
                has_been_copied = False

    except FileNotFoundError:
        print(f"Error: The file {source} does not exist.")
        has_been_copied = False
    except PermissionError:
        print("Error: Permission denied.")
        has_been_copied = False
    except Exception as e:
        print(f"An error occurred: {e}")
        has_been_copied = False

    # add the file ash to the COPIED_FILES_LOG file if the copy happened succesfully
    if has_been_copied:
        with open(COPIED_FILES_LOG, 'a') as file:
            file.write(hash_file + "\n")
            print(f"The hash {hash_file} has been added to the copied files log")

def main():
    # Iterate over all files in the directory
    video_files = files_in(REMOTE_VIDEO_DIRECTORY, EXTENSION)

    print (f"Found {len(video_files)} video files:")
    for video_path in video_files:
        print(os.path.basename(video_path))

    # calculate the ash of every file
    print("Calculating the hash of the files:")
    for video_path in video_files:
        hash_file = calculate_file_hash(video_path, 'sha256')
        print(f"The SHA-256 hash of the file {os.path.basename(video_path)} is: {hash_file}")
        # check if the file has already been copied (looking in the COPIED_FILES_LOG)
        if not os.path.exists(COPIED_FILES_LOG):
            # Create the COPIED_FILES_LOG file if it doesn't exist
            with open(COPIED_FILES_LOG, 'w') as file:
                pass
        with open(COPIED_FILES_LOG, 'r') as file:
            if hash_file in file.read():
                print(f"The file {os.path.basename(video_path)} has already been copied")
            else:
                print(f"The file {os.path.basename(video_path)} has not been copied yet")
                # if the file has not been copied yet, copy it to the destination folder
                copy_file(video_path, DESTINATION_FOLDER, hash_file)
                


if __name__ == "__main__":
    main()