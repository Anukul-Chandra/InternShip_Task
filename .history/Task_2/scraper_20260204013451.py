import requests
from bs4 import BeautifulSoup

url = "https://www.gsmarena.com/samsung_galaxy_s23_ultra-12002.php"

headers = {
    "User-Agent": "Mozilla/5.0"
}

res = requests.get(url, headers=headers, timeout=10)
soup = BeautifulSoup(res.text, "html.parser")

# --- Example extractions (structure may vary) ---
model = soup.find("h1").text.strip()

specs = soup.find_all("tr")

data = {}
for row in specs:
    th = row.find("th")
    td = row.find("td")
    if th and td:
        data[th.text.strip()] = td.text.strip()

print("Model:", model)
print("Battery:", data.get("Battery"))
print("Camera:", data.get("Main Camera"))
print("Display:", data.get("Display"))
