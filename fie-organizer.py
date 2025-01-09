import logging
from pathlib import Path
from shutil import move
from time import sleep
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration
SOURCE_DIR = Path("C:/Users/UserName/Downloads")  # Ensure this path is correct
DEST_DIRS = {
    "audio": Path("C:/Users/UserName/Downloads/Audio"),
    "video": Path("C:/Users/UserName/Downloads/Videos"),
    "image": Path("C:/Users/UserName/Downloads/Images"),
    "document": Path("C:/Users/UserName/Downloads/Documents"),
    "others": Path("C:/Users/UserName/Downloads/Others"),  # Folder for unsupported files
}
FILE_TYPES = {
    "audio": [".m4a", ".flac", ".mp3", ".wav", ".wma", ".aac"],
    "video": [".webm", ".mpg", ".mp4", ".avi", ".mov", ".wmv", ".flv"],
    "image": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".heic"],
    "document": [".doc", ".docx", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"],
}

# Utility Functions
def ensure_folder_exists(folder: Path):
    """Ensure a folder exists, creating it if necessary."""
    if not folder.exists():
        folder.mkdir(parents=True, exist_ok=True)
        logging.info(f"Created folder: {folder}")

def make_unique(dest: Path, name: str) -> str:
    """Generate a unique file name if a conflict exists."""
    counter = 1
    new_name = name
    while (dest / new_name).exists():
        stem, suffix = Path(name).stem, Path(name).suffix
        new_name = f"{stem}({counter}){suffix}"
        counter += 1
    return new_name

def move_file(dest: Path, entry: Path):
    """Move a file to the destination folder, ensuring uniqueness."""
    dest_file = dest / entry.name
    if dest_file.exists():
        dest_file = dest / make_unique(dest, entry.name)
    move(str(entry), str(dest_file))
    logging.info(f"Moved file: {entry.name} to {dest_file}")

def get_file_type(file: Path) -> str:
    """Determine the file type based on its extension."""
    for file_type, extensions in FILE_TYPES.items():
        if file.suffix.lower() in extensions:
            return file_type
    return "others"  # Default to "Others" for unsupported files

# Event Handler
class MoverHandler(FileSystemEventHandler):
    """Handles file system events to categorize and move files."""

    def on_modified(self, event):
        """Triggered when the source directory is modified."""
        for entry in SOURCE_DIR.iterdir():
            if entry.is_file():
                file_type = get_file_type(entry)
                self.move_to_folder(file_type, entry)

    def move_to_folder(self, file_type: str, entry: Path):
        """Move a file to its corresponding folder."""
        dest_folder = DEST_DIRS[file_type] / datetime.now().strftime("%Y-%m-%d")
        ensure_folder_exists(dest_folder)
        move_file(dest_folder, entry)

# Main Execution
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,  # Change logging to DEBUG for troubleshooting
                        format="%(asctime)s - %(levelname)s - %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")


    # Ensure all destination folders exist
    for folder in DEST_DIRS.values():
        ensure_folder_exists(folder)

    if not SOURCE_DIR.exists():
        logging.error(f"Source directory does not exist: {SOURCE_DIR}")
    else:
        logging.info(f"Watching directory: {SOURCE_DIR}")

        event_handler = MoverHandler()
        observer = Observer()
        observer.schedule(event_handler, str(SOURCE_DIR), recursive=True)
        observer.start()

        try:
            while True:
                sleep(10)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
