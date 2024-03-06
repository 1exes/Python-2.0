from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://dashboard.honeygain.com/")
    page.goto("https://dashboard.honeygain.com/login")
    page.get_by_placeholder("honeygain@example.com").click()
    page.get_by_placeholder("honeygain@example.com").fill("edgar.richter05@gmail.com")
    page.get_by_label("Password").click()
    page.get_by_label("Password").fill("testhoney")
    page.get_by_label("Password").press("Enter")
    page.get_by_role("main").get_by_role("button").first.click()
    page.get_by_label("Password").click()
    page.get_by_label("Password").fill("testhoneygain")
    page.get_by_role("button", name="Continue with email").click()
    page.get_by_role("button", name="Accept all").click()
    page.get_by_role("main").locator("img").first.click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
