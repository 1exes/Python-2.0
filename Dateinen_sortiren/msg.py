import os
import shutil
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime, timedelta
import threading

# Quellordner und Hauptzielordner
source_dirs = [
    "C:\\Users\\richte\\Downloads\\",
]

# Hauptzielordner
main_dir_media = "C:\\Users\\richte\\Downloads\\Media"
main_dir_documents = "C:\\Users\\richte\\Downloads\\"
main_dir_misc = "C:\\Users\\richte\\Downloads\\sonstiges"
archive_dir = "C:\\Users\\richte\\Downloads\\Archive"
archive_threshold_days = 30

# Unterordner für verschiedene Dateitypen
subdirs = {
    main_dir_media: ["Sound_Effects", "Music", "Videos", "Images"],
    main_dir_documents: ["Documents"],
    main_dir_misc: ["sonstiges"],
}

# Geschützte Ordner, die nicht gelöscht werden sollen
protected_dirs = [
    main_dir_media,
    main_dir_documents,
    main_dir_misc,
    archive_dir
]
for main_dir in subdirs:
    protected_dirs.extend([os.path.join(main_dir, subdir) for subdir in subdirs[main_dir]])

# Unterstützte Dateitypen
image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw", ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]
video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg", ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]
audio_extensions = [".m4a", ".flac", ".mp3", ".wav", ".wma", ".aac"]
document_extensions = [".doc", ".docx", ".odt", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx", ".csv", ".tsv"]

# Logging-Konfiguration
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Funktion zum Erstellen der Haupt- und Unterordner, falls sie nicht existieren
def create_directories():
    main_dirs = [main_dir_media, main_dir_documents, main_dir_misc, archive_dir]
    for main_dir in main_dirs:
        if not os.path.exists(main_dir):
            try:
                os.makedirs(main_dir)
                logging.info(f"Created main directory: {main_dir}")
            except OSError as e:
                logging.error(f"Failed to create main directory: {main_dir}. Error: {str(e)}")
                
        for subdir in subdirs.get(main_dir, []):
            subdir_path = os.path.join(main_dir, subdir)
            if not os.path.exists(subdir_path):
                try:
                    os.makedirs(subdir_path)
                    logging.info(f"Created subdirectory: {subdir_path}")
                except OSError as e:
                    logging.error(f"Failed to create subdirectory: {subdir_path}. Error: {str(e)}")

# Funktion zur Erstellung eines eindeutigen Dateinamens im Zielordner, um Duplikate zu vermeiden
def make_unique(dest, name):
    filename, extension = os.path.splitext(name)
    counter = 1
    while os.path.exists(os.path.join(dest, name)):
        name = f"{filename}({counter}){extension}"
        counter += 1
    return name

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

# Funktion zum Archivieren alter Dateien in einem ZIP-Archiv (Kopien der Dateien)
def archive_old_files():
    now = datetime.now()
    cutoff_date = now - timedelta(days=archive_threshold_days)
    for main_dir in [main_dir_media, main_dir_documents, main_dir_misc]:
        for subdir in subdirs.get(main_dir, []):
            dest_dir = os.path.join(main_dir, subdir)
            try:
                for entry in os.scandir(dest_dir):
                    if entry.is_file() and datetime.fromtimestamp(entry.stat().st_mtime) < cutoff_date:
                        archive_name = os.path.join(archive_dir, entry.name)
                        shutil.make_archive(archive_name, 'zip', dest_dir, entry.name)
                        logging.info(f"Archived file: {entry.name}")
            except (shutil.Error, OSError) as e:
                logging.error(f"Failed to archive files in {dest_dir}. Error: {str(e)}")

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
                        if not self.check_audio_files(entry, name) and \
                           not self.check_video_files(entry, name) and \
                           not self.check_image_files(entry, name) and \
                           not self.check_document_files(entry, name):
                            self.move_misc_files(entry, name)
            except (shutil.Error, OSError) as e:
                logging.error(f"Error scanning directory {source_dir}. Error: {str(e)}")

    def check_audio_files(self, entry, name):
        try:
            for audio_extension in audio_extensions:
                if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
                    if entry.stat().st_size < 10_000_000 or "SFX" in name:
                        dest = os.path.join(main_dir_media, "Sound_Effects")
                    else:
                        dest = os.path.join(main_dir_media, "Music")
                    move_file(dest, entry.path, name)
                    logging.info(f"Moved audio file: {name} to {dest}")
                    return True
            return False
        except (shutil.Error, OSError) as e:
            logging.error(f"Error moving audio file {name}. Error: {str(e)}")
            return False

    def check_video_files(self, entry, name):
        try:
            for video_extension in video_extensions:
                if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                    dest = os.path.join(main_dir_media, "Videos")
                    move_file(dest, entry.path, name)
                    logging.info(f"Moved video file: {name} to {dest}")
                    return True
            return False
        except (shutil.Error, OSError) as e:
            logging.error(f"Error moving video file {name}. Error: {str(e)}")
            return False

    def check_image_files(self, entry, name):
        try:
            for image_extension in image_extensions:
                if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                    dest = os.path.join(main_dir_media, "Images")
                    move_file(dest, entry.path, name)
                    logging.info(f"Moved image file: {name} to {dest}")
                    return True
            return False
        except (shutil.Error, OSError) as e:
            logging.error(f"Error moving image file {name}. Error: {str(e)}")
            return False

    def check_document_files(self, entry, name):
        try:
            for document_extension in document_extensions:
                if name.endswith(document_extension) or name.endswith(document_extension.upper()):
                    dest = os.path.join(main_dir_documents, "Documents")
                    move_file(dest, entry.path, name)
                    logging.info(f"Moved document file: {name} to {dest}")
                    return True
            return False
        except (shutil.Error, OSError) as e:
            logging.error(f"Error moving document file {name}. Error: {str(e)}")
            return False

    def move_misc_files(self, entry, name):
        try:
            dest = os.path.join(main_dir_misc, "Misc")
            move_file(dest, entry.path, name)
            logging.info(f"Moved miscellaneous file: {name} to {dest}")
        except (shutil.Error, OSError) as e:
            logging.error(f"Error moving miscellaneous file {name}. Error: {str(e)}")

# Funktion zur Initialisierung und Überwachung der Verzeichnisänderungen
def start_monitoring():
    event_handler = MoverHandler()
    observer = Observer()
    for source_dir in source_dirs:
        observer.schedule(event_handler, source_dir, recursive=True)
    observer.start()
    logging.info(f"Monitoring started for directories: {', '.join(source_dirs)}")
    try:
        while True:
            archive_old_files()
            cleanup_empty_folders()
            threading.Event().wait(60)
    except KeyboardInterrupt:
        observer.stop()
        logging.info("Monitoring stopped by user")
    observer.join()

if __name__ == "__main__":
    create_directories()
    start_monitoring()
