import os # for the files paths and other useful stuffs
import print_color # for the colored prints
import video # for the functions calculate_file_hash, files_in and copy_file
import preferences # for the functions load_preferences, save_preferences, validate_preferences and preferences_routine

# CONSTANTS
# Calculate the path of the videos on the camcorder
IN_SECURE_MODE = True # if true the script will also check if the copy happened succesfully, it take more time

ROOT_CAMCORDER = os.path.join("fs_sim","camcorder")
VIDEO_PATH_FROM_ROOT = os.path.join("PRIVATE", "AVCHD", "BDMV", "STREAM")

EXTENSION = ".MTS"




# global variables




# FUNCTIONS
def main():

    global to_be_concatenated
    to_be_concatenated = []
    global hash_to_be_concatenated
    hash_to_be_concatenated = []

    global current_preferences
    current_preferences = preferences.preferences_routine() # load the preferences in the global variable and ask the user for the root camcorder path if it is not set

    global COPIED_FILES_LOG
    COPIED_FILES_LOG = os.path.join(current_preferences["destination_folder"], "copied_files.txt")


    # Iterate over all files in the directory
    video_files = video.files_in(os.path.join(current_preferences["root_camcorder"], VIDEO_PATH_FROM_ROOT), EXTENSION)

    print (f"Found {len(video_files)} video files:")
    for video_path in video_files:
        print(os.path.basename(video_path))

    # calculate the ash of every file and copy the ones that haven't been copied yet
    print("Calculating the hash of the files...")
    for video_path in video_files:
        hash_file = video.calculate_file_hash(video_path, 'sha256')
        if current_preferences["in_debug_mode"]:
            print_color.purple(f"The SHA-256 hash of the file {os.path.basename(video_path)} is: {hash_file}")
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





                if os.path.getsize(video_path) > current_preferences["size_limit"]:
                    to_be_concatenated.append(video_path)
                    hash_to_be_concatenated.append(hash_file)

                    if current_preferences["in_debug_mode"]:
                        print_color.purple(f"The file {video_path} have been recognized as part of a splitted video, added to the concatenation list")
                else:
                    if len(to_be_concatenated) > 0:
                        to_be_concatenated.append(video_path)
                        hash_to_be_concatenated.append(hash_file)

                        if current_preferences["in_debug_mode"]:
                            print_color.purple(f"The file {video_path} have been recognized as the final part of a splitted video, added to the concatenation list")

                        # concatenate the files in to_be_concatenated with the output in the destination folder
                        video.concat(to_be_concatenated, current_preferences["destination_folder"], hash_to_be_concatenated, COPIED_FILES_LOG, current_preferences["in_debug_mode"])

                        to_be_concatenated = [] # reset the list of files to be concatenated
                        hash_to_be_concatenated = [] # reset the list of hash of the files to be concatenated
                    else:
                        video.copy_file(video_path, current_preferences["destination_folder"], hash_file, COPIED_FILES_LOG, current_preferences["in_secure_mode"], current_preferences["in_debug_mode"])
                        # rename the copied video file in a descriptive way (based on the date and time of the video (YYYY-MM-DD_HH-MM-SS.MTS))
                        video.rename_copied_file(os.path.basename(video_path), current_preferences["destination_folder"], current_preferences["in_debug_mode"])




    # save the preferences
    preferences.save_preferences(current_preferences)

if __name__ == "__main__":
    main()