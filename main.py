import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import os
import preferences
import camcorder
import sys

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

# -- menu functions and preferences --
def on_exit():
    """Function to exit the application."""
    root.quit()

def on_open():
    """Function to execute on application open."""
    global current_preferences
    # Load the preferences
    current_preferences = preferences.preferences_routine()

    # populate the entry with the preferences
    entry_root_camcorder.delete(0, tk.END)
    entry_root_camcorder.insert(0, current_preferences["root_camcorder"])

    entry_destination_folder.delete(0, tk.END)
    entry_destination_folder.insert(0, current_preferences["destination_folder"])

    entry_in_secure_mode.select() if current_preferences["in_secure_mode"] else entry_in_secure_mode.deselect()

    entry_in_debug_mode.select() if current_preferences["in_debug_mode"] else entry_in_debug_mode.deselect()

    entry_size_limit.delete(0, tk.END)
    entry_size_limit.insert(0, current_preferences["size_limit"])



def about():
    """Show an 'About' message."""
    messagebox.showinfo("Information", "Application created by Marco Nani.\n\nFor more information visit:\nwww.example.com")

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

def select_destination_folder():
    """Function to select the destination folder."""
    folder_path = filedialog.askdirectory()
    if folder_path:
        if os.name == "nt":
            folder_path = folder_path.replace("/", "\\")
        entry_destination_folder.delete(0, tk.END)
        entry_destination_folder.insert(0, folder_path)


# -- transfer function --
def start_transfer():
    """Function to start the transfer."""


    # - preferences management -

    preferences_ok = True

    # check the correctness of the preferences:

    # Check if the root camcorder folder is set
    if current_preferences["root_camcorder"] == "":
        preferences_ok = False
        messagebox.showerror("Error", "The root camcorder folder is not set in the preferences.")
        return

    # Check if the destination folder is set
    if current_preferences["destination_folder"] == "":
        preferences_ok = False
        messagebox.showerror("Error", "The destination folder is not set in the preferences.")
        return

    # Check if the root camcorder folder exists
    if not os.path.isdir(current_preferences["root_camcorder"]):
        preferences_ok = False
        messagebox.showerror("Error", "The root camcorder folder does not exist.")
        return

    # Check if the size limit is a number
    try:
        int(entry_size_limit.get())
    except ValueError:
        preferences_ok = False
        messagebox.showerror("Error", "The size limit must be a number.")
        return

    if preferences_ok:
        print("Preferences are ok")
        # Update the preferences with the values in the entries
        current_preferences["root_camcorder"] = entry_root_camcorder.get()
        current_preferences["destination_folder"] = entry_destination_folder.get()
        current_preferences["in_secure_mode"] = var_in_secure_mode.get()
        current_preferences["in_debug_mode"] = var_in_debug_mode.get()
        current_preferences["size_limit"] = int(entry_size_limit.get())

        # Save the preferences
        preferences.save_preferences(current_preferences)

        print("Starting the transfer...")

        button_start_transfer.config(state=tk.DISABLED)
        update_progress(0) # reset the progress bar
        camcorder.start_transfer(update_progress)
        button_start_transfer.config(state=tk.NORMAL)



    else:
        print("Preferences are not ok")
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
file_menu.add_command(label="Open the preference file in explorer", command=open_preferences_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=on_exit)

# Add the "Help" menu
help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=about)


# --- WIDGETS ---
# columnconfigure and rowconfigure are used to configure the grid layout
root.columnconfigure(0, minsize=100)
root.columnconfigure(1, minsize=500)
root.columnconfigure(2, minsize=100)
root.rowconfigure(0, minsize=50)
root.rowconfigure(1, minsize=50)
root.rowconfigure(2, minsize=50)
root.rowconfigure(3, minsize=50)
root.rowconfigure(4, minsize=50)
root.rowconfigure(5, minsize=50)
root.rowconfigure(6, minsize=50)
root.rowconfigure(7, minsize=50)
root.rowconfigure(8, minsize=50)
root.rowconfigure(9, minsize=50)
root.rowconfigure(10, minsize=50)

# --- 1° ROW ---
label_root_camcorder = tk.Label(root, text="Root camcorder folder:")
label_root_camcorder.grid(row=0, column=0, sticky="e", padx=10)

entry_root_camcorder = tk.Entry(root)
entry_root_camcorder.grid(row=0, column=1, sticky="ew", padx=10)

button_root_camcorder = tk.Button(root, text="Select folder", command=select_root_camcorder_folder)
button_root_camcorder.grid(row=0, column=2, sticky="w", padx=10)

# --- 2° ROW ---
label_destination_folder = tk.Label(root, text="Destination folder:")
label_destination_folder.grid(row=1, column=0, sticky="e", padx=10)

entry_destination_folder = tk.Entry(root)
entry_destination_folder.grid(row=1, column=1, sticky="ew", padx=10)

button_destination_folder = tk.Button(root, text="Select folder", command=select_destination_folder)
button_destination_folder.grid(row=1, column=2, sticky="w", padx=10)

# --- 3° ROW ---
label_advanced_settings = tk.Label(root, text="Advanced settings:", fg="blue")
label_advanced_settings.grid(row=2, column=0, sticky="w", padx=10)

# --- 4° ROW ---
label_in_secure_mode = tk.Label(root, text="In secure mode:")
label_in_secure_mode.grid(row=3, column=0, sticky="e", padx=10)

var_in_secure_mode = tk.BooleanVar()
entry_in_secure_mode = tk.Checkbutton(root, variable=var_in_secure_mode)
entry_in_secure_mode.grid(row=3, column=1, sticky="w", padx=10)

# --- 5° ROW ---
label_in_debug_mode = tk.Label(root, text="In debug mode:")
label_in_debug_mode.grid(row=4, column=0, sticky="e", padx=10)

var_in_debug_mode = tk.BooleanVar()
entry_in_debug_mode = tk.Checkbutton(root, variable=var_in_debug_mode)
entry_in_debug_mode.grid(row=4, column=1, sticky="w", padx=10)

# --- 6° ROW ---
label_size_limit = tk.Label(root, text="Size limit:")
label_size_limit.grid(row=5, column=0, sticky="e", padx=10)

entry_size_limit = tk.Entry(root)
entry_size_limit.grid(row=5, column=1, sticky="w", padx=10)

# --- 7° ROW ---
button_start_transfer = tk.Button(root, text="Start transfer", command=start_transfer)
button_start_transfer.grid(row=6, column=0, columnspan=3, sticky="ew", padx=10, pady=10)

# --- 8° ROW ---
label_output = tk.Label(root, text="Output:")
label_output.grid(row=7, column=0, columnspan=3, sticky="w", padx=10)

output_text = RedirectText(root, height=10, width=80)
output_text.grid(row=8, column=0, columnspan=3, padx=10, pady=10)

# --- 9° ROW ---
# Label to display the percentage of progress
progress_label = tk.Label(root, text="not started yet", anchor='center')
progress_label.grid(row=9, column=0, columnspan=3)

# --- 10° ROW ---
# Add a progress bar
global progress_bar
progress_bar = ttk.Progressbar(root, orient='horizontal', mode='determinate', maximum=100)
progress_bar.grid(row=10, column=0, columnspan=3, sticky="ew", padx=10, pady=10)




# Redirect stdout and stderr to the Text widget
sys.stdout = output_text
sys.stderr = output_text

# Load preferences on application start
on_open()

# Start the main loop of the application
root.mainloop()
