import os
import shutil
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime, timedelta

# Quellordner und Zielordner
source_dirs = [
    "C:\\Users\\edgar\\Downloads\\",
    "C:\\Users\\edgar\\Documents\\"
]
dest_dir_sfx = "C:\\Users\\edgar\\Downloads\\Sound_Effects"
dest_dir_music = "C:\\Users\\edgar\\Downloads\\Music"
dest_dir_video = "C:\\Users\\edgar\\Downloads\\Videos"
dest_dir_image = "C:\\Users\\edgar\\Downloads\\Images"
dest_dir_documents = "C:\\Users\\edgar\\Downloads\\Documents"
dest_dir_misc = "C:\\Users\\edgar\\Downloads\\Misc"
archive_dir = "C:\\Users\\edgar\\Downloads\\Archive"
backup_dir = "C:\\Users\\edgar\\Downloads\\Backup"
archive_threshold_days = 30

# Unterstützte Dateitypen
image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw", ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]
video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg", ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]
audio_extensions = [".m4a", ".flac", ".mp3", ".wav", ".wma", ".aac"]
document_extensions = [".doc", ".docx", ".odt", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]

def create_directories():
    directories = [dest_dir_sfx, dest_dir_music, dest_dir_video, dest_dir_image, dest_dir_documents, dest_dir_misc, archive_dir, backup_dir]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logging.info(f"Created directory: {directory}")

def make_unique(dest, name):
    filename, extension = os.path.splitext(name)
    counter = 1
    while os.path.exists(os.path.join(dest, name)):
        name = f"{filename}({counter}){extension}"
        counter += 1
    return name

def move_file(dest, entry, name):
    dest_path = os.path.join(dest, name)
    if os.path.exists(dest_path):
        unique_name = make_unique(dest, name)
        old_name = os.path.join(dest, name)
        new_name = os.path.join(dest, unique_name)
        os.rename(old_name, new_name)
    shutil.move(entry, os.path.join(dest, name))
    logging.info(f"Moved file: {name} to {dest}")

def backup_file(src):
    backup_name = os.path.join(backup_dir, os.path.basename(src))
    shutil.copy(src, backup_name)
    logging.info(f"Backed up file: {os.path.basename(src)} to {backup_name}")

def archive_old_files():
    now = datetime.now()
    cutoff_date = now - timedelta(days=archive_threshold_days)
    for dest_dir in [dest_dir_sfx, dest_dir_music, dest_dir_video, dest_dir_image, dest_dir_documents, dest_dir_misc]:
        for entry in os.scandir(dest_dir):
            if entry.is_file() and datetime.fromtimestamp(entry.stat().st_mtime) < cutoff_date:
                archive_name = os.path.join(archive_dir, entry.name)
                shutil.make_archive(archive_name, 'zip', dest_dir, entry.name)
                os.remove(entry.path)
                logging.info(f"Archived file: {entry.name}")

def cleanup_empty_folders():
    for source_dir in source_dirs:
        for dirpath, dirnames, filenames in os.walk(source_dir, topdown=False):
            if not dirnames and not filenames:
                # Überprüfen, ob der Ordner älter als 1 Minute ist, um versehentlich erstellte Ordner zu vermeiden
                if not is_recently_created(dirpath):
                    os.rmdir(dirpath)
                    logging.info(f"Deleted empty folder: {dirpath}")

def is_recently_created(folder):
    one_minute_ago = datetime.now() - timedelta(minutes=1)
    folder_created_time = datetime.fromtimestamp(os.path.getctime(folder))
    return folder_created_time > one_minute_ago

class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        for source_dir in source_dirs:
            for entry in os.scandir(source_dir):
                name = entry.name
                if entry.is_file():
                    if not self.check_audio_files(entry, name) and \
                       not self.check_video_files(entry, name) and \
                       not self.check_image_files(entry, name) and \
                       not self.check_document_files(entry, name):
                        self.move_misc_files(entry, name)

    def check_audio_files(self, entry, name):
        for audio_extension in audio_extensions:
            if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
                if entry.stat().st_size < 10_000_000 or "SFX" in name:
                    dest = dest_dir_sfx
                else:
                    dest = dest_dir_music
                backup_file(entry.path)  # Sicherheitskopie erstellen
                move_file(dest, entry.path, name)
                logging.info(f"Moved audio file: {name} to {dest}")
                return True
        return False

    def check_video_files(self, entry, name):
        for video_extension in video_extensions:
            if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                backup_file(entry.path)  # Sicherheitskopie erstellen
                move_file(dest_dir_video, entry.path, name)
                logging.info(f"Moved video file: {name} to {dest_dir_video}")
                return True
        return False

    def check_image_files(self, entry, name):
        for image_extension in image_extensions:
            if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                backup_file(entry.path)  # Sicherheitskopie erstellen
                move_file(dest_dir_image, entry.path, name)
                logging.info(f"Moved image file: {name} to {dest_dir_image}")
                return True
        return False

    def check_document_files(self, entry, name):
        for document_extension in document_extensions:
            if name.endswith(document_extension) or name.endswith(document_extension.upper()):
                backup_file(entry.path)  # Sicherheitskopie erstellen
                move_file(dest_dir_documents, entry.path, name)
                logging.info(f"Moved document file: {name} to {dest_dir_documents}")
                return True
        return False

    def move_misc_files(self, entry, name):
        dest = dest_dir_misc
        move_file(dest, entry.path, name)
        logging.info(f"Moved miscellaneous file: {name} to {dest}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    create_directories()
    event_handler = MoverHandler()
    observer = Observer()
    for source_dir in source_dirs:
        observer.schedule(event_handler, source_dir, recursive=True)
    observer.start()
    try:
        while True:
            cleanup_empty_folders()
            archive_old_files()
            observer.join(10)  # Observer alle 10 Sekunden überprüfen
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
