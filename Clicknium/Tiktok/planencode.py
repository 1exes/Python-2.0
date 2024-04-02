from clicknium import clicknium as cc, locator
import time
import pyautogui
from random import shuffle
from datetime import datetime, timedelta

# Funktion zum Hochladen der Videos
def upload_videos(start_number, end_number, daily_posts, best_upload_times):
    try:
        # Tab für TikTok Upload öffnen
        print("Öffne TikTok Upload...")
        tab = cc.edge.open("https://www.tiktok.com/upload?lang=en")
        time.sleep(5)
        print("TikTok Upload geöffnet.")

        # Liste der Video-Nummern erstellen und in zufälliger Reihenfolge sortieren
        video_numbers = list(range(start_number, end_number + 1))
        shuffle(video_numbers)
        print(f"Video-Nummern erstellt: {video_numbers}")

        # Schleife für das Hochladen der Videos
        for num in video_numbers:
            # Aktuelle Zeit und Datum abrufen
            current_time = datetime.now()

            while True:
                # Nächste beste Hochladezeit ermitteln
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
                print(f"Video wird hochgeladen am {next_upload_time.strftime('%Y-%m-%d %H:%M:%S')}. Nächste Hochladezeit in {int(hours)} Stunden und {int(minutes)} Minuten.")
                
                if wait_time <= 600:
                    break
                
                time.sleep(600)
                current_time = datetime.now()
            
            time.sleep(wait_time)
            
            print(f"Beginne mit dem Hochladen von Video {num}...")
            tab.find_element(locator.tiktok.one).click(by='mouse-emulation')
            time.sleep(5)

            file_path = fr"C:\Users\edgar\Videos\{num}.mp4"
            pyautogui.write(file_path)
            pyautogui.press('enter')
            print(f"Video {num} ausgewählt und hochgeladen.")

            tab.find_element(locator.tiktok.four).set_text("Funny", by='sendkey-after-click')
            time.sleep(60)

            tab.find_element(locator.tiktok.five).click(by='mouse-emulation')
            tab.find_element(locator.tiktok.div_noch_ein_video_hochladen).click(by='mouse-emulation')
            print("Assistent konfiguriert und nächstes Video ausgewählt.")

            time.sleep(10)
            print(f"Video {num} erfolgreich hochgeladen.")

        print("Alle Videos wurden hochgeladen.")
        tab.close()
        print("TikTok Upload geschlossen.")
    
    except Exception as e:
        print(f"Fehler beim Hochladen der Videos: {e}")

if __name__ == "__main__":
    try:
        start_number = int(input("Startzahl: "))
        end_number = int(input("Endzahl: "))

        daily_posts = int(input("Anzahl der täglichen Posts (3-5): "))
        if daily_posts < 3 or daily_posts > 5:
            print("Ungültige Anzahl der täglichen Posts.")
            exit()

        best_upload_times = [(10, 10), (14, 0), (15, 18), (17, 24), (22, 0), (23, 30)][:daily_posts]

        upload_videos(start_number, end_number, daily_posts, best_upload_times)

    except ValueError as ve:
        print("Ungültige Eingabe. Bitte geben Sie gültige Zahlen ein.")
