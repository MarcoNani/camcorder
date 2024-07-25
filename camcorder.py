import hashlib
import os

# CONSTANTS
# Calculate the path of the videos on the camcorder
ROOT_CAMCORDER = os.path.join("fs_sim","camcorder")
REMOTE_VIDEO_DIRECTORY = os.path.join(ROOT_CAMCORDER, "PRIVATE", "AVCHD", "BDMV", "STREAM")

EXTENSION = ".MTS"


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



if __name__ == "__main__":
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