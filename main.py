import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import os
import preferences
import camcorder
import video
import sys
import threading

# Initialize global variable
current_preferences = {}

# Custom Text widget to capture stdout
class RedirectText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)
        self.configure(state=tk.DISABLED)
        
    def write(self, text):
        # Write on console
        sys.__stdout__.write(text)

        # Write on the text widget
        self.configure(state=tk.NORMAL)
        self.insert(tk.END, text)
        self.configure(state=tk.DISABLED)
        self.yview(tk.END)  # Scroll to the end
    
    def flush(self):
        # Flushing is not needed for this application
        pass

# FUNCTIONS

def update_progress(value):
    """Function to update the progress bar."""
    progress_bar['value'] = value
    # Update the percentage label
    progress_label.config(text=f"Transferring the files: {value:.0f}% completed")

def update_H264_low_progress(value):
    """Function to update the progress bar."""
    progress_bar_h264_4M['value'] = value
    # Update the percentage label
    label_progress_h264_4M.config(text=f"Transcoding to H264 low bitrate: {value:.0f}% completed")

def update_H264_high_progress(value):
    """Function to update the progress bar."""
    progress_bar_h264_8M['value'] = value
    # Update the percentage label
    label_progress_h264_8M.config(text=f"Transcoding to H264 high bitrate: {value:.0f}% completed")

def update_H265_progress(value):
    """Function to update the progress bar."""
    progress_bar_h265_CRF_23['value'] = value
    # Update the percentage label
    label_progress_h265_CRF_23.config(text=f"Transcoding to H265 variable bitrate: {value:.0f}% completed")



def threaded_transfer():
    """Function to perform the transfer in a separate thread."""
    def run_transfer():
        to_be_transcoded = [] # list of videos to be transcoded
        try:
            to_be_transcoded = camcorder.start_transfer(update_progress)
        except Exception as e:
            messagebox.showerror("Error", f"Transfer failed: {e}")
        finally:
            # transcode the videos
            if to_be_transcoded:
                # call the function to transcode the videos
                video.transcode_list_of_videos(to_be_transcoded, preferences=current_preferences, update_H264_low_progress=update_H264_low_progress, update_H264_high_progress=update_H264_high_progress, update_H265_progress=update_H265_progress, overwrite=False, in_debug_mode=current_preferences["in_debug_mode"])


            # Re-enable the start button
            button_start_transfer.config(state=tk.NORMAL)
    
    # Run the transfer function in a new thread
    transfer_thread = threading.Thread(target=run_transfer)
    transfer_thread.start()

# -- menu functions and preferences --
def on_exit():
    """Function to exit the application."""
    root.quit()

def on_open():
    """Function to execute on application open."""
    global current_preferences
    # Load the preferences
    current_preferences = preferences.preferences_routine()

    # populate the GUI with the preferences
    entry_root_camcorder.delete(0, tk.END)
    entry_root_camcorder.insert(0, current_preferences["root_camcorder"])

    entry_destination_folder.delete(0, tk.END)
    entry_destination_folder.insert(0, current_preferences["destination_folder"])

    entry_in_secure_mode.select() if current_preferences["in_secure_mode"] else entry_in_secure_mode.deselect()

    entry_in_debug_mode.select() if current_preferences["in_debug_mode"] else entry_in_debug_mode.deselect()

    entry_size_limit.delete(0, tk.END)
    entry_size_limit.insert(0, current_preferences["size_limit"])

    entry_H264_low_enabled.select() if current_preferences["H264_low"]["enabled"] else entry_H264_low_enabled.deselect()
    entry_H264_low_bitrate.delete(0, tk.END)
    entry_H264_low_bitrate.insert(0, current_preferences["H264_low"]["bitrate"])

    entry_H264_high_enabled.select() if current_preferences["H264_high"]["enabled"] else entry_H264_high_enabled.deselect()
    entry_H264_high_bitrate.delete(0, tk.END)
    entry_H264_high_bitrate.insert(0, current_preferences["H264_high"]["bitrate"])

    entry_H265_enabled.select() if current_preferences["H265_VBR"]["enabled"] else entry_H265_enabled.deselect()
    entry_H265_CRF.delete(0, tk.END)
    entry_H265_CRF.insert(0, current_preferences["H265_VBR"]["CRF"])





