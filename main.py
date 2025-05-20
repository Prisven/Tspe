import requests
import time
import logging

# DADOS FIXOS
TOKEN = "7526311480:AAGubXHX4sGJDcvMFBvWYu9JSlJGa3DStng"
CANAL_ID = "@promocaore"
COD_AFILIADO = "abc123"  # Substitua pelo seu código real, se tiver

logging.basicConfig(level=logging.INFO)

# Simulação de produtos da Shopee
def buscar_ofertas():
    ofertas = [
        {
            "titulo": "Fone Bluetooth Xiaomi",
            "preco": 59.90,
            "id_produto": "1234567890"
        },
        {
            "titulo": "Tênis Esportivo Masculino",
            "preco": 129.99,
            "id_produto": "2345678901"
        },
        {
            "titulo": "Relógio Smartwatch D20",
            "preco": 34.90,
            "id_produto": "3456789012"
        }
    ]

    for oferta in ofertas:
        oferta["link"] = f"https://shope.ee/{oferta['id_produto']}?af_click_lookback=7d&af_siteid={COD_AFILIADO}"
    return ofertas

# Envia a mensagem para o Telegram
def enviar_telegram(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CANAL_ID,
        "text": texto,
        "parse_mode": "HTML"
    }
    try:
        r = requests.post(url, data=payload)
        if not r.ok:
            logging.error(f"Erro ao enviar mensagem: {r.text}")
    except Exception as e:
        logging.error(f"Erro Telegram: {e}")

# LOOP PRINCIPAL
def main():
    logging.info("Iniciando bot de promoções Shopee...")
    while True:
        ofertas = buscar_ofertas()
        for oferta in ofertas:
            texto = (
                f"🛍 <b>{oferta['titulo']}</b>\n"
                f"💰 <b>R${oferta['preco']:.2f}</b>\n"
                f"🔗 <a href='{oferta['link']}'>Comprar na Shopee</a>"
            )
            enviar_telegram(texto)
            time.sleep(2)  # Evita flood
        logging.info("Aguardando 5 minutos para nova rodada.")
        time.sleep(300)  # Espera 5 minutos

if __name__ == "__main__":
    main()
