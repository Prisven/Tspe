from playwright.sync_api import sync_playwright
import requests
import time
import logging
import os

TOKEN = os.getenv("TOKEN")        # Token do bot no env var
CANAL_ID = os.getenv("CANAL_ID")  # Canal do Telegram no env var, ex: @promocaore
COD_AFILIADO = os.getenv("COD_AFILIADO")  # Código afiliado Shopee no env var

logging.basicConfig(level=logging.INFO)

def pegar_ofertas():
    ofertas = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_page()
        page.goto("https://shopee.com.br/ofertas")
        page.wait_for_selector('div[data-sqe="item"]', timeout=10000)

        cards = page.query_selector_all('div[data-sqe="item"]')
        for card in cards[:5]:
            try:
                titulo = card.query_selector('div._10Wbs-._5SSWfi.UjjMrh').inner_text()
                preco = card.query_selector('span._29R_un').inner_text()
                link = card.query_selector('a').get_attribute('href')
                link_completo = f"https://shopee.com.br{link}?af_click_lookback=7d&af_siteid={COD_AFILIADO}"
                ofertas.append({
                    "titulo": titulo,
                    "preco": preco,
                    "link": link_completo
                })
            except Exception as e:
                logging.error(f"Erro ao extrair dados do card: {e}")
        browser.close()
    return ofertas

def enviar_telegram(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CANAL_ID,
        "text": texto,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    try:
        r = requests.post(url, data=payload)
        if not r.ok:
            logging.error(f"Erro ao enviar mensagem: {r.text}")
    except Exception as e:
        logging.error(f"Erro Telegram: {e}")

def main():
    logging.info("Iniciando bot de promoções Shopee no Render...")
    while True:
        ofertas = pegar_ofertas()
        if not ofertas:
            logging.info("Nenhuma oferta encontrada no momento.")
        for oferta in ofertas:
            texto = (
                f"🛍 <b>{oferta['titulo']}</b>\n"
                f"💰 <b>{oferta['preco']}</b>\n"
                f"🔗 <a href='{oferta['link']}'>Comprar na Shopee</a>"
            )
            enviar_telegram(texto)
            time.sleep(2)
        logging.info("Esperando 10 minutos para nova busca.")
        time.sleep(600)

if __name__ == "__main__":
    main()
