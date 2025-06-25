import asyncio
import os
from playwright.async_api import async_playwright
from telegram import Bot

# Paramètres depuis les variables d’environnement Railway
URL_TLS = os.getenv("URL_TLS", "https://fr.tlscontact.com/appointment/ma/maRAK2fr/20067244")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN)

async def main():
    print("🔍 Lancement de la vérification TLScontact...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
        page = await browser.new_page()
        await page.goto(URL_TLS)

        try:
            await page.wait_for_selector(".tls-appointment-content", timeout=15000)
            slots = await page.query_selector_all(".tls-appointment-time-picker .tls-appointment-month-slot")

            if slots:
                print("✅ Créneau détecté !")
                await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"✅ Créneau disponible sur TLScontact !\n{URL_TLS}")
            else:
                print("❌ Aucun créneau trouvé.")
                await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="❌ Aucun créneau TLScontact disponible.")
        except Exception as e:
            print("⚠️ Erreur pendant la vérification :", e)
            await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"⚠️ Erreur lors de la vérification TLScontact : {e}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
