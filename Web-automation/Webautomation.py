from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.google.com/search?q=Honeygain&oq=Honeygain&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCDYxMDNqMGoyqAIAsAIA&sourceid=chrome&ie=UTF-8")
    page.get_by_role("button", name="Alle akzeptieren").click()
    page.get_by_role("link", name="Home | Honeygain Honeygain").click()
    page.get_by_role("button", name="Accept selected").click()
    page.get_by_role("link", name="Login").click()
    page.get_by_placeholder("honeygain@example.com").click()
    page.get_by_placeholder("honeygain@example.com").fill("edgar.richter05@gmail.com")
    page.get_by_label("Password").click()
    page.get_by_label("Password").fill("honeygaintest")
    page.get_by_role("button", name="Continue with email").click()
    page.get_by_role("banner").get_by_role("button").nth(2).click()
    page.locator(".sc-bdnyFh > svg").first.click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
