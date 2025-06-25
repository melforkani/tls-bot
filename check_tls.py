from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import telegram
import asyncio
import os

# CONFIGURATION
url_tls = os.getenv("https://fr.tlscontact.com/appointment/ma/maRAK2fr/20067244")
telegram_token = os.getenv("7702671519:AAG7b9_qsnXZAFH8-rYs3o9qeXa78qzaBvY")
telegram_chat_id = os.getenv("7554340275")
check_interval = int(os.getenv("CHECK_INTERVAL", 1200))  # défaut : 20 min

bot = telegram.Bot(token=telegram_token)

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)

def check_tls():
    print("🕵️ Vérification en cours...")
    driver.get(url_tls)

    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tls-appointment-content"))
        )

        time_slots = driver.find_elements(By.CSS_SELECTOR, ".tls-appointment-time-picker .tls-appointment-month-slot")

        if len(time_slots) > 0:
            print("✅ Créneau potentiellement dispo")
            asyncio.run(bot.send_message(chat_id=telegram_chat_id, text="✅ Créneau TLScontact trouvé ! Vérifie ici : " + url_tls))
        else:
            print("❌ Aucun créneau visible")
    except Exception as e:
        print("Erreur lors de la vérification :", e)

while True:
    check_tls()
    time.sleep(check_interval)
