# Camcorder
Camcorder is a program that let you transfer your videos taken with a Sony HDR-CX405 camcorder to your pc.

## Features:
- Transfer all the videos thaken with the camcorder in the AVCHD format
- Remember what videos have already been transferred and don't re transfer them
- Transcode videos in H264 and H265
- Automatically concat splitted videos
- Rename videos with a descriptive name indicating the date and the time when the videos was taken
- Save preferences in a file and re-load them at the next opening let the user configuring the program once and then never thinking again
- Preferences can be setted manually modifing a Json or with the GUI
- Automatic video deinterlacing

## Installation:
1. Install ffmpeg in your preferred way (I have installed it with winget, the Windows packet manager).
2.  Install the Python interpreter
3. Install the ffmpeg-python library:

    `pip install ffmpeg-python`

4. Clone the repository or download it as a ZIP file (if you have downloaded it as a ZIP, unzip it).
5. Run `main.py` with the python interpeter:

    `python main.py`

Done.

## Note:
After the first transfer has started a folder called preferences will be created in the same folder where main.py is located to store the program preferences. If this file is deleted or in corrupted the programm will try to load readable preferences and put the others as the default. If anything is readable the program will load all the default preferences. The next time a valid transfer has started preferences file is overwrited with the correct one.
