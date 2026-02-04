# -*- coding: utf-8 -*-

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import re

from db_utils import fetch_phone_from_db, insert_phone_into_db
from scraper_utils import scrape_samsung_phone

app = FastAPI()

# Allow frontend (HTML file) to talk to API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Formatting ----------------
def generate_review(phone):
    return (
        f"{phone[0]} specifications:\n"
        f"- Release Year: {phone[1]}\n"
        f"- Display: {phone[2]}\n"
        f"- Battery: {phone[3]}\n"
        f"- Camera: {phone[4]}\n"
        f"- RAM: {phone[5]}\n"
        f"- Storage: {phone[6]}\n"
        f"- Price: ${phone[7]}"
    )

# ---------------- Phone name extraction ----------------
def extract_phone_names(question: str):
    q = question.lower()
    parts = re.split(r'and|,', q)

    phones = []
    for part in parts:
        if "samsung" in part:
            name = (
                part.replace("compare", "")
                .replace("between", "")
                .replace("vs", "")
                .strip()
            )
            phones.append(name)

    return phones

# ---------------- API ----------------
@app.post("/ask")
def ask(question: str):

    phone_queries = extract_phone_names(question)

    if not phone_queries:
        return {"answer": "Please clearly mention Samsung phone names."}

    results = []

    for phone_query in phone_queries:

        # 1️⃣ DB first
        data = fetch_phone_from_db(phone_query)

        if not data:
            # 2️⃣ Prepare search keyword for GSMArena
            search_keyword = (
                phone_query
                .replace("samsung", "")
                .replace("galaxy", "")
                .strip()
            )

            scraped = scrape_samsung_phone(search_keyword)

            if not scraped:
                return {
                    "answer": f"Sorry, data not found online for {phone_query}."
                }

            # 3️⃣ Insert scraped data
            insert_phone_into_db(scraped)

            # 4️⃣ Fetch again from DB
            data = fetch_phone_from_db(scraped["model"])

        results.append(data[0])

    # -------- Single phone --------
    if len(results) == 1:
        return {"answer": generate_review(results[0])}

    # -------- Comparison --------
    p1, p2 = results

    return {
        "answer": (
            f"{p1[0]} vs {p2[0]}:\n"
            f"- Display: {p1[2]} vs {p2[2]}\n"
            f"- Battery: {p1[3]} vs {p2[3]}\n"
            f"- Camera: {p1[4]} vs {p2[4]}\n"
            f"- Price: ${p1[7]} vs ${p2[7]}\n\n"
            f"Overall, {p1[0]} is more premium, "
            f"while {p2[0]} is more budget-friendly."
        )
    }
