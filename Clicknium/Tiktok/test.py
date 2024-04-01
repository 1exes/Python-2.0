from webbrowser import Chrome
import click
from clicknium import clicknium as cc, locator, ui
import time
import pyautogui
from random2 import randint


# Anzahl der Videos, Start- und Endzahl abfragen
start_number = int(input("Startzahl: "))
end_number = int(input("Endzahl: "))

# Zufällige Zahl generieren und ausgeben
random_num = randint(start_number, end_number)



tab = cc.edge.open("https://www.tiktok.com/upload?lang=en") #opens the web browser on tiktok

time.sleep(5)

tab.find_element(locator.tiktok.one).click(by='mouse-emulation') #starts the mouse emulation and locates the upload buttontab = cc.edge.open("https://www.tiktok.com/@mindset404")

#starts the upload

time.sleep(5)

file_path = fr"C:\Users\edgar\Videos\{random_num}.mp4"
pyautogui.write(file_path)

pyautogui.press('enter')



#automate the wizard

tab.find_element(locator.tiktok.four).set_text("Funny", by='sendkey-after-click')

time.sleep(60)

tab.find_element(locator.tiktok.five).click(by='mouse-emulation')