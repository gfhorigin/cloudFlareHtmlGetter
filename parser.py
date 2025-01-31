from pathlib import  Path
from bs4 import BeautifulSoup
from patchright.sync_api import sync_playwright, Browser, BrowserContext, Page

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(channel='chrome', headless=False, args=[
                '--disable-blink-features=AutomationControlled'
            ])
    context = browser.new_context()

    url = 'https://dexscreener.com/?rankBy=trendingScoreH6&order=desc&chainIds=solana&dexIds=raydium,meteora&minLiq=1000&minMarketCap=3000000&maxAge=24&min24HVol=10000000'
    page = context.new_page()
    page.goto(url)

    page.wait_for_event('load')

    soup = BeautifulSoup(page.content(), 'html.parser')
    output_dir = Path("html_output")  # Папка для сохранения файлов
    output_dir.mkdir(exist_ok=True)  # Создаем папку если ее нет
    filepath = f"{output_dir}/dexscreener_page.html"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(soup.prettify())

    page.close()
    browser.close()

