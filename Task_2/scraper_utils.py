# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_samsung_phone(phone_slug):
    """
    phone_slug example:
    samsung_galaxy_s21
    samsung_galaxy_a54
    samsung_galaxy_m51
    """

    search_url = f"https://www.gsmarena.com/res.php3?sSearch={phone_slug}"
    res = requests.get(search_url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(res.text, "html.parser")

    phone_link = soup.select_one(".makers a")
    if not phone_link:
        return None

    phone_url = "https://www.gsmarena.com/" + phone_link["href"]

    phone_page = requests.get(phone_url, headers=HEADERS, timeout=10)
    phone_soup = BeautifulSoup(phone_page.text, "html.parser")

    model = phone_soup.find("h1").text.strip()

    specs = phone_soup.find_all("tr")
    data = {}

    for row in specs:
        th = row.find("th")
        td = row.find("td")
        if th and td:
            data[th.text.strip()] = td.text.strip()

    return {
        "model": model,
        "release_date": "Unknown",
        "display": data.get("Display"),
        "battery": data.get("Battery"),
        "camera": data.get("Main Camera"),
        "ram": "Unknown",
        "storage": "Unknown",
        "price": 0
    }
