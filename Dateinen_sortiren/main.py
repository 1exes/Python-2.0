import os
import shutil
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import magic
from datetime import datetime, timedelta
import threading
import time


# Initialisiere Magic
mime = magic.Magic(mime=True)

# Quellordner und Zielordner
source_dirs = ["C:\\Users\\richte\\Downloads\\"]
main_dir_media = "C:\\Users\\richte\\Downloads\\Media"
main_dir_documents = "C:\\Users\\richte\\Downloads\\Documents"
main_dir_misc = "C:\\Users\\richte\\Downloads\\Misc"
archive_dir = "C:\\Users\\richte\\Downloads\\Archive"
backup_dir = "C:\\Users\\richte\\Downloads\\Backup"
archive_threshold_days = 30

# Unterverzeichnisse für Dateitypen
subdirs = {
    "media": ["Images", "Videos", "Audio"],
    "documents": ["PDFs", "Word_Documents", "Spreadsheets", "Presentations", "Text_Files"],
    "misc": [],
    "archive": [],
    "backup": []
}

# Unterstützte Dateitypen
image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".webp", ".tiff", ".bmp", ".ico"]
video_extensions = [".webm", ".mpg", ".mpeg", ".mp4", ".avi", ".wmv", ".mov", ".flv"]
audio_extensions = [".m4a", ".flac", ".mp3", ".wav", ".wma", ".aac"]
document_extensions = [".doc", ".docx", ".odt", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx", ".csv", ".tsv", ".txt"]

# Liste der Zielordner, die nicht gelöscht werden sollen
protected_dirs = [
    main_dir_media,
    main_dir_documents,
    main_dir_misc,
    archive_dir,
    backup_dir
]

# Logging-Konfiguration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Funktion zum Erstellen der Zielordner und Unterverzeichnisse, falls sie nicht existieren
def create_directories():
    directories = [main_dir_media, main_dir_documents, main_dir_misc, archive_dir, backup_dir]
    for main_dir in directories:
        if not os.path.exists(main_dir):
            try:
                os.makedirs(main_dir)
                logging.info(f"Created directory: {main_dir}")
            except OSError as e:
                logging.error(f"Failed to create directory: {main_dir}. Error: {str(e)}")
        for subdir in subdirs[main_dir.split("\\")[-1].lower()]:
            full_subdir_path = os.path.join(main_dir, subdir)
            if not os.path.exists(full_subdir_path):
                try:
                    os.makedirs(full_subdir_path)
                    logging.info(f"Created subdirectory: {full_subdir_path}")
                except OSError as e:
                    logging.error(f"Failed to create subdirectory: {full_subdir_path}. Error: {str(e)}")

# Funktion zur Erstellung eines eindeutigen Dateinamens im Zielordner, um Duplikate zu vermeiden
def make_unique(dest, name):
    filename, extension = os.path.splitext(name)
    counter = 1
    while os.path.exists(os.path.join(dest, name)):
        name = f"{filename}({counter}){extension}"
        counter += 1
    return name

# Funktion zum Kopieren einer Datei in ein ZIP-Archiv ohne das Original zu löschen
def archive_file(entry, name):
    archive_path = os.path.join(archive_dir, f"{name}.zip")
    try:
        shutil.make_archive(os.path.splitext(archive_path)[0], 'zip', os.path.dirname(entry), os.path.basename(entry))
        logging.info(f"Archived file: {name}")
    except (shutil.Error, OSError) as e:
        logging.error(f"Failed to archive file {name}. Error: {str(e)}")

# Funktion zum Verschieben einer Datei in einen Zielordner und zur Vermeidung von Duplikaten
def move_file(dest, entry, name):
    dest_path = os.path.join(dest, name)
    try:
        if os.path.exists(dest_path):
            unique_name = make_unique(dest, name)
            old_name = os.path.join(dest, name)
            new_name = os.path.join(dest, unique_name)
            os.rename(old_name, new_name)
        shutil.move(entry, os.path.join(dest, name))
        logging.info(f"Moved file: {name} to {dest}")
    except (shutil.Error, OSError) as e:
        logging.error(f"Failed to move file {name} to {dest}. Error: {str(e)}")

# Funktion zum Archivieren alter Dateien
def archive_old_files():
    now = datetime.now()
    cutoff_date = now - timedelta(days=archive_threshold_days)
    for main_dir in [main_dir_media, main_dir_documents, main_dir_misc]:
        try:
            for root, dirs, files in os.walk(main_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    if datetime.fromtimestamp(os.path.getmtime(file_path)) < cutoff_date:
                        archive_file(file_path, file)
        except (shutil.Error, OSError) as e:
            logging.error(f"Failed to archive files in {main_dir}. Error: {str(e)}")

# Funktion zum Bereinigen leerer Ordner in den Quellordnern
def cleanup_empty_folders():
    for source_dir in source_dirs:
        try:
            for dirpath, dirnames, filenames in os.walk(source_dir, topdown=False):
                if not dirnames and not filenames:
                    if not is_recently_created(dirpath) and dirpath not in protected_dirs:
                        os.rmdir(dirpath)
                        logging.info(f"Deleted empty folder: {dirpath}")
        except (shutil.Error, OSError) as e:
            logging.error(f"Failed to clean up empty folders in {source_dir}. Error: {str(e)}")

# Funktion zur Überprüfung, ob ein Ordner kürzlich erstellt wurde
def is_recently_created(folder):
    try:
        one_minute_ago = datetime.now() - timedelta(minutes=1)
        folder_created_time = datetime.fromtimestamp(os.path.getctime(folder))
        return folder_created_time > one_minute_ago
    except OSError as e:
        logging.error(f"Error checking folder creation time for {folder}. Error: {str(e)}")
        return False

# Klasse für den FileSystemEventHandler zum Überwachen und Verschieben von Dateien
class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        for source_dir in source_dirs:
            try:
                for entry in os.scandir(source_dir):
                    name = entry.name
                    if entry.is_file():
                        mime_type = mime.from_file(entry.path)
                        if mime_type.startswith("image/"):
                            self.move_image_files(entry, name)
                        elif mime_type.startswith("video/"):
                            self.move_video_files(entry, name)
                        elif mime_type.startswith("audio/"):
                            self.move_audio_files(entry, name)
                        elif mime_type in ["application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
                            self.move_document_files(entry, name)
                        else:
                            self.move_misc_files(entry, name)
            except (shutil.Error, OSError) as e:
                logging.error(f"Error scanning directory {source_dir}. Error: {str(e)}")

    def move_image_files(self, entry, name):
        dest = os.path.join(main_dir_media, "Images")
        move_file(dest, entry.path, name)
        logging.info(f"Moved image file: {name} to {dest}")

    def move_video_files(self, entry, name):
        dest = os.path.join(main_dir_media, "Videos")
        move_file(dest, entry.path, name)
        logging.info(f"Moved video file: {name} to {dest}")

    def move_audio_files(self, entry, name):
        dest = os.path.join(main_dir_media, "Audio")
        move_file(dest, entry.path, name)
        logging.info(f"Moved audio file: {name} to {dest}")

    def move_document_files(self, entry, name):
        if name.endswith(".pdf"):
            dest = os.path.join(main_dir_documents, "PDFs")
        elif name.endswith(".doc") or name.endswith(".docx"):
            dest = os.path.join(main_dir_documents, "Word_Documents")
        elif name.endswith(".xls") or name.endswith(".xlsx"):
            dest = os.path.join(main_dir_documents, "Spreadsheets")
        elif name.endswith(".ppt") or name.endswith(".pptx"):
            dest = os.path.join(main_dir_documents, "Presentations")
        else:
            dest = os.path.join(main_dir_documents, "Text_Files")
        move_file(dest, entry.path, name)
        logging.info(f"Moved document file: {name} to {dest}")

    def move_misc_files(self, entry, name):
        move_file(main_dir_misc, entry.path, name)
        logging.info(f"Moved miscellaneous file: {name} to {main_dir_misc}")

# Watchdog Observer einrichten
if __name__ == "__main__":
    create_directories()
    event_handler = MoverHandler()
    observer = Observer()
    for source_dir in source_dirs:
        observer.schedule(event_handler, source_dir, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
