# ingest coins

import os
import requests
from datetime import datetime
import psycopg2

def get_crypto_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"

    parametri = {
        "ids": "bitcoin,ethereum,solana",
        "vs_currencies": "usd",
        "include_market_cap": "true",
        "include_24hr_vol": "true"
    }

    raspuns = requests.get(url, params=parametri)
    date = raspuns.json()

    return date

def pregateste_randuri(date):
    randuri = []

    moment = datetime.now()

    for moneda, valori in date.items():
        rand = {
            "coin_id":     moneda,
            "price_usd":   valori["usd"],
            "market_cap":  valori["usd_market_cap"],
            "volume_24h":  valori["usd_24h_vol"],
            "fetched_at":  moment
        }
        randuri.append(rand)

    return randuri

def salveaza_in_db(randuri):
    conexiune = psycopg2.connect(
        host=os.getenv("PGHOST", "host.docker.internal"),
        port=int(os.getenv("PGPORT", "5432")),
        user=os.getenv("PGUSER", "postgres"),
        password=os.getenv("PGPASSWORD", ""),
        dbname=os.getenv("PGDATABASE", "postgres")
    )

    cursor = conexiune.cursor()

    for rand in randuri:
        cursor.execute("""
            INSERT INTO raw_coins
                (coin_id, price_usd, market_cap, volume_24h, fetched_at)
            VALUES
                (%s, %s, %s, %s, %s)
        """, (
            rand["coin_id"],
            rand["price_usd"],
            rand["market_cap"],
            rand["volume_24h"],
            rand["fetched_at"]
        ))

    conexiune.commit()
    cursor.close()
    conexiune.close()

    print(f"Salvate {len(randuri)} randuri in baza de date!")

rezultat = get_crypto_prices()
randuri = pregateste_randuri(rezultat)
salveaza_in_db(randuri)
