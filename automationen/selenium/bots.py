from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from dotenv import load_dotenv

# Lade die Umgebungsvariablen aus der .env-Datei
load_dotenv()

# Abrufen der Anmeldeinformationen aus Umgebungsvariablen
INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME')
INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD')

# Erstelle eine neue Instanz des Firefox-Browsers
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

# Öffne Instagram
driver.get("https://www.instagram.com")

try:
    # Warte, bis die Seite vollständig geladen ist und das Login-Feld sichtbar ist
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'username'))
    )
    
    # Handhabung von Cookie-Zustimmungen
    try:
        accept_cookies_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept All') or contains(text(), 'Alle akzeptieren')]"))
        )
        accept_cookies_button.click()
    except Exception as e:
        print("Kein Cookie-Zustimmungs-Popup gefunden.")

    # Finde und fülle das Benutzername-Feld
    username_field = driver.find_element(By.NAME, 'username')
    username_field.send_keys(INSTAGRAM_USERNAME)

    # Finde und fülle das Passwort-Feld
    password_field = driver.find_element(By.NAME, 'password')
    password_field.send_keys(INSTAGRAM_PASSWORD)

    # Sende das Formular ab
    password_field.send_keys(Keys.RETURN)

    # Warte, bis der nächste Schritt geladen ist, um sicherzustellen, dass die Anmeldung erfolgreich war
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="dialog"]'))
    )

    # Überprüfe, ob die Anmeldung erfolgreich war
    if "https://www.instagram.com/accounts/onetap/" in driver.current_url:
        print("Erfolgreich eingeloggt!")
    else:
        print("Login fehlgeschlagen.")

except Exception as e:
    print("Ein Fehler ist aufgetreten:", e)

finally:
    # Schließe den Browser
    driver.quit()
