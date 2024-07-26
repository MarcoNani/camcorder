import print_color # for the colored prints
import hashlib # for generating file hashs
import os # for the files paths and other useful stuffs
import shutil # for copying files
import filecmp # for checking if two files are identycal


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

def copy_file(source, destination_dir, hash_file, copied_files_log_file, in_secure_mode=True, in_debug_mode=False):
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
        
        if in_secure_mode:
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

    # add the file ash to the copied_files_log_file file if the copy happened succesfully
    if has_been_copied:
        with open(copied_files_log_file, 'a') as file:
            file.write(hash_file + "\n")
            if in_debug_mode:
                print(f"The hash {hash_file} has been added to the copied files log")
