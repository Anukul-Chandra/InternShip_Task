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
def fetch_samsung_by_question(question):
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM samsung_phones
        WHERE LOWER(model) LIKE %s
    """, ('%' + question.lower() + '%',))
    rows = cur.fetchall()
    cur.close()
    return rows

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

# --------- FASTAPI ENDPOINT ---------
@app.post("/ask")
def ask(question: str):
    q = question.lower()

    # Comparison intent
    if "compare" in q:
        return {
            "answer": (
                "The system supports comparison between any Samsung phones "
                "available in the database. Please ensure both models exist "
                "in the data source."
            )
        }

    # Generic Samsung phone query
    if "samsung" in q:
        data = fetch_samsung_by_question(q)
        answer = generate_review(data)
        return {"answer": answer}

    return {"answer": "Please ask about a Samsung smartphone."}
