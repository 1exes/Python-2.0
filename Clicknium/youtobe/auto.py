from cgitb import text
from webbrowser import Chrome
import click
from clicknium import clicknium as cc, locator, ui
import time
import pyautogui
from random import randint, shuffle

# Anzahl der Videos, Start- und Endzahl abfragen
start_number = int(input("Startzahl: "))
end_number = int(input("Endzahl: "))

# Liste der Video-Nummern erstellen und in zufälliger Reihenfolge sortieren
video_numbers = list(range(start_number, end_number + 1))
shuffle(video_numbers)

# Tab für TikTok Upload öffnen
tab = cc.edge.open("https://studio.youtube.com/channel/UCu6cByOlYCJBGZJhOLHVFVA/videos/upload?d=ud&filter=%5B%5D&sort=%7B%22columnType%22%3A%22date%22%2C%22sortOrder%22%3A%22DESCENDING%22%7D")
time.sleep(5)

# Schleife für das Hochladen der Videos in zufälliger Reihenfolge
for num in video_numbers:
    tab.find_element(locator.chrome.dateien_auswählen).click(by='mouse-emulation')  # Upload-Button klicken
    time.sleep(5)

    file_path = fr"C:\Users\edgar\Videos\{num}.mp4"
    pyautogui.write(file_path)
    pyautogui.press('enter')

    # Automatisierung des Assistenten
    tab.find_element(locator.tiktok.four).set_text("Funny", by='sendkey-after-click')
    time.sleep(60)

    tab.find_element(locator.tiktok.datum).click(by='mouse-emulation')

    tab.find_element(locator.tiktok.five).click(by='mouse-emulation')
    
    time.sleep(10)
    
    tab.find_element(locator.tiktok.div_noch_ein_video_hochladen).click()
   
    # Wartezeit nach dem Hochladen eines Videos
    time.sleep(10)

print("Alle Videos wurden hochgeladen.")

# Browser schließen
tab.close()

