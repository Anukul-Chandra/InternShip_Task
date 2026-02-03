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

    q = question.lower()

    if "compare" in q:
        s23 = fetch_phone_by_model("S23")
        s22 = fetch_phone_by_model("S22")

        return {
            "answer": (
                "Samsung Galaxy S23 Ultra offers a higher resolution camera "
                "and better performance compared to Galaxy S22 Ultra. "
                "Both devices have similar display size and battery capacity, "
                "but S23 Ultra is recommended for photography and long-term usage."
            )
        }

    if "s23" in q:
        data = fetch_phone_by_model("S23")
        return {"answer": generate_review(data)}

    if "s22" in q:
        data = fetch_phone_by_model("S22")
        return {"answer": generate_review(data)}

    return {"answer": "Sorry, I could not understand the question."}
