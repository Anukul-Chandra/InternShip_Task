from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import io
import base64
import math

# Server e GUI chara plot korar jonno
matplotlib.use('Agg')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- INPUT MODEL ---
class TradeRequest(BaseModel):
    symbol: str
    start_date: str
    end_date: str
    budget: float

# --- TRADING BOT LOGIC (Modified for Web) ---
class TradingBot:
    def __init__(self, symbol, start_date, end_date, budget):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.budget = budget
        self.balance = budget
        self.shares = 0
        self.position_open = False
        self.trade_log = []
        self.data = None

    def run(self):
        # 1. Download
        data = yf.download(self.symbol, start=self.start_date, end=self.end_date)
        if data.empty:
            return None
            
        # Fix Multi-Index
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
            
        # 2. Clean & Indicators
        data = data.drop_duplicates().ffill()
        data['SMA50'] = data['Close'].rolling(window=50).mean()
        data['SMA200'] = data['Close'].rolling(window=200).mean()
        self.data = data

        # 3. Strategy Loop
        for i in range(len(data)):
            date = data.index[i]
            row = data.iloc[i]
            price = float(row['Close'])
            sma50 = row['SMA50']
            sma200 = row['SMA200']

            # Handle Series issue
            if isinstance(sma50, pd.Series): sma50 = sma50.item()
            if isinstance(sma200, pd.Series): sma200 = sma200.item()

            if pd.isna(sma50) or pd.isna(sma200):
                continue

            # Buy Signal
            if sma50 > sma200 and not self.position_open:
                self.shares = math.floor(self.balance / price)
                if self.shares > 0:
                    cost = self.shares * price
                    self.balance -= cost
                    self.position_open = True
                    self.trade_log.append({
                        "date": str(date.date()),
                        "type": "BUY",
                        "price": round(price, 2),
                        "shares": self.shares,
                        "balance": round(self.balance, 2)
                    })

            # Sell Signal
            elif sma50 < sma200 and self.position_open:
                revenue = self.shares * price
                self.balance += revenue
                self.shares = 0
                self.position_open = False
                self.trade_log.append({
                    "date": str(date.date()),
                    "type": "SELL",
                    "price": round(price, 2),
                    "shares": 0,
                    "balance": round(self.balance, 2)
                })

            # Force Close at End
            if i == len(data) - 1 and self.position_open:
                revenue = self.shares * price
                self.balance += revenue
                self.trade_log.append({
                    "date": str(date.date()),
                    "type": "FORCE SELL",
                    "price": round(price, 2),
                    "shares": 0,
                    "balance": round(self.balance, 2)
                })
                self.shares = 0
                self.position_open = False

        return {
            "final_balance": round(self.balance, 2),
            "profit": round(self.balance - self.budget, 2),
            "logs": self.trade_log
        }

    def generate_plot(self):
        if self.data is None: return None
        
        plt.figure(figsize=(10, 5))
        plt.plot(self.data.index, self.data['Close'], label='Close Price', alpha=0.5)
        plt.plot(self.data.index, self.data['SMA50'], label='SMA 50', color='orange', linestyle='--')
        plt.plot(self.data.index, self.data['SMA200'], label='SMA 200', color='blue', linestyle='--')
        plt.title(f'Analysis: {self.symbol}')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Save to buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()
        return img_str

# --- API ENDPOINTS ---

@app.post("/simulate")
def simulate_trade(req: TradeRequest):
    bot = TradingBot(req.symbol, req.start_date, req.end_date, req.budget)
    result = bot.run()
    
    if not result:
        return {"error": "No data found for this symbol/date range."}
        
    plot_image = bot.generate_plot()
    
    return {
        "status": "success",
        "result": result,
        "plot": plot_image
    }

@app.get("/")
def home():
    return FileResponse("index.html")