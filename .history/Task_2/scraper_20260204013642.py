import requests
from bs4 import BeautifulSoup
import psycopg2

# ---------- STEP 1: Scrape data ----------
url = "https://www.gsmarena.com/samsung_galaxy_s23_ultra-12002.php"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

model = soup.find("h1").text.strip()

specs = soup.find_all("tr")
data = {}

for row in specs:
    th = row.find("th")
    td = row.find("td")
    if th and td:
        data[th.text.strip()] = td.text.strip()

print("Scraped model:", model)

# ---------- STEP 2: Insert into PostgreSQL ----------
conn = psycopg2.connect(
    dbname="phones",
    user="anukulchandra",
    password="",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

cur.execute("""
INSERT INTO samsung_phones
(model, release_date, display, battery, camera, ram, storage, price)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
ON CONFLICT (model) DO NOTHING
""", (
    model,
    "2023",
    data.get("Display"),
    data.get("Battery"),
    data.get("Main Camera"),
    "12GB",
    "256GB",
    1199
))

conn.commit()
cur.close()
conn.close()

print("Inserted into PostgreSQL")