def about():
    """Show an 'About' message."""
    messagebox.showinfo("Information", "Application created by Marco Nani.\n\nFor more information visit:\ngithub.com/MarcoNani/camcorder")

def open_root_camcorder_folder():
    """Open the root camcorder folder in the file explorer."""
    try:
        path = current_preferences["root_camcorder"]
        # Verify if the path is a directory
        if os.path.isdir(path):
            os.startfile(path)
        else:
            messagebox.showerror("Error", "The root camcorder path is not a directory.")
    except KeyError:
        messagebox.showerror("Error", "Root camcorder folder not set in preferences.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open folder: {e}")

def open_destination_folder():
    """Open the destination folder in the file explorer."""
    try:
        path = current_preferences["destination_folder"]
        # Verify if the path is a directory
        if os.path.isdir(path):
            os.startfile(path)
        else:
            messagebox.showerror("Error", "The destination folder path is not a directory.")
    except KeyError:
        messagebox.showerror("Error", "Destination folder not set in preferences.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open folder: {e}")

def open_preferences_file():
    """Open the preference file directory in explorer."""
    try:
        path = preferences.DEFAULT_PREFERENCES_PATH
        os.startfile(path)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open preferences file: {e}")


# -- folder functions --
def select_root_camcorder_folder():
    """Function to select the root camcorder folder."""
    folder_path = filedialog.askdirectory()
    if folder_path:
        if os.name == "nt":
            folder_path = folder_path.replace("/", "\\")
        entry_root_camcorder.delete(0, tk.END)
        entry_root_camcorder.insert(0, folder_path)
        current_preferences["root_camcorder"] = folder_path

def select_destination_folder():
    """Function to select the destination folder."""
    folder_path = filedialog.askdirectory()
    if folder_path:
        if os.name == "nt":
            folder_path = folder_path.replace("/", "\\")
        entry_destination_folder.delete(0, tk.END)
        entry_destination_folder.insert(0, folder_path)
        current_preferences["destination_folder"] = folder_path


# -- transfer function --
def start_transfer():
    """Function to start the transfer."""
    # - preferences management -
    preferences_ok = True


    # read the preferences from the GUI
    current_preferences["root_camcorder"] = entry_root_camcorder.get()
    current_preferences["destination_folder"] = entry_destination_folder.get()
    current_preferences["in_secure_mode"] = var_in_secure_mode.get()
    current_preferences["in_debug_mode"] = var_in_debug_mode.get()
    current_preferences["size_limit"] = int(entry_size_limit.get())
    current_preferences["H264_low"]["enabled"] = var_H264_low_enabled.get()
    current_preferences["H264_low"]["bitrate"] = entry_H264_low_bitrate.get()
    current_preferences["H264_high"]["enabled"] = var_H264_high_enabled.get()
    current_preferences["H264_high"]["bitrate"] = entry_H264_high_bitrate.get()
    current_preferences["H265_VBR"]["enabled"] = var_H265_enabled.get()
    current_preferences["H265_VBR"]["CRF"] = entry_H265_CRF.get()


    # TODO: call the function to control the correctivness of the preferences




    if preferences_ok:
        # Save the preferences
        preferences.save_preferences(current_preferences)


        print("Starting the transfer...")

        # Disable the button and reset progress
        button_start_transfer.config(state=tk.DISABLED)
        update_progress(0) # reset the progress bar

        # Start the transfer in a new thread
        threaded_transfer()
    else:
        messagebox.showerror("Error", "Some preferences are not valid. Please check the values.")
        return





# Create the root window (the main window of the application)
root = tk.Tk()
root.title("Camcorder")

# --- MENU BAR ---

