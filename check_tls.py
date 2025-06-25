import os
import asyncio
from playwright.async_api import async_playwright
import aiohttp

# CONFIGURATION via variables d'environnement
URL_TLS = os.getenv("URL_TLS", "https://fr.tlscontact.com/appointment/ma/maRAK2fr/20067244")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 1200))  # en secondes

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

async def send_telegram_message(text: str):
    async with aiohttp.ClientSession() as session:
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
        async with session.post(TELEGRAM_API_URL, data=payload) as resp:
            if resp.status != 200:
                print(f"Erreur Telegram: statut {resp.status}")
            else:
                print("Message Telegram envoyé.")

async def check_tls(page):
    print("🕵️ Vérification de la disponibilité...")
    await page.goto(URL_TLS, wait_until="domcontentloaded")

    try:
        # Attente de la présence de l'élément principal des créneaux
        await page.wait_for_selector(".tls-appointment-content", timeout=15000)

        # Recherche des créneaux
        slots = await page.query_selector_all(".tls-appointment-time-picker .tls-appointment-month-slot")

        if len(slots) > 0:
            print("✅ Créneau potentiellement dispo")
            await send_telegram_message(f"✅ Créneau TLScontact trouvé ! Vérifie ici : {URL_TLS}")
        else:
            print("❌ Aucun créneau visible")
            await send_telegram_message(f"❌ Aucun créneau TLScontact disponible pour le moment.")
    except Exception as e:
        print(f"⚠️ Erreur lors de la vérification : {e}")
        await send_telegram_message(f"⚠️ Erreur lors de la vérification : {e}")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
        page = await browser.new_page()

        while True:
            await check_tls(page)
            await asyncio.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())
