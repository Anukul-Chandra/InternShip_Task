from fastapi import FastAPI
from db_utils import fetch_phone_from_db, insert_phone_into_db
from scraper_utils import scrape_samsung_phone

app = FastAPI()

def generate_review(phone):
    return (
        f"{phone[0]} specifications:\n"
        f"- Display: {phone[2]}\n"
        f"- Battery: {phone[3]}\n"
        f"- Camera: {phone[4]}\n"
        f"- RAM: {phone[5]}\n"
        f"- Storage: {phone[6]}\n"
        f"- Price: ${phone[7]}"
    )

@app.post("/ask")
def ask(question: str):
    q = question.lower()

    if "samsung" not in q:
        return {"answer": "Please ask about a Samsung phone."}

    # Create slug for search
    phone_slug = q.replace("samsung", "").replace("galaxy", "").strip().replace(" ", "_")

    # 1️⃣ DB check
    data = fetch_phone_from_db(phone_slug)
    if data:
        return {"answer": generate_review(data[0])}

    # 2️⃣ Scrape if not found
    scraped = scrape_samsung_phone(phone_slug)
    if not scraped:
        return {"answer": "Sorry, phone data not found online."}

    # 3️⃣ Insert into DB
    insert_phone_into_db(scraped)

    # 4️⃣ Fetch again & respond
    data = fetch_phone_from_db(scraped["model"])
    return {"answer": generate_review(data[0])}
