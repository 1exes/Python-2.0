from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.google.com/search?q=epicgames&oq=epicgames&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCDI3NDFqMGoyqAIAsAIA&sourceid=chrome&ie=UTF-8")
    page.get_by_role("button", name="Alle akzeptieren").click()
    page.get_by_role("link", name="Startseite - Epic Games Epic").click()
    page.get_by_label("Anmelden").click()
    page.frame_locator("iframe[title=\"Widget\\, das eine Cloudflare-Sicherheitsherausforderung enthält\"]").get_by_label("Bestätigen Sie, dass Sie ein").check()
    page.frame_locator("iframe[title=\"Widget\\, das eine Cloudflare-Sicherheitsherausforderung enthält\"]").get_by_label("Bestätigen Sie, dass Sie ein").check()
    page.goto("https://www.epicgames.com/login?state=%2Fsite%2Fde%2Fhome&lang=de")
    page.goto("https://www.epicgames.com/login?state=%2Fsite%2Fde%2Fhome&lang=de&__cf_chl_rt_tk=vmyKIbahZmjdTXmniR2Ch97hs8pwps6lT3IrqW4hg0k-1709722116-0.0.1.1-1663")
    page.goto("https://www.epicgames.com/login?state=%2Fsite%2Fde%2Fhome&lang=de")

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