# Create the menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Elements of the menu bar
# Add the "File" menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open root camcorder folder in the file explorer", command=open_root_camcorder_folder)
file_menu.add_command(label="Open destination folder in the file explorer", command=open_destination_folder)
file_menu.add_command(label="Open the preference file", command=open_preferences_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=on_exit)

# Add the "Help" menu
help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=about)

# --- WIDGETS ---
# columnconfigure and rowconfigure are used to configure the grid layout
#root.columnconfigure(0, minsize=100)
#root.columnconfigure(1, minsize=100)
#root.columnconfigure(2, minsize=100)
#root.columnconfigure(3, minsize=100)
#root.columnconfigure(4, minsize=100)
#root.columnconfigure(5, minsize=100)
#root.columnconfigure(6, minsize=100)


# --- 0° ROW ---
label_root_camcorder = tk.Label(root, text="Root camcorder folder:")
label_root_camcorder.grid(row=0, column=0, sticky="e", padx=10)

entry_root_camcorder = tk.Entry(root)
entry_root_camcorder.grid(row=0, column=1, columnspan=5, sticky="ew", padx=10)

button_root_camcorder = tk.Button(root, text="Select folder", command=select_root_camcorder_folder)
button_root_camcorder.grid(row=0, column=6, sticky="w", padx=10)



# --- 1° ROW ---
label_destination_folder = tk.Label(root, text="Destination folder:")
label_destination_folder.grid(row=1, column=0, sticky="e", padx=10)

entry_destination_folder = tk.Entry(root)
entry_destination_folder.grid(row=1, column=1, columnspan=5, sticky="ew", padx=10)

button_destination_folder = tk.Button(root, text="Select folder", command=select_destination_folder)
button_destination_folder.grid(row=1, column=6, sticky="w", padx=10)



# --- 2° ROW ---
label_advanced_settings = tk.Label(root, text="Advanced settings:", fg="blue") # TODO: make the text bigger
label_advanced_settings.grid(row=2, column=0, sticky="w", padx=10)

label_transcoding_settings = tk.Label(root, text="Transcoding settings:", fg="blue") # TODO: make the text bigger
label_transcoding_settings.grid(row=2, column=4, sticky="w", padx=10)



# --- 3° ROW ---
# Advanced settings
label_in_secure_mode = tk.Label(root, text="In secure mode:")
label_in_secure_mode.grid(row=3, column=0, sticky="e", padx=10)

var_in_secure_mode = tk.BooleanVar()
entry_in_secure_mode = tk.Checkbutton(root, variable=var_in_secure_mode)
entry_in_secure_mode.grid(row=3, column=1, sticky="w", padx=10)


# Transcoding settings
label_H264_low = tk.Label(root, text="H264 low bitrate:")
label_H264_low.grid(row=3, column=4, sticky="e", padx=10)

var_H264_low_enabled = tk.BooleanVar()
entry_H264_low_enabled = tk.Checkbutton(root, variable=var_H264_low_enabled)
entry_H264_low_enabled.grid(row=3, column=5, sticky="w", padx=10)

entry_H264_low_bitrate = tk.Entry(root)
entry_H264_low_bitrate.grid(row=3, column=6, columnspan=5, sticky="ew", padx=10)



# --- 4° ROW ---
# Advanced settings
label_in_debug_mode = tk.Label(root, text="In debug mode:")
label_in_debug_mode.grid(row=4, column=0, sticky="e", padx=10)

var_in_debug_mode = tk.BooleanVar()
entry_in_debug_mode = tk.Checkbutton(root, variable=var_in_debug_mode)
entry_in_debug_mode.grid(row=4, column=1, sticky="w", padx=10)


# Transcoding settings
label_H264_high = tk.Label(root, text="H264 high bitrate:")
label_H264_high.grid(row=4, column=4, sticky="e", padx=10)

var_H264_high_enabled = tk.BooleanVar()
entry_H264_high_enabled = tk.Checkbutton(root, variable=var_H264_high_enabled)
entry_H264_high_enabled.grid(row=4, column=5, sticky="w", padx=10)

