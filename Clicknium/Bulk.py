from fileinput import close
from webbrowser import Chrome
import click
from clicknium import clicknium as cc, locator, ui
import time
import pyautogui
from random import randint

# Anzahl der Videos, Start- und Endzahl abfragen
start_number = int(input("Startzahl: "))
end_number = int(input("Endzahl: "))

# Tab für TikTok Upload öffnen
tab = cc.edge.open("https://www.tiktok.com/upload?lang=en")
time.sleep(5)

# Schleife für das Hochladen der Videos
for num in range(start_number, end_number + 1):
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


