from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chrome.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.google.com/search?q=tiktok&oq=tiktok&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCDQxNDhqMGoyqAIAsAIA&sourceid=chrome&ie=UTF-8")
    page.get_by_role("button", name="Alle akzeptieren").click()
    page.get_by_role("link", name="Make Your Day - TikTok TikTok").click()
    page.get_by_role("button", name="Alle akzeptieren").click()
    page.get_by_role("link", name="Telefonnr./E-Mail/").click()
    page.get_by_role("link", name="Mit E-Mail-Adresse oder").click()
    page.get_by_placeholder("E-Mail-Adresse oder").click()
    page.get_by_placeholder("Passwort").click()
    page.get_by_placeholder("E-Mail-Adresse oder").click()
    page.get_by_placeholder("E-Mail-Adresse oder").fill("fgfdgd")
    page.get_by_placeholder("Passwort").click()
    page.get_by_placeholder("Passwort").fill("fdgdfgfdg")
    page.get_by_label("Anmelden").get_by_role("button", name="Anmelden").click()
    page.locator("a").filter(has_text="Aktualisieren").click()
    page.locator("#captcha-verify-image").click()
    page.locator("#captcha-verify-image").click()
    page.locator("#captcha-verify-image").click()
    page.get_by_text("1", exact=True).click()
    page.locator("#captcha-verify-image").click()
    page.locator("#captcha-verify-image").click()
    page.get_by_label("Close").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
