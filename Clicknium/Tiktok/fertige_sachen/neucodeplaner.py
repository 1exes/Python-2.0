from clicknium import clicknium as cc, locator
import time
import pyautogui
from random import shuffle
from datetime import datetime, timedelta

def keep_computer_awake():
    pyautogui.moveRel(1, 1)
    pyautogui.moveRel(-1, -1)

def upload_video(num, upload_interval, video_description, tab, best_upload_times=None):
    try:
        current_time = datetime.now()
        next_upload_time = None

        if upload_interval == "best_times":
            if best_upload_times is None:
                print("Bitte geben Sie die besten Hochladezeiten an.")
                return

            while True:
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

        elif upload_interval == "hourly":
            wait_time = 3600  # 1 Stunde warten
            print(f"Nächstes Video wird in 1 Stunde hochgeladen.")

        time.sleep(wait_time)

        tab.find_element(locator.tiktok.one).click(by='mouse-emulation')
        time.sleep(5)

        file_path = fr"C:\Users\edgar\Videos\{num}.mp4"
        pyautogui.write(file_path)
        pyautogui.press('enter')

        tab.find_element(locator.tiktok.four).set_text(video_description, by='sendkey-after-click')  # Beschreibung setzen
        time.sleep(60)

        tab.find_element(locator.tiktok.five).click(by='mouse-emulation')
        tab.find_element(locator.tiktok.div_noch_ein_video_hochladen).click(by='mouse-emulation')

        time.sleep(10)
        print(f"Video Nr. {num} erfolgreich hochgeladen.")
        
        tab.close()  # Browser schließen

    except KeyboardInterrupt:
        print("Programm wurde unterbrochen.")
        tab.close()
        exit()

    except Exception as e:
        print(f"Fehler beim Hochladen von Video Nr. {num}: {e}")
        tab.close()

def main():
    start_number = int(input("Startzahl: "))
    end_number = int(input("Endzahl: "))

    video_numbers = list(range(start_number, end_number + 1))
    shuffle(video_numbers)

    upload_interval = input("Möchten Sie die 5 besten TikTok-Hochladezeiten ('best_times') oder stündlich hochladen ('hourly')? ")

    if upload_interval not in ["best_times", "hourly"]:
        print("Ungültige Auswahl.")
        return

    video_description = input("Bitte geben Sie die Beschreibung für das Video ein: ")

    best_upload_times = None
    if upload_interval == "best_times":
        daily_posts = int(input("Anzahl der täglichen Posts (3-5): "))
        if daily_posts < 3 or daily_posts > 5:
            print("Ungültige Anzahl der täglichen Posts.")
            return

        best_upload_times = [(8, 10), (14, 0), (16, 53), (17, 16), (23, 42)][:daily_posts]

    for num in video_numbers:
        tab = cc.edge.open("https://www.tiktok.com/upload?lang=en")
        time.sleep(5)
        upload_video(num, upload_interval, video_description, tab, best_upload_times)
        keep_computer_awake()  # Halte den Computer wach

    print("Alle Videos wurden hochgeladen.")

if __name__ == "__main__":
    main()