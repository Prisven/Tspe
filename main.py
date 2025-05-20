import requests
import time
import os
import logging

TOKEN = os.getenv("7526311480:AAGubXHX4sGJDcvMFBvWYu9JSlJGa3DStng")
CANAL_ID = os.getenv("@promocaore")
API_OFERTAS = "https://dummyjson.com/products"  # API de teste

logging.basicConfig(level=logging.INFO)

def buscar_ofertas():
    try:
        resposta = requests.get(API_OFERTAS)
        if resposta.status_code == 200:
            data = resposta.json()
            produtos = data.get("products", [])[:5]
            ofertas = []
            for p in produtos:
                ofertas.append({
                    "titulo": p["title"],
                    "preco": p["price"],
                    "link": f"https://dummyjson.com/products/{p['id']}"
                })
            return ofertas
        else:
            logging.error(f"Erro na API: {resposta.status_code}")
            return []
    except Exception as e:
        logging.error(f"Erro ao buscar ofertas: {e}")
        return []

def enviar_telegram(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    dados = {
        "chat_id": CANAL_ID,
        "text": texto,
        "parse_mode": "HTML"
    }
    try:
        resposta = requests.post(url, data=dados)
        if not resposta.ok:
            logging.error(f"Erro ao enviar mensagem: {resposta.text}")
    except Exception as e:
        logging.error(f"Erro na requisição Telegram: {e}")

def main():
    logging.info("Bot iniciado.")
    while True:
        ofertas = buscar_ofertas()
        if ofertas:
            for oferta in ofertas:
                texto = f"🛍 <b>{oferta['titulo']}</b>\n💰 <b>R${oferta['preco']}</b>\n🔗 {oferta['link']}"
                enviar_telegram(texto)
                time.sleep(3)
        else:
            logging.info("Nenhuma oferta nova.")
        time.sleep(300)

if __name__ == "__main__":
    main()
