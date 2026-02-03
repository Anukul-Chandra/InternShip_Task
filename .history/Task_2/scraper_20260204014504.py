# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import psycopg2


# ---------------- CONFIG ----------------
PHONE_URLS = [
    "https://www.gsmarena.com/samsung_galaxy_s23_ultra-12002.php",
    "https://www.gsmarena.com/samsung_galaxy_s22_ultra-11251.php",
    # ভবিষ্যতে এখানে Samsung এর যেকোনো phone add করলেই হবে
]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# ---------------- DATABASE CONNECTION ----------------
conn = psycopg2.connect(
    dbname="phones",
    user="anukulchandra",
    password="",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# ---------------- SCRAPE FUNCTION ----------------
def scrape_phone(url):
    response = requests.get(url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    model = soup.find("h1").text.strip()

    specs = soup.find_all("tr")
    data = {}

    for row in specs:
        th = row.find("th")
        td = row.find("td")
        if th and td:
            data[th.text.strip()] = td.text.strip()

    return {
        "model": model,
        "release_date": "2023",   # demo value
        "display": data.get("Display"),
        "battery": data.get("Battery"),
        "camera": data.get("Main Camera"),
        "ram": "12GB",
        "storage": "256GB",
        "price": 1199
    }

# ---------------- MAIN LOOP ----------------
for url in PHONE_URLS:
    phone = scrape_phone(url)

    print("Scraping:", phone["model"])

    cur.execute("""
        INSERT INTO samsung_phones
        (model, release_date, display, battery, camera, ram, storage, price)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (model) DO NOTHING
    """, (
        phone["model"],
        phone["release_date"],
        phone["display"],
        phone["battery"],
        phone["camera"],
        phone["ram"],
        phone["storage"],
        phone["price"]
    ))

conn.commit()
cur.close()
conn.close()

print("All phones inserted successfully")
