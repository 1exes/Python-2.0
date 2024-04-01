from webbrowser import Chrome
import click
from clicknium import clicknium as cc, locator, ui
import time
import pyautogui
from random import randint, shuffle
from datetime import datetime, timedelta




# Anzahl der Videos, Start- und Endzahl abfragen
start_number = int(input("Startzahl: "))
end_number = int(input("Endzahl: "))

# Liste der Video-Nummern erstellen und in zufälliger Reihenfolge sortieren
video_numbers = list(range(start_number, end_number + 1))
shuffle(video_numbers)

# Anzahl der täglichen Posts auswählen (zwischen 3 und 5)
daily_posts = int(input("Anzahl der täglichen Posts (3-5): "))
if daily_posts < 3 or daily_posts > 5:
    print("Ungültige Anzahl der täglichen Posts.")
    exit()

# Liste der besten Hochladezeiten festlegen (als Stunden und Minuten)
best_upload_times = [(10, 10), (14, 0), (18, 45), (20, 15), (22, 0)][:daily_posts]  # Beispielzeiten, angepasst an daily_posts

# Tab für TikTok Upload öffnen
tab = cc.edge.open("https://www.tiktok.com/upload?lang=en")
time.sleep(5)

# Schleife für das Hochladen der Videos in zufälliger Reihenfolge
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
        
        # Falls keine zukünftige Zeit gefunden wurde, zur ersten Zeit des nächsten Tages springen
        if next_upload_time is None:
            next_upload_time = current_time.replace(hour=best_upload_times[0][0], minute=best_upload_times[0][1], second=0, microsecond=0) + timedelta(days=1)
        
        # Wartezeit bis zur nächsten Hochladezeit
        wait_time = (next_upload_time - current_time).total_seconds()
        
        # Zeit in der Konsole anzeigen
        hours, remainder = divmod(wait_time, 3600)
        minutes, _ = divmod(remainder, 60)
        print(f"Video wird hochgeladen am {next_upload_time.strftime('%Y-%m-%d %H:%M:%S')}. Nächste Hochladezeit in {int(hours)} Stunden und {int(minutes)} Minuten.")
        
        # Wartezeit überprüfen
        if wait_time <= 600:
            break
        
        # Alle 10 Minuten aktualisieren
        time.sleep(600)
        current_time = datetime.now()
    
    # Wartezeit bis zur nächsten Hochladezeit
    time.sleep(wait_time)
    
    tab.find_element(locator.tiktok.one).click(by='mouse-emulation')  # Upload-Button klicken
    time.sleep(5)

    file_path = fr"C:\Users\edgar\Videos\{num}.mp4"
    pyautogui.write(file_path)
    pyautogui.press('enter')

    # Automatisierung des Assistenten
    tab.find_element(locator.tiktok.four).set_text("Funny", by='sendkey-after-click')
    time.sleep(60)

    tab.find_element(locator.tiktok.five).click(by='mouse-emulation')
    
    tab.find_element(locator.tiktok.div_noch_ein_video_hochladen).click(by='mouse-emulation')
   
    # Wartezeit nach dem Hochladen eines Videos
    time.sleep(10)

print("Alle Videos wurden hochgeladen.")

# Browser schließen
tab.close()
