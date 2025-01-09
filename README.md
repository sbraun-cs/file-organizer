Script Description:
This Python script is designed to monitor the Downloads folder on a Windows system and automatically organize files into specific subfolders based on their type. It uses the watchdog library to watch for changes in the Downloads folder and moves files to their designated folders such as Audio, Videos, Images, Documents, and Others. If the file doesn't match any predefined type, it is placed into the "Others" folder.

Key Features:
Automatic Folder Organization:

It sorts files into distinct folders based on their extensions:
Audio: .mp3, .wav, .aac, etc.
Video: .mp4, .avi, .mov, etc.
Image: .jpg, .png, .gif, etc.
Document: .pdf, .docx, .pptx, etc.
Others: Files with unsupported extensions are moved here.
Folder Creation:

The script ensures that all destination folders exist. If any of the folders (Audio, Videos, Images, Documents, Others) do not exist, they are automatically created.
Unique File Naming:

If a file already exists in the destination folder, the script ensures that the file is renamed by appending a counter to its name, thus preventing overwriting of files with the same name.
Event-Driven:

The script uses watchdog to continuously monitor the Downloads folder for any changes. When new files are added, the script automatically sorts them into the appropriate folder.
Timestamped Folders:

Files are moved into subfolders named by the current date (e.g., YYYY-MM-DD), creating a structured archive in the destination folders.
Usage Instructions:
Configuration:

Set the SOURCE_DIR to the path of your Downloads folder (C:/Users/UserName/Downloads).
Define the destination folders and their respective file types in the DEST_DIRS and FILE_TYPES dictionaries.

Running the Script:
The script runs continuously, watching for new files in the Downloads folder. To start it, run the script using Python.
Dependencies:

This script requires the watchdog library. You can install it with:
pip install watchdog
