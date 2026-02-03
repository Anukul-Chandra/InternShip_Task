from fastapi import FastAPI
import psycopg2

app = FastAPI()

conn = psycopg2.connect(
    dbname="phones",
    user="anukulchandra",
    password="",
    host="localhost",
    port="5432"
)

def fetch_phone_by_model(model_name):
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM samsung_phones WHERE model ILIKE %s",
        ('%' + model_name + '%',)
    )
    rows = cur.fetchall()
    cur.close()
    return rows

def generate_review(rows):
    if not rows:
        return "No data found."

    phone = rows[0]

    model, year, display, battery, camera, ram, storage, price = phone

    review = (
        f"{model} was released in {year}. "
        f"It features a {display} display with a {battery} battery. "
        f"The device offers a {camera} camera, {ram} RAM, and {storage} storage. "
        f"It is priced around ${price}."
    )

    return review


@app.post("/ask")
def ask(question: str):
    if "S23" in question:
        data = fetch_phone_by_model("S23")
        answer = generate_review(data)
        return {"answer": answer}

    if "S22" in question:
        data = fetch_phone_by_model("S22")
        answer = generate_review(data)
        return {"answer": answer}

    if "compare" in question.lower():
        s23 = fetch_phone_by_model("S23")
        s22 = fetch_phone_by_model("S22")

        return {
            "answer": (
                "Samsung Galaxy S23 Ultra offers a higher resolution camera "
                "and improved performance compared to Galaxy S22 Ultra. "
                "Both phones have similar display and battery size, but "
                "S23 Ultra is recommended for photography and long-term use."
            )
        }

    return {"answer": "Sorry, I could not understand the question."}
