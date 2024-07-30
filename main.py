import tkinter as tk
from tkinter import messagebox
import os
import preferences

# Initialize global variable
current_preferences = {}

# FUNCTIONS
def on_exit():
    """Function to exit the application."""
    root.quit()

def on_open():
    """Function to execute on application open."""
    # Declare the variable as global
    global current_preferences
    # Load the preferences
    current_preferences = preferences.preferences_routine()

def about():
    """Show an 'About' message."""
    messagebox.showinfo("Information", "Application created by Marco Nani.\n\nFor more information visit:\nwww.example.com")

def open_root_camcorder_folder():
    """Open the root camcorder folder in the file explorer."""
    try:
        os.startfile(current_preferences["root_camcorder"])
    except KeyError:
        messagebox.showerror("Error", "Root camcorder folder not set in preferences.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open folder: {e}")

def open_destination_folder():
    """Open the destination folder in the file explorer."""
    try:
        os.startfile(current_preferences["destination_folder"])
    except KeyError:
        messagebox.showerror("Error", "Destination folder not set in preferences.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open folder: {e}")

def open_preferences_folder():
    """Open the preference file directory in explorer."""
    try:
        os.startfile(preferences.DEFAULT_PREFERENCES_PATH)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open preferences folder: {e}")

# Create the root window (the main window of the application)
root = tk.Tk()
root.title("Camcorder")

# Create the menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Elements of the menu bar
# Add the "File" menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open root camcorder folder in the file explorer", command=open_root_camcorder_folder)
file_menu.add_command(label="Open destination folder in the file explorer", command=open_destination_folder)
file_menu.add_command(label="Open the preference file directory in explorer", command=open_preferences_folder)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=on_exit)

# Add the "Help" menu
help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=about)

# Load preferences on application start
on_open()

# Start the main loop of the application
root.mainloop()
