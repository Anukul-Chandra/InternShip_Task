# -*- coding: utf-8 -*-

from fastapi import FastAPI
import re

from db_utils import fetch_phone_from_db, insert_phone_into_db
from scraper_utils import scrape_samsung_phone

app = FastAPI()


# ---------------- Simple text formatter ----------------
# This function just turns raw DB data into a readable response
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


# ---------------- Phone name parsing ----------------
# This tries to pull Samsung phone names from the user question.
# It works for both single phone queries and comparison queries.
def extract_phone_names(question: str):
    q = question.lower()

    # If the user is comparing, phones are usually separated by "and" or commas
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


# ---------------- Main API endpoint ----------------
@app.post("/ask")
def ask(question: str):

    # Step 1: Try to figure out which Samsung phones the user is talking about
    phone_queries = extract_phone_names(question)

    if not phone_queries:
        return {"answer": "Please clearly mention Samsung phone names."}

    results = []

    for phone_query in phone_queries:

        # Step 2: First check if the phone already exists in our database
        data = fetch_phone_from_db(phone_query)

        if not data:
            # Step 3: If not found in DB, try to fetch it from a phone website
            slug = (
                phone_query
                .replace("samsung", "")
                .replace("galaxy", "")
                .strip()
                .replace(" ", "_")
            )

            scraped = scrape_samsung_phone(slug)

            # If scraping also fails, we stop here
            if not scraped:
                return {
                    "answer": f"Sorry, data not found online for {phone_query}."
                }

            # Step 4: Save the newly scraped phone into the database
            insert_phone_into_db(scraped)

            # Step 5: Fetch again from DB so everything comes from one source
            data = fetch_phone_from_db(scraped["model"])

        results.append(data[0])

    # ---------------- Single phone request ----------------
    if len(results) == 1:
        return {"answer": generate_review(results[0])}

    # ---------------- Phone comparison ----------------
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
