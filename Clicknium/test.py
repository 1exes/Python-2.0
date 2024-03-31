from webbrowser import Chrome
import click
from clicknium import clicknium as cc, locator, ui
import time
import pyautogui



tab = cc.edge.open("https://www.tiktok.com/upload?lang=en") #opens the web browser on tiktok

time.sleep(5)

tab.find_element(locator.tiktok.one).click(by='mouse-emulation') #starts the mouse emulation and locates the upload buttontab = cc.edge.open("https://www.tiktok.com/@mindset404")

#starts the upload

time.sleep(5)

pyautogui.write(r"C:\Users\edgar\Videos\3.mp4")

pyautogui.press('enter')



#automate the wizard

tab.find_element(locator.tiktok.four).set_text("Funny", by='sendkey-after-click')

time.sleep(60)

tab.find_element(locator.tiktok.five).click(by='mouse-emulation')