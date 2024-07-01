from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import random

# Deine Instagram-Anmeldedaten
username = "WatchWildeLife"
password = "test#123"

# Proxy-Einstellungen
proxy = "213.232.116.98:30010"
proxy_username = "edgar_richter05_gmail_c"
proxy_password = "f60636c9d1"

# Chrome WebDriver Pfad
webdriver_path = "C:\\Users\\edgar\\Documents\\GitHub\\Python-2.0\\automationen\\chromedriver.exe"

# Chrome-Optionen mit Proxy
chrome_options = Options()
chrome_options.add_argument(f'--proxy-server=http://{proxy}')
# ChromeOptions hat keine direkte Unterstützung für Proxy-Authentifizierung.
# Wir müssen das WebDriver-Objekt manuell erstellen und die Authentifizierung separat behandeln.

# WebDriver initialisieren
driver = webdriver.Chrome(executable_path=webdriver_path, options=chrome_options)

def random_delay(min_seconds=5, max_seconds=10):
    """Fügt eine zufällige Verzögerung zwischen min_seconds und max_seconds ein"""
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)

def login(username, password):
    driver.get("https://www.instagram.com/accounts/login/")
    random_delay()

    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")

    username_input.send_keys(username)
    password_input.send_keys(password)
    random_delay()

    password_input.send_keys(Keys.RETURN)
    random_delay(5, 10)  # Längere Verzögerung für das Laden der Seite

def follow_user(target_username):
    driver.get(f"https://www.instagram.com/{target_username}/")
    random_delay()

    follow_button = driver.find_element(By.XPATH, "//button[text()='Follow']")
    follow_button.click()
    random_delay()

def like_user_posts(target_username, amount=1):
    driver.get(f"https://www.instagram.com/{target_username}/")
    random_delay()

    posts = driver.find_elements(By.XPATH, "//a[contains(@href, '/p/')]")
    for post in posts[:amount]:
        post.click()
        random_delay()

        like_button = driver.find_element(By.XPATH, "//span[@aria-label='Like']")
        like_button.click()
        random_delay()

        close_button = driver.find_element(By.XPATH, "//button[contains(@class, 'wpO6b')]")
        close_button.click()
        random_delay()

def comment_user_post(target_username, comment):
    driver.get(f"https://www.instagram.com/{target_username}/")
    random_delay()

    first_post = driver.find_element(By.XPATH, "//a[contains(@href, '/p/')]")
    first_post.click()
    random_delay()

    comment_area = driver.find_element(By.XPATH, "//textarea[@aria-label='Add a comment…']")
    comment_area.click()
    comment_area.send_keys(comment)
    random_delay()

    comment_area.send_keys(Keys.RETURN)
    random_delay()

def main():
    try:
        login(username, password)
        follow_user("target_username")
        like_user_posts("target_username", amount=1)
        comment_user_post("target_username", "Nice post!")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
