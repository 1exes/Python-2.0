import json
import threading
from tqdm import tqdm
from webbrowser import Chrome
import click
from clicknium import clicknium as cc, locator, ui
import time
import pyautogui
from random import choice, shuffle
from datetime import datetime, timedelta
import os
import logging
from logging.handlers import RotatingFileHandler
import glob

# Liste von User-Agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
]

# Rate-Limiting-Zeit
RATE_LIMIT_DELAY = 10  # Zeit in Sekunden zwischen den Anfragen

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[RotatingFileHandler('upload_log.txt', maxBytes=100000, backupCount=5)]
)

def keep_computer_awake():
    pyautogui.moveRel(1, 1)
    pyautogui.moveRel(-1, -1)

def write_to_log(message, level='INFO'):
    logging.log(getattr(logging, level.upper()), message)

def perform_upload_video(num, best_upload_times, video_path, tab):
    user_agent = choice(USER_AGENTS)
    
    # Überprüfen, ob tab.driver existiert
    if hasattr(tab, 'driver'):
        tab.driver.execute_script(f"Object.defineProperty(navigator, 'userAgent', {{value: '{user_agent}', writable: false}});")
    else:
        write_to_log("Fehler: 'BrowserTab' object has no attribute 'driver'", level='ERROR')
        return

    # Ihr bestehender Code für den Video-Upload
    write_to_log("Video-Upload wird gestartet...")
    tab.find_element(locator.tiktok.one).click(by='mouse-emulation')
    time.sleep(5)

    if os.path.getsize(video_path) > (50 * 1024 * 1024):
        write_to_log(f"Die Datei {video_path} ist zu groß. Überspringe das Hochladen dieses Videos.", level='WARNING')
        return

    pyautogui.write(video_path)
    pyautogui.press('enter')

    tab.find_element(locator.tiktok.four).set_text("Funny", by='sendkey-after-click')
    time.sleep(60)

    tab.find_element(locator.tiktok.five).click(by='mouse-emulation')
    tab.find_element(locator.tiktok.div_noch_ein_video_hochladen).click(by='mouse-emulation')
    time.sleep(10)

    keep_computer_awake()
    write_to_log(f"Video Nr. {num} erfolgreich hochgeladen.")

def upload_video(num, best_upload_times, video_path, tab):
    try_count = 3
    while try_count > 0:
        try:
            write_to_log(f"Beginne mit dem Hochladen von Video Nr. {num}...")
            
            current_time = datetime.now()
            next_upload_time = None
            
            for hour, minute in best_upload_times:
                if current_time.hour < hour or (current_time.hour == hour and current_time.minute < minute):
                    next_upload_time = current_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
                    break
            
            if next_upload_time is None:
                next_upload_time = current_time.replace(hour=best_upload_times[0][0], minute=best_upload_times[0][1], second=0, microsecond=0) + timedelta(days=1)
            
            wait_time = (next_upload_time - current_time).total_seconds()
            
            hours, remainder = divmod(wait_time, 3600)
            minutes, _ = divmod(remainder, 60)
            write_to_log(f"Nächstes Hochladezeitfenster für Video Nr. {num} ist um {next_upload_time.strftime('%H:%M')}. Nächste Hochladezeit in {int(hours)} Stunden und {int(minutes)} Minuten.")
            
            if wait_time > 600:
                write_to_log("Warte auf das nächste Hochladezeitfenster...")
                time.sleep(wait_time)
            
            perform_upload_video(num, best_upload_times, video_path, tab)  # Aufruf der Funktion mit Rate Limiting
            break

        except KeyboardInterrupt:
            write_to_log("Programm wurde abgebrochen.")
            break

        except Exception as e:
            write_to_log(f"Fehler: {e}", level='ERROR')
            try_count -= 1
            if try_count > 0:
                write_to_log(f"Versuche es erneut. Versuche übrig: {try_count}")
            else:
                write_to_log("Maximale Anzahl von Versuchen erreicht. Das Skript wird beendet.")
        
        finally:
            tab.close() if 'tab' in locals() else None
            time.sleep(RATE_LIMIT_DELAY)

def load_config():
    try:
        use_config = input("Möchten Sie die Einstellungen aus der config.json Datei laden? (j/n): ").lower()
        
        if use_config == 'j':
            config_path = r"C:\Users\edgar\Documents\GitHub\Python-2.0\Clicknium\Tiktok\fertige_sachen\config.json"
            with open(config_path, 'r') as config_file:
                config = json.load(config_file)

            video_folder_path = config.get('video_folder_path')
            best_upload_times = config.get('tiktok_best_upload_times')
            
            video_files = glob.glob(f"{video_folder_path}\\*.mp4")
            video_numbers = list(range(1, len(video_files) + 1))
            shuffle(video_numbers)
        else:
            video_folder_path = input("Bitte geben Sie den Pfad zum Videofolder an: ")
            best_upload_times = [(8, 10), (14, 0), (16, 53), (17, 16), (22, 57)]

            video_files = glob.glob(f"{video_folder_path}\\*.mp4")
            video_numbers = list(range(1, len(video_files) + 1))
            shuffle(video_numbers)

        return video_numbers, best_upload_times, video_files

    except Exception as e:
        write_to_log(f"Fehler beim Laden der Konfiguration: {e}", level='ERROR')
        return None, None, None

if __name__ == "__main__":
    try:
        video_numbers, best_upload_times, video_files = load_config()
        
        if video_numbers is None:
            write_to_log("Konfiguration konnte nicht geladen werden. Das Skript wird beendet.", level='ERROR')
            exit()

        write_to_log("Öffne TikTok Upload-Seite...")
        tab = cc.edge.open("https://www.tiktok.com/upload?lang=en")
        time.sleep(5)

        threads = []

        for idx, video_file in enumerate(video_files):
            thread = threading.Thread(target=upload_video, args=(video_numbers[idx], best_upload_times, video_file, tab))
            threads.append(thread)
            thread.start()

        for thread in tqdm(threads, desc="Videos hochladen", ncols=100):
            thread.join()

        write_to_log("Alle Videos wurden hochgeladen.")

    except KeyboardInterrupt:
        write_to_log("Programm wurde abgebrochen.")

    except Exception as e:
        write_to_log(f"Fehler: {e}", level='ERROR')
