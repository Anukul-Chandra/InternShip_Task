

import requests
from bs4 import BeautifulSoup
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def scrape_wikipedia(model_name: str):
    print(f"DEBUG: Starting scrape for {model_name}") 
    clean_name = model_name.replace(" ", "_").title()
    
    if "Samsung" not in clean_name:
        clean_name = "Samsung_" + clean_name
    if "Galaxy" not in clean_name:
        parts = clean_name.split("_")
        if len(parts) > 1 and parts[0] == "Samsung":
            parts.insert(1, "Galaxy")
            clean_name = "_".join(parts)

    url = f"https://en.wikipedia.org/wiki/{clean_name}"
    print(f"🔎 Checking Wikipedia URL: {url}")

    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code != 200:
            print(f"❌ Wiki page failed. Status: {res.status_code}")
            return None

        soup = BeautifulSoup(res.text, "html.parser")
        infobox = soup.find("table", {"class": "infobox"})
        
        
        if not infobox:
            print("❌ Infobox table not found on Wiki page.")
            return None

        data = {}
        for row in infobox.find_all("tr"):
            th = row.find("th")
            td = row.find("td")
            if th and td:
                key = th.text.strip().lower()
                val = td.text.strip()
                val = re.sub(r'\[.*?\]', '', val)
                data[key] = val

        print("✅ Data scraped successfully!")
        return {
            "model": clean_name.replace("_", " "),
            "release_year": "2023",
            "release_date": data.get("first released", "Unknown"),
            "display": data.get("display", "Unknown"),
            "battery": data.get("battery", "Unknown"),
            "camera": data.get("rear camera", "Unknown"),
            "ram": data.get("memory", "Unknown"),
            "storage": data.get("storage", "Unknown"),
            "price": 0
        }

    except Exception as e:
        print(f"⚠️ Scraping crash: {e}")
        return None

def get_backup_data(model_name):
    print(f"DEBUG: Checking backup data for {model_name}")
    m = model_name.lower()
     
    if "s22" in m:
        print("✅ Found S22 in backup!")
        return {
            "model": "Samsung Galaxy S22 (Backup)",
            "release_year": "2022",
            "release_date": "February 2022",
            "display": "6.1 inch Dynamic AMOLED 2X",
            "battery": "3700 mAh",
            "camera": "50MP Wide",
            "ram": "8 GB",
            "storage": "128/256 GB",
            "price": 699
        }
    print("❌ No backup data found.")
    return None

def scrape_phone(model_name: str):
    data = scrape_wikipedia(model_name)
    if not data:
        print("⚠️ Wiki failed, switching to BACKUP...")
        data = get_backup_data(model_name)
    return data