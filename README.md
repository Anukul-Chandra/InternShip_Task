## 🚀 InternShip Task Assignment Submission

This repository contains the solutions for the InternShip Task Assignment Submission given by **Genuine Technology & Reserch LTD** , consisting of two independent tasks: a **Stock Trading Bot** and a **Samsung Phone Advisor Agent**.

---

## 📋 Table of Contents
1. Video Demonstration
2. Task 1: Stock Trading Strategy Bot
3. Task 2: Samsung Phone Advisor (AI Agent)
4. Installation & Setup
5. Project Structure

---

## 🎥 Video Demonstration

A complete walkthrough of both projects running successfully can be viewed here:

👉 **[INSERT YOUR GOOGLE DRIVE VIDEO LINK HERE]**

> Please ensure the link permission is set to **Anyone with the link can view**

---

## 📈 Task 1: Stock Trading Strategy Bot

### Description
This module implements an automated trading strategy based on **Technical Analysis** using **Simple Moving Averages (SMA)**.  
It simulates trading decisions using historical stock market data.

### Key Logic
- **Indicators Used:** 50-day SMA & 200-day SMA  
- **Golden Cross (Buy Signal):** SMA50 crosses above SMA200  
- **Death Cross (Sell Signal):** SMA50 crosses below SMA200  
- **Initial Capital:** $5000  
- **Output:** Total profit or loss

### Output Preview
![Trading Bot Graph](https://github.com/user-attachments/assets/a3310be3-5636-417a-8090-eccc93f9eb3c)

---

## 📱 Task 2: Samsung Phone Advisor (AI Agent)

### Description
A web-based intelligent AI agent that provides real-time specifications and comparisons for Samsung smartphones.  
It uses a hybrid approach combining **SQLite database caching** with **real-time web scraping**.

**Live Demo:** https://samsung-phone-adviser-1.onrender.com/

### Key Features
- Smart search for phone specs  
- Comparison between two Samsung models  
- Local DB first, web scrape if missing  
- Responsive UI using Bootstrap & JavaScript  

### Output Preview

**Comparison Result**
![Comparison Result](![photo_2026-02-05 02 24 33](https://github.com/user-attachments/assets/bf5e9849-0648-4d30-98ca-38f20a7bb906)
)

**Single Phone Result**
![Single Result](![photo_2026-02-05 02 24 58](https://github.com/user-attachments/assets/8a9f71ff-bd50-4fe0-807b-cd423b1f29fb)
)

---

## ⚙️ Installation & Setup

### Clone Repository
```bash
git clone https://github.com/Anukul-Chandra/Samsung-Phone-Adviser.git
cd Samsung-Phone-Adviser
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Task 1
```bash
jupyter notebook "Task 1 Trading Bot.ipynb"
```

### Run Task 2
```bash
cd Task_2
uvicorn main:app --reload
```

App will run at: http://127.0.0.1:8000

---

## 📂 Project Structure

```
├── Task 1 Trading Bot.ipynb
├── Task_2/
│   ├── main.py
│   ├── db_utils.py
│   ├── scraper_utils.py
│   ├── index.html
│   └── phones.db
├── requirements.txt
└── README.md
```

---

End of Documentation
