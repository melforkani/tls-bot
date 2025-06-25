import asyncio
from playwright.async_api import async_playwright
import telegram
import os

url_tls = os.getenv("URL_TLS")
telegram_token = os.getenv("TELEGRAM_TOKEN")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

bot = telegram.Bot(token=telegram_token)

async def check_tls():
    print("🕵️ Vérification en cours…")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url_tls)
        content = await page.content()
        if "Désolé, il n'y a pas de rendez-vous disponible" in content:
            msg = "❌ Aucun créneau disponible pour le moment."
            print(msg)
            await bot.send_message(chat_id=telegram_chat_id, text=msg)
        else:
            msg = f"✅ Créneau TLScontact trouvé ! {url_tls}"
            print(msg)
            await bot.send_message(chat_id=telegram_chat_id, text=msg)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(check_tls())
