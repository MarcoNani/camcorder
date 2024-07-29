# color constants
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
PURPLE = '\033[95m'
RESET = '\033[0m'

# FUNCTIONS
def red(text):
    print(f"{RED}{text}{RESET}")

def yellow(text):
    print(f"{YELLOW}{text}{RESET}")

def green(text):
    print(f"{GREEN}{text}{RESET}")

def purple(text):
    print(f"{PURPLE}{text}{RESET}")
