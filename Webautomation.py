from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.google.com/search?q=instagram&oq=instagram&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCDM3MDZqMGoyqAIAsAIA&sourceid=chrome&ie=UTF-8")
    page.get_by_role("button", name="Alle akzeptieren").click()
    page.get_by_role("link", name="Instagram Instagram https://").click()
    page.get_by_role("button", name="Alle Cookies erlauben").click()
    page.locator("div").filter(has_text=re.compile(r"^Passwort$")).nth(1).click()
    page.get_by_label("Passwort").fill("d")
    page.get_by_label("Telefonnummer, Benutzername").fill("d")
    page.get_by_label("Telefonnummer, Benutzername").click()
    page.locator("div").filter(has_text=re.compile(r"^Anmelden$")).first.click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
