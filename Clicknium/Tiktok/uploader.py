from clicknium import clicknium as cc, locator
import time
import pyautogui
from random import shuffle
from datetime import datetime, timedelta
import sys

def load_video_description(filename):
    try:
        with open(filename, "r") as f:
            description = f.read().strip()
        return description
    except Exception as e:
        print(f"Fehler beim Laden der Video-Beschreibung: {e}")
        return None

def main(video_path, description_file, daily_posts, best_upload_times):
    try:
        tab = cc.edge.open("https://www.tiktok.com/upload?lang=en")
        time.sleep(5)
        
        for num in range(1, 11):
            current_time = datetime.now()
            
            while True:
                next_upload_time = None
                for hour, minute in best_upload_times:
                    potential_upload_time = current_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
                    if current_time < potential_upload_time:
                        next_upload_time = potential_upload_time
                        break
                
                if next_upload_time is None:
                    next_upload_time = current_time.replace(hour=best_upload_times[0][0], minute=best_upload_times[0][1], second=0, microsecond=0) + timedelta(days=1)
                
                wait_time = (next_upload_time - current_time).total_seconds()
                
                hours, remainder = divmod(wait_time, 3600)
                minutes, _ = divmod(remainder, 60)
                print(f"Video {num} wird hochgeladen... Nächstes Video wird hochgeladen am {next_upload_time.strftime('%Y-%m-%d %H:%M:%S')}. Nächste Hochladezeit in {int(hours)} Stunden und {int(minutes)} Minuten.")
                
                if wait_time <= 600:
                    break
                
                time.sleep(600)
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

if __name__ == "__main__":
    video_path = sys.argv[1]
    description_file = sys.argv[2]
    daily_posts = int(sys.argv[3])
    best_upload_times = eval(sys.argv[4])
    
    main(video_path, description_file, daily_posts, best_upload_times)
