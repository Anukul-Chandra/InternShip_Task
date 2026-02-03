from fastapi import FastAPI
import psycopg2

app = FastAPI()

# --------- DATABASE CONNECTION ---------
conn = psycopg2.connect(
    dbname="phones",
    user="anukulchandra",
    password="",
    host="localhost",
    port="5432"
)

# --------- AGENT 1: DATA EXTRACTOR ---------
def fetch_samsung_by_keyword(keyword):
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM samsung_phones
        WHERE LOWER(model) LIKE %s
    """, ('%' + keyword.lower() + '%',))
    rows = cur.fetchall()
    cur.close()
    return rows

def compare_phones(phone1, phone2):
    if not phone1 or not phone2:
        return "One or both Samsung phones are not available in the database."

    p1 = phone1[0]
    p2 = phone2[0]

    return (
        f"{p1[0]} and {p2[0]} comparison:\n"
        f"- Camera: {p1[4]} vs {p2[4]}\n"
        f"- Battery: {p1[3]} vs {p2[3]}\n"
        f"- Display: {p1[2]} vs {p2[2]}\n"
        f"- Price: ${p1[7]} vs ${p2[7]}\n\n"
        f"Overall, {p1[0]} offers higher-end features, "
        f"while {p2[0]} is a more budget-friendly option."
    )


# --------- AGENT 2: REVIEW GENERATOR ---------
def generate_review(rows):
    if not rows:
        return "No Samsung phone data found in the database."

    model, year, display, battery, camera, ram, storage, price = rows[0]

    return (
        f"{model} was released in {year}. "
        f"It features a {display} display, a {battery} battery, "
        f"{camera} camera setup, {ram} RAM, and {storage} storage. "
        f"The price is approximately ${price}."
    )

@app.post("/ask")
def ask(question: str):
    q = question.lower()

    # -------- COMPARISON --------
    if "compare" in q:
        words = q.replace("compare", "").replace("between", "").split("and")

        if len(words) >= 2:
            phone1_key = words[0].strip()
            phone2_key = words[1].strip()

            phone1 = fetch_samsung_by_keyword(phone1_key)
            phone2 = fetch_samsung_by_keyword(phone2_key)

            return {
                "answer": compare_phones(phone1, phone2)
            }

        return {"answer": "Please specify two Samsung phones to compare."}

    # -------- SINGLE PHONE QUERY --------
    if "samsung" in q:
        data = fetch_samsung_by_keyword(q)
        return {"answer": generate_review(data)}

    return {"answer": "Please ask about Samsung smartphones."}
