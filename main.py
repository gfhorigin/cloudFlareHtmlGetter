import asyncio
from pathlib import  Path
from patchright.async_api import async_playwright, Browser, BrowserContext, Page


async def main() -> None:
    async with async_playwright() as playwright:
        async with await playwright.chromium.launch(
            channel='chrome',
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled'
            ]
        ) as browser:  # type: Browser
            context: BrowserContext = await browser.new_context()
            url = 'https://dexscreener.com/?rankBy=trendingScoreH6&order=desc&chainIds=solana&dexIds=raydium,meteora&minLiq=1000&minMarketCap=3000000&maxAge=24&min24HVol=10000000'

            page: Page = await context.new_page()

            await page.goto(url)

            await page.wait_for_event("load",timeout=120000)

            ht = await page.content()
            output_dir = Path("html_output")  # Папка для сохранения файлов
            output_dir.mkdir(exist_ok=True)  # Создаем папку если ее нет
            filepath = f"{output_dir}/dexscreener_page.html"

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(ht)

            await page.close()
            await browser.close()
            await asyncio.Future()

if __name__ == '__main__':

    page = asyncio.run(main())