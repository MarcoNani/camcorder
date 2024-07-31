import print_color # for the colored prints
import hashlib # for generating file hashs
import os # for the files paths and other useful stuffs
import shutil # for copying files
import filecmp # for checking if two files are identycal
import datetime # for the date and time
import ffmpeg # for the video concatenation
import subprocess # for the ffmpeg command execution


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
                print_color.purple(f"The hash {hash_file} has been added to the copied files log")


def obtain_modification_date(file_path):
    # Get the timestamp of the last modification
    modification_timestamp = os.path.getmtime(file_path)

    # Convert the timestamp into a readable format
    modification_date = datetime.datetime.fromtimestamp(modification_timestamp)

    # Transform the modification date into a string formatted as 'YYYY-MM-DD_HH-MM-SS'
    formatted_modification_date = modification_date.strftime('%Y-%m-%d_%H-%M-%S')

    return formatted_modification_date

def check_file_existence(file_path):
    # Check if the file exists
    if os.path.exists(file_path):
        return True
    else:
        return False

def rename_copied_file(file_name, destination_folder, in_debug_mode=True, keep_old_name=False):
    # Build the complete path of the copied file
    copied_file_path = os.path.join(destination_folder, file_name)

    # Obtain the modification date of the copied file
    modification_date = obtain_modification_date(copied_file_path)

    # Split the file name and the extension
    file_name, extension = os.path.splitext(file_name)

    # Build the new file name with the modification date
    if keep_old_name:
        new_file_name = f"{modification_date}_{file_name}"
    else:
        new_file_name = f"{modification_date}"

    # if there is already a file with the same name in the destination folder, add a number to the new file name to avoid conflicts (e.g. 2021-01-01_12-00-00_1.MTS)
    if check_file_existence(os.path.join(destination_folder, f"{new_file_name}{extension}")):
        number = 1
        while check_file_existence(os.path.join(destination_folder, f"{new_file_name}_{number}")):
            number += 1
        new_file_name = f"{new_file_name}_{number}"

    # add the extension to the new file name
    new_file_name = f"{new_file_name}{extension}"

    # Build the complete path of the new file
    new_file_path = os.path.join(destination_folder, new_file_name)

    # Rename the copied file
    os.rename(copied_file_path, new_file_path)

    if in_debug_mode:
        print_color.green(f"The file has been renamed to {new_file_name}")


def transcode_H264_fixed(input_video_path, output_directory, bitrate='8M', in_debug_mode=False):
    # Get the file name and the extension
    file_name = os.path.basename(input_video_path)
    file_name, extension = os.path.splitext(file_name)

    # Get the output file name
    suffix = f"_H264_{bitrate}bps"
    output_file_name = f"{file_name}{suffix}.mp4"

    # Get the output file path
    output_video_path = os.path.join(output_directory, output_file_name)

    if in_debug_mode:
        print(f"Output video path: {output_video_path}")

    # ffmpeg command
    command = [
        'ffmpeg',
        '-i', input_video_path,
        '-vf', 'yadif=0:-1:0',
        '-c:v', 'libx264',
        '-b:v', bitrate,
        '-preset', 'medium',
        '-c:a', 'copy',
        output_video_path
    ]

    # Set the log level to suppress stdout only if not in debug mode
    if not in_debug_mode:
        command.insert(1, '-loglevel')
        command.insert(2, 'error')  # Show errors only

    print("Transcoding the video...")
    try:
        # Use subprocess.run to suppress only stdout
        with open(os.devnull, 'w') as devnull:
            result = subprocess.run(command, stdout=devnull, stderr=None if in_debug_mode else subprocess.PIPE)

        if result.returncode == 0:
            print_color.green(f"The video has been transcoded successfully to {output_video_path}.")
        else:
            print_color.red(f"Error during video transcoding: {result.stderr.decode('utf-8')}")
    except subprocess.CalledProcessError as e:
        print_color.red(f"Error during video transcoding: {e}")

def transcode_H265_CRF(input_video_path, output_directory, crf=23, in_debug_mode=False):
    # Get the file name and the extension
    file_name = os.path.basename(input_video_path)
    file_name, extension = os.path.splitext(file_name)

    # Get the output file name
    suffix = f"_H265_CRF{crf}"
    output_file_name = f"{file_name}{suffix}.mp4"

    # Get the output file path
    output_video_path = os.path.join(output_directory, output_file_name)

    if in_debug_mode:
        print(f"Output video path: {output_video_path}")

    # ffmpeg command
    command = [
        'ffmpeg',
        '-i', input_video_path,
        '-vf', 'yadif=0:-1:0',
        '-c:v', 'libx265',
        '-crf', str(crf),
        '-preset', 'medium',
        '-c:a', 'copy',
        output_video_path
    ]

    # Set the log level to suppress stdout only if not in debug mode
    if not in_debug_mode:
        command.insert(1, '-loglevel')
        command.insert(2, 'error')  # Show errors only

    print("Transcoding the video...")
    try:
        # Use subprocess.run to suppress only stdout
        with open(os.devnull, 'w') as devnull:
            result = subprocess.run(command, stdout=devnull, stderr=None if in_debug_mode else subprocess.PIPE)

        if result.returncode == 0:
            print_color.green(f"The video has been transcoded successfully to {output_video_path}.")
        else:
            print_color.red(f"Error during video transcoding: {result.stderr.decode('utf-8')}")
    except subprocess.CalledProcessError as e:
        print_color.red(f"Error during video transcoding: {e}")

# Example usage
transcode_H264_fixed("tests_py\\video_1.MTS", "tests_py", '8M', True)
transcode_H264_fixed("tests_py\\video_1.MTS", "tests_py", '4M', False)
transcode_H265_CRF("tests_py\\video_1.MTS", "tests_py", 23, False)
transcode_H265_CRF("tests_py\\video_1.MTS", "tests_py", 20, True)