entry_H264_high_bitrate = tk.Entry(root)
entry_H264_high_bitrate.grid(row=4, column=6, columnspan=5, sticky="ew", padx=10)



# --- 5° ROW ---
# Advanced settings
label_size_limit = tk.Label(root, text="Size limit:")
label_size_limit.grid(row=5, column=0, sticky="e", padx=10)

entry_size_limit = tk.Entry(root)
entry_size_limit.grid(row=5, column=1, sticky="w", padx=10)


# Transcoding settings
label_H265 = tk.Label(root, text="H265 variable bitrate CRF:")
label_H265.grid(row=5, column=4, sticky="e", padx=10)

var_H265_enabled = tk.BooleanVar()
entry_H265_enabled = tk.Checkbutton(root, variable=var_H265_enabled)
entry_H265_enabled.grid(row=5, column=5, sticky="w", padx=10)

entry_H265_CRF = tk.Entry(root)
entry_H265_CRF.grid(row=5, column=6, columnspan=5, sticky="ew", padx=10)



# --- 6° ROW ---
button_start_transfer = tk.Button(root, text="Start transfer", command=start_transfer)
button_start_transfer.grid(row=6, column=0, columnspan=7, sticky="ew", padx=10, pady=10)



# --- 7° ROW ---
label_output = tk.Label(root, text="Output:")
label_output.grid(row=7, column=0, sticky="w", padx=10)



# --- 8° ROW ---
output_text = RedirectText(root, height=10, width=80)
output_text.grid(row=8, column=0, columnspan=7, padx=10, pady=10)



# --- 9° ROW ---
# Add a progress bar
# Label to display the percentage of progress
progress_label = tk.Label(root, text="Transferring the files: not started", anchor='center')
progress_label.grid(row=9, column=0, columnspan=2, sticky="e", padx=10)
global progress_bar
progress_bar = ttk.Progressbar(root, orient='horizontal', mode='determinate', maximum=100)
progress_bar.grid(row=9, column=3, columnspan=4, sticky="ew", padx=10, pady=10)



# --- 10° ROW ---
# label to display what type of transcode is being done
label_progress_h264_8M = tk.Label(root, text="Transcoding to H264 low bitrate: not started", anchor='center')
label_progress_h264_8M.grid(row=10, column=0, columnspan=2, sticky="e", padx=10)
global progress_bar_h264_8M
progress_bar_h264_8M = ttk.Progressbar(root, orient='horizontal', mode='determinate', maximum=100)
progress_bar_h264_8M.grid(row=10, column=3, columnspan=4, sticky="ew", padx=10, pady=10)



# --- 11° ROW ---
# label to display what type of transcode is being done
label_progress_h264_4M = tk.Label(root, text="Transcoding to H264 high bitrate: not started", anchor='center')
label_progress_h264_4M.grid(row=11, column=0, columnspan=2, sticky="e", padx=10)
global progress_bar_h264_4M
progress_bar_h264_4M = ttk.Progressbar(root, orient='horizontal', mode='determinate', maximum=100)
progress_bar_h264_4M.grid(row=11, column=3, columnspan=4, sticky="ew", padx=10, pady=10)



# --- 12° ROW ---
# label to display what type of transcode is being done
label_progress_h265_CRF_23 = tk.Label(root, text="Transcoding to H265 variable bitrate: not started", anchor='center')
label_progress_h265_CRF_23.grid(row=12, column=0, columnspan=2, sticky="e", padx=10)
global progress_bar_h265_CRF_23
progress_bar_h265_CRF_23 = ttk.Progressbar(root, orient='horizontal', mode='determinate', maximum=100)
progress_bar_h265_CRF_23.grid(row=12, column=3, columnspan=4, sticky="ew", padx=10, pady=10)



# Redirect stdout and stderr to the Text widget
sys.stdout = output_text
sys.stderr = output_text

# Load preferences on application start
on_open()

# Start the main loop of the application
root.mainloop()
