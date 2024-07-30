import tkinter as tk
from tkinter import messagebox, filedialog
import os
import preferences

# Initialize global variable
current_preferences = {}

# FUNCTIONS

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
        entry_root_camcorder.delete(0, tk.END)
        entry_root_camcorder.insert(0, folder_path)

def select_destination_folder():
    """Function to select the destination folder."""
    folder_path = filedialog.askdirectory()
    if folder_path:
        entry_destination_folder.delete(0, tk.END)
        entry_destination_folder.insert(0, folder_path)




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


# --- 1° ROW ---
label_root_camcorder = tk.Label(root, text="Root camcorder folder:")
label_root_camcorder.grid(row=0, column=0, sticky="e")

entry_root_camcorder = tk.Entry(root)
entry_root_camcorder.grid(row=0, column=1, sticky="ew")

button_root_camcorder = tk.Button(root, text="Select folder", command=select_root_camcorder_folder)
button_root_camcorder.grid(row=0, column=2, sticky="w")

# --- 2° ROW ---
label_destination_folder = tk.Label(root, text="Destination folder:")
label_destination_folder.grid(row=1, column=0, sticky="e")

entry_destination_folder = tk.Entry(root)
entry_destination_folder.grid(row=1, column=1, sticky="ew")

button_destination_folder = tk.Button(root, text="Select folder", command=select_destination_folder)
button_destination_folder.grid(row=1, column=2, sticky="w")




# Load preferences on application start
on_open()

# Start the main loop of the application
root.mainloop()
