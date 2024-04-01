from clicknium import clicknium as cc, locator
import time
import pyautogui
from random import randint, shuffle
from datetime import datetime, timedelta

def load_config(filename):
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
        video_path = lines[0].strip()
        description_file = lines[1].strip()
        return video_path, description_file
    except Exception as e:
        print(f"Fehler beim Laden der Konfigurationsdatei: {e}")
        exit(1)

def load_video_description(filename):
    try:
        with open(filename, "r") as f:
            description = f.read().strip()
        return description
    except Exception as e:
        print(f"Fehler beim Laden der Video-Beschreibung: {e}")
        exit(1)

try:
    print("Programm gestartet...")
    
    video_path, description_file = load_config("config.txt")
    print(f"Konfiguration geladen. Videos werden aus {video_path} geladen und Beschreibungen aus {description_file}.")

    start_number = int(input("Startzahl: "))
    end_number = int(input("Endzahl: "))

    video_numbers = list(range(start_number, end_number + 1))
    shuffle(video_numbers)
    
    daily_posts = int(input("Anzahl der täglichen Posts (1-3): "))
    if daily_posts < 1 or daily_posts > 3:
        print("Ungültige Anzahl der täglichen Posts.")
        exit(1)

    best_upload_times = [(9, 45), (14, 0), (14, 15), (15, 15), (16, 0), (20, 13)][:daily_posts]

    tab = cc.edge.open("https://www.tiktok.com/upload?lang=en")
    print("Webbrowser geöffnet. Warte 5 Sekunden...")
    time.sleep(5)

    for num in video_numbers[:10]:
        current_time = datetime.now()
        
        while True:
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
            print(f"Nächstes Video wird hochgeladen am {next_upload_time.strftime('%Y-%m-%d %H:%M:%S')}. Nächste Hochladezeit in {int(hours)} Stunden und {int(minutes)} Minuten.")
            
            if wait_time <= 600:
                break
            
            time.sleep(60)
            current_time = datetime.now()
        
        time.sleep(wait_time)
        
        tab.find_element(locator.tiktok.one).click(by='mouse-emulation')
        time.sleep(5)

        file_path = f"{video_path}\\{num}.mp4"
        pyautogui.write(file_path)
        pyautogui.press('enter')

        description = load_video_description(description_file)
        tab.find_element(locator.tiktok.four).set_text(description, by='sendkey-after-click')
        time.sleep(60)
       
        time.sleep(10)
        print(f"Video {num}.mp4 hochgeladen und beschrieben.")

    print("Alle Videos wurden hochgeladen.")

except Exception as e:
    print(f"Ein Fehler ist aufgetreten: {e}")

finally:
    try:
        tab.close()
    except:
        pass
