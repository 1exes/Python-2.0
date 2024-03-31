import time

import pyautogui

from clicknium import clicknium as cc, ui, locator



tab = cc.chrome.open("https://www.tiktok.com/upload?lang=en") #opens the web browser on tiktok

time.sleep(5)

tab.find_element(locator.tiktok.one).click(by='mouse-emulation') #starts the mouse emulation and locates the upload button

#starts the upload

time.sleep(5)

pyautogui.write(r"P:/ath/to/your/file/here.mp4")

pyautogui.press('enter')



#automate the wizard

tab.find_element(locator.tiktok.four).set_text("Funny", by='sendkey-after-click')

time.sleep(10)

tab.find_element(locator.tiktok.five).click(by='mouse-emulation')