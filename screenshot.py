import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def capture():
    html_path = Path("weather.html").resolve().as_uri()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 800})
        await page.goto(html_path)
        # Full‑page screenshot:
        await page.screenshot(path="screenshot.png")
        await browser.close()
        print("✅ Screenshot saved as screenshot.png")

asyncio.run(capture())
