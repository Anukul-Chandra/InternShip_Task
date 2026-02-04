
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db_utils import fetch_phone_from_db, insert_phone_into_db
from scraper_utils import scrape_phone

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# this function checks the database if the phone exist then show if not then it scrapping from the website 
def get_phone_data(model_name):
    clean_name = model_name.strip()
    print(f"🔍 Processing: {clean_name}")
    
    #  database check 
    db_data = fetch_phone_from_db(clean_name)
    if db_data:
        print(f"✅ Found in DB: {clean_name}")
        row = db_data[0]
        return {
            "model": row[0], "release_year": row[1], "release_date": row[2],
            "display": row[3], "battery": row[4], "camera": row[5],
            "ram": row[6], "storage": row[7], "price": row[8]
        }
    
    # scarpping
    print(f"🌍 Scraping web for: {clean_name}")
    scraped_data = scrape_phone(clean_name)
    
    if scraped_data:
        insert_phone_into_db(scraped_data)
        return scraped_data
    
    return None

@app.post("/ask")
def ask(question: str):
    question = question.lower()
    
    # Comparison Mode
    if "vs" in question:
        parts = question.split("vs")
        phone1_name = parts[0].strip()
        phone2_name = parts[1].strip()
        
        data1 = get_phone_data(phone1_name)
        data2 = get_phone_data(phone2_name)
        
        return {
            "mode": "comparison",
            "phone1": data1 or {"model": "Not Found"},
            "phone2": data2 or {"model": "Not Found"}
        }

    # Single Mode
    else:
        data = get_phone_data(question)
        if data:
            return {"mode": "single", "data": data}
        else:
            return {"mode": "not_found"}

@app.get("/")
def home():
    return {"message": "Smart Phone Advisor Running!"}